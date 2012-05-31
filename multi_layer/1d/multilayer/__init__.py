r"""
Package containing various functions related to the multilayer shallow
water equations.
"""

__all__ = ['bathy','bc','plot','qinit','solver','source','wind']

import bathy
import bc
import plot
import qinit
import solver
import source
import wind

# Define aux array indices
aux_index_1d = ['bathy','wind','h_hat_1','h_hat_2','kappa']
aux_index_2d = ['bathy','','']