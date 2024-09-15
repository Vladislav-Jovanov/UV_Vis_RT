#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 18 16:19:18 2022

@author: tzework
"""
from tkinter import Frame, Button, Label, StringVar, Scrollbar, Listbox, IntVar
import os
from tkinter.filedialog import askopenfilenames
from RW_data.RW_files import Files_RW
from Figure.Figure import FigureE60
from Data.Process import Process_data
from tkWindget.tkWindget import AppFrame, Rotate, OnOffButton, FigureFrame

#ax.set_yscale('log')
class container():
    pass

class plot_RTA(AppFrame):
    def __init__(self,**kwargs):
        super().__init__(**kwargs,appgeometry=(900, 540, 25, 25))
        self.init_variables()
        self.init_frames()
        self.init_mainframe()
        self.init_sideframe()
        self.init_tlmain()
        self.init_trmain()
        try:
            tmp=Files_RW().check_E60_ini(self.scriptdir,self.ini_name,self.split)
            self.filedir=tmp.filedir
        except:
            self.filedir='Documents'
            self.write_to_ini()
    
    def __str__(self):
        return 'Graph plotting'
    
        
    def init_variables(self):
        self.split=':='
        self.scriptdir=os.path.dirname(__file__)#path of this __file__ not the __main__
        self.ini_name=os.path.basename(__file__).replace(os.path.basename(__file__).split('.')[-1],'ini')
        self.errormsg=StringVar()
        self.errormsg.set('')#to display messages
        self.raw=container()
        self.raw.filename=[]
        self.raw.basename=[]
        self.raw.data=[]
        self.listboxwidth=24
    
    def write_to_ini(self):
        write=[]
        write.append(f'load_file_path{self.split}{self.filedir}')
        
        Files_RW().write_to_file(self.scriptdir,self.ini_name,write)
        
    def init_frames(self):    
        #for the buttons and file list
        self.sideframe = Frame(self.frameroot)
        self.sideframe.grid(column=0,row=0,rowspan=3)
        self.sideframe.columnconfigure(0, weight = 1)
        self.sideframe.rowconfigure(0, weight = 1)
        
        #for the controls
        self.tlmain=Frame(self.frameroot)
        self.tlmain.grid(column=1, row=1, columnspan=5,sticky='W')
        self.tlmain.columnconfigure(0, weight = 1)
        self.tlmain.rowconfigure(0, weight = 1)
        self.trmain=Frame(self.frameroot)
        self.trmain.grid(column=6, row=1, columnspan=3,sticky="E")
        self.trmain.columnconfigure(0, weight = 1)
        self.trmain.rowconfigure(0, weight = 1)
        
        #for the graph and toolbar
        self.mainframe = Frame(self.frameroot)
        #self.mainframe.pack(pady = (50,50), padx = (50,50))
        self.mainframe.grid(column=1,row=2,columnspan=8)
        self.mainframe.columnconfigure(0, weight = 1)
        self.mainframe.rowconfigure(0, weight = 1)
        
        
    def placeholder(self):
        pass
    
    def init_sideframe(self):
        rowcount=1
        Label(self.sideframe, textvariable=self.errormsg, font='Courier', fg='#f00', bg='lightgray',width=24).grid(row = rowcount, column = 1,columnspan=2) 
        
        rowcount+=1
        Button(self.sideframe, text="Open \ndata file(s)", command=self.Get_raw_file,width=12,bg='lightgray').grid(row=rowcount,column=1)
        Button(self.sideframe, text="Clear selected\ndata", command=self.Remove_loaded,width=12,bg='lightgray').grid(row=rowcount,column=2)
        
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
            
    
    def update_listbox(self):
        #self.listboxwidth=max(self.listboxwidth,len(self.raw.basename[-1]))
        self.listbox.insert(len(self.raw.basename),self.raw.basename[-1])
        #self.listbox.configure(width=self.listboxwidth)
        self.sideframe.update()
    
    
    def process_raw_file(self,filename):
        out=0
        if filename.split('.')[-1]=='dsp':
            tmp=Files_RW().load_dsp(filename)
        elif filename.split('.')[-1]=='dtsp':
            tmp=Files_RW().load_dtsp(filename)
            
        if tmp.error!='':
            self.errormsg.set(tmp.error)
        elif not self.raw.data:
            #if tmp.type in ['Reflectance','Transmittance','Absorbance','Reflectance_abs','Transmittance_abs', 'Absorption_abs']: #I only allow loading of %R files 
            Process_data().convert_units(tmp)#converts into nm
            self.raw.data.append(tmp)
            self.raw.filename.append(filename)
            self.raw.basename.append(os.path.basename(filename))
            self.update_listbox()
            out=1
        elif self.raw.data:
            #if tmp.type==self.raw.data[-1].type: #I only allow loading of %R files
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
        tmp=askopenfilenames(title="Select raw E60 data files.", initialdir=self.filedir, filetypes=[("E60 dsp files IHTM dtsp files","*.dsp *.dtsp")])#openfilenames gives you a touple####
        if tmp:#to check if anything has been read out
            #change the folder where to look for the files
            for item in tmp:
                if item not in self.raw.filename:
                    out=self.process_raw_file(item)
                    if out:#if sucess
                        self.filedir=os.path.dirname(item)
                        self.write_to_ini()
                        self.legend.enable_press()
                        self.plot_all()
                    else:
                        self.errormsg.set('Some files not loaded.')
                else:
                    self.errormsg.set('Some files not loaded.')
        
        
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
        if len(self.raw.filename)==0:
            self.legend.change_state("off")
            self.legend.disable_press()
        self.plot_all()
    
        
        
    def init_mainframe(self):
        self.figure=FigureFrame(parent=self.mainframe,figclass=FigureE60)
        self.figure.grid(row=1,column=1)
        
    def init_tlmain(self):
        Label(self.tlmain,text='Resize the y-scale:  ').grid(column=0,row=0,sticky='W')
        self.y_scale=Rotate(parent=self.tlmain,direction='horizontal',width=5,choice_list=[100,150,200,250,300,50],typevar=IntVar,command=self.change_scale)
        self.y_scale.grid(column=1, row=0, sticky='E')
        self.figure.plot.ax.set_ylim(0,self.y_scale.choice.get()+3)
        
    def change_scale(self,val):
        self.figure.plot.ax.set_ylim(0,val+3)
        self.figure.canvas.draw()
        
    def init_trmain(self):
        self.legend=OnOffButton(parent=self.trmain,imagepath=os.path.join(self.scriptdir,'images'),images=[f'leg_{image}' for image in ['on.png','off.png']],command=self.update_legend)
        self.legend.grid(column=1,row=1)
        #it should be rewritten because you do not need separate functions in figure class
        
    def change_legend(self):
        if self.legend.get_state()=="on":
            self.figure.plot.ax.legend(self.raw.basename,loc='lower right')
        else:
            if self.figure.plot.ax.get_legend():
                self.figure.plot.ax.get_legend().remove()
    
    def update_legend(self):
        self.change_legend()
        self.figure.canvas.draw()
    
    def plot_all(self):
        self.errormsg.set('')
        
        while len(self.figure.plot.ax.lines):
            self.figure.plot.ax.lines[0].remove()#lines.pop() doesn't work any more check all interactive graphs
        
        self.figure.plot.ax.set_prop_cycle(None)#resets the color cycle
        #flag=0
        xmin=2000
        xmax=100
        
        if len(self.raw.data):
            for item in self.raw.data:
                x=item.wlength
                y=item.data
                xmin=min(min(x),xmin)
                xmax=max(max(x),xmax)
                self.figure.plot.ax.plot(x,y)
            self.figure.plot.ax.set_ylabel(f'{self.raw.data[-1].type} ({self.raw.data[-1].data_units})',fontsize=10, position=(0,0.5),labelpad=5)
            self.change_legend()
        else:
            if xmin==2000 or xmax==100:
                xmin=200
                xmax=1200
            self.figure.plot.ax.set_ylabel('',fontsize=10, position=(0,0.5),labelpad=5)
            if self.figure.plot.ax.get_legend():
                self.figure.plot.ax.get_legend().remove()    
                
        
        self.figure.plot.ax.set_xlim(xmin,xmax)
        self.figure.plot.ax.set_ylim(0,self.y_scale.choice.get()+3)
        
        
        self.figure.canvas.draw()    
