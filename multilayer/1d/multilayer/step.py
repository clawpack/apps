# encoding: utf-8
r"""
Module contains routines implementing call back functions needed for a single
time step.

*before_step* - Checks for negative depths, sets the wind, and calculates kappa
                and checks against the Richardson tolerance.
                
*friction_source* - Implements Manning's-N type friction source term
"""

import numpy as np

from aux import set_no_wind,kappa_index

class NegativeDepthError(Exception):
    r"""Error raised when depth becomes negative in a layer"""
    def __init__(self,layer,location):
        self.layer = layer
        self.location = location
        msg = "Negative depth found in layer %s at %s" % (layer,location)
        super(NegativeDepthError,self).__init__(msg)

class RichardsonExceededError(Exception):
    r"""Error raised when the Richardson tolerance has been exceeded"""
    
    def __init__(self,indices,solution):
        self.indices = indices
        self.solution = solution
        msg = "Richardson tolerance exceeded at indices %s" % indices
        super(RichardsonExceededError,self).__init__(msg)



def before_step(solver,state,wind_func=set_no_wind,dry_tolerance=1e-3,
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
    num_layers = state.problem_data['num_layers']
    rho = state.problem_data['rho']
    g = state.problem_data['g']
    one_minus_r = state.problem_data['one_minus_r']
    x = state.grid.dimensions[0].centers
    
    # State arrays
    q = state.q
    aux = state.aux
    
    # Zero out negative values
    for layer in xrange(num_layers):
        m = num_layers * layer
        negative_indices = (q[m,:] < 0.0).nonzero()[0]
        q[m,negative_indices] = 0.0
        q[m+1,negative_indices] = 0.0
        
        if raise_on_negative:
            if len(negative_indices) < 0:
                locations = x[negative_indices]
                raise NegativeDepthError(layer,locations)
    
    
    # Set wind field
    wind_func(state)
    
    # Calculate kappa
    h = np.zeros((num_layers,q.shape[1]))
    u = np.zeros(h.shape)
    for layer in xrange(num_layers):
        layer_index = 2*layer
        h[layer,:] = state.q[layer_index,:] / rho[layer]
        wet_index = h[layer,:] > dry_tolerance
        u[layer,wet_index] = state.q[layer_index+1,wet_index] / state.q[layer_index,wet_index]
    aux[kappa_index,:] = (u[0,:] - u[1,:])**2 / (g * one_minus_r * (h[0,:] + h[1,:]))
    if np.any(aux[kappa_index,wet_index] > richardson_tolerance):
        # Actually calculate where the indices failed
        bad_indices = (aux[kappa_index,wet_index] > richardson_tolerance).nonzero()[0]
        if raise_on_richardson:
            state.aux = aux
            raise RichardsonExceededError(bad_indices,state)
        else:
            print "Hyperbolicity may have failed at the following points:"
            for i in bad_indices:
                print "\tkappa(%s) = %s" % (i,aux[kappa_index,i])



def friction_source(solver,state,dt,TOLERANCE=1e-30):
    r""""""
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