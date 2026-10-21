"""Render an evidence-based Booking Q&A review JSON; no network or send actions."""
import argparse
import json
from pathlib import Path
from urllib.parse import parse_qsl, urlsplit
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak,
)

LABELS = {
    'checked': '已检查', 'not_applicable': '不适用', 'unscanned': '未检查',
    'login_required': '待登录', 'access_failed': '无法访问',
    'needs_facts': '待核实 - 尚未批准', 'awaiting_approval': '待用户批准',
    'published': '已发布', 'submitted_pending_moderation': '已提交待平台审核',
    'answered_by_other': '已由团队回答', 'archived_by_other': '已由团队归档',
}


def validate(data):
    required = ['title', 'report_id', 'date', 'checked_at', 'coverage_complete',
                'summary', 'accounts', 'properties', 'questions']
    for key in required:
        if key not in data:
            raise ValueError(f'Missing field: {key}')
    if not isinstance(data['coverage_complete'], bool):
        raise ValueError('coverage_complete must be boolean')
    account_names = [a['account'] for a in data['accounts']]
    if not account_names or len(set(account_names)) != len(account_names):
        raise ValueError('Account inventory is empty or duplicated')
    prop_keys = set()
    for p in data['properties']:
        if p['account'] not in account_names:
            raise ValueError('Property account absent from inventory')
        if p.get('property_id'):
            key = (p['account'], str(p['property_id']))
            if key in prop_keys:
                raise ValueError(f'Duplicate property: {key}')
            prop_keys.add(key)
        if p['status'] == 'checked' and not isinstance(p.get('question_count'), int):
            raise ValueError('Checked property requires an observed question count')
    seen = set()
    for q in data['questions']:
        if q['review_id'] in seen:
            raise ValueError('Review IDs must be unique')
        seen.add(q['review_id'])
        if (q['account'], str(q['property_id'])) not in prop_keys:
            raise ValueError('Question property absent from inventory')
        if not q['original'].strip():
            raise ValueError('Question text cannot be empty')
        if q['status'] == 'awaiting_approval' and (
            not q.get('draft', '').strip() or q.get('unknowns')
        ):
            raise ValueError('Awaiting approval needs a final draft without unresolved facts')
        source = q.get('source_url', '')
        if source:
            parsed = urlsplit(source)
            if parsed.scheme not in ('http', 'https'):
                raise ValueError('Source URL must be HTTP(S)')
            secret_keys = {'ses', 'token', 'op_token', 'auth', 'access_token', 'password'}
            if any(k.lower() in secret_keys for k, _ in parse_qsl(parsed.query)):
                raise ValueError('Remove session/secret parameters from source URL')
    for a in data['accounts']:
        observed = sum(p['status'] == 'checked' for p in data['properties']
                       if p['account'] == a['account'] and p.get('property_id'))
        if observed != a['checked_properties']:
            raise ValueError('Account checked count differs from property evidence')
        if data['coverage_complete'] and (
            a.get('expected_properties') is None
            or observed != a['expected_properties']
            or a['status'] != 'checked'
        ):
            raise ValueError('Complete coverage conflicts with account inventory')
    if data['coverage_complete'] and any(
        p['status'] not in ('checked', 'not_applicable') for p in data['properties']
    ):
        raise ValueError('Complete coverage includes unchecked properties')


