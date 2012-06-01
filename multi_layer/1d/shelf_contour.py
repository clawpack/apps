#!/usr/bin/env python

import sys
import os
import numpy as np
import matplotlib.pyplot as plt

from clawpack.pyclaw.solution import Solution
import clawpack.visclaw.data as data

rho = [1025.0,1045.0]
eta_init = [0.0,-300.0]

def plot_contour(out_dir="./_output",num_layers=2,num_frames=1000,ref_lines=[-130e3,-30e3]):
    """Plot a contour plot of a shelf based simluation"""
    
    # Create plot data
    plot_data = data.ClawPlotData()
    plot_data.outdir = out_dir
    
    # Read in bathymetry
    sol = [Solution(0,path=out_dir,read_aux=True)]
    b = sol[0].state.aux[0,:]
    
    # Extract x coordinates, this assumes that these do not change through the
    # simluation (they should not)
    x = sol[0].state.grid.dimensions[0].centers
    
    # Read in all solutions
    print "Reading in solutions..."
    for frame in xrange(1,num_frames):
        try:
            sol.append(Solution(frame,path=out_dir))
        except IOError:
            # We have reached the last frame before given num_frames reached
            num_frames = frame - 1
            break
    print "Found %s frames to plot." % num_frames
    
    # Create plotting arrays
    print "Constructing plotting variables..."
    eta = np.ndarray((num_frames,num_layers,len(x)))
    t = np.ndarray((num_frames))
    for frame in xrange(num_frames):
        # Append data to eta and t lists
        t[frame] = sol[frame].t / 3600.0
        
        # Calculate from the bottom up
        layer_index = 2 * (num_layers-1)
        eta[frame,num_layers - 1,:] = sol[frame].q[layer_index,:] / rho[-1] + b
        
        # Calculate the rest of the layers
        for layer in xrange(num_layers-2,-1,-1):
            layer_index = 2 * layer
            eta[frame,layer,:] = sol[frame].q[layer_index,:] / rho[layer] + eta[frame,layer+1,:]
    
    # Create mesh grid for plot
    X,T = np.meshgrid(x,t)
    
    # Plot the contours of each layer
    clines = np.linspace(.025,.4,15)
    title = ['top','internal']
    print "Creating plots..."
    fig = plt.figure(1,figsize=[10,8])
    for layer in xrange(num_layers):
        axes = fig.add_subplot(1,num_layers,layer+1)

        # Plot positive and negative contours
        eta_plot = eta[:,layer,:] - eta_init[layer]
        plot = axes.contour(X,T, eta_plot,clines,colors='r')
        plot = axes.contour(X,T,-eta_plot,clines,colors='b',linestyle='dashed')
        for ref_line in ref_lines:
            axes.plot([ref_line,ref_line],[0,2],'k--')
        
        # X ticks and labels
        axes.set_xticks([-300e3,-200e3,-100e3,-30e3])
        axes.set_xticklabels([300,200,100,30],fontsize=15)
        axes.set_xlabel("Kilometers offshore",fontsize=15)
        axes.set_xlim([-200e3,0.0])
        
        # First plot from left to right, write y ticks
        if layer == 0:
            plt.yticks(fontsize=15)
            axes.set_ylabel("Hours",fontsize=20)
        else:
            # Remove tick labels
            axes.set_yticklabels(['' for label in axes.get_yticklabels()])
        
        axes.set_title("Contours of %s surface" % title[layer],fontsize=15)
        
    
    file_name = os.path.join(out_dir,"shelf_contour.png")
    print "Writing out to %s" % file_name
    plt.savefig(file_name)

if __name__=="__main__":
    if len(sys.argv) > 1:
        plot_contour(*sys.argv[1:])
    else:
        plot_contour()
