# encoding: utf-8

r"""
Routines for implementing source terms in the multilayer shallow
water equations.

:Source Terms:
 - *Friction* (1d,2d)
 - *Wind* (2d), the wind source term is directly incorporated into the Riemann
   solver
 - *Coriolis* (2d)
"""

def friction_source_1d(solver,state,dt,TOLERANCE=1e-30):
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

def friction_source_2d(solver,state,dt,TOLERANCE=1e-30):
    r"""Friction source term for 2d problems"""

    num_layers = state.problem_data['num_layers']
    manning = state.problem_data['manning']
    g = state.problem_data['g']
    rho = state.problem_data['rho']
    dry_tolerance = state.problem_data['dry_tolerance']
    
    raise NotImplemented("2D friction source term not fully implemented.")
    
def coriolis_source_2d(solver,state,dt):
    r"""Coriolis source term for 2d problems"""
    raise NotImplemented("2D Coriolis source term not implemented!")