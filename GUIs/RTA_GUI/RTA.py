#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 15:00:13 2023

@author: tze
"""

from submodules.RW_files import Read_from, Write_to
from submodules.Figures import FigureLineMap
from submodules.tkWindget import AppFrame, FigureFrame, LoadSingleFile, SaveSingleFile
from submodules.DataProcess import absorbance_IHTM
import os
from tkinter import Frame, StringVar, Label, DISABLED, NORMAL
from common.filetypes import IHTM_type




class calc_A(AppFrame):
    def __init__(self,**kwargs):
        super().__init__(**kwargs,file=__file__,appgeometry=(1000, 650, 25, 25))
        self.init_frames()
        self.init_variables()
        self.init_commandframe()

    def __str__(self):
        return 'Total A calculation'

    def init_frames(self):
        self.commandframe=Frame(self.frameroot)
        self.commandframe.grid(row=0,column=0,sticky='N')
        self.commandframe.columnconfigure(0, weight = 1)
        self.commandframe.rowconfigure(0, weight = 1)
        self.figure=FigureFrame(parent=self.frameroot,figclass=FigureLineMap,figkwargs={'figsize':(15/2.54,14/2.54)})
        self.figure.grid(row=0,column=1,sticky='NSWE')
        self.figure.columnconfigure(0, weight = 1)
        self.figure.rowconfigure(0, weight = 1)
        
    def init_variables(self):
        self.errormsg=StringVar(self.frameroot)

    def init_commandframe(self):
        rowcount=0
        Label(self.commandframe, textvariable=self.errormsg, font='Courier', fg='#f00', bg='lightgray',width=24).grid(row = rowcount, column = 1,sticky='EW')
        rowcount+=1
        self.reflectance=LoadSingleFile(parent=self.commandframe,ini=self.ini, read=Read_from.ihtm, bg='lightblue', path='load_file_path', write_ini=self.write_ini, text='Load reflectance file', filetypes=IHTM_type,font=('Courier',10))
        self.reflectance.add_action(self.action_reflectance)
        self.reflectance.grid(row=rowcount,column=1)
        rowcount+=1
        self.transmittance=LoadSingleFile(parent=self.commandframe,ini=self.ini, read=Read_from.ihtm, bg='lightgreen', path='load_file_path', write_ini=self.write_ini, text='Load transmittance file', filetypes=IHTM_type,font=('Courier',10))
        self.transmittance.add_action(self.action_transmittance)
        self.transmittance.grid(row=rowcount,column=1)
        rowcount+=1
        self.save_data=SaveSingleFile(parent=self.commandframe,ini=self.ini, write_ini=self.write_ini, text='Save data', filetypes=[('IHTM E60','*.dtsp' )],write=self.save_data)
        self.save_data.grid(row=rowcount,column=1)
        self.save_data.config(state=DISABLED)

    def action_reflectance(self):
        tmp=self.reflectance.get_data()
        filename=self.reflectance.labelbutton.get_var()
        if tmp!=None and 'T0' in filename:
            self.reflectance.reset()
            self.transmittance._load_data(os.path.join(self.ini['load_file_path'],filename))
            if os.path.exists(os.path.join(self.ini['load_file_path'],filename.replace('T0','R0'))):
                self.reflectance._load_data(os.path.join(self.ini['load_file_path'],filename.replace('T0','R0')))
        elif tmp!=None and 'R0' in filename:
            if os.path.exists(os.path.join(self.ini['load_file_path'],filename.replace('R0','T0'))):
                self.transmittance._load_data(os.path.join(self.ini['load_file_path'],filename.replace('R0','T0')))
        elif tmp!=None and tmp['#data_summary']['y1_name']=='Reflectance':
            pass
        else:
            self.reflectance.reset()
        self.main()

    def action_transmittance(self):
        tmp=self.transmittance.get_data()
        filename=self.transmittance.labelbutton.get_var()
        if tmp!=None and 'R0' in filename:
            self.transmittance.reset()
            self.reflectance._load_data(os.path.join(self.ini['load_file_path'],filename))
            if os.path.exists(os.path.join(self.ini['load_file_path'],filename.replace('R0','T0'))):
                self.transmittance._load_data(os.path.join(self.ini['load_file_path'],filename.replace('R0','T0')))
        elif tmp!=None and 'T0' in filename:
            if os.path.exists(os.path.join(self.ini['load_file_path'],filename.replace('T0','R0'))):
                self.reflectance._load_data(os.path.join(self.ini['load_file_path'],filename.replace('T0','R0')))
        elif tmp!=None and tmp['#data_summary']['y1_name']=='Transmittance':
            pass
        else:
            self.transmittance.reset()
        self.main()

    def save_data(self,filename):
        Write_to.data(filename,self.data)

    def calculcate_data(self):
        R=self.reflectance.get_data()
        T=self.transmittance.get_data()
        if R!=None and T!=None:
            self.data=absorbance_IHTM(R,T)
            self.save_data.config(state=NORMAL)
            filename=self.reflectance.labelbutton.get_var()
            if "R0" in filename:
                filename=filename.replace('R0','A0')
            self.save_data.add_filename(filename[0:filename.index('.d')])
        else:
            self.data=None

    def main(self):
        self.calculcate_data()
        self.plot()

    def plot(self):
        if self.data!=None:
            R=self.reflectance.get_data()
            T=self.transmittance.get_data()
            self.figure.plot.plot_absorbance(R,T,self.data)
