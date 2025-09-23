#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  3 09:28:41 2025

@author: tze
"""

from os import path, chdir, system
from numpy import savetxt

dirname=path.dirname(path.abspath(__file__))
chdir(dirname)
system('git submodule update --init --recursive --remote')
for item in ['tkWindget', 'RW_data', 'AppHub', 'DataProcess', 'Figures']:
    if path.isdir(path.join(dirname,item)):
        chdir(path.join(dirname,item))
        system('git checkout main')

basedir=path.dirname(path.abspath(__file__))
text=['[Desktop Entry]','Encoding=UTF-8','Name=UV_Vis data process','Type=Application',
      'Exec='+ path.join(basedir,'run_app.py')+' %F',
      'Icon='+path.join(basedir,'icons','UV_Vis'),
      'Categories=Development']

user=path.expanduser('~')

desktop=path.join(user,'Desktop','test.desktop')
if not desktop:
    with open(desktop,'w') as f:
        for line in text:
            savetxt(f, [line], newline='\n', fmt='%s')