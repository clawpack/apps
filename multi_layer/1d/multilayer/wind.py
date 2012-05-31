# encoding: utf-8

"""Functions for including wind fields in the 1d swe equations

The parameter WIND_FIELD controls which field is assumed to contain the wind
field in the aux array.  Also includes a function for calculating the wind
drag coefficient.
"""

import numpy as np

wind_index = 1

def set_no_wind(state):
    """Set wind field to zero"""
    state.aux[wind_index,...] = 0.0

def set_oscillatory_wind(state,A=5.0,N=2.0,omega=2.0,t_length=10.0):
    """Assigns an oscillatory wind field to state
    
    :Input:
     - *state* (:class:pyclaw.state.State)
     - *A* (float)
     - *N* (float)
     - *omega* (float)
     - *t_length* (float)
     
    """
    L = state.grid.upper[0] - state.grid.lower[0]
    x = state.grid.dimensions[0].centers
    state.aux[wind_index,:] = A * np.sin(np.pi*N*x/L) \
                       * np.sin(2.0*np.pi*omega/t_length*state.t)

def set_hurricane_wind(state):
    r"""Set a hurricane wind field to state
    
    :Input:
    
    """
    raise NotImplemented("Hurricane wind fields have not been implemented yet.")
    state.aux[4:5,...] = 0.0