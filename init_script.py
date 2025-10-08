#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  3 09:28:41 2025

@author: tze
"""

from os import path, chdir, system
from numpy import savetxt
from platform import system as psys

dirname=path.dirname(path.abspath(__file__))
chdir(dirname)
system('git submodule update --init --recursive --remote')
for item in ['tkWindget', 'RW_data', 'AppHub', 'DataProcess', 'Figures']:
    if path.isdir(path.join(dirname,item)):
        chdir(path.join(dirname,item))
        system('git checkout main')

basedir=path.dirname(path.abspath(__file__))
linuxtext=['[Desktop Entry]','Encoding=UTF-8','Name=UV_Vis data process','Type=Application',
      'Exec='+ path.join(basedir,'run_app.py')+' %F',
      'Icon='+path.join(basedir,'icons','UV_Vis'),
      'Categories=Development']

user=path.expanduser('~')

if psys()=="Linux":
    desktop=path.join(user,'Desktop','UV_Vis_App.desktop')
    if not path.isfile(desktop):
        with open(desktop,'w') as f:
            for line in linuxtext:
                savetxt(f, [line], newline='\n', fmt='%s')
        system('chmod +x desktop')