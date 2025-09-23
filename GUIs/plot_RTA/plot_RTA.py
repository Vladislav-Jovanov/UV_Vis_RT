#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 22 21:40:59 2025

@author: tze
"""
from tkinter import Frame
from tkWindget.tkWindget import AppFrame,FigureFrame,LoadMultipleFiles
from Figures.Figures import FigureXY2
from DataProcess.DataProcess import convert_unit_IHTM
from RW_data.RW_files import Read_from


class plot_RTA(AppFrame):
    def __init__(self,**kwargs):
        super().__init__(**kwargs,file=__file__,appgeometry=(900, 550, 25, 25))
        self._init_frames()
        self.multiple_load=LoadMultipleFiles(parent=self.controlframe, ini=self.ini,write_ini=self.write_ini,read=self.read_data,filetypes=[('UV_Vis files','*.dsp *.dtsp'),('E60 files','*.dsp'),('IHTM UV_Vis','*.dtsp')])
        self.multiple_load.add_action(self.plot_stuff)
        self.multiple_load.grid(row=0,column=0)
        
    def _init_frames(self):    
        #for the buttons and file list
        self.controlframe = Frame(self.frameroot)
        self.controlframe.grid(column=0,row=0)
        self.figframe=FigureFrame(parent=self.frameroot,figclass=FigureXY2,figkwargs={'figsize':(15/2.54,8/2.54),'axsize':[2/15,3/15,7/15,5/8]})
        self.figframe.grid(column=1,row=0)
        
    def read_data(self,filename):
        if filename.split('.')[-1]=='dsp':
            tmp=Read_from.dsp(filename)
            convert_unit_IHTM(tmp,'','y1')
            convert_unit_IHTM(tmp,'n','x1')
        elif filename.split('.')[-1]=='dtsp':
            tmp=Read_from.ihtm(filename)
            convert_unit_IHTM(tmp,'','y1')
        return tmp
    
    def plot_stuff(self):
        self.figframe.plot.plot_xy_lists(self.multiple_load.get_data(),self.multiple_load.get_mask())
    
    def __str__(self):
        return "Curve Displaying App"
    
if __name__=='__main__':
    plot_RTA().init_start()