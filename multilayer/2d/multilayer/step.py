# encoding: utf-8
r"""
Module contains routines implementing call back functions needed for a single
time step.

*before_step* - Checks for negative depths, sets the wind, and calculates kappa
                and checks against the Richardson tolerance.
                
*friction_source* - Implements Manning's-N type friction source term
"""

import numpy as np

from aux import set_no_wind,wind_index

class NegativeDepthError(Exception):
    r"""Error raised when depth becomes negative in a layer"""
    def __init__(self,layer,location):
        self.layer = layer
        self.location = location
        msg = "Negative depth found in layer %s at %s" % (layer,location)
        super(NegativeDepthError,self).__init__(msg)

class RichardsonExceededError(Exception):
    r"""Error raised when the Richardson tolerance has been exceeded"""
    
    def __init__(self,indices):
        self.indices = indices
        msg = "Richardson tolerance exceeded at indices %s" % indices
        super(RichardsonExceededError,self).__init__(msg)



def before_step(solver,solution,wind_func=set_no_wind,dry_tolerance=1e-3,
                    richardson_tolerance=0.95,raise_on_negative=False,
                    raise_on_richardson=False):
    r"""
    Sets data fields and performs calculations needed before a time
    step is taken.
    
    :Input:
     - *solver* (:class:pyclaw.solver.Solver)
     - *solution* (:class:pyclaw.solution.Solution)
     - *wind_func* (func)
     - *dry_tolerance* (float)
     - *richardson_tolerance* (float)
     - *raise_on_negative* (bool)
     - *raise_on_richardson* (bool)
    
    :Output:
    
    :Raises:
      - (Exception) - Richardson tolerance exceeded.  Only raised if 
        raise_on_fail is set to True.
    """
    
    # Extract relevant data
    num_layers = solution.states[0].problem_data['num_layers']
    rho = solution.states[0].problem_data['rho']
    g = solution.states[0].problem_data['g']
    one_minus_r = solution.states[0].problem_data['one_minus_r']
    x = solution.states[0].grid.dimensions[0].centers
    
    # State arrays
    q = solution.states[0].q
    aux = solution.states[0].aux
    
    # Zero out negative values
    for layer in xrange(num_layers):
        m = num_layers * layer
        negative_indices = (q[m,...] < 0.0).nonzero()[0]
        q[m,negative_indices] = 0.0
        q[m+1,negative_indices] = 0.0
        
        if raise_on_negative:
            if len(negative_indices) < 0:
                locations = x[negative_indices]
                raise NegativeDepthError(layer,locations)
    
    
    # Set wind field
    wind_func(solution.state)
    
    # Calculate kappa
    h = np.zeros((num_layers,q.shape[1:]))
    u = np.zeros(h.shape)
    for layer in xrange(num_layers):
        layer_index = 3*layer
        h[layer,...] = solution.q[layer_index,...] / rho[layer]
        wet_index = h[layer,...] > dry_tolerance
        u[layer,wet_index] = solution.q[layer_index+1,wet_index] / solution.q[layer_index,wet_index]
    kappa = (u[0,...] - u[1,...])**2 / (g * one_minus_r * (h[0,...] + h[1,...]))
    if np.any(kappa > richardson_tolerance):
        # Actually calculate where the indices failed
        bad_indices = (kappa > richardson_tolerance).nonzero()[0]
        print "Hyperbolicity may have failed at the following points:"
        # for i in bad_indices:
        #     print "\tkappa(%s) = %s" % (i,aux[kappa_index,i+1])
        if raise_on_richardson:
            raise RichardsonExceededError(bad_indices)



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
            

def wind_source(solver,state,dt):
    r""""""
    
    # Add momentum to top layer
    wind_x = state.aux[wind_index[0],...]
    wind_y = state.aux[wind_index[1],...]
    wind_speed = np.sqrt(wind_x**2 + wind_y**2)
    tau = wind_drag(wind_speed) * state.problem_data['rho_air'] * wind_speed
    state.q[1,...] += dt * tau * wind_x / state.problem_data['rho'][0]
    state.q[2,...] += dt * tau * wind_y / state.problem_data['rho'][0]
    

def wind_drag(wind_speed):
    r""""""
    return 10e-3 * ((wind_speed <= 11.0) * np.ones(wind_speed.shape) * 1.2 +
                    (wind_speed > 11) * (wind_speed <= 25) * (0.49 + 0.065 * wind_speed) +
                    (wind_speed > 25) * 0.49 * 0.065 * 25.0)
    