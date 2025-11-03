#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 18 16:19:18 2022

@author: tzework
"""
from numpy import log10, abs
from tkinter import Frame, Button, Label, RAISED, IntVar, DISABLED, NORMAL
from RW_data.RW_files import Read_from, Write_to
from Figures.Figures import FigureXY2
from DataProcess.DataProcess import convert_unit_IHTM, absolute_reflectance_IHTM, multiply_2col_IHTM, divide_2col_IHTM, average_IHTM, copy_IHTM
from tkWindget.tkWindget import Rotate, CheckBox, AppFrame, FigureFrame, LoadSingleFile, SaveSingleFile
from common.filetypes import raw_process, ref_file


class E60_tot_RT(AppFrame):
    def __init__(self,**kwargs):
        super().__init__(**kwargs,file=__file__,appgeometry=(1200, 540, 25, 25))
        self.init_variables()
        self.init_frames()
        self.init_displayframe()
        self.init_dataframe()
        self.init_loadframe()

    def __str__(self):
        return 'E60_process_data'

    def placeholder(self):
        pass    

    def init_variables(self):
        self.display_control={}
        self.data_buttons={}
        self.movavg_list=[0,1,3,5,7]
        self.data=None
        self.one_minus_data=None
        self.logdata=None
        self.init=False#needed during init phase

    def init_frames(self):    
        #for the buttons and file list
        self.controlframe = Frame(self.frameroot)
        self.controlframe.grid(column=0,row=0)
        self.figframe=FigureFrame(parent=self.frameroot,figclass=FigureXY2,figkwargs={'figsize':(15/2.54,8/2.54),'axsize':[2/15,3/15,7/15,5/8]})
        self.figframe.grid(column=1,row=0)
        #for load file
        self.loadframe=Frame(self.controlframe)#,background='aquamarine2'
        self.loadframe.grid(column=0,row=0,sticky='E')
        #for the display control
        self.displayframe=Frame(self.controlframe)
        self.displayframe.grid(column=0,row=1,sticky='E')
        #for the data manipulatoin
        self.dataframe=Frame(self.controlframe)#,background='bisque2'
        self.dataframe.grid(column=0,row=2,sticky='E')

    def init_loadframe(self):
        rowcount=0
        Label(self.loadframe,text='Load files',relief=RAISED,background='bisque2', borderwidth=2,width=35,anchor = "e").grid(row=rowcount,column=1,sticky='E')
        rowcount+=1
        self.load_abs_ref=LoadSingleFile(parent=self.loadframe,ini=self.ini, path='ref_file_path', write_ini=self.write_ini,  text='Load absolute\nreference', filetypes=ref_file)
        self.load_abs_ref.add_action(self.load_abs_action)
        self.load_abs_ref._action()
        self.load_abs_ref.grid(row=rowcount,column=1,sticky='E')
        rowcount+=1
        self.load_abs_check=CheckBox(parent=self.loadframe,text='Use absolute reference',commandon=self.abs_check_on,commandoff=self.abs_check_off)
        self.load_abs_check.change_state('on')
        self.load_abs_check.grid(row=rowcount, column=1,sticky='E')
        rowcount+=1
        self.load_rel_ref=LoadSingleFile(parent=self.loadframe,ini=self.ini, read=Read_from.dsp, path='load_file_path', write_ini=self.write_ini, text='Load measured\nreference', filetypes=raw_process)
        self.load_rel_ref.add_action(self.load_rel_action)
        self.load_rel_ref.grid(row=rowcount,column=1,sticky='E')
        rowcount+=1
        self.load_rel_check=CheckBox(parent=self.loadframe,text='Use measured reference',commandon=self.rel_check_on,commandoff=self.rel_check_off)
        self.load_rel_check.change_state('on')
        self.load_rel_check.grid(row=rowcount, column=1,sticky='E')
        rowcount+=1
        self.load_measured=LoadSingleFile(parent=self.loadframe,ini=self.ini, read=Read_from.dsp, path='load_file_path', write_ini=self.write_ini, text='Load measured\ndata', filetypes=raw_process)
        self.load_measured.add_action(self.load_measured_action)
        self.load_measured.grid(row=rowcount,column=1,sticky='E')

    def init_displayframe(self):
        rowcount=0
        Label(self.displayframe,text='Display control',relief=RAISED,background='bisque2', borderwidth=2,width=35,anchor = "e").grid(row=rowcount,column=1,columnspan=3,sticky='E')
        rowcount+=1
        self.displayall=Button(self.displayframe,text='Plot all\navailable',command=self.select_display)
        self.displayall.grid(row=rowcount,column=1)
        self.displaynone=Button(self.displayframe,text='Clear\nplot',command=self.deselect_display)
        self.displaynone.grid(row=rowcount,column=3)
        Label(self.displayframe,width=1).grid(column=2,row=rowcount,rowspan=4)
        rowcount+=1

        self.display_control['ref_abs']=CheckBox(parent=self.displayframe,text='Absolute reference',command=self.main)
        self.display_control['ref_abs'].disable_press()
        self.display_control['ref_abs'].grid(row=rowcount,column=1,sticky='W')
        self.display_control['data']=CheckBox(parent=self.displayframe,text='Data',command=self.main)
        self.display_control['data'].disable_press()
        self.display_control['data'].grid(row=rowcount,column=3,sticky='W')
        rowcount+=1
        self.display_control['ref_raw']=CheckBox(parent=self.displayframe,text='Measured reference',command=self.main)
        self.display_control['ref_raw'].disable_press()
        self.display_control['ref_raw'].grid(row=rowcount,column=1,sticky='W')
        self.display_control['1-data']=CheckBox(parent=self.displayframe,text='1-Data',command=self.main)
        self.display_control['1-data'].disable_press()
        self.display_control['1-data'].grid(row=rowcount,column=3,sticky='W')
        rowcount+=1

        self.display_control['data_raw']=CheckBox(parent=self.displayframe,text='Measured data',command=self.main)
        self.display_control['data_raw'].disable_press()
        self.display_control['data_raw'].grid(row=rowcount,column=1,sticky='W')
        self.display_control['log_data']=CheckBox(parent=self.displayframe,text='log(Data)',command=self.main)
        self.display_control['log_data'].disable_press()
        self.display_control['log_data'].grid(row=rowcount,column=3,sticky='W')

    def init_dataframe(self):
        rowcount=0
        Label(self.dataframe,text='Data control',relief=RAISED,background='bisque2', borderwidth=2,width=35,anchor = "e").grid(row=rowcount,column=0,columnspan=2,sticky='E')
        rowcount+=1
        Label(self.dataframe, text='Points to smooth:',anchor='w').grid(row=rowcount, column=0,sticky='W')
        self.data_buttons['save']=SaveSingleFile(parent=self.dataframe,ini=self.ini, write_ini=self.write_ini, text='Save Data', filetypes=[('IHTM E60','*.dtsp' )],write=self.save_data)
        self.data_buttons['save'].config(state=DISABLED)
        self.data_buttons['save'].grid(column=1,row=rowcount,rowspan=2,sticky='E')
        rowcount+=1
        self.avg_num=Rotate(parent=self.dataframe,direction='horizontal',width=5,choice_list=self.movavg_list,textvariable=IntVar,command=self.movavg_change)
        
        self.avg_num.grid(column=0,row=rowcount,sticky='w')
        rowcount+=1
        self.data_buttons['savelog']=SaveSingleFile(parent=self.dataframe,ini=self.ini, write_ini=self.write_ini, text='Save log(Data)', filetypes=[('IHTM E60','*.dtsp' )],write=self.save_log_data)
        self.data_buttons['savelog'].config(state=DISABLED)
        self.data_buttons['savelog'].grid(column=0,row=rowcount,sticky='W')
        self.data_buttons['save1-data']=SaveSingleFile(parent=self.dataframe,ini=self.ini, write_ini=self.write_ini, text='Save 1-Data', filetypes=[('IHTM E60','*.dtsp' )],write=self.save_one_minus_data)
        self.data_buttons['save1-data'].config(state=DISABLED)
        self.data_buttons['save1-data'].grid(column=1,row=rowcount,sticky='E')

    def load_rel_action(self):
        tmp=self.load_rel_ref.get_data()
        if tmp==None:
            if self.display_control['ref_raw'].get_state()=='on':
                self.display_control['ref_raw'].execute_press()
                self.display_control['ref_raw'].disable_press()
        else:
            self.display_control['ref_raw'].enable_press()
            convert_unit_IHTM(tmp,'','y1')
            convert_unit_IHTM(tmp,'n','x1')
            tmp['#data_summary']['y1_label']='Rel_ref'
        self.main()

    def rel_check_on(self):
        self.load_rel_ref.enable()
        if self.load_rel_ref.get_data()!=None:
            self.display_control['ref_raw'].enable_press()
        else:
            self.display_control['ref_raw'].disable_press()
        self.main()

    def rel_check_off(self):
        self.load_rel_ref.disable()
        self.display_control['ref_raw'].change_state('off')
        self.display_control['ref_raw'].disable_press()
        self.main()

    def load_abs_action(self):
        tmp=self.load_abs_ref.get_data()
        if tmp==None:
            if self.display_control['ref_abs'].get_state()=='on':
                self.display_control['ref_abs'].execute_press()
            self.display_control['ref_abs'].disable_press()
        else:
            self.display_control['ref_abs'].enable_press()
            if tmp['#data_summary']['tot_col']!=2:
                for i in range (1,tmp['#data_summary']['tot_col']):
                    tmp['#data_summary'].pop(f'y1_{i}_name')
                    tmp['#data_summary'].pop(f'y1_{i}_unit')
                    tmp['#data_summary'].pop(f'y1_{i}_prefix')
                    tmp['#data_summary'].pop(f'y1_{i}_col')
                tmp['#data_table']=tmp['#data_table'][:,0:2]
                tmp['#data_summary']['y1_name']='Reflectance'
                tmp['#data_summary']['y1_col']=1
                tmp['#data_summary']['y1_unit']=''
                tmp['#data_summary']['y1_prefix']=''
                tmp['#data_summary']['tot_col']=2
                tmp['#data_summary']['y1_label']='Abs_ref'
                convert_unit_IHTM(tmp,'n','x1')
                convert_unit_IHTM(tmp,'','y1')
        self.main()

    def abs_check_on(self):
        self.load_abs_ref.enable()
        if self.load_abs_ref.get_data()!=None:
            self.display_control['ref_abs'].enable_press()
        else:
            self.display_control['ref_abs'].disable_press()
        self.main()

    def abs_check_off(self):
        self.load_abs_ref.disable()
        self.display_control['ref_abs'].change_state('off')
        self.display_control['ref_abs'].disable_press()
        self.main()

    def load_measured_action(self):
        tmp=self.load_measured.get_data()
        if tmp!=None:
            convert_unit_IHTM(tmp,'','y1')
            convert_unit_IHTM(tmp,'n','x1')
            if tmp['#data_summary']['y1_name']=='Reflectance':
                if self.load_abs_check.get_state()=='off':
                    self.load_abs_check.enable_press()
                    self.load_abs_check.execute_press()
                if self.load_rel_check.get_state()=='off':
                    self.load_rel_check.enable_press()
                    self.load_rel_check.execute_press()
            else:
                if self.load_abs_check.get_state()=='on':
                    self.load_abs_check.enable_press()
                    self.load_abs_check.execute_press()
                if self.load_rel_check.get_state()=='on':
                    self.load_rel_check.enable_press()
                    self.load_rel_check.execute_press()
            #since many users will forget to switch to transmittance
            self.data_buttons['save1-data'].config(state=NORMAL)
            self.data_buttons['savelog'].config(state=NORMAL)
            self.data_buttons['save'].config(state=NORMAL)
            self.display_control['1-data'].enable_press()
            self.display_control['log_data'].enable_press()
            self.display_control['data_raw'].enable_press()
            self.display_control['data'].enable_press()
            filename=self.load_measured.labelbutton.get_var()
            self.data_buttons['save'].add_filename(filename[0:filename.index('.dsp')])
            self.data_buttons['save1-data'].add_filename(filename[0:filename.index('.dsp')].replace('R0','1-R0'))
            self.data_buttons['savelog'].add_filename(filename[0:filename.index('.dsp')].replace('T0','T->A0'))
        else:
            self.data_buttons['save1-data'].config(state=DISABLED)
            self.data_buttons['save'].config(state=DISABLED)
            self.data_buttons['savelog'].config(state=DISABLED)
            self.display_control['log_data'].change_state('off')
            self.display_control['1-data'].change_state('off')
            self.display_control['data'].change_state('off')
            self.display_control['data_raw'].change_state('off')
            self.display_control['log_data'].disable_press()
            self.display_control['1-data'].disable_press()
            self.display_control['data'].disable_press()
            self.display_control['data_raw'].disable_press()
        self.main()
       
    def select_display(self):
        for key in self.display_control.keys():
            if self.display_control[key].is_enabled():
                self.display_control[key].change_state('on')
        self.main()

    def deselect_display(self):
        for key in self.display_control.keys():
            self.display_control[key].change_state('off')
        self.main()

    def movavg_change(self,avg):
        self.main()
 
    def calculate_data(self):
        D=self.load_measured.get_data()
        R=self.load_rel_ref.get_data()
        A=self.load_abs_ref.get_data()
        if (A!=None and self.load_abs_check.get_state()=='on') and (R!=None and self.load_rel_check.get_state()=='on') and D!=None:
            self.data=average_IHTM(absolute_reflectance_IHTM(D,R,A),self.avg_num.get_var(),'y1')
        if (A!=None and self.load_abs_check.get_state()=='on') and (R==None or self.load_rel_check.get_state()=='off') and D!=None:
            self.data=average_IHTM(multiply_2col_IHTM(D,A),self.avg_num.get_var(),'y1')
        if (A==None or self.load_abs_check.get_state()=='off') and (R!=None and self.load_rel_check.get_state()=='on') and D!=None:
            self.data=average_IHTM(divide_2col_IHTM(D,R),self.avg_num.get_var(),'y1')
        if (A==None or self.load_abs_check.get_state()=='off') and (R==None or self.load_rel_check.get_state()=='off') and D!=None:
            self.data=average_IHTM(D,self.avg_num.get_var(),'y1')
        if D==None:
            self.data=None
            self.one_minus_data=None
            self.logdata=None
        else:
            #since MB keeps forgetting to switch to reflectance
            #if D['#data_summary']['y1_name']=='Reflectance':
            self.one_minus_data=copy_IHTM(self.data)
            self.one_minus_data['#data_table'][:,1]=1-self.one_minus_data['#data_table'][:,1]
            self.one_minus_data['#data_summary']['y1_label']=f"{self.one_minus_data['#data_summary']['y1_label']}".replace('R0','1-R0')
            #if D['#data_summary']['y1_name']=='Transmittance':
            self.logdata=copy_IHTM(self.data)
            self.logdata['#data_table'][:,1]=-log10(abs(self.logdata['#data_table'][:,1])+1e-9)
            self.logdata['#data_summary']['y1_label']=f"{self.logdata['#data_summary']['y1_label']}".replace('T0','T->A0')

    def save_data(self,filename):
        Write_to.data(filename,self.data)

    def save_one_minus_data(self,filename):
        Write_to.data(filename,self.one_minus_data)

    def save_log_data(self,filename):
        Write_to.data(filename,self.logdata)

    def main(self):
        if self.init==True:#needed during init phase
            self.calculate_data()
            tmp={}
            tmp['ref_abs']=self.load_abs_ref.get_data()
            tmp['ref_raw']=self.load_rel_ref.get_data()
            tmp['data_raw']=self.load_measured.get_data()
            tmp['data']=self.data
            tmp['1-data']=self.one_minus_data
            tmp['log_data']=self.logdata
            self.figframe.plot.plot_xy_dict(tmp,self.display_control)
        if self.init==False:
            self.init=True