#!/usr/bin/env python
# encoding: utf-8

r"""Plot convergence plots for wet and dry wave family tests.

Note that in order to use this data the individual runs must be executed using
`wave_family.py` and located at `$DATA_PATH`

"""

import os

import numpy as np
from scipy.linalg import norm
from scipy import polyfit

# Plot customization
import matplotlib

# Figure default size
matplotlib.rcParams['figure.figsize'] = [6.0,4.5]

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
num_layers = 2

# Plot settings for specfic experiments
styles = ['go','cs','r+','bx','m.']
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

def row_output(field="",method="",order="",latex=False):
    if latex:
        column_delimiter = "&"
        new_line = r"\\" + " \n"
    else:
        column_delimiter = r"|"
        new_line = "\n"
    output = column_delimiter + str(field).rjust(25)
    output += " %s " % column_delimiter + str(method).rjust(25)
    if isinstance(order,float):
        output += " %s " % column_delimiter + str(round(order,2)).rjust(25)
    else:
        output += " %s " % column_delimiter + str(order).rjust(25)
    output += " %s%s" % (column_delimiter, new_line)
    return output


def make_table(methods,fields,order,title,latex=False):
    r"""Make a convergence table comparing each method"""

    output = "Convergence Orders - %s".center(80) % title

    if latex:
        minor_row_delimiter = "\hline"
        major_row_delimiter = "\hline \hline"
        new_line = r"\\" + " \n"
        output += "\n"
        output += r"""\begin{table}[tb]
    \label{table:convergence_%s}
    \begin{center}
        \begin{tabular}{|l|l|l|}""" % title
        output += "\n"
    else:
        minor_row_delimiter = "-" * (25 * 3 + 9)
        major_row_delimiter = "=" * (25 * 3 + 9)
        new_line = "\n"
    output += new_line
    output += major_row_delimiter + new_line
    output += row_output("Field","Method","Order",latex)
    output += major_row_delimiter + new_line
    for (i,field) in enumerate(fields):
        output += row_output(field,methods[0],order[i][0],latex)
        for (m,method) in enumerate(methods[1:]):
            output += row_output("",method,order[i][m],latex)
        output += minor_row_delimiter + new_line

    if latex:
        output += """        
        \end{tabular}
    \end{center}
\end{table}"""
    return output


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


def create_convergence_plot(base_path, eigen_methods=[1,2,3,4], 
                                       resolutions=[64], 
                                       table_file=None, latex_tables=False):
    r"""Create plots comparing each eigenspace method 

    """

    # Parameters
    fields = 4
    plot_titles = ["Top Layer Depths",
                   "Top Layer Velocities",
                   "Bottom Layer Depths",
                   "Bottom Layer Velocities"]
    file_names = ['convergence_top_surface',
                  'convergence_bot_surface',
                  'convergence_top_velocity',
                  'convergence_bot_velocity']

    # Extract data from plot settings dict
    frame = plot_settings[base_path]["frame"]

    # Calculate error
    # error[field,eigen_method,resolution]
    error = np.zeros((fields,len(eigen_methods),len(resolutions)))

    # Extract base solution
    path = os.path.join(data_path,base_path,
                                    'ml_e%s_n%s_output' % (4,base_resolution))
    x_base,b_base,h_base,eta_base,u_base = \
                        extract_data(Solution(frame,path=path,read_aux=True))

    # Calculate errors
    for (m,method) in enumerate(eigen_methods):
        for (n,resolution) in enumerate(resolutions):

            # Load solution and extract data        
            path = os.path.join(data_path,base_path,
                                'ml_e%s_n%s_output' % (method,resolution))
            x,b,h,eta,u = extract_data(Solution(frame,path=path,read_aux=True))

            error[0,m,n] = norm(h[0][:] - np.interp(x,x_base,h_base[0][:]))
            error[1,m,n] = norm(h[1][:] - np.interp(x,x_base,h_base[1][:]))
            error[2,m,n] = norm(u[0][:] - np.interp(x,x_base,u_base[0][:]))
            error[3,m,n] = norm(u[1][:] - np.interp(x,x_base,u_base[1][:]))

    # Calculate order
    order = [[] for i in xrange(fields)]
    for field in xrange(fields):
        for (m,method) in enumerate(eigen_methods):
            order[field].append(-polyfit(np.log(resolutions),np.log(error[field,m,:]),1)[1])

    # Create figures and axes
    figs_list = [plt.figure() for n in xrange(fields)]
    axes_list = [fig.add_subplot(111) for fig in figs_list]

    # Plot errors
    for (m,method) in enumerate(eigen_methods):
        for i in xrange(fields):
            # import pdb; pdb.set_trace()
            axes_list[i].loglog(resolutions,error[i,m,:],styles[m],label=eigen_labels[m])

    # Set plot characteristics
    for (i,axes) in enumerate(axes_list):
        axes.legend()
        axes.set_title(plot_titles[i])
        axes.set_xlim([resolutions[0]-8,resolutions[-1]+32])
        axes.set_xlabel("Number of Cells")
        axes.set_ylabel("L^2 Error")
        axes.set_xticks(resolutions)
        axes.set_xticklabels(resolutions)

    # Save figures
    out_path = os.path.join(os.curdir,'comparison_plots',base_path)
    if not os.path.exists(out_path):
        os.makedirs(out_path)
    for (i,fig) in enumerate(figs_list):
        fig.savefig(os.path.join(out_path,'.'.join((file_names[i],'pdf'))))        

    # Make table, latex is saved to a file
    if table_file:
        table_file.write(make_table(eigen_labels,plot_titles,order,base_path,latex_tables))
        table_file.write("\n"*2)
    else:
        print make_table(eigen_labels,plot_titles,order,base_path,latex_tables)


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
    resolutions = [64,128,256,512,1024]
    eigen_methods = [1,2,3,4]

    # Create convergence plots
    make_latex_tables = True
    table_file = None
    table_file = open('./convergence_tables.tex','w')
    print "Writing tables to %s" % table_file.name
    create_convergence_plot('wet_wave_3',eigen_methods=eigen_methods,resolutions=resolutions,table_file=table_file,latex_tables=make_latex_tables)
    create_convergence_plot('wet_wave_4',eigen_methods=eigen_methods,resolutions=resolutions,table_file=table_file,latex_tables=make_latex_tables)
    create_convergence_plot('dry_wave_3',eigen_methods=eigen_methods,resolutions=resolutions,table_file=table_file,latex_tables=make_latex_tables)
    create_convergence_plot('dry_wave_4',eigen_methods=[1,2,4],resolutions=resolutions,table_file=table_file,latex_tables=make_latex_tables)
    table_file.close()

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