def build(data, output, font_path=None):
    from reportlab.platypus import Flowable, KeepTogether
    from reportlab.lib.enums import TA_CENTER
    validate(data)
    candidates = [font_path] if font_path else []
    candidates += ['C:/Windows/Fonts/msyh.ttc', '/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc']
    font_file = next((Path(p) for p in candidates if p and Path(p).is_file()), None)
    if not font_file:
        raise FileNotFoundError('Provide a Chinese TrueType font using --font')
    pdfmetrics.registerFont(TTFont('QAChinese', str(font_file), subfontIndex=0))
    ink = colors.HexColor('#173B49')
    muted = colors.HexColor('#536A73')
    green = colors.HexColor('#168460')
    red = colors.HexColor('#CE5151')
    amber = colors.HexColor('#A96F0D')
    styles = {
        'body': ParagraphStyle('body', fontName='QAChinese', fontSize=9.2, leading=14, wordWrap='CJK', textColor=ink),
        'small': ParagraphStyle('small', fontName='QAChinese', fontSize=8, leading=12, wordWrap='CJK', textColor=muted),
        'title': ParagraphStyle('title', fontName='QAChinese', fontSize=22, leading=30, textColor=ink, spaceAfter=8),
        'h1': ParagraphStyle('h1', fontName='QAChinese', fontSize=15, leading=22, textColor=ink, spaceAfter=8),
        'h2': ParagraphStyle('h2', fontName='QAChinese', fontSize=11, leading=17, textColor=ink, spaceAfter=5),
        'head': ParagraphStyle('head', fontName='QAChinese', fontSize=9, leading=13, textColor=colors.white, wordWrap='CJK'),
    }

    def para(text, style='body'):
        return Paragraph(escape(str(text or '')).replace('\n', '<br/>'), styles[style])

    class Icon(Flowable):
        def __init__(self, kind, size=13):
            Flowable.__init__(self)
            self.kind, self.width, self.height = kind, size, size
        def draw(self):
            c, s = self.canv, self.width
            tone = {'check': green, 'urgent': red, 'later': amber, 'pause': muted}.get(self.kind, muted)
            c.setFillColor(tone)
            c.roundRect(0, 0, s, s, 3, fill=1, stroke=0)
            c.setStrokeColor(colors.white)
            c.setFillColor(colors.white)
            c.setLineWidth(1.6)
            if self.kind == 'check':
                p = c.beginPath(); p.moveTo(s*.2,s*.5); p.lineTo(s*.43,s*.27); p.lineTo(s*.82,s*.76); c.drawPath(p)
            elif self.kind == 'pause':
                c.rect(s*.28,s*.22,s*.13,s*.56,fill=1,stroke=0); c.rect(s*.59,s*.22,s*.13,s*.56,fill=1,stroke=0)
            else:
                c.line(s*.5,s*.75,s*.5,s*.43); c.circle(s*.5,s*.22,s*.055,fill=1,stroke=0)

    def badge(kind, text):
        t = Table([[Icon(kind), para(text, 'small')]], colWidths=[19,43])
        t.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),0),('TOPPADDING',(0,0),(-1,-1),0),('BOTTOMPADDING',(0,0),(-1,-1),0)]))
        return t

    def grid(rows, widths, header=True, small=False):
        content = []
        for i,row in enumerate(rows):
            content.append([v if isinstance(v, Flowable) else para(v,'head' if header and i==0 else ('small' if small else 'body')) for v in row])
        t = Table(content,colWidths=widths,repeatRows=1 if header else 0,hAlign='LEFT')
        ops=[('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7),('LINEBELOW',(0,0),(-1,-1),.4,colors.HexColor('#DCE6E9'))]
        if header:
            ops += [('BACKGROUND',(0,0),(-1,0),ink),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.HexColor('#F3F7F8'),colors.white])]
        else:
            ops += [('BACKGROUND',(0,0),(0,-1),colors.HexColor('#ECF3F5'))]
        t.setStyle(TableStyle(ops))
        return t

    ordered=sorted(data['questions'], key=lambda q:q.get('action_rank',100))
    groups=[]; index={}
    same_fields=['account','property_id','original','translation','draft','draft_translation','status','draft_version']
    for q in ordered:
        key=q.get('display_group') or q['review_id']
        if key in index:
            g=index[key]
            if any(q.get(k)!=g[0].get(k) for k in same_fields):
                raise ValueError('Cannot combine different question or reply versions')
            g.append(q)
        else:
            g=[q];groups.append(g);index[key]=g
    def ids(group):
        return ' / '.join(q['review_id'].rsplit('-',1)[-1] for q in group)
    def kind(q):
        if q['status']=='awaiting_approval':return 'check'
        return 'urgent' if q.get('action_label')=='优先核实' else 'later'
    ready=[g for g in groups if g[0]['status']=='awaiting_approval']
    needs=[g for g in groups if g[0]['status']!='awaiting_approval']
    ready_n=sum(len(g) for g in ready)
    facts_n=sum(q['status']=='needs_facts' for q in ordered)
    checked=sum(a['checked_properties'] for a in data['accounts'])
    checked_a=sum(a['status']=='checked' for a in data['accounts'])
    coverage='完整检查' if data['coverage_complete'] else '部分检查'
    story=[para('Booking 客人问答 · 快速审阅','title'),para(f"{data['date']}  |  {data['report_id']}  |  {coverage}",'small'),Spacer(1,12)]
    question_label=data.get('question_count_label',f'{len(ordered)}条未答')
    stats=[['覆盖情况','问题处理','发布情况'],[f"{checked_a}/{len(data['accounts'])}个账号 · {checked}套已查",f"{question_label} · {ready_n}条待批准 · {facts_n}条待核实",'详见条目状态；本版没有新增发布']]
    if data.get('scan_notice'):
        story += [para(data['scan_notice'],'small'),Spacer(1,8)]
    story += [grid(stats,[174,207,142]),Spacer(1,13),para('建议处理顺序','h1')]
    rows=[['状态','编号 / 房源','客人问什么','我的建议','下一步']]
    for g in groups:
        q=g[0]
        label=q.get('action_label') or ('先回复' if q['status']=='awaiting_approval' else '先核实')
        status_text=label+'\n'+('待批准' if q['status']=='awaiting_approval' else '待核实')
        rows.append([badge(kind(q),status_text),ids(g)+'\n'+q.get('short_property',q['address']),q.get('short_question',q['translation']),q.get('recommendation','审批后回复' if q['status']=='awaiting_approval' else '先补齐事实，再确认答复。'),q.get('next_step','批准具体回复版本' if q['status']=='awaiting_approval' else '\n'.join(q.get('unknowns',[])))])
    story += [grid(rows,[76,106,105,120,116]),Spacer(1,10),para('图标说明：绿色对勾 = 拟稿可审、等你批准；红色 = 优先核实；黄色 = 后续核实。均不代表已发给客人。','small'),Spacer(1,8)]
    if not data['coverage_complete']:
        pending='、'.join(a['group'].replace(' PTY LTD','').replace(' REALTY GROUP','') for a in data['accounts'] if a['status']!='checked')
        story += [para('覆盖缺口：'+pending+' 待登录；其房源总数和问题数未核实。','small')]
    story += [para('排序是处理建议，页面未显示提问日期，未判断超时。完整问答见后页；房源覆盖见末页。','small')]

    def detail(group):
        q=group[0]
        status='待你批准 · 可先回复' if q['status']=='awaiting_approval' else '待核实 · 当前仅有暂缓草稿'
        header=f"{ids(group)}  |  {q.get('short_property',q['address'])}"
        rows=[['状态',status],['客人原问',q['original']],['中文意思',q['translation']],['建议回复全文',q.get('draft') or '待核实后拟定'],['回复中文',q.get('draft_translation','')],['依据',q.get('evidence_summary') or '\n'.join(q.get('evidence',[]))]]
        if q.get('unknowns'):
            rows.append(['需要核实',q.get('next_step') or '\n'.join(q['unknowns'])])
        items=[para(header,'h2'),para(f"房源ID {q['property_id']} · 回复 v{q['draft_version']} · 公开问答 · {len(group)}条独立记录",'small'),Spacer(1,6),grid(rows,[74,449],False,True),Spacer(1,4)]
        if len(group)>1:
            items.append(para('以上原问、回复适用于所列各独立编号；相同原文仅合并展示，发布时仍逐条核对。','small'))
        url=q.get('source_url','')
        if url:
            items.append(Paragraph('<link href="'+escape(url,{'"':'&quot;'})+'" color="#14776D">打开该房源客人问答</link>',styles['small']))
        items.append(Spacer(1,14))
        return KeepTogether(items)

    if ready:
        story += [PageBreak(),para('可先回复 · 等你批准','h1'),para('绿色对勾仅表示拟稿准备好，批准前不会发布。','small'),Spacer(1,12)]
        for g in ready:story.append(detail(g))
        example_ids='、'.join(q['review_id'].rsplit('-',1)[-1] for q in ready[0])
        story += [para(f"批准方式示例：批准 {example_ids} 的回复 v{ready[0][0]['draft_version']}。请使用本次实际列出的编号及回复版本。",'small')]
    if needs:
        story += [PageBreak(),para('先核实 · 再确定正式回复','h1'),para('以下英文保留供审阅；建议优先补齐右侧/表内事项，再回答客人的实质问题。','small'),Spacer(1,10)]
        for g in needs:story.append(detail(g))
    story += [PageBreak(),para('覆盖清单 · 实际检查范围','h1'),para('检查时间：'+data['checked_at'],'small'),Spacer(1,8)]
    account_rows=[['账号 / 集团','已查 / 本轮总数','结果']]
    account_labels={a['account']:f'A{i+1}' for i,a in enumerate(data['accounts'])}
    for a in data['accounts']:
        count=a.get('expected_properties')
        result='已查完本账号' if a['status']=='checked' else '待登录 · 问题数未知'
        account_rows.append([account_labels[a['account']]+' · '+a['account']+'\n'+a['group'],str(a['checked_properties'])+' / '+(str(count) if count is not None else '未知'),result])
    story += [grid(account_rows,[266,90,167],True,True),Spacer(1,12)]
    prop_rows=[['房源 / 地址','房源ID','检查结果']]
    for p in data['properties']:
        if not p.get('property_id'):continue
        count=p.get('question_count')
        result=('已查 · '+str(count)+'条未答') if p['status']=='checked' else LABELS.get(p['status'],p['status'])
        if p.get('operating_status')=='closed' or '关闭' in p.get('note',''):result+=' · 已关闭房源'
        prop_rows.append([account_labels[p['account']]+' · '+(p.get('address') or p['name']),p['property_id'],result])
    story += [grid(prop_rows,[285,98,140],True,True),Spacer(1,9)]
    drafts=sum(p['status']=='not_applicable' for p in data['properties'])
    if drafts:story.append(para(f'另有{drafts}个注册草稿，无正式房源ID/问答入口，列为不适用，未计入已查房源。','small'))
    story.append(para('报告版本变更：'+data.get('revision_note','本版按实际检查结果生成。'),'small'))
    def footer(c,doc):
        c.setFillColor(muted);c.setFont('QAChinese',7)
        prefixes={q['review_id'].rsplit('-',1)[0]+'-' for q in ordered}
        prefix_note='编号前缀 '+next(iter(prefixes)) if len(prefixes)==1 else '审阅编号见条目'
        c.drawString(36,22,data['report_id']+' | 内部审阅 · '+prefix_note)
        c.drawRightString(A4[0]-36,22,f'第 {doc.page} 页')
    output=Path(output);output.parent.mkdir(parents=True,exist_ok=True)
    doc=SimpleDocTemplate(str(output),pagesize=A4,leftMargin=36,rightMargin=36,topMargin=30,bottomMargin=38,title=data['title'],author='SEEDNEST')
    doc.build(story,onFirstPage=footer,onLaterPages=footer)


if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('input');parser.add_argument('output');parser.add_argument('--font')
    args=parser.parse_args()
    build(json.loads(Path(args.input).read_text(encoding='utf-8-sig')),args.output,args.font)
    print(args.output)
