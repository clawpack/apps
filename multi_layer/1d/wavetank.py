#!/usr/bin/env python
# encoding: utf-8

r""" Run the suite of tests for the 1d two-layer equations"""

import os
import sys
import types

import numpy as np

import wind
import init_solution

from multilayer import create_output_paths, setup, before_step, plot
        
def oscillatory_wind(num_cells,eigen_method,**kargs):
    r"""docstring for oscillatory_wind"""

    # Construct output and plot directory paths
    prefix = 'ml_e%s_n%s' % (eigen_method,num_cells)
    name = 'oscillatory_wind'
    outdir,plotdir,log_path = create_output_paths(name,prefix,**kargs)

    # Initialize common pieces of the solver and pass through all non-specific parameters
    solver,solution,controller = setup(num_cells=num_cells,log_path=log_path,**kargs)

    # Set wall boundary conditions
    solver.bc_lower[0] = 3
    solver.bc_upper[0] = 3

    # Set wind function
    wind_func = lambda state:wind.set_oscillatory_wind(state,
                                        A=5.0,N=2.0,omega=2.0,t_length=10.0)
    solver.before_step = lambda solver,solution:before_step(solver,solution,
                                        wind_func=wind_func,stop_on_fail=False)
    
    # Set aux arrays including bathymetry, wind field and linearized depths
    init_solution.set_jump_bathymetry(solution.state,0.5,[-1.0,-1.0])
    wind_func(solution.state)
    init_solution.set_h_hat(solution.state,0.5,[0.0,-0.25],[0.0,-0.25])
    
    # Set initial condition
    init_solution.set_q_quiescent(solution.state)
    
    # Change pertinent problem data
    solution.state.problem_data['eigen_method'] = eigen_method
    solution.state.problem_data['rho'] = [1025.0,1045.0]
    solution.state.problem_data['r'] = solution.state.problem_data['rho'][0] \
                                     / solution.state.problem_data['rho'][1]
    solution.state.problem_data['one_minus_r'] = \
                                        1.0 - solution.state.problem_data['r']
    
    # Set output
    controller.output_style = 1
    controller.num_output_times = 160
    controller.tfinal = 10.0
    controller.outdir = outdir
    controller.write_aux = True
    
    # Run simulation
    state = controller.run()
    
    # Plotting
    plot_kargs = {'xlower':solution.state.grid.x.lower,
                  'xupper':solution.state.grid.x.upper,
                  'rho':solution.state.problem_data['rho'],
                  'dry_tolerance':solution.state.problem_data['dry_tolerance']}
    plot("./setplot_oscillatory.py",outdir=outdir,plotdir=plotdir,
         htmlplot=kargs.get('htmlplot',False),iplot=kargs.get('iplot',False),
         **plot_kargs)

if __name__ == "__main__":
    oscillatory_wind(100,2,iplot=True)