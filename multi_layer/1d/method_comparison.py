#!/usr/bin/env python
# encoding: utf-8

r"""Plot convergence plots for wet and dry wave family tests."""

import os

import numpy as np

# Plot customization
import matplotlib

# Markers and line widths
matplotlib.rcParams['lines.linewidth'] = 2.0
matplotlib.rcParams['lines.markersize'] = 6
matplotlib.rcParams['lines.markersize'] = 8

# Font Sizes
matplotlib.rcParams['font.size'] = 16
matplotlib.rcParams['axes.labelsize'] = 15
matplotlib.rcParams['legend.fontsize'] = 12
matplotlib.rcParams['xtick.labelsize'] = 12
matplotlib.rcParams['ytick.labelsize'] = 12

# DPI of output images
matplotlib.rcParams['savefig.dpi'] = 100

# Import plotting package now
import matplotlib.pyplot as plt

from clawpack.pyclaw.solution import Solution

# General parameters
data_path = os.path.abspath(os.environ["DATA_PATH"])
base_resolution = 5000
base_method = 4
styles = ['go','cs','r+','bx']

# Plot settings for specfic experiments
plot_settings = {"wet_wave_3":{"xlim":(0.50,0.60),
                               "ylim":[(0.2,1.1),(0.0,0.05),(-0.12,0.02)],
                               "frame":30,
                               "locs":[6,1,4]},
                 "wet_wave_4":{"xlim":(0.80,0.88),
                               "ylim":[(0.3,1.1),(-0.025,0.25),(-0.025,0.25)],
                               "frame":12,
                               "locs":[7,1,1]},
                 "dry_wave_3":{"xlim":(0.35,0.50),
                               "ylim":[(0.1,1.1),(0.0,0.06),(-0.15,0.02)],
                               "frame":42,
                               "locs":[6,1,4]},
                 "dry_wave_4":{"xlim":(0.35,0.5),
                               "ylim":[(0.4,1.2),(0.10,0.5),(-0.025,0.15)],
                               "frame":50,
                               "locs":[4,4,1]}
                }

# Labels                 
y_labels = ['Depth','Top Velocity','Bottom Velocity']
eigen_labels = ['linearized static','linearized dynamic',
                'velocity difference','LAPACK']

def extract_data(sol,rho=[0.95,1.0],dry_tolerance=1e-3):
    r"""Extract relevant quantities from solution object sol"""

    # Empty lists for data
    h = [None,None]
    u = [None,None]
    eta = [None,None]
            
    b = sol.state.aux[0,:]
    
    h[0] = sol.state.q[0,:] / rho[0]
    h[1] = sol.state.q[2,:] / rho[1]
    
    index = np.nonzero(h[1] > dry_tolerance)
    eta[1] = b
    eta[1][index] = h[1] + b 
    eta[0] = h[0] + eta[1]

    index = np.nonzero(h[0] > dry_tolerance)
    u[0] = np.zeros(h[0].shape)
    u[0][index] = sol.state.q[1,:] / sol.state.q[0,:]

    index = np.nonzero(h[1] > dry_tolerance)
    u[1] = np.zeros(h[0].shape)
    u[1][index] = sol.state.q[3,:] / sol.state.q[2,:]

    x = sol.domain.grid.dimensions[0].centers

    return x,b,h,eta,u

def create_eigen_plot(base_path,eigen_methods=[1,2,3,4],resolution=64):

    # Extract data from plot settings dict
    x_limits = plot_settings[base_path]["xlim"]
    y_limits = plot_settings[base_path]["ylim"]
    frame = plot_settings[base_path]["frame"]
    locations = plot_settings[base_path]["locs"]

    # Create figures and axes
    fig_list = [plt.figure() for n in xrange(3)]
    axes_list = [fig.add_subplot(111) for fig in fig_list]

    for (n,method) in enumerate(eigen_methods):
        # Load solution and extract data        
        path = os.path.join(data_path,base_path,
                            'ml_e%s_n%s_output' % (method,resolution))
        x,b,h,eta,u = extract_data(Solution(frame,path=path,read_aux=True))

        # Plot data
        axes_list[0].plot(x,eta[0],styles[n],label='_nolegend_')
        axes_list[0].plot(x,eta[1],styles[n],label=eigen_labels[method-1])
        axes_list[1].plot(x,u[0],styles[n],label=eigen_labels[method-1])
        axes_list[2].plot(x,u[1],styles[n],label=eigen_labels[method-1])

    # Plot reference solutions
    path = os.path.join(data_path,base_path,
                                'ml_e%s_n%s_output' % (4,base_resolution))
    x,b,h,eta,u = extract_data(Solution(frame,path=path,read_aux=True))
    axes_list[0].plot(x,eta[0],'k',label='_nolegend_')
    axes_list[0].plot(x,eta[1],'k',label='Base')
    # axes_list[0].plot(x,b,'k:',label="bathymetry")
    axes_list[1].plot(x,u[0],'k',label='Base')
    axes_list[2].plot(x,u[1],'k',label='Base')

    # Set legend, title and axis labels
    for (n,axes) in enumerate(axes_list):
        axes.set_xlim(x_limits)
        axes.set_ylim(y_limits[n])

        axes.set_title("Eigen Method Comparisons with N = %s" % resolution)
        axes.set_xlabel('x')
        axes.set_ylabel(y_labels[n])
        axes.legend(loc=locations[n])

    out_path = os.path.join(os.curdir,'comparison_plots',base_path)
    if not os.path.exists(out_path):
        os.makedirs(out_path)
    fig_list[0].savefig(os.path.join(out_path,'surfaces_n%s.pdf' % resolution))
    fig_list[1].savefig(os.path.join(out_path,'u_top_n%s.pdf' % resolution))
    fig_list[2].savefig(os.path.join(out_path,'u_bottom_n%s.pdf' % resolution))


