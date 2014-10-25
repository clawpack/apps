"""
Create fgmax_grid.txt and fgmax_transect input files 
"""


from clawpack.geoclaw import fgmax_tools
import numpy


# Default values (might be changed below)
tstart_max =  4.       # when to start monitoring max values
tend_max = 1.e10       # when to stop monitoring max values
dt_check = 0.1         # target time (sec) increment between updating 
                       # max values
min_level_check = 4    # which levels to monitor max on
arrival_tol = 1.e-2    # tolerance for flagging arrival


# ======================== 
# Lat-Long grid on x-axis:

fg = fgmax_tools.FGmaxGrid()
fg.point_style = 2       # will specify a 2d grid of points
fg.nx = 100
fg.ny = 80
fg.x1 = 88.
fg.y1 = -2.
fg.x2 = 93.
fg.y2 = 2.
fg.tstart_max = tstart_max
fg.tend_max = tend_max
fg.dt_check = dt_check
fg.min_level_check = min_level_check
fg.arrival_tol = arrival_tol

fg.input_file_name = 'fgmax_grid1.txt'
fg.write_input_data()


# ===============================
# Quadrilateral grid on diagonal:

fg = fgmax_tools.FGmaxGrid()
fg.point_style = 3       # will specify a 2d grid of points
fg.n12 = 100
fg.n23 = 80

# rotate grid1 from above by pi/4 to place on diagonal:
x1 = 88.
y1 = -2.
x2 = 93.
y2 = -2.
x3 = 93.
y3 = 2.
x4 = 88.
y4 = 2.
c = numpy.cos(numpy.pi / 4.)
s = numpy.sin(numpy.pi / 4.)
fg.x1 = c*x1 - s*y1
fg.y1 = s*x1 + c*y1
fg.x2 = c*x2 - s*y2
fg.y2 = s*x2 + c*y2
fg.x3 = c*x3 - s*y3
fg.y3 = s*x3 + c*y3
fg.x4 = c*x4 - s*y4
fg.y4 = s*x4 + c*y4

fg.tstart_max = tstart_max
fg.tend_max = tend_max
fg.dt_check = dt_check
fg.min_level_check = min_level_check
fg.arrival_tol = arrival_tol

fg.input_file_name = 'fgmax_grid2.txt'
fg.write_input_data()



# ===============================
# Transect on x-axis:

fg = fgmax_tools.FGmaxGrid()
fg.point_style = 1       # will specify a 1d grid of points
fg.npts = 100
fg.x1 = 85.
fg.y1 = 0.
fg.x2 = 93.
fg.y2 = 0.
fg.tstart_max = tstart_max
fg.tend_max = tend_max
fg.dt_check = dt_check
fg.min_level_check = min_level_check
fg.arrival_tol = arrival_tol

fg.input_file_name = 'fgmax_transect1.txt'
fg.write_input_data()


# ===============================
# Transect on diagonal:

fg = fgmax_tools.FGmaxGrid()
fg.point_style = 1       # will specify a 1d grid of points
fg.npts = 100
fg.x1 = 60.
fg.y1 = 60.
fg.x2 = 66.
fg.y2 = 66.
fg.tstart_max = tstart_max
fg.tend_max = tend_max
fg.dt_check = dt_check
fg.min_level_check = min_level_check
fg.arrival_tol = arrival_tol

fg.input_file_name = 'fgmax_transect2.txt'
fg.write_input_data()


# ===============================
# Points along shoreline:
# Around circle in first quadrant at 90 meters from center

fg = fgmax_tools.FGmaxGrid()
fg.point_style = 0       # will specify a list of points
fg.npts = 500

from numpy import pi
theta = numpy.linspace(-pi/8.,3*pi/8,fg.npts)  
fg.X = 90.*numpy.cos(theta)  
fg.Y = 90.*numpy.sin(theta)

fg.tstart_max = tstart_max
fg.tend_max = tend_max
fg.dt_check = dt_check
fg.min_level_check = min_level_check
fg.arrival_tol = arrival_tol

fg.input_file_name = 'fgmax_along_shore.txt'
fg.write_input_data()


