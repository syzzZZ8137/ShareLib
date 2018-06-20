# -*- coding: utf-8 -*-
"""
Created on Mon Sep 11 16:35:22 2017

@author: jax.chen
"""

import os 
import pandas as pd
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import * 
from reportlab.lib import colors 
import reportlab.rl_config
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import copy
import logo_pagenum_class
from datetime import datetime

#r:基础指标
#r1：月度return
#r2：相关系数矩阵
#r3:情景分析结果
#r4:回归分析结果


os.chdir("D:\\工作\\期货市场量化研报")  #设置根目录
pdfmetrics.registerFont(TTFont('song', 'C:\Windows\Fonts\simfang.ttf'))
pdfmetrics.registerFont(TTFont('hei', 'C:\Windows\Fonts\simhei.ttf'))
pdfmetrics.registerFont(TTFont('kai', 'C:\Windows\Fonts\STKAITI.TTF'))
reportlab.rl_config.warnOnMissingFontGlyphs = 0

#定义风格的函数，三个参数分别为：段落类型，字体，字号
def Style(style_='Normal',fontName_='kai',color_='black',fontSize_=11):
    _Style = copy.deepcopy(styles[style_])
    _Style.fontName = fontName_
    _Style.fontSize = fontSize_
    _Style.textColor = color_
    return _Style    



styles = getSampleStyleSheet()
normalStyle=Style() #定义正文风格
titleStyle=Style('Title','hei','ReportLabBlue',25)  #定义标题风格
headingStyle1=Style('Heading1','hei','ReportLabBlue',15)
headingStyle2=Style('Heading2','hei','ReportLabBlue',12)
smallStyle=Style(fontSize_=7)

#创建pdf
doc = SimpleDocTemplate('report.pdf',rightMargin=30,leftMargin=30,topMargin=100,bottomMargin=10)

elements = []

#title
elements.append(Paragraph('国信期货量化研究报告', titleStyle))
elements.append(Spacer(0,20))
elements.append(Paragraph('1.品种介绍', headingStyle1))
elements.append(Spacer(0,150))

elements.append(Paragraph('2.月度胜率统计', headingStyle1))
elements.append(Spacer(0,150))

elements.append(Paragraph('3.持仓成交统计', headingStyle1))
elements.append(Spacer(0,15))

for i in range(14):
    img1 = Image('雷达图\\%d.jpg'%(i*3),120,120)
    img2 = Image('雷达图\\%d.jpg'%(i*3+1),120,120)
    img3 = Image('雷达图\\%d.jpg'%(i*3+2),120,120)
    
    table1 = Table([[img1,img2,img3]])
    table1.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP')]))
    
    elements.append(table1)

img1 = Image('雷达图\\42.jpg',120,120)
img2 = Image('雷达图\\43.jpg',120,120)
table1 = Table([[img1,img2]])
table1.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP')]))
elements.append(table1)




#elements.append(PageBreak())
elements.append(Paragraph('4.总结', headingStyle1))

doc.build(elements,canvasmaker=logo_pagenum_class.PageNumCanvas)

