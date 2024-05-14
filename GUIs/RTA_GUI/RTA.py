#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 15:00:13 2023

@author: tze
"""

from RW_data.RW_files import Files_RW
from Figs.figClass import TMMfigure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from tkWindget.tkWindget import AppFrame
import numpy as np
import os



class calc_A(AppFrame):
    def __init__(self,**kwargs):
        super().__init__(**kwargs,appgeometry=(900, 540, 25, 25))
        self.plot=TMMfigure()
        sample='PDMS_2.5-TiO2'
        filedir='/home/tze/Documents/'
        filenameT=f'{sample}_T01.dtsp'
        filenameR=f'{sample}_R01.dtsp'
        self.plot.axtl.set_title(f'{sample}', fontsize=10)
        #self.plot.axbl.set_title('CN221204', fontsize=10)
        tmpT=Files_RW().load_dtsp(os.path.join(filedir,filenameT))
        tmpR=Files_RW().load_dtsp(os.path.join(filedir,filenameR))
        self.color_list=['red','lightgray','white']
        Z=np.zeros(np.shape(tmpT.data))
        Z=np.expand_dims(Z, axis=0)
        B=(100-tmpT.data-tmpR.data)/100
        B=np.expand_dims(B,axis=0)
        A=np.append(Z,B,axis=0)
        #A=np.append(A,A[-1,:]+Z,axis=0)
        #A=np.append(A,A[-1,:]+Z,axis=0)
        #print(A[-1,:])
        A=np.append(A,A[-1,:]+np.expand_dims(tmpT.data,axis=0)/100,axis=0)
        #print(A[-1,:])
        A=np.append(A,A[-1,:]+np.expand_dims(tmpR.data,axis=0)/100,axis=0)
        #print(A[-1,:])
        self.save_data(tmpT,tmpR,filedir,sample)
        self.plot_all(tmpT.wlength*1e-9,tmpR.data/100,tmpT.data/100,A)
        self.plot.axbl.legend(['Active', 'T', 'R'],loc='upper right',bbox_to_anchor=(1.1, 1.15),framealpha=0.5)
        
        self.canvas=FigureCanvasTkAgg(self.plot.fig,master=self.frameroot)
        self.canvas.get_tk_widget().grid(row=1,column=1)
        self.canvas.draw()
        toolbar = NavigationToolbar2Tk(self.canvas, self.frameroot, pack_toolbar=False)
        toolbar.update()
        toolbar.grid(row=2,column=1)
        
    def plot_all(self,wlength,R,T,A):
        self.plot.axtl.plot(wlength*1e9,1-R,'red')
        self.plot.axtl.plot(wlength*1e9,T,'blue')
        self.plot.axtl.legend([r'1-R',r'T'],loc='lower right')
        for idx in range(0,np.shape(A)[0]-1):
            self.plot.axbl.fill_between(wlength*1e9,A[idx,:],A[idx+1,:],color=self.color_list[idx])
        self.plot.axtl.set_xlim(wlength[0]*1e9,wlength[-1]*1e9)
        self.plot.axtl.set_ylim(0,1.01)
        self.plot.axbl.set_xlim(wlength[0]*1e9,wlength[-1]*1e9)
        self.plot.axbl.set_ylim(0,1)
        
    def save_data(self,tmpT,tmpR,filedir,sample):
        tmpA=100-tmpT.data-tmpR.data
        header=[]
        text='#data_header'
        header.append(text)
        text='wavelength\tAbsorption_abs'
        header.append(text)
        text='nm\t%'
        header.append(text)
        text='#data_table'
        header.append(text)
        data=np.append(tmpT.wlength[:,np.newaxis],tmpA[:,np.newaxis],axis=1)
        fmtlist=['%s','%.6e']
        Files_RW().write_header_data(filedir,f'{sample}_A.dtsp',header,data,fmtlist)
    
    def __str__(self):
        return 'Total A calculation'
    
        
if __name__=='__main__':
    Test_GUI().init_start()