"""
Create fgmax_grid.txt and fgmax_transect input files 
"""


from clawpack.geoclaw import fgmax_tools as F 


def make_fgmax_grid():
    FG = F.fgmax_grid_parameters()
    FG.fname = 'fgmax_grid.txt'
    FG.point_style = 2       # will specify a 2d grid of points
    FG.x1 = -120.
    FG.x2 = -60.
    FG.y1 = -60.
    FG.y2 = 0.
    FG.dx = 0.2 
    FG.tstart_max =  0.     # when to start monitoring max values
    FG.tend_max = 1.e10       # when to stop monitoring max values
    FG.dt_check = 60.         # target time (sec) increment between updating 
                               # max values
    FG.min_level_check = 2    # which levels to monitor max on
    FG.arrival_tol = 1.e-2    # tolerance for flagging arrival
    F.make_fgmax(FG)

def make_fgmax_transect():
    FG = F.fgmax_grid_parameters()
    FG.fname = 'fgmax_transect.txt'
    FG.point_style = 1       # will specify a 1d grid of points
    FG.x1 = -120
    FG.x2 = -70
    FG.y1 = -17.975
    FG.y2 = -17.975
    FG.npts = 500
    FG.tstart_max =  0.     # when to start monitoring max values
    FG.tend_max = 1.e10       # when to stop monitoring max values
    FG.dt_check = 60.         # target time (sec) increment between updating 
                               # max values
    FG.min_level_check = 2    # which levels to monitor max on
    FG.arrival_tol = 1.e-2    # tolerance for flagging arrival
    F.make_fgmax(FG)

if __name__ == "__main__":
    make_fgmax_grid()
    make_fgmax_transect()


