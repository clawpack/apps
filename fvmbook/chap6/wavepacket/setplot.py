
""" 
Set up the plot figures, axes, and items to be done for each frame.

This module is imported by the plotting routines and then the
function setplot is called to set the plot parameters.
    
""" 

import setrun
rundata = setrun.setrun()

#--------------------------
def setplot(plotdata):
#--------------------------
    
    """ 
    Specify what is to be plotted at each frame.
    Input:  plotdata, an instance of clawpack.visclaw.data.ClawPlotData.
    Output: a modified version of plotdata.
    
    """ 

    plotdata.clearfigures()  # clear any old figures,axes,items data


    # Figure for q[0]
    plotfigure = plotdata.new_plotfigure(name='q[0]', figno=1)

    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes(name='Solution')
    plotaxes.xlimits = 'auto'
    plotaxes.ylimits = [-1.1, 1.1]
    plotaxes.title = 'q[0]'

    # Set up for item on these axes:
    plotitem = plotaxes.new_plotitem(name='solution', plot_type='1d')
    plotitem.plot_var = 0
    plotitem.plotstyle = '-o'
    plotitem.color = 'b'
    plotaxes.afteraxes = plot_true_soln
    plotitem.show = True       # show on plot?
    
    # Parameters used only when creating html and/or latex hardcopy
    # e.g., via clawpack.visclaw.frametools.printframes:

    plotdata.printfigs = True                # print figures
    plotdata.print_format = 'png'            # file format
    plotdata.print_framenos = 'all'          # list of frames to print
    plotdata.print_fignos = 'all'            # list of figures to print
    plotdata.html = True                     # create html files of plots?
    plotdata.latex = True                    # create latex file of plots?
    plotdata.latex_figsperline = 2           # layout of plots
    plotdata.latex_framesperline = 1         # layout of plots
    plotdata.latex_makepdf = False           # also run pdflatex?
    
    return plotdata


#-------------------
def plot_true_soln(current_data):
#-------------------
    from numpy import linspace, mod, exp, where, sin
    from pylab import plot
    xlower = rundata.clawdata.lower[0]
    xupper = rundata.clawdata.upper[0]
    mthbc_xupper = rundata.clawdata.bc_upper[0]
    u = rundata.probdata.u
    beta = rundata.probdata.beta
    freq = rundata.probdata.freq

    xtrue = linspace(xlower,xupper,1000)
    t = current_data.t
    xshift = xtrue - u*t
    if mthbc_xupper in [2, 'periodic']:
        # for periodic boundary conditions
        xshift = xlower + mod(xshift-xlower, \
                 xupper-xlower)
    x0 = 0.5
    qtrue = exp(-beta*(xshift - x0)**2) * sin(freq*xshift)
    plot(xtrue, qtrue, 'r')


