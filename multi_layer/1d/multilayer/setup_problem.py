# encoding: utf-8
r"""
Module contains functions for setting up generic settings.  Calling
these routines will then pass back objects that should be specialized
to the particular example.
"""


def setup(lower=0.0,upper=1.0,num_layers=2,num_cells=100,log_path='./pyclaw.log',
          use_petsc=False,solver_type='classic'):
    r"""Generic setup routine for all 1d multi-layer runs in PyClaw
    
    :Input:
     - *lower* (float)
     - *upper* (float)
     - *num_layers* (int)
     - *num_cells* (int)
     - *log_path* (string)
     - *use_petsc* (bool)
     - *solver_type* (string)
     
    :Output:
     - *solver* (pyclaw.solver) 
     - *solution* (pyclaw.solution)
     - *controller* (pyclaw.controller)
    """
    
    # Load in appropriate PyClaw library
    if use_petsc:
        import petclaw as pyclaw
    else:
        import pyclaw
    
    # Redirect loggers
    runclaw.replace_stream_handlers('io',log_path,log_file_append=False)
    for logger_name in ['io','solution','plot','evolve','f2py','data']:
        runclaw.replace_stream_handlers(logger_name,log_path)
        
    # Create solver object
    if solver_type == 'classic':
        solver = pyclaw.ClawSolver1D()
    else:
        raise NotImplementedError("Classic is the only solver type supported currently")
        
    # Solver parameters
    solver.bc_lower[0] = 1
    solver.bc_upper[0] = 1
    solver.aux_bc_lower[0] = 1
    solver.aux_bc_upper[0] = 1
    solver.cfl_desired = 0.9
    solver.cfl_max = 1.0
    solver.max_steps = 5000
    solver.fwave = True
    solver.kernel_language = 'Fortran'
    solver.num_waves = 4
    solver.limiters = 3
    solver.source_split = 1
        
    # Setup Riemann solver
    import riemann
    solver.rp = riemann.rp1_layered_shallow_water
    
    # Set callback functions
    solver.before_step = before_step
    solver.step_source = friction_source
            
    # Create solution
    x = pyclaw.Dimension('x',lower,upper,num_cells)
    domain = pyclaw.Domain([x])
    state = pyclaw.State(domain,2*num_layers,3+num_layers)
    state.aux[kappa_index,:] = 0.0

    # Set physics data
    state.problem_data['g'] = 9.8
    state.problem_data['manning'] = 0.0
    state.problem_data['rho_air'] = 1.15e-3
    state.problem_data['rho'] = [0.95,1.0]
    state.problem_data['r'] = state.problem_data['rho'][0] / state.problem_data['rho'][1]
    state.problem_data['one_minus_r'] = 1.0 - state.problem_data['r']
    state.problem_data['num_layers'] = num_layers
        
    # Need to send some problem parameters through to the fortran
    state.problem_data['dry_tolerance'] = 1e-3
    state.problem_data['eigen_method'] = 2
    state.problem_data['inundation_method'] = 2
    state.problem_data['entropy_fix'] = False
        
    solution = pyclaw.Solution(state,domain)
    solution.t = 0.0
    
    # Create controller
    controller = pyclaw.Controller()
    controller.solution = solution
    controller.solver = solver
    controller.output_style = 1
    controller.tfinal = 0.5
    controller.num_output_times = 50
    controller.outdir = './_output'
    controller.write_aux_init = True
    # controller.write_aux_always = True
    
    return solver,solution,controller
