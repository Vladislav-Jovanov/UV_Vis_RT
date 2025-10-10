#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  3 09:28:41 2025

@author: tze
"""

from os import path, chdir, system
from numpy import savetxt
from platform import system as psys

linkname='UV_Vis data process'
pngicon='UV_Vis.png'
icoicon='UV_Vis.ico'
linuxname='UV_Vis_App.desktop'
scriptname='run_app.py'
windgetlist=['tkWindget', 'RW_data', 'AppHub', 'DataProcess', 'Figures']

dirname=path.dirname(path.abspath(__file__))
initfinish=path.join(dirname,'init_finished.ini')
if not path.isfile(initfinish):
    chdir(dirname)
    system('git submodule update --init --recursive --remote')
    for item in windgetlist:
        if path.isdir(path.join(dirname,item)):
            chdir(path.join(dirname,item))
            system('git checkout main')
    if psys()=="Linux":
        system(f'chmod +x {path.join(dirname,scriptname)}')
    open(initfinish,'w').close()

if psys()=="Linux":
    linuxtext=['[Desktop Entry]','Encoding=UTF-8','Name='+linkname,'Type=Application',
          'Exec='+ path.join(dirname,scriptname)+' %F',
          'Icon='+path.join(dirname,'icons',pngicon),
          'Categories=Development']
    user=path.expanduser('~')
    desktop=path.join(user,'Desktop',linuxname)
    if not path.isfile(desktop):
        with open(desktop,'w') as f:
            for line in linuxtext:
                savetxt(f, [line], newline='\n', fmt='%s')
        system(f'chmod +x {desktop}')
if psys()=='Windows':
    from winshell import shortcut, desktop
    from sys import executable

    desktop = desktop()
    shortcut_path=path.join(desktop,linkname+".lnk")
    icon_path = path.join(dirname,'icons',icoicon)

    target_path = executable.replace('python.exe','pythonw.exe')
    target_script=path.join(dirname,scriptname)

    if not path.isfile(shortcut_path):
        with shortcut(shortcut_path) as link:
            link.path=target_path
            link.arguments=target_script
            link.icon_location=(icon_path,0)
