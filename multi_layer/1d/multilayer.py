#!/usr/bin/env python
# encoding: utf-8

import os
import sys
import types
import glob

import numpy as np

import wind

# Function called before each time step
def before_step(solver,solution,wind_func=wind.set_no_wind,
                dry_tolerance=1e-3,richardson_tolerance=0.95,
                stop_on_fail=False):
    r""""""
    # Extract relevant data
    num_layers = solution.states[0].problem_data['num_layers']
    rho = solution.states[0].problem_data['rho']
    g = solution.states[0].problem_data['g']
    one_minus_r = solution.states[0].problem_data['one_minus_r']
    
    # State arrays
    q = solution.states[0].q
    aux = solution.states[0].aux
    
    # Zero out negative values
    q = q * (q > 0.0)
    
    # Calculate wind
    wind_func(solution.state)
    
    # Calculate kappa
    h = np.zeros((num_layers,q.shape[1]))
    u = np.zeros(h.shape)
    for layer in xrange(num_layers):
        layer_index = 2*layer
        h[layer,:] = solution.q[layer_index,:] / rho[layer]
        wet_index = h[layer,:] > dry_tolerance
        u = np.zeros((2,solution.q.shape[1]))
        u[layer,wet_index] = solution.q[layer_index+1,wet_index] / solution.q[layer_index,wet_index]
    aux[2,:] = (u[0,:] - u[1,:])**2 / (g * one_minus_r * (h[0,:] + h[1,:]))
    if np.any(aux[2,wet_index] > richardson_tolerance):
        # Actually calculate where the indices failed
        bad_indices = (aux[2,wet_index] > richardson_tolerance).nonzero()[0]
        print "Hyperbolicity may have failed at the following points:"
        for i in bad_indices:
            print "\tkappa(%s) = %s" % (i,aux[2,i])
        if stop_on_fail:
            raise Exception("Richardson tolerance exceeded!")
            

# Friction source function
def friction_source(solver,state,dt,TOLERANCE=1e-30):
    r""""""
    num_layers = state.problem_data['num_layers']
    manning = state.problem_data['manning']
    g = state.problem_data['g']
    rho = state.problem_data['rho']
    dry_tolerance = state.problem_data['dry_tolerance']
    
    if manning > TOLERANCE:

        for i in xrange(state.q.shape[1]):
            h = state.q[2,i] / rho[1]
            if h < dry_tolerance:
                h = state.q[0,i] / rho[0]
                u = state.q[1,i] / rho[0]
                layer_index = 0
            else:
                u = state.q[2,i] / rho[1]
                layer_index = 1
        
            gamma = u * g * manning**2 / h**(4/3)
            dgamma = 1.0 + dt * gamma
            hu_index = 2 * (layer_index) + 1
            state.q[hu_index,i] = state.q[hu_index,i] / dgamma * rho[layer_index]
            

def create_path(path,overwrite=False):
    r""""""
    if not os.path.exists(path):
        os.makedirs(path)
    elif overwrite:
        data_files = glob.glob(path,"*")
        for data_file in data_files:
            os.remove(data_file)

def create_output_paths(name,prefix,**kargs):
    r""""""
    if kargs.has_key('outdir'):
        outdir = kargs['outdir']
    else:
        base_path = os.environ.get('DATA_PATH',os.getcwd())
        outdir = os.path.join(base_path,name,"%s_output" % prefix)
    if kargs.has_key('plotdir'):
        plotdir = kargs['plotdir']
    else:
        base_path = os.environ.get('DATA_PATH',os.getcwd())
        plotdir = os.path.join(base_path,name,"%s_plots" % prefix)
    if kargs.has_key('logfile'):
        log_path = kargs['logfile']
    else:
        base_path = os.environ.get('DATA_PATH',os.getcwd())
        log_path = os.path.join(base_path,name,"%s_log.txt" % prefix)
        
    create_path(outdir,overwrite=kargs.get('overwrite',False))
    create_path(plotdir,overwrite=kargs.get('overwrite',False))
    create_path(os.path.dirname(log_path),overwrite=False)
    
    return outdir,plotdir,log_path


def replace_stream_handlers(logger_name,log_path,log_file_append=True):
    r"""Replace the stream handlers in the logger logger_name
        
        This routine replaces all stream handlers in logger logger_name with a 
        file handler which outputs to the log file at log_path. If 
        log_file_append is True then the log files is opened for appending, 
        otherwise it is written over.
    """
    import logging
    
    logger = logging.getLogger(logger_name)
    handler_list = [handler for handler in logger.handlers if isinstance(handler,logging.StreamHandler)]
    for handler in handler_list:
        # Create new handler
        if log_file_append:
            new_handler = logging.FileHandler(log_path,'a')
        else:
            new_handler = logging.FileHandler(log_path,'w')
            log_file_append = True
        new_handler.setLevel(handler.level)
        # new_handler.name = handler.name
        new_handler.setFormatter(handler.formatter)
            
        # Remove old handler
        if isinstance(handler,logging.FileHandler):
            handler.close()
            if os.path.exists(handler.baseFilename):
                os.remove(handler.baseFilename)
        logger.removeHandler(handler)
          
        # Add new handler  
        logger.addHandler(new_handler)

            
def setup(lower=0.0,upper=1.0,num_layers=2,num_cells=100,log_path='./pyclaw.log',
          use_petsc=False,iplot=False,htmlplot=False,outdir='./_output',solver_type='classic'):
    r"""Generic setup routine for all 1d multi-layer runs in PyClaw"""
    
    # Load in appropriate PyClaw library
    if use_petsc:
        import petclaw as pyclaw
    else:
        import pyclaw
    
    # Redirect loggers
    replace_stream_handlers('io',log_path,log_file_append=False)
    for logger_name in ['io','solution','plot','evolve','f2py','data']:
        replace_stream_handlers(logger_name,log_path)
        
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
    controller.tfinal = 1.0
    controller.num_output_times = 50
    controller.outdir = './_output'
    controller.write_aux_init = True
    
    return solver,solution,controller

    
def plot(setplot_path,outdir,plotdir=None,htmlplot=False,iplot=False,**plot_kargs):
    r""""""
    
    # Construct plotdir if not provided
    if plotdir is None:
        plotdir = os.path.join(os.path.split(outdir)[:-2],"_plots")
    
    if htmlplot or iplot:
        import pyclaw.plot
    
        # Grab and import the setplot function
        path = os.path.abspath(os.path.expandvars(os.path.expanduser(setplot_path)))
        setplot_module_dir = os.path.dirname(path)
        setplot_module_name = os.path.splitext(os.path.basename(setplot_path))[0]
        sys.path.insert(0,setplot_module_dir)
        setplot_module = __import__(setplot_module_name)
        reload(setplot_module)
        setplot = lambda plotdata:setplot_module.setplot(plotdata,**plot_kargs)
        
        if not isinstance(setplot,types.FunctionType):
            raise ImportError("Failed importing %s.setplot" % setplot_module_name)
        
        if iplot:
            from visclaw import Iplotclaw
        
            ip=Iplotclaw.Iplotclaw(setplot=setplot)
            ip.plotdata.outdir = outdir
            ip.plotdata.format = 'ascii'
        
            ip.plotloop()
            
        if htmlplot:
            from visclaw import plotclaw            
            plotclaw.plotclaw(outdir,plotdir,format='ascii',setplot=setplot)
            

    
    
    
            
