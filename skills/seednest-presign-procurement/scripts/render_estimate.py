"""Render an owner-facing AUD estimate from reviewed line items; no price selection."""
from __future__ import annotations
import argparse,json,os
from pathlib import Path
from datetime import date
from decimal import Decimal,ROUND_HALF_UP,InvalidOperation
from collections import OrderedDict
from html import escape
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
from reportlab.lib.enums import TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle

TIERS={'au-high':'澳洲购买 · 高档','au-low':'澳洲购买 · 标准版','mixed':'澳洲＋国内混合购买'}
CENT=Decimal('0.01')

def number(v,label):
    if isinstance(v,bool):raise ValueError(f'{label}: boolean is not a number')
    try:d=Decimal(str(v))
    except InvalidOperation:raise ValueError(f'{label}: invalid number')
    if not d.is_finite() or d<0:raise ValueError(f'{label}: must be finite and nonnegative')
    return d

def calculate(data):
    for key in ('property','date','tier','configuration','items'):
        if key not in data:raise ValueError(f'Missing {key}')
    if data['tier'] not in TIERS:raise ValueError('Unknown tier')
    date.fromisoformat(data['date'])
    if not isinstance(data['items'],list) or not data['items']:raise ValueError('No items')
    groups=OrderedDict();optional=[];unknown=[];total=Decimal(0);normalized=[]
    for idx,item in enumerate(data['items'],1):
        for key in ('category','name','quantity','unit','unit_price_aud'):
            if key not in item:raise ValueError(f'Item {idx}: missing {key}')
        qty=number(item['quantity'],f'Item {idx} quantity')
        if qty==0:continue
        if not isinstance(item.get('optional',False),bool):raise ValueError('optional must be boolean')
        price=None if item['unit_price_aud'] is None else number(item['unit_price_aud'],f'Item {idx} price').quantize(CENT,rounding=ROUND_HALF_UP)
        if price is not None and not item.get('source_reference'):raise ValueError(f'Item {idx}: priced item lacks source_reference')
        if item.get('supply_channel')=='au-warehouse' and price is not None:
            if item.get('warehouse_available') is not True or item.get('warehouse_price_confirmed') is not True:
                raise ValueError(f'Item {idx}: warehouse availability and price must be verified')
        line=dict(item,quantity_decimal=qty,price_decimal=price,
                  amount=None if price is None else (qty*price).quantize(CENT,rounding=ROUND_HALF_UP))
        normalized.append(line)
        if item.get('optional',False):optional.append(line);continue
        groups.setdefault(item['category'],[]).append(line)
        if price is None:unknown.append(line)
        else:total+=line['amount']
    if not normalized:raise ValueError('No positive-quantity items')
    return {'groups':groups,'optional':optional,'unknown':unknown,'total':total,'items':normalized}

def currency(d):return '待核' if d is None else f'A${d:,.2f}'

