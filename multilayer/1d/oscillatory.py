#!/usr/bin/env python
# encoding: utf-8

r""" Run the suite of tests for the 1d two-layer equations"""

from clawpack.riemann import layered_shallow_water_1D
import clawpack.clawutil.runclaw as runclaw
from clawpack.pyclaw.plot import plot

import multilayer as ml
        
def oscillatory_wind(num_cells,eigen_method,**kargs):
    r"""docstring for oscillatory_wind"""

    # Construct output and plot directory paths
    prefix = 'ml_e%s_n%s' % (eigen_method,num_cells)
    name = 'oscillatory_wind'
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
    # Here we implement our own wall boundary conditions for the multi-layer 
    # equations
    solver.bc_lower[0] = 0 
    solver.bc_upper[0] = 0
    solver.user_bc_lower = ml.bc.wall_qbc_lower
    solver.user_bc_upper = ml.bc.wall_qbc_upper
    solver.aux_bc_lower[0] = 1
    solver.aux_bc_upper[0] = 1
    
    # Set the Riemann solver
    solver.rp = layered_shallow_water_1D

    # Set the before step functioning including the wind forcing
    wind_func = lambda state:ml.aux.set_oscillatory_wind(state,
                                        A=5.0,N=2.0,omega=2.0,t_length=10.0)
    solver.before_step = lambda solver,solution:ml.step.before_step(solver,solution,
                                            wind_func=wind_func,raise_on_richardson=True)
                                            
    # Use simple friction source term
    solver.step_source = ml.step.friction_source
    
    # ============================
    # = Create Initial Condition =
    # ============================
    num_layers = 2
    
    x = pyclaw.Dimension('x',0.0,1.0,num_cells)
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
    ml.aux.set_jump_bathymetry(solution.state,0.5,[-1.0,-1.0])
    wind_func(solution.state)
    ml.aux.set_h_hat(solution.state,0.5,[0.0,-0.25],[0.0,-0.25])
    
    # Set sea at rest initial condition
    ml.qinit.set_quiescent_init_condition(solution.state)
    
    # ================================
    # = Create simulation controller =
    # ================================
    controller = pyclaw.Controller()
    controller.solution = solution
    controller.solver = solver
    
    # Output parameters
    controller.output_style = 1
    controller.tfinal = 10.0
    controller.num_output_times = 160
    controller.write_aux_init = True
    controller.outdir = outdir
    controller.keep_copy = True
    controller.write_aux_always = True
    
    # ==================
    # = Run Simulation =
    # ==================
    try:
        state = controller.run()
    except ml.step.RichardsonExceededError as e:
        print e
        # print "Writing out last solution available to frame %s." % str(len(controller.frames))
        # e.solution.write(len(controller.frames),path=controller.outdir,write_aux=True)
    
    # ============
    # = Plotting =
    # ============
    plot_kargs = {'xlower':solution.state.grid.x.lower,
                  'xupper':solution.state.grid.x.upper,
                  'rho':solution.state.problem_data['rho'],
                  'dry_tolerance':solution.state.problem_data['dry_tolerance']}
    plot(setplot="./setplot_oscillatory.py",outdir=outdir,
         plotdir=plotdir,htmlplot=kargs.get('htmlplot',False),
         iplot=kargs.get('iplot',False),file_format=controller.output_format,
         **plot_kargs)
         
         
if __name__ == "__main__":
    oscillatory_wind(100,2,htmlplot=True)