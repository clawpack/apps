
""" 
Set up the plot figures, axes, and items to be done for each frame.

This module is imported by the plotting routines and then the
function setplot is called to set the plot parameters.
    
""" 

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

    plotfigure = plotdata.new_plotfigure(name='Depth and velocity', figno=1)
    plotfigure.kwargs = {'figsize':(6,8)}

    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.axescmd = 'subplot(3,1,1)'   # top figure
    plotaxes.xlimits = [0,2.5]
    plotaxes.ylimits = [0,2.5]
    plotaxes.title = 'Depth h'

    # Set up for item on these axes:
    plotitem = plotaxes.new_plotitem(plot_type='1d_plot')
    plotitem.plot_var = 0
    plotitem.plotstyle = '-'
    plotitem.color = 'b'

    # Figure for momentum

    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.axescmd = 'subplot(3,1,2)'
    plotaxes.xlimits = [0,2.5]
    plotaxes.ylimits = [-0.5,1.]
    plotaxes.title = 'Momentum hu'

    # Set up for item on these axes:
    plotitem = plotaxes.new_plotitem(plot_type='1d_plot')
    plotitem.plot_var = 1
    plotitem.plotstyle = '-'
    plotitem.color = 'b'

    # Figure for velocity

    def u_velocity(current_data):
        from pylab import divide,zeros
        q = current_data.q # solution at the current time
        h = q[0,:]
        hu = q[1,:]
        u = divide(hu, h, where='h>1e-3', out=zeros(hu.shape))
        return u
        
    def aa(current_data):
        from pylab import tight_layout
        tight_layout()  # improve the spacing of plots for titles

    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.axescmd = 'subplot(3,1,3)'   # bottom figure
    plotaxes.xlimits = [0,2.5]
    plotaxes.ylimits = [-.5,0.5]
    plotaxes.title = 'Velocity u'
    plotaxes.afteraxes = aa

    # Set up for item on these axes:
    plotitem = plotaxes.new_plotitem(plot_type='1d_plot')
    plotitem.plot_var = u_velocity
    plotitem.plotstyle = '-'
    plotitem.color = 'b'

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

    
