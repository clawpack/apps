# encoding: utf-8

r"""
Functions used in the solver objects
"""

import wind

def before_step(solver,solution,wind_func=wind.set_no_wind,dry_tolerance=1e-3,
                    richardson_tolerance=0.95,raise_on_fail=False):
    r"""
    Sets data fields and performs calculations needed before a time
    step is taken.
    
    :Input:
     - *solver* (:class:pyclaw.solver.Solver)
     - *solution* (:class:pyclaw.solution.Solution)
     - *wind_func* (func)
     - *dry_tolerance* (float)
     - *richardson_tolerance* (float)
     - *raise_on_fail* (bool)
    
    :Output:
    
    :Raises:
      - (Exception) - Richardson tolerance exceeded.  Only raised if 
        stop_on_fail is set to True.
    """
    
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
    
    # Set wind field
    wind_func(solution.state)
    
    # Calculate kappa
    h = np.zeros((num_layers,q.shape[1]))
    u = np.zeros(h.shape)
    for layer in xrange(num_layers):
        layer_index = 2*layer
        h[layer,:] = solution.q[layer_index,:] / rho[layer]
        wet_index = h[layer,:] > dry_tolerance
        u[layer,wet_index] = solution.q[layer_index+1,wet_index] / solution.q[layer_index,wet_index]
    aux[kappa_index,:] = (u[0,:] - u[1,:])**2 / (g * one_minus_r * (h[0,:] + h[1,:]))
    if np.any(aux[kappa_index,wet_index] > richardson_tolerance):
        # Actually calculate where the indices failed
        bad_indices = (aux[kappa_index,wet_index] > richardson_tolerance).nonzero()[0]
        print "Hyperbolicity may have failed at the following points:"
        for i in bad_indices:
            print "\tkappa(%s) = %s" % (i,aux[kappa_index,i+1])
        if stop_on_fail:
            raise Exception("Richardson tolerance exceeded!")
