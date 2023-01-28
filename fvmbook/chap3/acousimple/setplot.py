
""" 
Set up the plot figures, axes, and items to be done for each frame.

This module is imported by the plotting routines and then the
function setplot is called to set the plot parameters.
    
""" 

# compute impedance Z from the data in setprob.data (created by setrun.py):
# note that Z = sqrt(K*rho) where K is called bulk in setrun and setprob.

from numpy import sqrt
from clawpack.clawutil.data import ClawData
#setprob = UserData('setprob.data')
setprob = ClawData('setprob.data')
setprob.read('setprob.data', force=True)
Z = sqrt(setprob.bulk * setprob.rho)
print('Impedance Z = %.3f' % Z)


#--------------------------
def setplot(plotdata=None):
#--------------------------
    
    """ 
    Specify what is to be plotted at each frame.
    Input:  plotdata, an instance of clawpack.visclaw.data.ClawPlotData.
    Output: a modified version of plotdata.
    
    """ 

    if plotdata is None:
        from clawpack.visclaw.data import ClawPlotData
        plotdata = ClawPlotData()

    plotdata.clearfigures()  # clear any old figures,axes,items data

    def adjust_axes(current_data):
        from pylab import tight_layout
        tight_layout()

    # Figure for pressure and velocity:
    plotfigure = plotdata.new_plotfigure(name='Pressure and Velocity', figno=1)
    plotfigure.kwargs = {'figsize':(6,7)}

    # Pressure:
    # ---------

    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.axescmd = 'subplot(2,1,1)'   # top figure
    plotaxes.xlimits = [-1,1]
    plotaxes.ylimits = [-.5,1.]
    plotaxes.title = 'Pressure'

    # Set up for item on these axes:
    plotitem = plotaxes.new_plotitem(plot_type='1d_plot')
    plotitem.plot_var = 0
    plotitem.plotstyle = '-'
    plotitem.color = 'b'


    # Velocity:
    # ---------

    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.axescmd = 'subplot(2,1,2)'   # bottom figure
    plotaxes.xlimits = [-1,1]
    plotaxes.ylimits = [-1.,1.]
    plotaxes.title = 'Velocity'
    plotaxes.afteraxes = adjust_axes

    # Set up for item on these axes:
    plotitem = plotaxes.new_plotitem(plot_type='1d_plot')
    plotitem.plot_var = 1
    plotitem.plotstyle = '-'
    plotitem.color = 'b'

    # ===================================================================
    # Figure showing p,u and decomposition into characteristic vars w1,w2

    plotfigure = plotdata.new_plotfigure(name='characteristic variables',
                                         figno=2)
    plotfigure.kwargs = {'figsize':(6,7)}

    # Pressure and velocity:
    # ----------------------

    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.axescmd = 'subplot(2,1,1)'   # top figure
    plotaxes.xlimits = [-1,1]
    plotaxes.ylimits = [-1.,1.]
    plotaxes.title = 'Pressure (blue) and velocity (magenta)'

    # Set up for item on these axes:
    plotitem = plotaxes.new_plotitem(plot_type='1d_plot')
    plotitem.plot_var = 0
    plotitem.plotstyle = '-'
    plotitem.color = 'b'

    # Set up for item on these axes:
    plotitem = plotaxes.new_plotitem(plot_type='1d_plot')
    plotitem.plot_var = 1
    plotitem.plotstyle = '-'
    plotitem.color = 'm'

    # characteristic variables:
    # -------------------------

    def w1(current_data):
        q = current_data.q  # use data from current frame
        p = q[0,:]
        u = q[1,:]
        w1 = (-p + Z*u)/(2*Z)
        return w1

    def w2(current_data):
        q = current_data.q  # use data from current frame
        p = q[0,:]
        u = q[1,:]
        w2 = (p + Z*u)/(2*Z)
        return w2

    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.axescmd = 'subplot(2,1,2)'   # bottom figure
    plotaxes.xlimits = [-1,1]
    plotaxes.ylimits = [-1.,1.]
    plotaxes.title = 'w1 (green) and w2 (red)'
    plotaxes.afteraxes = adjust_axes

    # Set up for item on these axes:
    plotitem = plotaxes.new_plotitem(plot_type='1d_plot')
    plotitem.plot_var = w1
    plotitem.plotstyle = '-'
    plotitem.color = 'g'

    # Set up for item on these axes:
    plotitem = plotaxes.new_plotitem(plot_type='1d_plot')
    plotitem.plot_var = w2
    plotitem.plotstyle = '-'
    plotitem.color = 'r'

    # Parameters used only when creating html and/or latex hardcopy
    # e.g., via clawpack.visclaw.frametools.printframes:

    plotdata.printfigs = True                # print figures
    plotdata.print_format = 'png'            # file format
    plotdata.print_framenos = 'all'          # list of frames to print
    plotdata.print_fignos = 'all'            # list of figures to print
    plotdata.html = True                     # create html files of plots?
    plotdata.html_homelink = '../README.html'
    plotdata.latex = True                    # create latex file of plots?
    plotdata.latex_figsperline = 2           # layout of plots
    plotdata.latex_framesperline = 1         # layout of plots
    plotdata.latex_makepdf = False           # also run pdflatex?

    return plotdata

    
