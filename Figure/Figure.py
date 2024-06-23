#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 18 16:19:18 2022

@author: tzework
"""
from matplotlib.figure import Figure

class container():
    pass


class FigureE60():
    def __init__(self):
        #matplotlib muliplies axes size with large figure size that is why you always divide with large figure size
        self.dim=container()
        self.dim.figwidth=10/2.54#fullfigure size
        self.dim.figheight=8/2.54#fullfigure size
        self.dim.x0=2/(2.54*self.dim.figwidth)#relative to large figure
        self.dim.y0=2/(2.54*self.dim.figwidth)#relative to large figure
        self.dim.w=7/(2.54*self.dim.figwidth)#small fig size in percentage of large figure
        self.dim.h=5/(2.54*self.dim.figheight)#small fig size in percentage of large figure

        self.fig=Figure()
        self.fig.set_size_inches((self.dim.figwidth,self.dim.figheight))
        self.ax=self.fig.add_axes([self.dim.x0,self.dim.y0,self.dim.w,self.dim.h])
        self.ax.tick_params(labelsize=8)
        self.ax.set_xlabel('wavelength [nm]',fontsize=10, position=(0.5,0),labelpad=5)
        self.ax.set_ylabel('',fontsize=10,  position=(0,0.5),labelpad=5)
        self.ax.set_xlim(200,1200)
        
    def plot_data(self,axes,x,y):
        axes.plot(x,y)
        
    def update_limits(self,axes,xmin,xmax,ymin,ymax):
        axes.set_xlim(xmin,xmax)
        axes.set_ylim(ymin,ymax)
        
    def clear_data(self,axes,index):
        axes.lines.pop(index)
        
    def update_label(self, axes, label, string):
        if label=='x_label':
            axes.set_xlabel(string,fontsize=10, position=(0.5,0),labelpad=5)
        elif label=='y_label':
            axes.set_ylabel(string,fontsize=10, position=(0,0.5),labelpad=5)
            
            
class Figure_top_bottom(Figure):
    def __init__(self):
        #matplotlib muliplies axes size with large figure size that is why you always divide with large figure size
        super().__init__()
        xdim=9.5
        ydim=14
        axx=7
        axy=5
        axx0=1.5
        axy0=1.5
        spacing=1.5
        
        self.set_size_inches((xdim/2.54,ydim/2.54))
        self.axb=self.add_axes((axx0/xdim,axy0/ydim,axx/xdim,axy/ydim))
        self.axb.tick_params(labelsize=8)
        self.axb.set_xlabel('wavelength (nm)',fontsize=10, position=(0.5,0),labelpad=5)
        self.axb.set_ylabel('Absorbance (%)',fontsize=10,  position=(0,0.5),labelpad=5)
        
                               
        self.axt=self.add_axes([axx0/xdim,(axy0+axy+spacing)/ydim,axx/xdim,axy/ydim])
        self.axt.tick_params(labelsize=8)
        self.axt.set_xlabel('wavelength (nm)',fontsize=10, position=(0.5,0),labelpad=5)
        self.axt.set_ylabel('All contributions (%)',fontsize=10,  position=(0,0.5),labelpad=5)
        #self.axt.legend(['1-R','T'],loc='upper right',bbox_to_anchor=(1.1, 1.15),framealpha=0.5)