#!/usr/bin/env python3
from GUIs.tot_RT.tot_RT import E60_tot_RT
from AppHub.Hub import MultipleApps

MultipleApps(app_list={'E60_data_process':E60_tot_RT}).init_start()
