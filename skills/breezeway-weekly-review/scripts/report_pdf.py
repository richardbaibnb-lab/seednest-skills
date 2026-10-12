"""Render an audited Markdown report and captioned local evidence images to PDF.
Usage: report_pdf.py report.md images.json output.pdf
images.json: [{"path":"absolute.jpg", "caption":"Property, date, finding", "url":"https://..."}]
"""
import sys, re, json, html
from pathlib import Path
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, KeepTogether

font_path = Path('C:/Windows/Fonts/simsun.ttc')
if font_path.exists():
    pdfmetrics.registerFont(TTFont('STSong-Light', str(font_path), subfontIndex=0))
else:
    pdfmetrics.registerFont(UnicodeCIDFont('STSong-Light'))
body = ParagraphStyle('body',fontName='STSong-Light',fontSize=10,leading=15,spaceAfter=7,wordWrap='CJK')
heading = ParagraphStyle('heading',parent=body,fontSize=15,leading=21,spaceBefore=10,spaceAfter=12,textColor=colors.HexColor('#135B65'))
title = ParagraphStyle('title',parent=heading,fontSize=23,leading=30)
def rich(s):
    s=html.escape(s.replace('**',''))
    return re.sub(r'\[([^]]+)\]\((https?://[^)]+)\)',lambda m:f'<link href="{m[2]}" color="#13748A">{m[1]}</link>',s)
def p(s,style=body): return Paragraph(rich(s),style)
def main():
    src,images,out=map(Path,sys.argv[1:4]); story=[]
    lines=src.read_text(encoding='utf-8-sig').splitlines(); i=0
    while i<len(lines):
        line=lines[i].strip(); i+=1
        if not line: continue
        if line.startswith('|'):
            rows=[line]
            while i<len(lines) and lines[i].strip().startswith('|'):
                rows.append(lines[i].strip()); i+=1
            cells=[[x.strip() for x in r.strip('|').split('|')] for r in rows if not re.match(r'^\|[\s:|\-]+\|$',r)]
            widths=[67,176,272] if cells[0][0]=='顺序' else [130,160,225]
            t=Table([[p(c) for c in row] for row in cells],colWidths=widths,repeatRows=1,hAlign='LEFT')
            t.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('BACKGROUND',(0,0),(-1,0),colors.HexColor('#DDEDEF')),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,colors.HexColor('#F3F7F7')]),('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7)]))
            story.extend([t,Spacer(1,12)])
        elif line.startswith('# '): story.append(p(line[2:],title))
        elif line.startswith('## '): story.append(p(line[3:],heading))
        else: story.append(p(line.removeprefix('- ')))
    for item in json.loads(images.read_text(encoding='utf-8-sig')):
        img=Image(item['path']); scale=min(500/img.imageWidth,570/img.imageHeight)
        img.drawWidth=img.imageWidth*scale; img.drawHeight=img.imageHeight*scale
        story.extend([PageBreak(),p('现场照片证据',heading),p(item['caption']),Spacer(1,12),img])
        if item.get('url'):story.extend([Spacer(1,12),p('[打开原任务报告]('+item['url']+')')])
    out.parent.mkdir(parents=True,exist_ok=True)
    def footer(c,d):
        c.setFont('STSong-Light',9); c.setFillColor(colors.HexColor('#647078')); c.drawString(40,24,'Breezeway | 清洁任务与照片检查'); c.drawRightString(A4[0]-40,24,str(d.page))
    SimpleDocTemplate(str(out),pagesize=A4,leftMargin=40,rightMargin=40,topMargin=34,bottomMargin=42,title=src.stem,author='Seednest').build(story,onFirstPage=footer,onLaterPages=footer)
    print('PDF created')
if __name__=='__main__': main()
