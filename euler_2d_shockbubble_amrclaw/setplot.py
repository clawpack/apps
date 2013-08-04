
""" 
Set up the plot figures, axes, and items to be done for each frame.

This module is imported by the plotting routines and then the
function setplot is called to set the plot parameters.
    
""" 

from clawpack.clawutil.data import ClawData
setprob_data = ClawData()
setprob_data.add_attribute('gamma')
setprob_data.read('setprob.data')
gamma = setprob_data.gamma

def pressure(current_data):
    q = current_data.q
    rho = q[0,:,:]
    u = q[1,:,:] / rho
    v = q[2,:,:] / rho
    E = q[3,:,:]
    p = (gamma - 1.) * (E - 0.5*rho*(u**2 + v**2))
    return p


#--------------------------
def setplot(plotdata):
#--------------------------
    
    """ 
    Specify what is to be plotted at each frame.
    Input:  plotdata, an instance of clawpack.visclaw.data.ClawPlotData.
    Output: a modified version of plotdata.
    
    """ 


    from clawpack.visclaw import colormaps
    from matplotlib import cm

    plotdata.clearfigures()  # clear any old figures,axes,items data

    # Figure for density
    # -------------------

    plotfigure = plotdata.new_plotfigure(name='Density', figno=0)
    plotfigure.kwargs = {'figsize':(16,5)}

    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.xlimits = 'auto'
    plotaxes.ylimits = 'auto'
    plotaxes.title = 'Density'
    plotaxes.scaled = True      # so aspect ratio is 1
    plotaxes.afteraxes = label_axes

    # Set up for item on these axes:
    plotitem = plotaxes.new_plotitem(plot_type='2d_schlieren')
    plotitem.schlieren_cmin = 0.0
    plotitem.schlieren_cmax = 1.0
    plotitem.plot_var = 0
    plotitem.add_colorbar = False
    plotitem.colorbar_shrink = 0.7
    plotitem.show = True       # show on plot?
    plotitem.amr_patchedges_show = [0]
    

    plotfigure = plotdata.new_plotfigure(name='Tracer', figno=1)
    plotfigure.kwargs = {'figsize':(16,5)}

    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.xlimits = 'auto'
    plotaxes.ylimits = 'auto'
    plotaxes.title = 'Tracer'
    plotaxes.scaled = True      # so aspect ratio is 1

    def aa(current_data):
        label_axes(current_data)
        addgauges(current_data)
    plotaxes.afteraxes = aa

    # Set up for item on these axes:
    plotitem = plotaxes.new_plotitem(plot_type='2d_pcolor')
    plotitem.pcolor_cmin = 0.
    plotitem.pcolor_cmax=1.0
    plotitem.plot_var = 4
    plotitem.pcolor_cmap = colormaps.yellow_red_blue
    plotitem.add_colorbar = False
    plotitem.colorbar_shrink = 0.7
    plotitem.show = True       # show on plot?
    plotitem.amr_patchedges_show = [0]
    

    plotfigure = plotdata.new_plotfigure(name='Pressure', figno=2)
    plotfigure.kwargs = {'figsize':(16,5)}


    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.xlimits = 'auto'
    plotaxes.ylimits = 'auto'
    plotaxes.title = 'Pressure'
    plotaxes.scaled = True      # so aspect ratio is 1
    plotaxes.afteraxes = label_axes

    # Set up for item on these axes:
    plotitem = plotaxes.new_plotitem(plot_type='2d_pcolor')
    plotitem.pcolor_cmin = 1.
    plotitem.pcolor_cmax = 6.
    plotitem.plot_var = pressure
    cmap = colormaps.make_colormap({0.:'w', 0.5:'y', 0.8: 'b', 
                0.9:'#ffaaaa', 1.:'#ff0000'})
    plotitem.pcolor_cmap = cmap
    plotitem.add_colorbar = True
    plotitem.colorbar_shrink = 0.7
    plotitem.show = True       # show on plot?
    plotitem.amr_patchedges_show = [0]
    

    plotfigure = plotdata.new_plotfigure(name='u-velocity', figno=3)
    plotfigure.kwargs = {'figsize':(16,5)}

    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.xlimits = 'auto'
    plotaxes.ylimits = 'auto'
    plotaxes.title = 'u-velocity'
    plotaxes.scaled = True      # so aspect ratio is 1
    plotaxes.afteraxes = label_axes

    # Set up for item on these axes:
    plotitem = plotaxes.new_plotitem(plot_type='2d_pcolor')
    plotitem.pcolor_cmin = 1.
    plotitem.pcolor_cmax = 2.
    def u(current_data):
        q = current_data.q
        rho = q[0,:,:]
        u = q[1,:,:] / rho
        return u
    plotitem.plot_var = u
    #cmap = colormaps.make_colormap({0.:'w', 0.5:'y', 0.8: 'b', 
    #            0.9:'#ffaaaa', 1.:'#ff0000'})
    #plotitem.pcolor_cmap = cmap
    plotitem.add_colorbar = True
    plotitem.colorbar_shrink = 0.7
    plotitem.show = True       # show on plot?
    plotitem.amr_patchedges_show = [0]

    # Figure for grid cells
    plotfigure = plotdata.new_plotfigure(name='cells', figno=4)
    plotfigure.kwargs = {'figsize':(16,5)}


    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.xlimits = 'auto'
    plotaxes.ylimits = 'auto'
    plotaxes.title = 'Grid patches'
    plotaxes.scaled = True

    # Set up for item on these axes:
    plotitem = plotaxes.new_plotitem(plot_type='2d_patch')
    linecolors, bgcolors = colormaps.make_amrcolors(nlevels=4)
    #plotitem.amr_patch_bgcolor = ['#ffeeee', '#eeeeff', '#eeffee', 'w']
    plotitem.amr_patch_bgcolor = bgcolors
    plotitem.amr_patchedges_color = linecolors
    plotitem.amr_celledges_show = [1,0]
    plotitem.amr_patchedges_show = [1]



    #-----------------------------------------
    # Figures for gauges
    #-----------------------------------------
    plotfigure = plotdata.new_plotfigure(name='q', figno=300, \
                    type='each_gauge')
    plotfigure.kwargs = {'figsize': (12,8)}
    plotfigure.clf_each_gauge = True

    plotaxes = plotfigure.new_plotaxes()
    plotaxes.axescmd = 'subplot(2,2,1)'
    plotaxes.xlimits = 'auto'
    plotaxes.ylimits = 'auto'
    plotaxes.title = 'Density'
    plotitem = plotaxes.new_plotitem(plot_type='1d_plot')
    plotitem.plot_var = 0
    plotitem.plotstyle = 'b-'

    plotaxes = plotfigure.new_plotaxes()
    plotaxes.axescmd = 'subplot(2,2,2)'
    plotaxes.xlimits = 'auto'
    plotaxes.ylimits = 'auto'
    plotaxes.title = 'x-momentum'
    plotitem = plotaxes.new_plotitem(plot_type='1d_plot')
    plotitem.plot_var = 1
    plotitem.plotstyle = 'b-'

    plotaxes = plotfigure.new_plotaxes()
    plotaxes.axescmd = 'subplot(2,2,3)'
    plotaxes.xlimits = 'auto'
    plotaxes.ylimits = 'auto'
    plotaxes.title = 'Energy'
    plotitem = plotaxes.new_plotitem(plot_type='1d_plot')
    plotitem.plot_var = 3
    plotitem.plotstyle = 'b-'

    plotaxes = plotfigure.new_plotaxes()
    plotaxes.axescmd = 'subplot(2,2,4)'
    plotaxes.xlimits = 'auto'
    plotaxes.ylimits = 'auto'
    plotaxes.title = 'Tracer'
    plotitem = plotaxes.new_plotitem(plot_type='1d_plot')
    plotitem.plot_var = 4
    plotitem.plotstyle = 'b-'




    # Parameters used only when creating html and/or latex hardcopy
    # e.g., via clawpack.visclaw.frametools.printframes:

    plotdata.printfigs = True                # print figures
    plotdata.print_format = 'png'            # file format
    plotdata.print_framenos = 'all'          # list of frames to print
    plotdata.print_fignos = 'all'            # list of figures to print
    plotdata.html = True                     # create html files of plots?
    plotdata.html_homelink = '../README.html'   # pointer for top of index
    plotdata.latex = True                    # create latex file of plots?
    plotdata.latex_figsperline = 2           # layout of plots
    plotdata.latex_framesperline = 1         # layout of plots
    plotdata.latex_makepdf = False           # also run pdflatex?

    return plotdata


def label_axes(current_data):
    import matplotlib.pyplot as plt
    plt.xlabel('z')
    plt.ylabel('r')
    #plt.draw()
    
    
# To plot gauge locations on pcolor or contour plot, use this as
# an afteraxis function:

def addgauges(current_data):
    from clawpack.visclaw import gaugetools
    gaugetools.plot_gauge_locations(current_data.plotdata, \
         gaugenos='all', format_string='ko', add_labels=True)
