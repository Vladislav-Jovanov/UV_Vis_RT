#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 15:00:13 2023

@author: tze
"""

from RW_data.RW_files import Files_RW
from Figure.Figure import Figure_top_bottom
from tkWindget.tkWindget import AppFrame, FigureFrame
import numpy as np
import os
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter import Frame, StringVar, Label, Button, SUNKEN, OptionMenu, DoubleVar, Entry, DISABLED, NORMAL




class calc_A(AppFrame):
    def __init__(self,**kwargs):
        super().__init__(**kwargs,file=__file__,appgeometry=(800, 650, 25, 25))
        self.init_frames()
        self.init_variables()
        self.init_commandframe()
        try:
            tmp=Files_RW().check_E60_ini(self.scriptdir,self.ini_name,self.split)
            self.filedir=tmp.filedir
            self.savedir=tmp.savedir
        except:
            self.filedir='Documents'
            self.savedir='Documents'
    
    def __str__(self):
        return 'Total A calculation'
    
    def init_frames(self):
        self.commandframe=Frame(self.frameroot)
        self.commandframe.grid(row=0,column=0,sticky='N')
        self.commandframe.columnconfigure(0, weight = 1)
        self.commandframe.rowconfigure(0, weight = 1)
        self.figure=FigureFrame(parent=self.frameroot,figclass=Figure_top_bottom)
        self.figure.grid(row=0,column=1,sticky='NSWE')
        self.figure.columnconfigure(0, weight = 1)
        self.figure.rowconfigure(0, weight = 1)
        
    def init_variables(self):
        #you should create some simple class for this since it is used everywhere
        #self.prefixes #self.convert_units
        #self.quantities={'Height': 'm', 'Magnitude': 'A', 'Phase': 'deg', 'Surface Potential': 'V'}
        #self.prefixes={'':1, 'm':1e-3,'μ':1e-6,'n':1e-9,'p':1e-12,'f':1e-15, 'k':1e3, 'M':1e6}
        self.quantities=['Reflectance_abs','Transmittance_abs']
        self.split=':='
        self.scriptdir=os.path.dirname(__file__)
        self.ini_name=os.path.basename(__file__).replace(os.path.basename(__file__).split('.')[-1],'ini')
        self.reflectance={'filename':StringVar(),'method':'','data': np.empty((0,0)),'data_unit':'', 'wlength':np.empty((0,)), 'wlength_unit':''}
        self.transmittance={'filename':StringVar(),'method':'','data': np.empty((0,0)), 'data_unit':'', 'wlength':np.empty((0,)), 'wlength_unit':''}
        self.errormsg=StringVar(self.frameroot)
        self.reflectance['filename'].set('Load reflectance file')
        self.transmittance['filename'].set('Load transmittance file')
        self.controls={}
        
    def set_empty(self,dictionary,string):
        dictionary['filename'].set(string)
        dictionary['method']=''
        dictionary['data']=np.empty((0,0))
        dictionary['data_unit']=''
        dictionary['wlength']=np.empty((0,))
        dictionary['wlength_unit']=''
        

        
    def init_commandframe(self):
        rowcount=0
        Label(self.commandframe, textvariable=self.errormsg, font='Courier', fg='#f00', bg='lightgray',width=24).grid(row = rowcount, column = 1,sticky='W')
        rowcount+=1
        self.controls['reflectance']=Button(self.commandframe, bg='lightblue', textvariable=self.reflectance['filename'], command=lambda string='Reflectance_abs':self.load_file(string))
        self.controls['reflectance'].grid(row=rowcount,column=1,sticky='EW')
        
        rowcount+=1
        self.controls['transmittance']=Button(self.commandframe, bg='lightgreen', textvariable=self.transmittance['filename'], command=lambda string='Transmittance_abs':self.load_file(string))
        self.controls['transmittance'].grid(row=rowcount,column=1,sticky='EW')
        #self.controls['transmittance'].config(state=DISABLED)
        
        
        
        
        rowcount+=1
        tmpframe=Frame(self.commandframe)
        tmpframe.grid(row=rowcount, column=1)
        #self.controls['plot_data']=Button(tmpframe, bg='lightblue', text='Plot data', command=self.plot_all)
        #self.controls['plot_data'].grid(row=1,column=1,sticky='EW')
        #self.controls['plot_data'].config(state=DISABLED)
        self.controls['save_data']=Button(tmpframe, bg='lightblue', text='Save data', command=self.save_data)
        self.controls['save_data'].grid(row=1,column=2,sticky='EW')
        self.controls['save_data'].config(state=DISABLED)
        
    
    def load_stuff(self,filename,string):
        self.filedir=os.path.dirname(filename)
        self.write_to_ini()
        tmp=Files_RW().load_dtsp(filename)
        if tmp.error!='':
            self.errormsg.set(tmp.error)
            return 1
        elif tmp.type!=string:
            self.errormsg.set('Wrong file loaded')
            return 1
        else:
            if string=="Transmittance_abs":
                self.process_data(self.transmittance,tmp,filename)    
            elif string=='Reflectance_abs':
                self.process_data(self.reflectance,tmp,filename)
            self.check_data(string)
            return 0
    
    def load_file(self,string):
        self.errormsg.set('')
        filename=askopenfilename(title="Select *.dtsp files.", initialdir=self.filedir, filetypes=[("IHTM dtsp files","*.dtsp")])#openfilenames gives you a touple####
        if filename:#to check if anything has been read out
            #change the folder where to look for the files
            check=self.load_stuff(filename,string)
            if not check:
                if string==self.quantities[0]:
                    newstring=self.quantities[1]
                    newfilename=filename.replace('_R','_T')
                else:
                    newstring=self.quantities[0]
                    newfilename=filename.replace('_T','_R')
                if os.path.isfile(newfilename):
                    self.load_stuff(newfilename,newstring)
                    self.plot_all()
                    
                
            
                
    def check_data(self,string):
        self.errormsg.set('')
        
        condition = (self.reflectance['filename'].get().split('_')[0]==self.transmittance['filename'].get().split('_')[0])
        #second one allows that you load up what ever you want
        #condition = (self.reflectance['filename'].get()!='Load reflectance file' and self.transmittance['filename'].get()!='Load transmittance file')
        if condition:
            #self.controls['plot_data'].config(state=NORMAL)
            self.plot_all()
            self.controls['save_data'].config(state=NORMAL)
        else:
            self.clear_plots()
            if string==self.quantities[0]:
                self.set_empty(self.transmittance, 'Load transmittance file')
            elif string==self.quantities[1]:
                self.set_empty(self.reflectance, 'Load reflectance file')
                
            #self.controls['plot_data'].config(state=DISABLED)
            self.controls['save_data'].config(state=DISABLED)
    
        
                    
    def process_data(self,dictionary,data,filename):
        dictionary['filename'].set(os.path.basename(filename))
        dictionary['method']=data.type
        dictionary['data']=data.data
        dictionary['data_unit']=data.data_units
        dictionary['wlength']=data.wlength
        dictionary['wlength_unit']=data.wlength_units
        
    def write_to_ini(self):
        write=[]
        write.append(f'load_file_path{self.split}{self.filedir}')
        write.append(f'save_file_path{self.split}{self.savedir}')
        
        Files_RW().write_to_file(self.scriptdir,self.ini_name,write)
            
    # def __init__(self,**kwargs):
    #     super().__init__(**kwargs,appgeometry=(900, 540, 25, 25))
    #     self.plot=TMMfigure()
    #     sample='PDMS_2.5-TiO2'
    #     filedir='/home/tze/Documents/'
    #     filenameT=f'{sample}_T01.dtsp'
    #     filenameR=f'{sample}_R01.dtsp'
    #     self.plot.axtl.set_title(f'{sample}', fontsize=10)
    #     #self.plot.axbl.set_title('CN221204', fontsize=10)
    #     #tmpT=Files_RW().load_dtsp(os.path.join(filedir,filenameT))
    #     #tmpR=Files_RW().load_dtsp(os.path.join(filedir,filenameR))
    #     self.color_list=['red','lightgray','white']
    #     #Z=np.zeros(np.shape(tmpT.data))
    #     #Z=np.expand_dims(Z, axis=0)
    #     #B=(100-tmpT.data-tmpR.data)/100
    #     #B=np.expand_dims(B,axis=0)
    #     #A=np.append(Z,B,axis=0)
    #     #A=np.append(A,A[-1,:]+Z,axis=0)
    #     #A=np.append(A,A[-1,:]+Z,axis=0)
    #     #print(A[-1,:])
    #     #A=np.append(A,A[-1,:]+np.expand_dims(tmpT.data,axis=0)/100,axis=0)
    #     #print(A[-1,:])
    #     #A=np.append(A,A[-1,:]+np.expand_dims(tmpR.data,axis=0)/100,axis=0)
    #     #print(A[-1,:])
    #     #self.save_data(tmpT,tmpR,filedir,sample)
    #     #self.plot_all(tmpT.wlength*1e-9,tmpR.data/100,tmpT.data/100,A)
    #     self.plot.axbl.legend(['Active', 'T', 'R'],loc='upper right',bbox_to_anchor=(1.1, 1.15),framealpha=0.5)
        
    #     self.canvas=FigureCanvasTkAgg(self.plot.fig,master=self.frameroot)
    #     self.canvas.get_tk_widget().grid(row=1,column=1)
    #     self.canvas.draw()
    #     toolbar = NavigationToolbar2Tk(self.canvas, self.frameroot, pack_toolbar=False)
    #     toolbar.update()
    #     toolbar.grid(row=2,column=1)
        
    def clear_plots(self):
        while len(self.figure.plot.axt.collections):
            self.figure.plot.axt.collections[-1].remove()
        while len(self.figure.plot.axt.lines):
            self.figure.plot.axt.lines[-1].remove()
        while len(self.figure.plot.axb.lines):
            self.figure.plot.axb.lines[-1].remove()
        self.figure.canvas.draw()
        
    def plot_all(self):
        self.clear_plots()
        self.figure.plot.axt.set_prop_cycle(None)
        self.figure.plot.axt.set_xlim(self.reflectance['wlength'][0],self.reflectance['wlength'][-1])
        self.figure.plot.axt.plot(self.reflectance['wlength'],self.transmittance['data'],color='black')
        self.figure.plot.axt.plot(self.reflectance['wlength'],100-self.reflectance['data'],color='blue')
        self.figure.plot.axt.set_ylim(min(0,np.min(self.transmittance['data'])),100)
        self.figure.plot.axt.fill_between(self.reflectance['wlength'],self.transmittance['data'],100-self.reflectance['data'],color='red')
        self.figure.plot.axt.legend(['T','1-R','A'],loc='lower right',framealpha=0.5)
        
        self.figure.plot.axb.set_prop_cycle(None)
        self.figure.plot.axb.set_xlim(self.reflectance['wlength'][0],self.reflectance['wlength'][-1])
        self.figure.plot.axb.set_ylim(min(0,np.min(100-self.reflectance['data']-self.transmittance['data'])),100)
        self.figure.plot.axb.plot(self.reflectance['wlength'],100-self.reflectance['data']-self.transmittance['data'],color='red')
        self.figure.canvas.draw()
        
    def save_data(self):
        tmpA=100-self.reflectance['data']-self.transmittance['data']
        header=[]
        text='#data_header'
        header.append(text)
        text='wavelength\tAbsorption_abs'
        header.append(text)
        text='nm\t%'
        header.append(text)
        text='#data_table'
        header.append(text)
        data=np.append(self.reflectance['wlength'][:,np.newaxis],tmpA[:,np.newaxis],axis=1)
        fmtlist=['%s','%.6e']
        filename = asksaveasfilename(title="Select the folder to save the processed data.", initialdir=self.savedir,filetypes=[("E60 tab sep file","*.dtsp")],initialfile=f'{self.reflectance["filename"].get().replace("_R","_A")}')
        if filename:
            Files_RW().write_header_data(os.path.dirname(filename),os.path.basename(filename),header,data,fmtlist)
            self.savedir=os.path.dirname(filename)
            self.write_to_ini()
    
    
    
        
