#!/usr/bin/env python3
from GUIs.tot_RT.tot_RT import E60_tot_RT as E60_tot_RT
from GUIs.plot_RTA.plot_RTA import plot_RTA
from GUIs.RTA_GUI.RTA import calc_A
from submodules.Hub import MultipleApps
from PIL import Image, ImageTk
from os import path

App=MultipleApps(app_list={'Process raw\ndata':E60_tot_RT, 'Calculate A': calc_A, 'plot RTA data':plot_RTA})
App.approot.title("Apps for UV_Vis data")
App.approot.iconphoto(True, ImageTk.PhotoImage(Image.open(path.join(path.dirname(path.abspath(__file__)),'icons','UV_Vis.png'))))
App.init_start()
