"""Render reviewed procurement input in the user's SEEDNEST report style."""
import argparse,json
from pathlib import Path
from decimal import Decimal
from html import escape
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle,Flowable,PageBreak,KeepTogether
from reportlab.lib.utils import ImageReader
from render_estimate import calculate,currency,TIERS

ROOT=Path(__file__).resolve().parents[1]
INK=colors.HexColor('#233044');GREEN=colors.HexColor('#185532');ACCENT=colors.HexColor('#22C55E');MUTED=colors.HexColor('#718096');LINE=colors.HexColor('#E4EAF0')
WIDTH=A4[0]-52

def render(data,path):
    calc=calculate(data);logo=ROOT/'assets/seednest-logo.png'
    if not logo.is_file():raise FileNotFoundError('SEEDNEST brand logo is required')
    pdfmetrics.registerFont(TTFont('BrandCN',r'C:\Windows\Fonts\msyh.ttc',subfontIndex=0))
    pdfmetrics.registerFont(TTFont('BrandBold',r'C:\Windows\Fonts\msyhbd.ttc',subfontIndex=0))
    styles={
      'body':ParagraphStyle('b',fontName='BrandCN',fontSize=9,leading=14,wordWrap='CJK',textColor=INK),
      'small':ParagraphStyle('s',fontName='BrandCN',fontSize=7.7,leading=11.8,wordWrap='CJK',textColor=MUTED),
      'bold':ParagraphStyle('bo',fontName='BrandBold',fontSize=9,leading=14,wordWrap='CJK',textColor=INK),
      'right':ParagraphStyle('r',fontName='BrandBold',fontSize=9,leading=14,alignment=2,textColor=INK),
      'head':ParagraphStyle('h',fontName='BrandBold',fontSize=7.8,leading=12,wordWrap='CJK',textColor=MUTED)}
    def p(s,k='body'):return Paragraph(escape(str(s)).replace('\n','<br/>'),styles[k])
    def circle_logo(c,x,y,size):
      c.saveState()
      clip=c.beginPath();clip.circle(x+size/2,y+size/2,size/2)
      c.clipPath(clip,stroke=0,fill=0)
      c.drawImage(str(logo),x,y,size,size,mask='auto',preserveAspectRatio=True)
      c.restoreState()
      c.saveState();c.setStrokeColor(colors.white);c.setLineWidth(1.2);c.circle(x+size/2,y+size/2,size/2,stroke=1,fill=0);c.restoreState()
    class Banner(Flowable):
      def __init__(self):Flowable.__init__(self);self.width=WIDTH;self.height=92
      def draw(self):
        c=self.canv;c.setFillColor(GREEN);c.rect(-32,-3,A4[0],165,fill=1,stroke=0)
        circle_logo(c,0,70,52)
        c.setFillColor(colors.white);c.setFont('BrandBold',23);c.drawString(0,35,'房源采购预算')
        c.setFont('BrandCN',8);c.drawString(0,15,'PRE-SIGNING ESTIMATE')
        c.setFillColor(colors.HexColor('#326A48'));c.roundRect(216,14,WIDTH-216,112,9,fill=1,stroke=0)
        def q(s,y,size,col,bold=False):
          st=ParagraphStyle('q',fontName='BrandBold' if bold else 'BrandCN',fontSize=size,leading=size*1.45,textColor=colors.HexColor('#'+col),wordWrap='CJK')
          pp=Paragraph(escape(s),st);_,h=pp.wrap(WIDTH-241,70);pp.drawOn(c,228,y-h)
        q('PROPERTY ADDRESS',115,7,'99E8AF',True);q(data['property'],98,10,'FFFFFF',True)
        q('采购档位 / 编制日期',57,7,'99E8AF',True);q(TIERS[data['tier']]+'  |  '+data['date'],41,9,'FFFFFF')
    class Section(Flowable):
      def __init__(self,title):Flowable.__init__(self);self.title=title;self.width=WIDTH;self.height=31;self.keepWithNext=True
      def draw(self):
        c=self.canv;c.setFillColor(ACCENT);c.roundRect(0,8,3,16,1.5,fill=1,stroke=0);c.setFillColor(INK);c.setFont('BrandBold',12);c.drawString(11,10,self.title)
    class Total(Flowable):
      def __init__(self):Flowable.__init__(self);self.width=WIDTH;self.height=90
      def draw(self):
        c=self.canv;c.setFillColor(colors.HexColor('#101827'));c.roundRect(0,0,WIDTH,82,9,fill=1,stroke=0)
        c.setFillColor(colors.HexColor('#A1AFC2'));c.setFont('BrandBold',10);c.drawString(16,55,'建议筹备预算' if not calc['unknown'] else '已估项目合计')
        c.setFont('BrandCN',8);c.drawString(16,34,'含采购、人工及已列备用金')
        c.setFillColor(colors.HexColor('#4ADE80'));c.setFont('BrandBold',27);c.drawRightString(WIDTH-17,30,currency(calc['total']))
    def table(rows,widths):
      tab=Table(rows,colWidths=widths,repeatRows=1,hAlign='LEFT')
      tab.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#F5F7FA')),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),9),('RIGHTPADDING',(0,0),(-1,-1),9),('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),8),('LINEBELOW',(0,0),(-1,-1),.4,LINE),('BOX',(0,0),(-1,-1),.5,LINE)]))
      return tab
    story=[Banner(),Spacer(1,17),Section('房源配置'),p(data['configuration']),Spacer(1,12),Total(),Spacer(1,12),Section('预算概览')]
    summary=[[p('采购类别','head'),p('金额 / AUD','head')]]
    for cat,lines in calc['groups'].items():
      known=[x['amount'] for x in lines if x['amount'] is not None];amount=sum(known,Decimal(0));suffix=' + 待核' if known and any(x['amount'] is None for x in lines) else ''
      summary.append([p(cat),p((currency(amount)+suffix) if known else '待核','right')])
    tab=table(summary,[WIDTH*.73,WIDTH*.27]);story.append(tab)
    story.extend([Spacer(1,14),p('签约前初步预算，最终以选品和报价为准。预算已包含清洁、摄影等人工费用；备用金不代表已发生支出。','small')])
    if calc['unknown']:story.append(p('仍有必要项目待核，当前金额尚非完整采购预算。','bold'))
    story.append(PageBreak())
    for cat,lines in calc['groups'].items():
      story.append(Section(cat))
      rs=[[p('采购项目','head'),p('配置说明','head'),p('金额 / AUD','head')]]
      for x in lines:
        rs.append([p(x['name'],'bold'),p(x.get('note','')+'\n数量：'+str(x['quantity'])+' '+x['unit'],'small'),p(currency(x['amount']),'right')])
      story.extend([table(rs,[WIDTH*.28,WIDTH*.54,WIDTH*.18]),Spacer(1,12)])
    if calc['optional']:
      story.append(Section('可选服务 · 不计入上述预算'))
      rs=[[p('服务项目','head'),p('说明','head'),p('金额 / AUD','head')]]
      for x in calc['optional']:rs.append([p(x['name'],'bold'),p(x.get('note',''),'small'),p(currency(x['amount']),'right')])
      story.extend([table(rs,[WIDTH*.28,WIDTH*.54,WIDTH*.18]),Spacer(1,14)])
    story.append(Section('预算口径与范围'))
    for s in data.get('assumptions',[])+data.get('exclusions',[]):story.extend([p('• '+s,'small'),Spacer(1,5)])
    # Source provenance stays in internal input; it is not printed in owner PDFs.
    def footer(c,doc):
      c.setStrokeColor(LINE);c.line(26,32,A4[0]-26,32);c.setFillColor(MUTED);c.setFont('BrandCN',7);c.drawString(26,19,'SEEDNEST Property Management');c.drawRightString(A4[0]-26,19,str(doc.page))
    def first(c,doc):footer(c,doc)
    def later(c,doc):
      footer(c,doc);circle_logo(c,26,A4[1]-45,28);c.setFillColor(GREEN);c.setFont('BrandBold',9);c.drawString(63,A4[1]-32,'房源采购预算');c.setFillColor(MUTED);c.setFont('BrandCN',7);c.drawRightString(A4[0]-26,A4[1]-32,data['property']);c.setStrokeColor(LINE);c.line(26,A4[1]-52,A4[0]-26,A4[1]-52)
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    doc=SimpleDocTemplate(str(path),pagesize=A4,leftMargin=26,rightMargin=26,topMargin=63,bottomMargin=47,title=data['property']+' - SEEDNEST采购预算',author='SEEDNEST')
    doc.build(story,onFirstPage=first,onLaterPages=later)
    audit={'total':str(calc['total']),'required_count':sum(len(x) for x in calc['groups'].values()),'optional_count':len(calc['optional']),'logo':str(logo)}
    path.with_suffix('.calculation.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2),encoding='utf-8');return audit
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('input');ap.add_argument('output');a=ap.parse_args()
    render(json.loads(Path(a.input).read_text(encoding='utf-8-sig')),a.output)


