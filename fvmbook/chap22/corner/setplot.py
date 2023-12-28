
""" 
Set up the plot figures, axes, and items to be done for each frame.

This module is imported by the plotting routines and then the
function setplot is called to set the plot parameters.
    
""" 

from __future__ import absolute_import
from __future__ import print_function

#--------------------------
def setplot(plotdata):
#--------------------------
    
    """ 
    Specify what is to be plotted at each frame.
    Input:  plotdata, an instance of clawpack.visclaw.data.ClawPlotData.
    Output: a modified version of plotdata.
    
    """ 


    from clawpack.visclaw import colormaps
    from numpy import linspace

    if plotdata is None:
        from clawpack.visclaw.data import ClawPlotData
        plotdata = ClawPlotData()

    plotdata.clearfigures()  # clear any old figures,axes,items data
    
    def plot_corner(current_data):
        from pylab import plot
        plot([.0,.0],[-1,0],'k',linewidth=2)
        plot([.0,1],[0,.55],'k',linewidth=2)

    def sigmatr(current_data):
        # trace of sigma
        q = current_data.q
        return q[0,:,:] + q[1,:,:]

    def div(current_data):
        from numpy import array,zeros,hstack,vstack
        q = current_data.q
        u = q[3,:,:]
        v = q[4,:,:]
        mx, my = u.shape
        if (mx<3) or (my<3):
            d = zeros(u.shape)
            return d
        dx, dy = current_data.dx, current_data.dy
        I = array(range(1,mx-1))
        J = array(range(1,my-1))
        ux = (u[I+1,:][:,J] - u[I-1,:][:,J]) / (2*dx)
        vy = (v[:,J+1][I,:] - v[:,J-1][I,:]) / (2*dy)
        dint = ux + vy
        
        #zx = zeros((mx-2,1))
        #zy = zeros((1,my))
        #d = vstack((zy, hstack((zx, ux+vy, zx)), zy))
        
        d0 = dint[:,0]
        d1 = dint[:,-1]
        d2 = vstack((d0, dint.T, d1)).T
        d0 = d2[0,:]
        d1 = d2[-1,:]
        d = vstack((d0,d2,d1))      
        return d

    def curl(current_data):
        from numpy import array,zeros,hstack,vstack
        q = current_data.q
        u = q[3,:,:]
        v = q[4,:,:]
        mx, my = u.shape
        if (mx<3) or (my<3):
            c = zeros(u.shape)
            return c
        dx, dy = current_data.dx, current_data.dy
        I = array(range(1,mx-1))
        J = array(range(1,my-1))
        vx = (v[I+1,:][:,J] - v[I-1,:][:,J]) / (2*dx)
        uy = (u[:,J+1][I,:] - u[:,J-1][I,:]) / (2*dy)
        cint = vx - uy

        c0 = cint[:,0]
        c1 = cint[:,-1]
        c2 = vstack((c0, cint.T, c1)).T
        c0 = c2[0,:]
        c1 = c2[-1,:]
        c = vstack((c0,c2,c1))      
        return c



    # Figure for trace of sigma
    plotfigure = plotdata.new_plotfigure(name='trace(sigma)', figno=0)

    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.xlimits = 'auto'
    plotaxes.ylimits = 'auto'
    plotaxes.title = 'trace(sigma)'
    plotaxes.scaled = True
    plotaxes.afteraxes = plot_corner

    # Set up for item on these axes:
    plotitem = plotaxes.new_plotitem(plot_type='2d_pcolor')
    plotitem.plot_var = sigmatr
    plotitem.pcolor_cmap = colormaps.red_yellow_blue
    plotitem.pcolor_cmin = -1.
    plotitem.pcolor_cmax = 1.
    plotitem.add_colorbar = True
    plotitem.show = True       # show on plot?
    


    # Figure for shear stress
    plotfigure = plotdata.new_plotfigure(name='shear', figno=1)

    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.xlimits = 'auto'
    plotaxes.ylimits = 'auto'
    plotaxes.title = 'shear stress'
    plotaxes.scaled = True
    plotaxes.afteraxes = plot_corner

    # Set up for item on these axes:
    plotitem = plotaxes.new_plotitem(plot_type='2d_pcolor')
    plotitem.plot_var = 2  # sigma_12
    plotitem.pcolor_cmap = colormaps.red_yellow_blue
    plotitem.pcolor_cmin = -0.2
    plotitem.pcolor_cmax = 0.2
    plotitem.add_colorbar = True
    plotitem.show = True       # show on plot?
    

    # Figure for contours 
    plotfigure = plotdata.new_plotfigure(name='contours', figno=2)

    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.xlimits = 'auto'
    plotaxes.ylimits = 'auto'
    plotaxes.title = 'pressure(black) and shear(green)'
    plotaxes.scaled = True
    plotaxes.afteraxes = plot_corner

    # Set up for item on these axes:
    plotitem = plotaxes.new_plotitem(plot_type='2d_contour')
    plotitem.plot_var = sigmatr
    plotitem.contour_levels = linspace(-2,8,50)
    plotitem.contour_colors = 'k'
    plotitem.show = True       # show on plot?

    # Set up for item on these axes:
    plotitem = plotaxes.new_plotitem(plot_type='2d_contour')
    plotitem.plot_var = 2  # sigma_12
    plotitem.contour_levels = linspace(-0.4,0.4,30)
    plotitem.contour_colors = 'g'
    plotitem.show = True       # show on plot?
    

    # Figure for contours 
    plotfigure = plotdata.new_plotfigure(name='divcurl', figno=5)
    plotfigure.kwargs = {'figsize':(9,6)}

    # div
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.axescmd = 'subplot(121)'
    plotaxes.xlimits = [-1,1]
    plotaxes.ylimits = [-1,1]
    plotaxes.title = 'div(u)'
    plotaxes.scaled = True
    plotaxes.afteraxes = plot_corner

    # Set up for item on these axes:
    plotitem = plotaxes.new_plotitem(plot_type='2d_pcolor')
    plotitem.plot_var = div
    plotitem.pcolor_cmap = colormaps.blue_white_red
    plotitem.pcolor_cmin = -1.
    plotitem.pcolor_cmax = 1.
    #plotitem = plotaxes.new_plotitem(plot_type='2d_contour')
    #plotitem.plot_var = div
    #plotitem.contour_levels = linspace(-2,8,20)
    #plotitem.contour_colors = 'r'
    #plotitem.kwargs = {'linestyles':'-'}
    plotitem.show = True       # show on plot?

    # curl
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.axescmd = 'subplot(122)'
    plotaxes.xlimits = [-1,1]
    plotaxes.ylimits = [-1,1]
    plotaxes.title = 'curl(u)'
    plotaxes.scaled = True
    plotaxes.afteraxes = plot_corner


    # Set up for item on these axes:
    plotitem = plotaxes.new_plotitem(plot_type='2d_pcolor')
    plotitem.plot_var = curl
    plotitem.pcolor_cmap = colormaps.blue_white_red
    plotitem.pcolor_cmin = -1.
    plotitem.pcolor_cmax = 1.
    #plotitem.contour_levels = linspace(-0.4,0.4,20)
    #plotitem.contour_colors = 'b'
    #plotitem.kwargs = {'linestyles':'-'}
    plotitem.show = True       # show on plot?
    
    

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

    
