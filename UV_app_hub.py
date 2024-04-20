#!/usr/bin/env python3
from GUIs.tot_RT.tot_RT import E60_tot_RT
from GUIs.plot_RTA.plot_RTA import plot_RTA
from AppHub.Hub import MultipleApps

MultipleApps(app_list={'E60_data_process':E60_tot_RT, 'plot_RTA_data':plot_RTA}).init_start()