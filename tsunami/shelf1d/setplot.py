
""" 
Set up the plot figures, axes, and items to be done for each frame.

This module is imported by the plotting routines and then the
function setplot is called to set the plot parameters.
    
""" 

#--------------------------
def setplot(plotdata):
#--------------------------
    
    """ 
    Specify what is to be plotted at each frame.
    Input:  plotdata, an instance of clawpack.visclaw.data.ClawPlotData.
    Output: a modified version of plotdata.
    
    """ 

    from numpy import loadtxt
    fname = plotdata.outdir + '/fort.H'
    B = loadtxt(fname)
    print "Loaded B"

    plotdata.clearfigures()  # clear any old figures,axes,items data

    def add_dashes(current_data):
        from pylab import ylim,plot
        plot([-30000,-30000], [-1,1],'k--')

    
    # Figure for eta
    plotfigure = plotdata.new_plotfigure(name='eta', figno=2)
    plotfigure.kwargs = {'figsize':(10,10)}

    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.axescmd = 'subplot(3,1,1)'
    def fixfig(current_data):
        from pylab import xticks,yticks,xlabel,ylabel,savefig,ylim,title
        t = current_data.t
        add_dashes(current_data)
        xticks([-300000,-200000,-100000, -30000],['300','200','100','30','0'],\
          fontsize=15)
        ylabel('Meters', fontsize=15)
        title('Surface at t = %i seconds' % int(t))

    plotaxes.afteraxes = fixfig
    plotaxes.ylimits = [-0.5, 1.0]
    plotaxes.title = 'Surface'

    # Set up for item on these axes:
    plotitem = plotaxes.new_plotitem(plot_type='1d')
    def surface(current_data):
        eta = B + current_data.q[0,:]
        return eta
    plotitem.plot_var = surface
    plotitem.plotstyle = '-'
    plotitem.color = 'b'
    plotitem.kwargs = {'linewidth':2}
    
    # Velocity

    plotaxes = plotfigure.new_plotaxes()
    plotaxes.axescmd = 'subplot(3,1,2)'
    def fixfig(current_data):
        from pylab import xticks,yticks,xlabel,ylabel,savefig,ylim,title
        t = current_data.t
        add_dashes(current_data)
        xticks([-300000,-200000,-100000, -30000],['300','200','100','30','0'],\
          fontsize=15)
        ylabel('Meters/sec', fontsize=15)
        title('Velocity at t = %i seconds' % int(t))
    plotaxes.afteraxes = fixfig
    plotaxes.ylimits = [-0.2,0.2]
    plotaxes.title = 'velocity'

    # Set up for item on these axes:
    plotitem = plotaxes.new_plotitem(plot_type='1d')
    def velocity(current_data):
        q = current_data.q
        return q[1,:]/q[0,:]
    plotitem.plot_var = velocity
    plotitem.plotstyle = '-'
    plotitem.color = 'b'
    plotitem.kwargs = {'linewidth':2}

    # Bathymetry / topography

    plotaxes = plotfigure.new_plotaxes('Topography')
    plotaxes.axescmd = 'subplot(3,1,3)'
    def fixfig(current_data):
        from pylab import xticks,yticks,xlabel,ylabel,savefig,ylim,title
        t = current_data.t
        add_dashes(current_data)
        xticks([-300000,-200000,-100000, -30000],['300','200','100','30','0'],\
          fontsize=15)
        ylim(-4500,0)
        xlabel('kilometres offshore', fontsize=15)
        ylabel('Meters', fontsize=15)
        title('')
    plotaxes.afteraxes = fixfig

    plotitem = plotaxes.new_plotitem(plot_type='1d')
    def topo(current_data):
        topo = B
        return topo
    plotitem.plot_var = topo
    plotitem.plotstyle = '-'
    plotitem.color = 'g'
    plotitem.kwargs = {'linewidth':2}

    

    # Parameters used only when creating html and/or latex hardcopy
    # e.g., via clawpack.visclaw.frametools.printframes:

    plotdata.printfigs = True                # print figures
    plotdata.print_format = 'png'            # file format
    plotdata.print_framenos = 'all'          # list of frames to print
    plotdata.print_fignos = [2,3]            # list of figures to print
    plotdata.html = True                     # create html files of plots?
    plotdata.html_homelink = '../README.html'   # pointer for top of index
    plotdata.latex = True                    # create latex file of plots?
    plotdata.latex_figsperline = 2           # layout of plots
    plotdata.latex_framesperline = 1         # layout of plots
    plotdata.latex_makepdf = False           # also run pdflatex?

    return plotdata

    
