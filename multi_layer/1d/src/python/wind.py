#!/usr/bin/env python
# encoding: utf-8

"""Functions for including wind fields in the 1d swe equations

The parameter WIND_FIELD controls which field is assumed to contain the wind
field in the aux array.  Also includes a function for calculating the wind
drag coefficient.
"""

import numpy as np

WIND_FIELD = 1

def set_no_wind(state):
    """Set wind field to zero"""
    state.aux[WIND_FIELD,:] = 0.0

def set_oscillatory_wind(state,A=5.0,N=2.0,omega=2.0,t_length=10.0):
    """Assigns an oscillatory wind field to state
    
    """
    L = state.grid.upper[0] - state.grid.lower[0]
    x = state.grid.dimensions[0].centers
    state.aux[WIND_FIELD,:] = A * np.sin(np.pi*N*x/L) \
                       * np.sin(2.0*np.pi*omega/t_length*state.t)
