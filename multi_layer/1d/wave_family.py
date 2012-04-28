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
sys.path.append('./src/python/')

import init_solution
import wind
import multilayer as ml
        
def wave_family(num_cells,eigen_method,wave_family,**kargs):
    r"""docstring for oscillatory_wind"""

    # Construct output and plot directory paths
    prefix = 'ml_e%s_n%s' % (eigen_method,num_cells)
    name = 'idealized_%s' % wave_family
    outdir,plotdir,log_path = runclaw.create_output_paths(name,prefix,**kargs)

    # Initialize common pieces of the solver and pass through all non-specific
    # parameters
    solver,solution,controller = ml.setup(num_cells=num_cells,log_path=log_path,**kargs)
    solver.before_step = lambda solver,solution:ml.before_step(solver,solution
                                                    ,stop_on_fail=False)
    
    # Change pertinent problem data
    solution.state.problem_data['eigen_method'] = eigen_method
    
    # Set aux arrays including bathymetry, wind field and linearized depths
    ml.set_jump_bathymetry(solution.state,0.5,[-1.0,-0.2])
    wind.set_no_wind(solution.state)
    ml.set_h_hat(solution.state,0.5,[0.0,-0.25],[0.0,-0.25])
    
    # Set initial condition
    if wave_family == 3:
        ml.set_wave_family_init_condition(solution.state,wave_family,0.45,0.1)
    elif wave_family == 4:
        # The perturbation must be less in this case otherwise the internal
        # wave will crest the bathymetry jump
        ml.set_wave_family_init_condition(solution.state,wave_family,0.45,0.04)
    
    # Set output
    controller.outdir = outdir
    controller.write_aux = True
    
    # Run simulation
    state = controller.run()
    
    # Plotting
    plot_kargs = {'xlower':solution.state.grid.x.lower,
                  'xupper':solution.state.grid.x.upper,
                  'rho':solution.state.problem_data['rho'],
                  'dry_tolerance':solution.state.problem_data['dry_tolerance']}
    plot(setplot_path="./setplot_wave_family.py",outdir=outdir,plotdir=plotdir,
         htmlplot=kargs.get('htmlplot',False),iplot=kargs.get('iplot',False),
         file_format=controller.output_format,**plot_kargs)

if __name__ == "__main__":
    # Run the test for the 3rd and 4th wave families for each eigen method
    for method in [1,2,3,4]:
        wave_family(100,method,3,iplot=False,htmlplot=True)
    for method in [1,2,3,4]:
        wave_family(100,method,4,iplot=False,htmlplot=True)