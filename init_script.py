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
initfinish=path.join(dirname,'init_finished.ini')
if not path.isfile(initfinish):
    chdir(dirname)
    system('git submodule update --init --recursive --remote')
    for item in ['tkWindget', 'RW_data', 'AppHub', 'DataProcess', 'Figures']:
        if path.isdir(path.join(dirname,item)):
            chdir(path.join(dirname,item))
            system('git checkout main')

    linuxtext=['[Desktop Entry]','Encoding=UTF-8','Name=UV_Vis data process','Type=Application',
          'Exec='+ path.join(dirname,'run_app.py')+' %F',
          'Icon='+path.join(dirname,'icons','UV_Vis'),
          'Categories=Development']

    user=path.expanduser('~')

    if psys()=="Linux":
        desktop=path.join(user,'Desktop','UV_Vis_App.desktop')
        if not path.isfile(desktop):
            with open(desktop,'w') as f:
                for line in linuxtext:
                    savetxt(f, [line], newline='\n', fmt='%s')
            system(f'chmod +x {desktop}')
    if psys()=='Windows':
        import winshell
        from win32com.client import Dispatch

        desktop = winshell.desktop()
        path = path.join(desktop, "UV_Vis data process.lnk")
        target = "pythonw "+path.join(dirname,'run_app.py')
        icon = path.join(dirname,'icons','UV_Vis')

        shell = Dispatch('WScript.Shell')
        shortcut = shell.CreateShortCut(path)
        shortcut.Targetpath = target
        shortcut.IconLocation = icon
        shortcut.save()
    open(initfinish,'w').close()