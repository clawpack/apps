"""
Create fgmax_grid.txt input file 
"""

from numpy import linspace


def make_fgmax_grid():
    xlower = -120
    xupper = -60
    ylower = -60
    yupper = 0
    dx = 0.2
    dy = dx
    nx = int(round((xupper-xlower)/dx)) + 1  
    ny = int(round((yupper-ylower)/dy)) + 1  
    if abs((nx-1)*dx + xlower - xupper) > 1e-6:
        print "Warning: abs((nx-1)*dx + xlower - xupper) = ", \
              abs((nx-1)*dx + xlower - xupper)
    if abs((ny-1)*dy + ylower - yupper) > 1e-6:
        print "Warning: abs((ny-1)*dy + ylower - yupper) = ", \
              abs((ny-1)*dy + ylower - yupper)
    tstart_max =   0.      # when to start monitoring max values
    tend_max = 1.e10       # when to stop monitoring max values
    dt_check = 60.       # target time increment between updating max values
    min_level_check = 2   # which levels to monitor 
    arrival_tol = 1.e-2        # tolerance for flagging arrival
    point_style = 2       # will specify a 2d grid of points

    npts = nx*ny

    fname = 'fgmax_grid.txt'
    fid = open(fname,'w')
    fid.write("%g                 # tstart_max\n"  % tstart_max)
    fid.write("%g                 # tend_max\n"  % tend_max)
    fid.write("%g                 # dt_check\n" % dt_check)
    fid.write("%i                 # min_level_check\n" % min_level_check)
    fid.write("%g                 # arrival_tol\n" % arrival_tol)
    fid.write("%g                 # point_style\n" % point_style)

    fid.write("%i  %i             # nx,ny\n" % (nx,ny))
    fid.write("%g   %g            # x1, y1\n" % (xlower,ylower))
    fid.write("%g   %g            # x2, y2\n" % (xupper,yupper))

    print "Created file ", fname
    print "   specifying fixed grid with shape %i by %i, with  %i points" \
            % (nx,ny,npts)
    print "   lower left = (%g,%g)  upper right = (%g,%g)" \
            % (xlower,ylower,xupper,yupper)
    fid.close()

def make_fgmax_transect():
    x1 = -120
    x2 = -70
    y1 = -17.975
    y2 = -17.975
    npts = 500
    xpts = linspace(x1,x2,npts)
    ypts = linspace(y1,y2,npts)

    tstart_max =   0.      # when to start monitoring max values
    tend_max = 1.e10       # when to stop monitoring max values
    dt_check = 60.       # target time increment between updating max values
    min_level_check = 2   # which levels to monitor 
    arrival_tol = 1.e-2        # tolerance for flagging arrival
    point_style = 1       # will specify a 1d grid of points

    fname = 'fgmax_transect.txt'
    fid = open(fname,'w')
    fid.write("%g                 # tstart_max\n"  % tstart_max)
    fid.write("%g                 # tend_max\n"  % tend_max)
    fid.write("%g                 # dt_check\n" % dt_check)
    fid.write("%i                 # min_level_check\n" % min_level_check)
    fid.write("%g                 # arrival_tol\n" % arrival_tol)
    fid.write("%g                 # point_style\n" % point_style)

    fid.write("%g                 # npts\n" % npts)
    fid.write("%g   %g            # x1, y1\n" % (x1,y1))
    fid.write("%g   %g            # x2, y2\n" % (x2,y2))

    print "Created file ", fname
    print "   specifying fixed grid with %i points equally spaced from " % npts
    print "   (%g,%g)  to  (%g,%g)" % (x1,y1,x2,y2)
    fid.close()

if __name__ == "__main__":
    make_fgmax_grid()
    make_fgmax_transect()


