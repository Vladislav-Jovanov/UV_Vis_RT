#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 18 16:19:18 2022

@author: tzework
"""
import numpy as np
from tkinter import Frame, Tk, Button, Label, SUNKEN, StringVar, IntVar, Scrollbar, Listbox
import os
from tkinter.filedialog import askopenfilename, askopenfilenames, asksaveasfilename
from RW_data.RW_files import Files_RW
from Figure.Figure import FigureE60
from Data.Process import Process_data
from tkWindget.tkWindget import Rotate, OnOffButton, AppFrame, FigureFrame

#ax.set_yscale('log')
class container():
    pass

class E60_tot_RT(AppFrame):
    def __init__(self,**kwargs):
        super().__init__(**kwargs,appgeometry=(900, 540, 25, 25))
        self.init_variables()
        self.init_frames()
        self.init_mainframe()
        self.init_ctl_frame()
        self.init_tl_frame()
        self.init_ctr_frame()
        self.init_tr_frame()
        self.init_sideframe()
        try:
            tmp=Files_RW().check_E60_ini(self.scriptdir,self.ini_name,self.split)
            self.filedir=tmp.filedir
            self.savedir=tmp.savedir
            self.refdir=tmp.refdir
            if tmp.reffile!='':
                self.reffile.set(tmp.reffile)
                self.process_reference_file(os.path.join(tmp.refdir,tmp.reffile))
        except:
            self.filedir='Documents'
            self.refdir='Documents'
            self.savedir='Documents'
            self.write_to_ini()
    
    def __str__(self):
        return 'E60_data_process'
    
        
    def init_variables(self):
        self.split=':='
        self.scriptdir=os.path.dirname(__file__)#path of this __file__ not the __main__
        self.ini_name=os.path.basename(__file__).replace(os.path.basename(__file__).split('.')[-1],'ini')
        self.reffile=StringVar()
        self.reffile.set('')
        self.errormsg=StringVar()
        self.errormsg.set('')#to display messages
        self.raw=container()
        self.raw.filename=[]
        self.raw.basename=[]
        self.raw.data=[]
        self.avgdata=container()
        self.listboxwidth=24
        self.pressnames=['ref','data','avg']
        self.pressbuttons={}
    
    def write_to_ini(self):
        write=[]
        write.append(f'reference_path{self.split}{self.refdir}')
        write.append(f'reference_file{self.split}{self.reffile.get()}')
        write.append(f'load_file_path{self.split}{self.filedir}')
        write.append(f'save_file_path{self.split}{self.savedir}')
        
        Files_RW().write_to_file(self.scriptdir,self.ini_name,write)
        
    def init_frames(self):    
        #for the buttons and file list
        self.sideframe = Frame(self.frameroot)
        self.sideframe.grid(column=0,row=0,rowspan=3)
        self.sideframe.columnconfigure(0, weight = 1)
        self.sideframe.rowconfigure(0, weight = 1)
        
        #for the label text avg points
        self.tl_frame=Frame(self.frameroot)
        self.tl_frame.grid(column=1,row=0)
        self.tl_frame.columnconfigure(0, weight = 1)
        self.tl_frame.rowconfigure(0, weight = 1)
        
        #for the label text what to show
        self.tr_frame=Frame(self.frameroot)
        self.tr_frame.grid(column=2,row=0,sticky='W')
        self.tr_frame.columnconfigure(0, weight = 1)
        self.tr_frame.rowconfigure(0, weight = 1)
        
        #for the graph and toolbar
        self.mainframe = Frame(self.frameroot)
        #self.mainframe.pack(pady = (50,50), padx = (50,50))
        self.mainframe.grid(column=1,row=2, columnspan=2)
        self.mainframe.columnconfigure(0, weight = 1)
        self.mainframe.rowconfigure(0, weight = 1)
        
        #for the avg points control
        self.ctl_frame=Frame(self.frameroot)
        self.ctl_frame.grid(column=1,row=1)
        self.ctl_frame.columnconfigure(0, weight = 1)
        self.ctl_frame.rowconfigure(0, weight = 1)
        
        #for the display control
        self.ctr_frame=Frame(self.frameroot)
        self.ctr_frame.grid(column=2,row=1)
        self.ctr_frame.columnconfigure(0, weight = 1)
        self.ctr_frame.rowconfigure(0, weight = 1)
        
    def placeholder(self):
        pass
    
    def init_sideframe(self):
        rowcount=1
        Label(self.sideframe, textvariable=self.errormsg, font='Courier', fg='#f00', bg='lightgray',width=24).grid(row = rowcount, column = 1,columnspan=2)
        rowcount+=1
        Button(self.sideframe, text="Open reference\ndata file", command=self.Get_ref_file,width=12,bg='lightgray').grid(row=rowcount,column=1)
        
        tmp=OnOffButton(parent=self.sideframe,imagepath=os.path.join(self.scriptdir,'images'),images=[f'use_{image}' for image in ['on.png','off.png']],command=self.plot_all)
        tmp.grid(row=rowcount,column=2)
        self.pressbuttons['use']=tmp
        
        rowcount+=1
        Button(self.sideframe, text="Open \ndata file(s)", command=self.Get_raw_file,width=12,bg='lightgray').grid(row=rowcount,column=1)
        Button(self.sideframe, text="Clear selected\ndata", command=self.Remove_loaded,width=12,bg='lightgray').grid(row=rowcount,column=2)
        rowcount+=1
        Button(self.sideframe, text="Save\ndata", command=self.save_data,width=12,bg='lightgray').grid(row=rowcount,column=1)
        Button(self.sideframe, text="Save\n1-R", command=self.save_one_data,width=12,bg='lightgray').grid(row=rowcount,column=2)
        #tmp=OnOffButton(parent=self.sideframe,imagepath=os.path.join(self.scriptdir,'images'),images=[f'log_{image}' for image in ['on.png','off.png']],command=self.plot_all)
        #tmp.enable_press()
        #tmp.grid(row=rowcount,column=2)
        #self.pressbuttons['log']=tmp
        
        rowcount+=1
        Label(self.sideframe, font='Courier',width=24,text='Reference data:',anchor='w').grid(row=rowcount,column=1,columnspan=2)
        rowcount+=1
        Label(self.sideframe, font='Courier',width=24, wraplength=240,justify='left',relief=SUNKEN, textvariable=self.reffile,anchor='w').grid(row=rowcount,column=1,columnspan=2)
        rowcount+=1
        Label(self.sideframe, font='Courier',width=24,text='Loaded files:',anchor='w').grid(row=rowcount,column=1,columnspan=2)
        rowcount+=1
        self.xscrollbar=Scrollbar(self.sideframe,orient='horizontal')
        self.xscrollbar.grid(row = rowcount, column = 1, columnspan=2, sticky='EW')
        rowcount+=1
        self.listbox=Listbox(self.sideframe, font='Courier', selectbackground='red', selectmode='extended',width=24, height=7)
        self.listbox.grid(row = rowcount, column = 1,columnspan=2,rowspan=5)
        self.scrollbar=Scrollbar(self.sideframe)
        self.scrollbar.grid(row = rowcount, column = 3, rowspan=5, sticky='NS')
        self.listbox.config(yscrollcommand = self.scrollbar.set)
        self.scrollbar.config(command = self.listbox.yview)
        #now configure xscrollbar
        self.listbox.config(xscrollcommand = self.xscrollbar.set)
        self.xscrollbar.config(command = self.listbox.xview)
    
    
    #IHTM type of file should be here
    #comment
    #setup
    #data_header
    #data_table
    def save_data(self):
        self.errormsg.set("")
        if self.raw.data:
            if (self.raw.data[0].type=="Reflectance" and self.pressbuttons['use'].get_state()=="off"):
                self.errormsg.set("Turn on the reference!")
                return
            if (self.raw.data[0].type in ["Transmittance","Absorbance"] and self.pressbuttons['use'].get_state()=="on"):
                self.errormsg.set("Turn off the reference!")
                return
            
            header=[]
            text='#data_header'
            header.append(text)
            text='wavelength\t'+self.raw.data[0].type+'_abs'
            header.append(text)
            text='nm\t%'
            header.append(text)
            text='#data_table'
            header.append(text)
            data=np.append(self.avgdata.wlength[:,np.newaxis],self.avgdata.data[:,np.newaxis],axis=1)
            fmtlist=['%s','%.6e']
            init_file=os.path.splitext(self.raw.basename[0])[0]
            filename = asksaveasfilename(title="Select the folder to save the processed data.", initialdir=self.savedir,filetypes=[("E60 tab sep file","*.dtsp")],initialfile=f'{init_file}.dtsp')
            if filename:
                Files_RW().write_header_data(os.path.dirname(filename),os.path.basename(filename),header,data,fmtlist)
                self.savedir=os.path.dirname(filename)
                self.write_to_ini()
    
    def save_one_data(self):
        self.errormsg.set("")
        if self.raw.data:
            if (self.raw.data[0].type=="Reflectance" and self.pressbuttons['use'].get_state()=="off"):
                self.errormsg.set("Turn on the reference!")
                return
            if self.raw.data[0].type in ["Transmittance","Absorbance"]:
                self.errormsg.set("Only 1-R!")
                return
            header=[]
            text='#data_header'
            header.append(text)
            text='wavelength\t'+'1-R_abs'
            header.append(text)
            text='nm\t%'
            header.append(text)
            text='#data_table'
            header.append(text)
            data=np.append(self.avgdata.wlength[:,np.newaxis],100-self.avgdata.data[:,np.newaxis],axis=1)
            fmtlist=['%s','%.6e']
            init_file=os.path.splitext(self.raw.basename[0])[0]
            init_file=init_file.replace("_R","_1-R")
            filename = asksaveasfilename(title="Select the folder to save the processed data.", initialdir=self.savedir,filetypes=[("E60 tab sep file","*.dtsp")],initialfile=f'{init_file}.dtsp')
            if filename:
                Files_RW().write_header_data(os.path.dirname(filename),os.path.basename(filename),header,data,fmtlist)
                self.savedir=os.path.dirname(filename)
                self.write_to_ini()
            
    def process_reference_file(self,filename):
        tmp=Files_RW().load_reference_TMM(filename)
        if tmp.error!='':
            self.reffile.set('')
            #self.turn_off_ref_switches()
            self.pressbuttons['ref'].disable_press()
            self.pressbuttons['use'].disable_press()
            self.pressbuttons['ref'].change_state('off')
            self.pressbuttons['use'].change_state('off')
            self.errormsg.set(tmp.error)
        else:
            self.reference=tmp
            self.reffile.set(os.path.basename(filename))
            Process_data().convert_units(self.reference)#converts into nm via mutuable property
            self.pressbuttons['ref'].enable_press()
            self.pressbuttons['use'].enable_press()
        
    def Get_ref_file(self):
        self.errormsg.set('')
        tmp=askopenfilename(title="Select reference data file.", initialdir=self.refdir, filetypes=[("TMM calculation files","*.tmm")])
        if tmp:#to check if anything has been read out
            #change the folder where to look for the files
            self.process_reference_file(tmp)
            if self.errormsg.get()=='':
                self.refdir=os.path.dirname(tmp)
                self.write_to_ini()
                self.plot_all()
    
    def update_listbox(self):
        #self.listboxwidth=max(self.listboxwidth,len(self.raw.basename[-1]))
        self.listbox.insert(len(self.raw.basename),self.raw.basename[-1])
        #self.listbox.configure(width=self.listboxwidth)
        self.sideframe.update()
    
    
    def process_raw_file(self,filename):
        out=0
        tmp=Files_RW().load_dsp(filename)
        if tmp.error!='':
            self.errormsg.set(tmp.error)
        elif not self.raw.data:
            if tmp.type in ['Reflectance','Transmittance','Absorbance']: #I only allow loading of %R files 
                Process_data().convert_units(tmp)#converts into nm
                self.raw.data.append(tmp)
                self.raw.filename.append(filename)
                self.raw.basename.append(os.path.basename(filename))
                self.update_listbox()
                out=1
        elif self.raw.data:
            if tmp.type==self.raw.data[-1].type: #I only allow loading of %R files
                Process_data().convert_units(tmp)#converts into nm
                self.raw.data.append(tmp)
                self.raw.filename.append(filename)
                self.raw.basename.append(os.path.basename(filename))
                self.update_listbox()
                out=1
            #returns success
        return out
   
         
    def Get_raw_file(self):
        self.errormsg.set('')
        tmp=askopenfilenames(title="Select raw E60 data files.", initialdir=self.filedir, filetypes=[("E60 dsp files","*.dsp")])#openfilenames gives you a touple####
        if tmp:#to check if anything has been read out
            #change the folder where to look for the files
            for item in tmp:
                if item not in self.raw.filename:
                    out=self.process_raw_file(item)
                    if out:#if sucess
                        self.filedir=os.path.dirname(item)
                        self.write_to_ini()
                        self.plot_all()
                    else:
                        self.errormsg.set('Some files not loaded.')
                else:
                    self.errormsg.set('Some files not loaded.')
        if self.raw.data:
            self.pressbuttons['avg'].enable_press()
            self.pressbuttons['data'].enable_press()
        
        
    def Remove_loaded(self):
        self.errormsg.set('')
        selected=[]
        for item in self.listbox.curselection():
            selected.append(item)
        selected.sort()
        selected.reverse()
        for item in selected:
            self.listbox.delete(item)
            self.raw.data.pop(item)
            self.raw.filename.pop(item)
            self.raw.basename.pop(item)
        if not len(self.raw.data):
            self.pressbuttons['avg'].disable_press()
            self.pressbuttons['data'].disable_press()
            self.pressbuttons['avg'].change_state('off')
            self.pressbuttons['data'].change_state('off')
        self.plot_all()
    
    def init_tr_frame(self):
        rowcount=1
        Label(self.tr_frame,font='Courier',width=20,text='Averaging points',background=None).grid(row=rowcount,column=1)
        
    def init_ctr_frame(self):
        rowcount=1
        self.movavg_list=[0,1,3,5,7]
        self.movavg=self.movavg_list[0]
        self.avg_num=Rotate(parent=self.ctr_frame,direction='horizontal',width=5,choice_list=self.movavg_list,typevar=IntVar,command=self.movavg_change)
        self.avg_num.grid(column=1,row=rowcount,sticky='WE')
        
    def movavg_change(self,avg):
        self.errormsg.set('')
        self.movavg=avg
        self.plot_all()
    
    def init_tl_frame(self):
        rowcount=1
        Label(self.tl_frame,font='Courier',width=20,text='Control display',background=None).grid(row=rowcount,column=1)
        
    def init_ctl_frame(self):
        rowcount=1
        columncount=1
        for idx,item in enumerate(self.pressnames):
            tmp=OnOffButton(parent=self.ctl_frame,imagepath=os.path.join(self.scriptdir,'images'),images=[f'{self.pressnames[idx]}_{image}' for image in ['on.png','off.png']],command=self.plot_all)
            tmp.grid(row=rowcount,column=columncount+idx)
            self.pressbuttons[item]=tmp
        
    def init_mainframe(self):
        self.figure=FigureFrame(parent=self.mainframe,figclass=FigureE60)
        self.figure.grid(row=1,column=1)
    
        #it should be rewritten because you do not need separate functions in figure class
    def plot_all(self):
        self.errormsg.set('')
        if len(self.raw.data):
            self.avgdata=Process_data().average_curves(self.raw.data)
            self.avgdata.data=Process_data().mov_average(self.avgdata.data,self.movavg)
            if self.pressbuttons['use'].get_state()=='on':#only for the reference last in the pressmarkers
                tmp=Process_data().absolute_reflectance(self.avgdata,self.reference)
                self.avgdata.data=tmp.data
                self.avgdata.wlength=tmp.wlength
        
        while len(self.figure.plot.ax.lines):
            self.figure.plot.ax.lines[0].remove()#lines.pop() doesn't work any more check all interactive graphs
        
        self.figure.plot.ax.set_prop_cycle(None)#resets the color cycle
        #flag=0
        xmin=2000
        xmax=100
        ymin=0
        ymax=103
        if self.raw.data:
            if self.raw.data[-1].type == 'Absorbance':
                ymax=1
        for item in self.pressnames:#only for center top right
            if item=='ref' and self.pressbuttons[item].get_state()=='on':
                x=self.reference.wlength
                y=self.reference.data
                xmin=min(min(x),xmin)
                xmax=max(max(x),xmax)
                self.figure.plot.ax.plot(x,100*y,'k')
                #flag=1
            if item=='data' and self.pressbuttons[item].get_state()=='on':
                #flag=2
                for item in self.raw.data:
                    x=item.wlength
                    y=item.data
                    xmin=min(min(x),xmin)
                    xmax=max(max(x),xmax)
                    self.figure.plot.ax.plot(x,y)
            if item=='avg' and self.pressbuttons[item].get_state()=='on':
                #flag=2
                x=self.avgdata.wlength
                y=self.avgdata.data
                xmin=min(min(x),xmin)
                xmax=max(max(x),xmax)
                self.figure.plot.ax.plot(x,y,'r')
        if xmin==2000 or xmax==100:
                ymin=0
                ymax=1
                xmin=200
                xmax=1200
                self.figure.plot.ax.set_ylabel('',fontsize=10, position=(0,0.5),labelpad=5)
        else:
            if len(self.raw.data):
                self.figure.plot.ax.set_ylabel(f'{self.raw.data[-1].type} ({self.raw.data[-1].data_units})',fontsize=10, position=(0,0.5),labelpad=5)
            else:
                self.figure.plot.ax.set_ylabel('(%)',fontsize=10, position=(0,0.5),labelpad=5)
                
        #if self.pressbuttons['log'].get_state()=='off':
        #    self.figure.ax.set_yscale('linear')
        #if self.pressbuttons['log'].get_state()=='on':
        #    self.figure.ax.set_yscale('log')
        #    if flag==2:
        #        ymin=min(y)*1e-1
        #    elif flag==1:
        #        ymin=min(y)*1e2*1e-1
        #    else:
        #        ymin=1e-1
        
        self.figure.plot.ax.set_xlim(xmin,xmax)
        self.figure.plot.ax.set_ylim(ymin,ymax)
        
        
        self.figure.canvas.draw()    
