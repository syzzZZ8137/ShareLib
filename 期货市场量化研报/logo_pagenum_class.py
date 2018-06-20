# -*- coding: utf-8 -*-
"""
Created on Fri Jun 15 11:26:20 2018

@author: Jax_GuoSen
"""


from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
import os
########################################################################
class PageNumCanvas(canvas.Canvas):
    """
    http://code.activestate.com/recipes/546511-page-x-of-y-with-reportlab/
    http://code.activestate.com/recipes/576832/
    """
 
    #----------------------------------------------------------------------
    def __init__(self, *args, **kwargs):
        """Constructor"""
        canvas.Canvas.__init__(self, *args, **kwargs)
        self.pages = []
 
    #----------------------------------------------------------------------
    def showPage(self):
        """
        On a page break, add information to the list
        """
        self.pages.append(dict(self.__dict__))
        self._startPage()
 
    #----------------------------------------------------------------------
    def save(self):
        """
        Add the page number to each page (page x of y)
        """
        page_count = len(self.pages)
 
        for page in self.pages:
            self.__dict__.update(page)
            self.draw_page_number(page_count)
            canvas.Canvas.showPage(self)
 
        canvas.Canvas.save(self)
 
    #----------------------------------------------------------------------
    def draw_page_number(self, page_count):
        """
        Add the page number
        """
        pdfmetrics.registerFont(TTFont('hei', 'C:\Windows\Fonts\simhei.ttf'))
        page = "第%s页" % (self._pageNumber)
        self.setFont("hei", 9)
        self.drawRightString(195*mm, 272*mm, page)
        
        logo = os.getcwd()+'\\logo.png'
        self.drawImage(logo,40,760,180,30)
