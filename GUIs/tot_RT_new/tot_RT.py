#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 18 16:19:18 2022

@author: tzework
"""
import numpy as np
from tkinter import Frame, Button, Label, SUNKEN, StringVar, IntVar
import os
from tkinter.filedialog import askopenfilename, askopenfilenames, asksaveasfilename
from RW_data.RW_files import Read_from, Write_to
from Figures.Figures import FigureXY2
#from DataProcess import convert_units
from tkWindget.tkWindget import Rotate, CheckBox, AppFrame, FigureFrame, LoadSingleFile



class E60_tot_RT(AppFrame):
    def __init__(self,**kwargs):
        super().__init__(**kwargs,file=__file__,appgeometry=(900, 540, 25, 25))
        self.init_variables()
        self.init_frames()
        self.init_loadframe()
        self.init_displayframe()
        self.init_dataframe()
        
        #if 'ref_file_name' in self.ini and 'ref_file_path' in self.ini:
        #    self.reffile.set(self.ini['ref_file_name'])
        #    self.process_reference_file(os.path.join(self.ini['ref_file_path'],self.ini['ref_file_name']))

    def __str__(self):
        return 'E60_process_data'
    
            
    def placeholder(self):
        pass    
    
    def init_variables(self):
        self.scriptdir=os.path.dirname(__file__)
        self.display_control={}
        self.data_buttons={}
        self.movavg_list=[0,1,3,5,7]

        
    def init_frames(self):    
        #for the buttons and file list
        self.controlframe = Frame(self.frameroot)
        self.controlframe.grid(column=0,row=0)
        
        self.figframe=FigureFrame(parent=self.frameroot,figclass=FigureXY2)
        self.figframe.grid(column=1,row=0)
        
        #for load file
        self.loadframe=Frame(self.controlframe)#,background='aquamarine2'
        self.loadframe.grid(column=0,row=0,sticky='E')
        
        #for the display control
        self.displayframe=Frame(self.controlframe)
        self.displayframe.grid(column=0,row=1,sticky='E')
        #self.ctr_frame.columnconfigure(0, weight = 1)
        #self.ctr_frame.rowconfigure(0, weight = 1)
        #for the data manipulatoin
        self.dataframe=Frame(self.controlframe)#,background='bisque2'
        self.dataframe.grid(column=0,row=2,sticky='E')
        
    def init_loadframe(self):
        rowcount=0
        Label(self.loadframe,text='Load files',relief=SUNKEN, borderwidth=2,width=35,anchor = "e").grid(row=rowcount,column=1,sticky='E')
        rowcount+=1
        self.load_abs_ref=LoadSingleFile(parent=self.loadframe,ini=self.ini, path='ref_file_path', write_ini=self.write_ini,  text='Load absolute\nreference', filetypes=[('Ref file','*.txt *.tmm' )])
        self.load_abs_ref.add_action(self.load_ref_action)
        self.load_abs_ref.grid(row=rowcount,column=1,sticky='E')
        rowcount+=1
        tmp=CheckBox(parent=self.loadframe,text='Use absolute reference',commandon=self.load_abs_ref.enable,commandoff=self.load_abs_ref.disable)
        tmp.change_state('on')
        tmp.grid(row=rowcount, column=1,sticky='E')
        
        rowcount+=1
        self.load_rel_ref=LoadSingleFile(parent=self.loadframe,ini=self.ini, read=Read_from.dsp, path='load_file_path', write_ini=self.write_ini, text='Load measured\nreference', filetypes=[('E60 file','*.dsp' )])
        self.load_rel_ref.grid(row=rowcount,column=1,sticky='E')
        rowcount+=1
        tmp=CheckBox(parent=self.loadframe,text='Use measured reference',commandon=self.load_rel_ref.enable,commandoff=self.load_rel_ref.disable)
        tmp.change_state('on')
        tmp.grid(row=rowcount, column=1,sticky='E')
        
        rowcount+=1
        self.load_measured=LoadSingleFile(parent=self.loadframe,ini=self.ini, read=Read_from.dsp, path='load_file_path', write_ini=self.write_ini, text='Load measured\ndata', filetypes=[('E60 file','*.dsp' )])
        self.load_measured.grid(row=rowcount,column=1,sticky='E')
        
    def init_displayframe(self):
        rowcount=0
        Label(self.displayframe,text='Display control',relief=SUNKEN, borderwidth=2,width=35,anchor = "e").grid(row=rowcount,column=1,columnspan=3,sticky='E')
        rowcount+=1
        self.displayall=Button(self.displayframe,text='Select all',command=self.select_display)
        self.displayall.grid(row=rowcount,column=1)
        self.displaynone=Button(self.displayframe,text='Select none',command=self.deselect_display)
        self.displaynone.grid(row=rowcount,column=3)
        Label(self.displayframe,width=1).grid(column=2,row=rowcount,rowspan=4)
        rowcount+=1
        
        self.display_control['ref_abs']=CheckBox(parent=self.displayframe,text='Absolute reference',command=self.checkbox_action)
        self.display_control['ref_abs'].grid(row=rowcount,column=1,sticky='W')
        self.display_control['data']=CheckBox(parent=self.displayframe,text='Data')
        self.display_control['data'].grid(row=rowcount,column=3,sticky='W')
        rowcount+=1
        self.display_control['ref_raw']=CheckBox(parent=self.displayframe,text='Measured reference')
        self.display_control['ref_raw'].grid(row=rowcount,column=1,sticky='W')
        self.display_control['1-data']=CheckBox(parent=self.displayframe,text='1-Data')
        self.display_control['1-data'].grid(row=rowcount,column=3,sticky='W')
        rowcount+=1
        
        self.display_control['data_raw']=CheckBox(parent=self.displayframe,text='Measured data')
        self.display_control['data_raw'].grid(row=rowcount,column=1,sticky='W')
        self.display_control['log_data']=CheckBox(parent=self.displayframe,text='Log(Data)')
        self.display_control['log_data'].grid(row=rowcount,column=3,sticky='W')
        
      
    def init_dataframe(self):
        rowcount=0
        Label(self.dataframe,text='Data control',relief=SUNKEN, borderwidth=2,width=35,anchor = "e").grid(row=rowcount,column=0,columnspan=2,sticky='E')
        rowcount+=1
        Label(self.dataframe, text='Points to smooth:',anchor='w').grid(row=rowcount, column=0,sticky='W')
        self.data_buttons['save']=Button(self.dataframe, text='Save data')
        self.data_buttons['save'].grid(column=1,row=rowcount,rowspan=2,sticky='E')
        rowcount+=1
        self.avg_num=Rotate(parent=self.dataframe,direction='horizontal',width=5,choice_list=self.movavg_list,typevar=IntVar,command=self.movavg_change)
        
        self.avg_num.grid(column=0,row=rowcount,sticky='w')
        rowcount+=1
        self.data_buttons['savelog']=Button(self.dataframe, text='Save log(data)')
        self.data_buttons['savelog'].grid(column=0,row=rowcount,sticky='W')
        self.data_buttons['save1-data']=Button(self.dataframe, text='Save 1-data')
        self.data_buttons['save1-data'].grid(column=1,row=rowcount,sticky='E')

    def load_ref_action(self):
        #self.figframe.plot.plot_loaded_curves([self.load_abs_ref.get_data()],[self.display_control['ref_abs'].get_state()])
        print(self.load_abs_ref.get_data())
        print(self.display_control['ref_abs'].get_state())
        
    def checkbox_action(self):
        self.load_ref_action()
    def movavg_change(self,avg):
        self.update_avg()
        #self.plot_all()
    
    def update_avg(self):
        pass
    
    def select_display(self):
        for key in self.display_control.keys():
            self.display_control[key].change_state('on')
    
    def deselect_display(self):
        for key in self.display_control.keys():
            self.display_control[key].change_state('off')
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
#                Files_RW().write_header_data(os.path.dirname(filename),os.path.basename(filename),header,data,fmtlist)
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
#                Files_RW().write_header_data(os.path.dirname(filename),os.path.basename(filename),header,data,fmtlist)
                self.savedir=os.path.dirname(filename)
                self.write_to_ini()
            
    def process_reference_file(self,filename):
        tmp=Read_from.ihtm(filename)
        if tmp['error']!='':
            self.reffile.set('')
            #self.turn_off_ref_switches()
            self.pressbuttons['ref'].disable_press()
            self.pressbuttons['use'].disable_press()
            self.pressbuttons['ref'].change_state('off')
            self.pressbuttons['use'].change_state('off')
            self.errormsg.set(tmp['error'])
        else:
            self.reference=tmp
            self.reference['#data_table']=self.reference['#data_table'][:,0:2]#to take only wavelength and reflectance
            for idx in range(0,self.reference['#data_summary']['tot_col']):
                if idx>1:
                    self.reference['#data_summary'].pop(f'y1_{idx}_name')
                    self.reference['#data_summary'].pop(f'y1_{idx}_col')
                    self.reference['#data_summary'].pop(f'y1_{idx}_unit')
            self.reference['#data_summary']['tot_col']=2
            self.reference['#data_summary']['y1_1_name']='Reflectance'
            self.reffile.set(os.path.basename(filename))
            print(self.reference['#data_summary'])
            A=self.reference
            #self.reference['#data_table'][:,0],self.reference['#data_summary']['x1_unit']=Process_data().convert_units(self.reference['#data_table'][:,0],self.reference['#data_summary']['x1_unit'])
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
        tmp=Read_from.ihtm(filename)
        if tmp.error!='':
            self.errormsg.set(tmp.error)
        elif not self.raw.data:
            if tmp.type in ['Reflectance','Transmittance','Absorbance']: #I only allow loading of %R files 
#                Process_data().convert_units(tmp)#converts into nm
                self.raw.data.append(tmp)
                self.raw.filename.append(filename)
                self.raw.basename.append(os.path.basename(filename))
                self.update_listbox()
                out=1
        elif self.raw.data:
            if tmp.type==self.raw.data[-1].type: #I only allow loading of %R files
 #               Process_data().convert_units(tmp)#converts into nm
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