def render(data,path,font_path=None):
    calc=calculate(data)
    candidates=[font_path,os.environ.get('SEEDNEST_PDF_FONT'),r'C:\Windows\Fonts\simsun.ttc']
    selected=next((Path(f) for f in candidates if f and Path(f).is_file()),None)
    if selected is None:raise ValueError('Provide a CJK TrueType font with --font')
    pdfmetrics.registerFont(TTFont('SeednestCJK',str(selected),subfontIndex=0))
    font='SeednestCJK';navy=colors.HexColor('#203B3B');muted=colors.HexColor('#536463');linecol=colors.HexColor('#D9E2DD')
    styles={
        'body':ParagraphStyle('body',fontName=font,fontSize=9.5,leading=15,wordWrap='CJK',textColor=navy),
        'small':ParagraphStyle('small',fontName=font,fontSize=8.5,leading=13,wordWrap='CJK',textColor=muted),
        'title':ParagraphStyle('title',fontName=font,fontSize=23,leading=31,wordWrap='CJK',textColor=navy,spaceAfter=9),
        'section':ParagraphStyle('section',fontName=font,fontSize=12,leading=19,wordWrap='CJK',textColor=navy,spaceBefore=13,spaceAfter=5,keepWithNext=True),
        'amount':ParagraphStyle('amount',fontName=font,fontSize=24,leading=33,textColor=navy,spaceAfter=7),
        'right':ParagraphStyle('right',fontName=font,fontSize=9,leading=14,wordWrap='CJK',alignment=TA_RIGHT,textColor=navy),
        'head':ParagraphStyle('head',fontName=font,fontSize=9,leading=14,wordWrap='CJK',textColor=colors.white)
    }
    def p(text,style='body'):return Paragraph(escape(str(text)).replace('\n','<br/>'),styles[style])
    story=[p('SEEDNEST','small'),Spacer(1,7),p('房源大致采购表','title'),p(data['property']),
           p(f"{data['date']}   |   {TIERS[data['tier']]}",'small'),Spacer(1,14),p(data['configuration']),Spacer(1,14)]
    label='已估项目合计' if calc['unknown'] else '采购预算估算'
    known_required=any(x['amount'] is not None for items in calc['groups'].values() for x in items)
    rounded=(calc['total']/100).quantize(Decimal('1'),rounding=ROUND_HALF_UP)*100
    story += [p(label,'small'),p(f'约 A${rounded:,.0f}' if known_required else '待核','amount')]
    if known_required:story.append(p(f"已计价明细合计 {currency(calc['total'])}，可选项另列。",'small'))
    if calc['unknown']:story.append(p('另有必要项目待核价，下列金额尚非完整采购预算。'))
    for note in data.get('assumptions',[]):story.append(p(note,'small'))
    story.append(p('采购预算概览','section'))
    summary=[[p('类别','head'),p('金额（AUD）','head')]]
    for category,items in calc['groups'].items():
        amt=sum((x['amount'] for x in items if x['amount'] is not None),Decimal(0))
        has_known=any(x['amount'] is not None for x in items)
        suffix=' + 待核项目' if has_known and any(x['amount'] is None for x in items) else ''
        summary.append([p(category),p((currency(amt)+suffix) if has_known else '待核','right')])
    summary.append([p(label),p(currency(calc['total']) if known_required else '待核','right')])
    def table(rows,widths):
        t=Table(rows,colWidths=widths,repeatRows=1,hAlign='LEFT')
        t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),navy),('VALIGN',(0,0),(-1,-1),'TOP'),
            ('LEFTPADDING',(0,0),(-1,-1),8),('RIGHTPADDING',(0,0),(-1,-1),8),
            ('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7),
            ('LINEBELOW',(0,1),(-1,-1),.35,linecol),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,colors.HexColor('#F4F7F3')])]))
        return t
    width=A4[0]-84
    story.append(table(summary,[width*.60,width*.40]))
    def detail_rows(items):
        rs=[[p('项目 / 规格','head'),p('数量','head'),p('单价 AUD','head'),p('小计 AUD','head')]]
        for x in items:
            text=x['name']+('\n'+x['note'] if x.get('note') else '')
            qty=format(x['quantity_decimal'],'f').rstrip('0').rstrip('.') if '.' in format(x['quantity_decimal'],'f') else str(x['quantity_decimal'])
            rs.append([p(text),p(qty+' '+x['unit'],'right'),p(currency(x['price_decimal']),'right'),p(currency(x['amount']),'right')])
        return rs
    for category,items in calc['groups'].items():
        rows=detail_rows(items)
        story += [p(category,'section'),table(rows,[width*.48,width*.13,width*.19,width*.20])]
    if calc['optional']:
        story += [p('可选升级（不计入上述合计）','section'),table(detail_rows(calc['optional']),[width*.48,width*.13,width*.19,width*.20])]
    notes=data.get('exclusions',[])
    if notes:
        story.append(p('范围与待确认事项','section'))
        story.extend(p(n,'small') for n in notes)
    if data.get('source_summary'):story.append(p(data['source_summary'],'small'))
    story += [Spacer(1,10),p('签约前初步预算，最终以选品和报价为准。','small')]
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    def footer(canvas,doc):
        canvas.setStrokeColor(linecol);canvas.line(42,38,A4[0]-42,38)
        canvas.setFont(font,8);canvas.setFillColor(muted)
        canvas.drawString(42,25,'SEEDNEST | 采购预算')
        canvas.drawRightString(A4[0]-42,25,f'{doc.page}')
    doc=SimpleDocTemplate(str(path),pagesize=A4,rightMargin=42,leftMargin=42,topMargin=38,bottomMargin=52,
        title=f"{data['property']} - 房源大致采购表",author='SEEDNEST')
    doc.build(story,onFirstPage=footer,onLaterPages=footer)
    audit={'property':data['property'],'tier':data['tier'],'date':data['date'],'known_required_total_aud':str(calc['total']),
        'unpriced_required_items':[x['name'] for x in calc['unknown']],
        'items':[{k:v for k,v in item.items() if k not in ('quantity_decimal','price_decimal')} for item in calc['items']]}
    path.with_suffix('.calculation.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2,default=str),encoding='utf-8')
    return audit

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('input');parser.add_argument('output');parser.add_argument('--font')
    args=parser.parse_args();data=json.loads(Path(args.input).read_text(encoding='utf-8-sig'))
    audit=render(data,args.output,args.font)
    print(json.dumps({'pdf':str(Path(args.output).resolve()),'known_required_total_aud':audit['known_required_total_aud'],'unpriced_required_items':audit['unpriced_required_items']},ensure_ascii=False))
