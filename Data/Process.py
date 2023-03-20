#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 18 16:19:18 2022

@author: tzework
"""
import numpy as np
#import matplotlib.pyplot as plt
from scipy import interpolate as ipl


class container():
    pass

class Process_data():

    def mov_average(self,array,n):
        #check otherways of smoothing maybe Fourier transform high frequency filter?
        avg_array=[];
        for i in range(0,len(array)):
            imin=max(0,i-n)
            imax=min(len(array),i+n+1)
            avg_array.append(sum(array[imin:imax]/(imax-imin)))
        return np.array(avg_array)

    def absolute_reflectance(self,A,B):#A.wlength A.data B is the same
        out=container()
        wmin=max(min(A.wlength),min(B.wlength))
        wmax=min(max(A.wlength),max(B.wlength))
        wstep=min((A.wlength[1]-A.wlength[0]),(B.wlength[1]-B.wlength[0]))
        afit = ipl.interp1d(A.wlength, A.data)
        bfit = ipl.interp1d(B.wlength, B.data)
        out.wlength=np.arange(wmin,wmax+wstep,wstep)
        out.data=afit(out.wlength)*bfit(out.wlength)
        return out

    def average_curves(self,data):#data.list in which A.wlength A.data
        wstep=0
        wmin=0
        wmax=np.inf
        out=container()
        for item in data:
            wmin=max(min(item.wlength),wmin)
            wmax=min(max(item.wlength),wmax)
            wstep=max((item.wlength[1]-item.wlength[0]),wstep)
        out.wlength=np.arange(wmin,wmax+wstep,wstep)
        sum=np.zeros(len(out.wlength))
        for item in data:
            fititem=ipl.interp1d(item.wlength, item.data)
            sum=sum+fititem(out.wlength)
        out.data=sum/len(data)
        out.wlength_units=data[0].wlength_units
        return out
        #interpolate reference to measured data find Si Sio2 data from 190 to 1100
        #measured.wlegnthmin:measured.wlength_step:measured.wlength_max #see in TMM
        #after that just multiply the data

    def convert_units(self,indata):#converts everything into nm because this is UV-VIS spectrometer
        if indata.wlength_units=='m':
            indata.wlength=indata.wlength*1e9
        elif indata.wlength_units in ['\03bcm','µm']:
            indata.wlength=indata.wlength*1e3
        elif indata.wlength_units=='nm':
            pass
        indata.wlength_units='nm'
