
""" 
Set up the plot figures, axes, and items to be done for each frame.

This module is imported by the plotting routines and then the
function setplot is called to set the plot parameters.
    
""" 

import os
import numpy as np


#--------------------------
def setplot(plotdata):
#--------------------------
    
    """ 
    Specify what is to be plotted at each frame.
    Input:  plotdata, an instance of pyclaw.plotters.data.ClawPlotData.
    Output: a modified version of plotdata.
    
    """ 


    from clawpack.visclaw import colormaps

    plotdata.clearfigures()  # clear any old figures,axes,items data

    def add_interface(current_data):
        # plot the interface between materials
        from pylab import plot
        plot([0,0,1],[-1,0,0.55],'g',linewidth=2)
    
    def fix_layout(current_data):
        from pylab import tight_layout
        tight_layout()

    plotdata.afterframe = fix_layout

    # Figure with 4 subplots
    plotfigure = plotdata.new_plotfigure(name='solution', figno=0)
    plotfigure.kwargs = {'figsize':(9,8)}

    # pressure:
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.axescmd = 'subplot(2,2,1)'
    plotaxes.xlimits = [-1,1]
    plotaxes.ylimits = [-1,1]
    plotaxes.title = 'pressure'
    plotaxes.scaled = True
    plotaxes.afteraxes = add_interface

    plotitem = plotaxes.new_plotitem(plot_type='2d_pcolor')
    plotitem.plot_var = 0
    plotitem.pcolor_cmap = colormaps.red_yellow_blue
    plotitem.pcolor_cmin = -0.2
    plotitem.pcolor_cmax = 0.2
    plotitem.add_colorbar = False
    #plotitem.add_colorbar = True
    #plotitem.colorbar_shrink = 0.7
    

    # Contours of pressure:
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.axescmd = 'subplot(2,2,2)'
    plotaxes.xlimits = [-1,1]
    plotaxes.ylimits = [-1,1]
    plotaxes.title = 'pressure'
    plotaxes.scaled = True
    plotaxes.afteraxes = add_interface

    plotitem = plotaxes.new_plotitem(plot_type='2d_contour')
    plotitem.plot_var = 0
    plotitem.contour_levels = np.linspace(-0.9,0.9,20)
    plotitem.kwargs = {'linestyles': '-'}  # all solid rather than dashed


    # u-velocity
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.axescmd = 'subplot(2,2,3)'
    plotaxes.xlimits = [-1,1]
    plotaxes.ylimits = [-1,1]
    plotaxes.title = 'u'
    plotaxes.scaled = True
    plotaxes.afteraxes = add_interface

    plotitem = plotaxes.new_plotitem(plot_type='2d_pcolor')
    plotitem.plot_var = 1
    plotitem.pcolor_cmap = colormaps.red_yellow_blue
    plotitem.pcolor_cmin = -0.2
    plotitem.pcolor_cmax = 0.2
    plotitem.add_colorbar = True
    plotitem.colorbar_shrink = 0.7
    

    # v-velocity
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.axescmd = 'subplot(2,2,4)'
    plotaxes.xlimits = [-1,1]
    plotaxes.ylimits = [-1,1]
    plotaxes.title = 'v'
    plotaxes.scaled = True
    plotaxes.afteraxes = add_interface

    plotitem = plotaxes.new_plotitem(plot_type='2d_pcolor')
    plotitem.plot_var = 2
    plotitem.pcolor_cmap = colormaps.red_yellow_blue
    plotitem.pcolor_cmin = -0.2
    plotitem.pcolor_cmax = 0.2
    plotitem.add_colorbar = True
    plotitem.colorbar_shrink = 0.7
    

    # Parameters used only when creating html and/or latex hardcopy
    # e.g., via pyclaw.plotters.frametools.printframes:

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

    
