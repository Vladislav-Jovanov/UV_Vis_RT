#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 22 21:40:59 2025

@author: tze
"""
from tkinter import Frame
from submodules.tkWindget import AppFrame,FigureFrame,LoadMultipleFiles
from submodules.Figures import FigureXY2
from submodules.RW_files import Help
from common.filetypes import display_type

class plot_RTA(AppFrame):
    def __init__(self,**kwargs):
        super().__init__(**kwargs,file=__file__,appgeometry=(900, 550, 25, 25))
        self._init_frames()
        self.multiple_load=LoadMultipleFiles(parent=self.controlframe, ini=self.ini,write_ini=self.write_ini,read=Help.read_UV_Vis,filetypes=display_type)
        self.multiple_load.add_action(self.plot_stuff)
        self.multiple_load.grid(row=0,column=0)
        
    def _init_frames(self):    
        #for the buttons and file list
        self.controlframe = Frame(self.frameroot)
        self.controlframe.grid(column=0,row=0)
        self.figframe=FigureFrame(parent=self.frameroot,figclass=FigureXY2,figkwargs={'figsize':(15/2.54,8/2.54),'axsize':[2/15,3/15,7/15,5/8]})
        self.figframe.grid(column=1,row=0)

    def plot_stuff(self):
        self.figframe.plot.plot_xy_lists(self.multiple_load.get_data(),self.multiple_load.get_mask())
    
    def __str__(self):
        return "Curve Displaying App"
    
if __name__=='__main__':
    plot_RTA().init_start()