#!/usr/bin/env python
# encoding: utf-8

r"""Runs idealized jump and sloped 1d shelf tests"""

import sys

import clawpack.riemann as riemann
import clawpack.clawutil.runclaw as runclaw
from clawpack.pyclaw.plot import plot

import multilayer as ml
        
def jump_shelf(num_cells,eigen_method,**kargs):
    r"""Shelf test"""

    # Construct output and plot directory paths
    prefix = 'ml_e%s_n%s' % (eigen_method,num_cells)
    name = 'jump_shelf'
    outdir,plotdir,log_path = runclaw.create_output_paths(name,prefix,**kargs)
    
    # Redirect loggers
    # This is not working for all cases, see comments in runclaw.py
    for logger_name in ['io','solution','plot','evolve','f2py','data']:
        runclaw.replace_stream_handlers(logger_name,log_path,log_file_append=False)

    # Load in appropriate PyClaw version
    if kargs.get('use_petsc',False):
        import clawpack.petclaw as pyclaw
    else:
        import clawpack.pyclaw as pyclaw

    # =================
    # = Create Solver =
    # =================
    if kargs.get('solver_type','classic') == 'classic':
        solver = pyclaw.ClawSolver1D()
    else:
        raise NotImplementedError('Classic is currently the only supported solver.')
        
    # Solver method parameters
    solver.cfl_desired = 0.9
    solver.cfl_max = 1.0
    solver.max_steps = 5000
    solver.fwave = True
    solver.kernel_language = 'Fortran'
    solver.num_waves = 4
    solver.limiters = 3
    solver.source_split = 1
        
    # Boundary conditions
    # Use wall boundary condition at beach
    solver.bc_lower[0] = 1
    solver.bc_upper[0] = 0
    solver.user_bc_upper = ml.bc.wall_qbc_upper
    solver.aux_bc_lower[0] = 1
    solver.aux_bc_upper[0] = 1
    
    # Set the Riemann solver
    solver.rp = riemann.rp1_layered_shallow_water

    # Set the before step function
    solver.before_step = lambda solver,solution:ml.step.before_step(solver,
                                                                    solution)
                                            
    # Use simple friction source term
    solver.step_source = ml.step.friction_source

    
    # ============================
    # = Create Initial Condition =
    # ============================
    num_layers = 2
    
    x = pyclaw.Dimension('x',-400e3,0.0,num_cells)
    domain = pyclaw.Domain([x])
    state = pyclaw.State(domain,2*num_layers,3+num_layers)
    state.aux[ml.aux.kappa_index,:] = 0.0

    # Set physics data
    state.problem_data['g'] = 9.8
    state.problem_data['manning'] = 0.0
    state.problem_data['rho_air'] = 1.15
    state.problem_data['rho'] = [1025.0,1045.0]
    state.problem_data['r'] = state.problem_data['rho'][0] / state.problem_data['rho'][1]
    state.problem_data['one_minus_r'] = 1.0 - state.problem_data['r']
    state.problem_data['num_layers'] = num_layers
    
    # Set method parameters, this ensures it gets to the Fortran routines
    state.problem_data['eigen_method'] = eigen_method
    state.problem_data['dry_tolerance'] = 1e-3
    state.problem_data['inundation_method'] = 2
    state.problem_data['entropy_fix'] = False
    
    solution = pyclaw.Solution(state,domain)
    solution.t = 0.0
    
    # Set aux arrays including bathymetry, wind field and linearized depths
    ml.aux.set_jump_bathymetry(solution.state,-30e3,[-4000.0,-100.0])
    ml.aux.set_no_wind(solution.state)
    ml.aux.set_h_hat(solution.state,0.5,[0.0,-300.0],[0.0,-300.0])
    
    # Set perturbation to sea at rest
    ml.qinit.set_acta_numerica_init_condition(solution.state,0.4)
    
    
    # ================================
    # = Create simulation controller =
    # ================================
    controller = pyclaw.Controller()
    controller.solution = solution
    controller.solver = solver
    
    # Output parameters
    controller.output_style = 1
    controller.tfinal = 7200.0
    controller.num_output_times = 300
    controller.write_aux_init = True
    controller.outdir = outdir
    controller.write_aux = True
    
    # ==================
    # = Run Simulation =
    # ==================
    state = controller.run()
    
    # ============
    # = Plotting =
    # ============
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
    
    # Redirect loggers
    # This is not working for all cases, see comments in runclaw.py
    for logger_name in ['io','solution','plot','evolve','f2py','data']:
        runclaw.replace_stream_handlers(logger_name,log_path,log_file_append=False)

    # Load in appropriate PyClaw version
    if kargs.get('use_petsc',False):
        import clawpack.petclaw as pyclaw
    else:
        import clawpack.pyclaw as pyclaw
        
    
    # =================
    # = Create Solver =
    # =================
    if kargs.get('solver_type','classic') == 'classic':
        solver = pyclaw.ClawSolver1D()
    else:
        raise NotImplementedError('Classic is currently the only supported solver.')
        
    # Solver method parameters
    solver.cfl_desired = 0.9
    solver.cfl_max = 1.0
    solver.max_steps = 5000
    solver.fwave = True
    solver.kernel_language = 'Fortran'
    solver.num_waves = 4
    solver.limiters = 3
    solver.source_split = 1
        
    # Boundary conditions
    # Use wall boundary condition at beach
    solver.bc_lower[0] = 1
    solver.bc_upper[0] = 0
    solver.user_bc_upper = ml.bc.wall_qbc_upper
    solver.aux_bc_lower[0] = 1
    solver.aux_bc_upper[0] = 1
    
    # Set the Riemann solver
    solver.rp = riemann.rp1_layered_shallow_water

    # Set the before step function
    solver.before_step = lambda solver,solution:ml.step.before_step(solver,solution)
                                            
    # Use simple friction source term
    solver.step_source = ml.step.friction_source

    
    # ============================
    # = Create Initial Condition =
    # ============================
    num_layers = 2
    
    x = pyclaw.Dimension('x',-400e3,0.0,num_cells)
    domain = pyclaw.Domain([x])
    state = pyclaw.State(domain,2*num_layers,3+num_layers)
    state.aux[ml.aux.kappa_index,:] = 0.0

    # Set physics data
    state.problem_data['g'] = 9.8
    state.problem_data['manning'] = 0.0
    state.problem_data['rho_air'] = 1.15
    state.problem_data['rho'] = [1025.0,1045.0]
    state.problem_data['r'] = state.problem_data['rho'][0] / state.problem_data['rho'][1]
    state.problem_data['one_minus_r'] = 1.0 - state.problem_data['r']
    state.problem_data['num_layers'] = num_layers
    
    # Set method parameters, this ensures it gets to the Fortran routines
    state.problem_data['eigen_method'] = eigen_method
    state.problem_data['dry_tolerance'] = 1e-3
    state.problem_data['inundation_method'] = 2
    state.problem_data['entropy_fix'] = False
    
    solution = pyclaw.Solution(state,domain)
    solution.t = 0.0
    
    # Set aux arrays including bathymetry, wind field and linearized depths
    x0 = -130e3
    x1 = -30e3
    ml.aux.set_sloped_shelf_bathymetry(solution.state,x0,x1,-4000.0,-100.0)
    ml.aux.set_no_wind(solution.state)
    ml.aux.set_h_hat(solution.state,0.5,[0.0,-300.0],[0.0,-300.0])
    
    # Set perturbation to sea at rest
    ml.qinit.set_acta_numerica_init_condition(solution.state,0.4)
    
    
    # ================================
    # = Create simulation controller =
    # ================================
    controller = pyclaw.Controller()
    controller.solution = solution
    controller.solver = solver
    
    # Output parameters
    controller.output_style = 1
    controller.tfinal = 7200.0
    controller.num_output_times = 300
    controller.write_aux_init = True
    controller.outdir = outdir
    controller.write_aux = True
    
    # ==================
    # = Run Simulation =
    # ==================
    state = controller.run()
    
    
    # ============
    # = Plotting =
    # ============
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
        eig_methods = [2]
        
    for method in eig_methods:
        jump_shelf(2000,method,iplot=False,htmlplot=True)
    # for method in eig_methods:
    #     sloped_shelf(2000,method,iplot=False,htmlplot=True)