def create_resolution_plot(base_path,method=2,resolutions=[64,128,256,512]):

    # Extract data from plot settings dict
    x_limits = plot_settings[base_path]["xlim"]
    y_limits = plot_settings[base_path]["ylim"]
    frame = plot_settings[base_path]["frame"]
    locations = plot_settings[base_path]["locs"]

    # Create figures and axes
    fig_list = [plt.figure() for n in xrange(3)]
    axes_list = [fig.add_subplot(111) for fig in fig_list]

    for (n,resolution) in enumerate(resolutions):
        # Load solution and extract data        
        path = os.path.join(data_path,base_path,
                            'ml_e%s_n%s_output' % (method,resolution))
        x,b,h,eta,u = extract_data(Solution(frame,path=path,read_aux=True))

        # Plot data
        axes_list[0].plot(x,eta[0],styles[n],label='_nolegend_')
        axes_list[0].plot(x,eta[1],styles[n],label="N = %s" % resolution)
        axes_list[1].plot(x,u[0],styles[n],label="N = %s" % resolution)
        axes_list[2].plot(x,u[1],styles[n],label="N = %s" % resolution)

    # Plot reference solutions
    path = os.path.join(data_path,base_path,
                                'ml_e%s_n%s_output' % (base_method,base_resolution))
    x,b,h,eta,u = extract_data(Solution(frame,path=path,read_aux=True))
    axes_list[0].plot(x,eta[0],'k',label='_nolegend_')
    axes_list[0].plot(x,eta[1],'k',label='Base')
    # axes_list[0].plot(x,b,'k:',label="bathymetry")
    axes_list[1].plot(x,u[0],'k',label='Base')
    axes_list[2].plot(x,u[1],'k',label='Base')

    # Set legend, title and axis labels
    for (n,axes) in enumerate(axes_list):
        axes.set_xlim(x_limits)
        axes.set_ylim(y_limits[n])
        axes.set_title("Comparison using the %s method" % eigen_labels[method-1])
        axes.set_xlabel('x')
        axes.set_ylabel(y_labels[n])
        axes.legend(loc=locations[n])

    out_path = os.path.join(os.curdir,'comparison_plots',base_path)
    if not os.path.exists(out_path):
        os.makedirs(out_path)
    fig_list[0].savefig(os.path.join(out_path,'surfaces_m%s.pdf' % method))
    fig_list[1].savefig(os.path.join(out_path,'u_top_m%s.pdf' % method))
    fig_list[2].savefig(os.path.join(out_path,'u_bottom_m%s.pdf' % method))

if __name__ == "__main__":

    # Tests run
    resolutions = [64,128,256,512]
    eigen_methods = [1,2,3,4]

    # Compare eigen_methods at each resolution
    for n in resolutions:
        create_eigen_plot('wet_wave_3',eigen_methods=eigen_methods,resolution=n)
        create_eigen_plot('wet_wave_4',eigen_methods=eigen_methods,resolution=n)
        create_eigen_plot('dry_wave_3',eigen_methods=eigen_methods,resolution=n)
        create_eigen_plot('dry_wave_4',eigen_methods=eigen_methods,resolution=n)

    # Compare resolutions of each eigen_method
    for method in eigen_methods:
        create_resolution_plot('wet_wave_3',method=method,resolutions=resolutions)
        create_resolution_plot('wet_wave_4',method=method,resolutions=resolutions)
        create_resolution_plot('dry_wave_3',method=method,resolutions=resolutions)
        create_resolution_plot('dry_wave_4',method=method,resolutions=resolutions)
    





