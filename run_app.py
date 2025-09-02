#!/usr/bin/env python3
from GUIs.tot_RT.tot_RT import E60_tot_RT as E60_tot_RT
from GUIs.plot_RTA.plot_RTA import plot_RTA
from GUIs.RTA_GUI.RTA import calc_A
from AppHub.Hub import MultipleApps

MultipleApps(app_list={'Process raw\ndata':E60_tot_RT, 'Calculate A': calc_A, 'plot RTA data':plot_RTA}).init_start()
