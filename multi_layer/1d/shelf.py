#!/usr/bin/env python
# encoding: utf-8

r""" Run the suite of tests for the 1d two-layer equations"""

import os
import sys
import types

import numpy as np

from pyclaw.plot import plot
import clawutil.runclaw as runclaw

# Add src/python local directory to python path for multilayer specific tests
sys.path.append('../src/python/')

import wind
import multilayer as ml
        
def jump_shelf(num_cells,eigen_method,**kargs):
    r"""Shelf test"""

    # Construct output and plot directory paths
    prefix = 'ml_e%s_n%s' % (eigen_method,num_cells)
    name = 'jump_shelf'
    outdir,plotdir,log_path = runclaw.create_output_paths(name,prefix,**kargs)
    
    # Initialize common pieces of the solver and pass through all non-specific
    # parameters
    solver,solution,controller = ml.setup(lower=-400e3,upper=0.0,num_cells=num_cells,log_path=log_path)

    # Set wall boundary condition at beach
    solver.bc_upper[0] = 0
    solver.user_bc_upper = ml.wall_qbc_upper        
    
    # Change pertinent problem data
    solution.state.problem_data['eigen_method'] = eigen_method
    solution.state.problem_data['inundation_method'] = 2
    solution.state.problem_data['rho'] = [1025.0,1045.0]
    solution.state.problem_data['rho_air'] = 1.15
    solution.state.problem_data['r'] = solution.state.problem_data['rho'][0] \
                                     / solution.state.problem_data['rho'][1]
    solution.state.problem_data['one_minus_r'] = \
                                        1.0 - solution.state.problem_data['r']
    
    # Set aux arrays including bathymetry, wind field and linearized depths
    ml.set_jump_bathymetry(solution.state,-30e3,[-4000.0,-100.0])
    wind.set_no_wind(solution.state)
    ml.set_h_hat(solution.state,0.5,[0.0,-300.0],[0.0,-300.0])
    ml.set_acta_numerica_init_condition(solution.state,0.4)
    
    # Set output
    controller.outdir = outdir
    controller.num_output_times = 300
    controller.tfinal = 7200.0
    controller.write_aux = True
    
    # Run simulation
    state = controller.run()
    
    # Plotting
    plot_kargs = {"eta":[0.0,-300.0],
                  "rho":solution.state.problem_data['rho'],
                  "g":solution.state.problem_data['g'],
                  "dry_tolerance":solution.state.problem_data['dry_tolerance'],
                  "bathy_ref_lines":[-30e3]}
    plot(setplot_path="./setplot_shelf.py",outdir=outdir,plotdir=plotdir,
         htmlplot=kargs.get('htmlplot',False),iplot=kargs.get('iplot',False),
         file_format=controller.output_format,**plot_kargs)
         
def sloped_shelf(num_cells,eigen_method,**kargs):
    r"""Shelf test"""

    # Construct output and plot directory paths
    prefix = 'ml_e%s_n%s' % (eigen_method,num_cells)
    name = 'sloped_shelf'
    outdir,plotdir,log_path = runclaw.create_output_paths(name,prefix,**kargs)
    
    # Initialize common pieces of the solver and pass through all non-specific
    # parameters
    solver,solution,controller = ml.setup(lower=-400e3,upper=0.0,num_cells=num_cells,log_path=log_path)

    # Set wall boundary condition at beach
    solver.bc_upper[0] = 0
    solver.user_bc_upper = ml.wall_qbc_upper        
    
    # Change pertinent problem data
    solution.state.problem_data['eigen_method'] = eigen_method
    solution.state.problem_data['inundation_method'] = 2
    solution.state.problem_data['rho'] = [1025.0,1045.0]
    solution.state.problem_data['rho_air'] = 1.15
    solution.state.problem_data['r'] = solution.state.problem_data['rho'][0] \
                                     / solution.state.problem_data['rho'][1]
    solution.state.problem_data['one_minus_r'] = \
                                        1.0 - solution.state.problem_data['r']
    
    # Set aux arrays including bathymetry, wind field and linearized depths
    x0 = -130e3
    x1 = -30e3
    ml.set_sloped_shelf_bathymetry(solution.state,x0,x1,-4000.0,-100.0)
    wind.set_no_wind(solution.state)
    ml.set_h_hat(solution.state,0.5,[0.0,-300.0],[0.0,-300.0])
    ml.set_acta_numerica_init_condition(solution.state,0.4)
    
    # Set output
    controller.outdir = outdir
    controller.num_output_times = 300
    controller.tfinal = 7200.0
    controller.write_aux = True
    
    # Run simulation
    state = controller.run()
    
    # Plotting
    plot_kargs = {"eta":[0.0,-300.0],
                  "rho":solution.state.problem_data['rho'],
                  "g":solution.state.problem_data['g'],
                  "dry_tolerance":solution.state.problem_data['dry_tolerance'],
                  "bathy_ref_lines":[x0,x1]}
    plot(setplot_path="./setplot_shelf.py",outdir=outdir,plotdir=plotdir,
         htmlplot=kargs.get('htmlplot',False),iplot=kargs.get('iplot',False),
         file_format=controller.output_format,**plot_kargs)


if __name__ == "__main__":
    # Run the test for the requested eigen methods for the jump and slope bathys
    if len(sys.argv) > 1:
        eig_methods = []
        for value in sys.argv[1:]:
            eig_methods.append(int(value))
    else:
        eig_methods = [1,2,3,4]
        
    # for method in eig_methods:
    #     jump_shelf(2000,method,iplot=False,htmlplot=True)
    for method in eig_methods:
        sloped_shelf(2000,method,iplot=False,htmlplot=True)