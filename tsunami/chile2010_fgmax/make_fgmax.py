"""
Create fgmax_grid.txt input files 

Set up to make fgmax points at cell centers of finest grid level,
as specified in setrun.py.  Assumes coarse grid has 2 degree resolution
and refinement by factors 3 and 4.  If you change setrun.py, you need to 
adjust things here too.

"""

from clawpack.geoclaw import fgmax_tools


dx_fine = 2./(3.*4.)  # grid resolution at finest level

fg = fgmax_tools.FGmaxGrid()
fg.point_style = 2       # will specify a 2d grid of points
fg.x1 = -120. + dx_fine/2.
fg.x2 = -60. - dx_fine/2.
fg.y1 = -60. + dx_fine/2.
fg.y2 = 0. - dx_fine/2.
fg.dx = dx_fine
fg.tstart_max =  10.     # when to start monitoring max values
fg.tend_max = 1.e10       # when to stop monitoring max values
fg.dt_check = 60.         # target time (sec) increment between updating 
                           # max values
fg.min_level_check = 3    # which levels to monitor max on
fg.arrival_tol = 1.e-2    # tolerance for flagging arrival

fg.input_file_name = 'fgmax_grid.txt'
fg.write_input_data()

