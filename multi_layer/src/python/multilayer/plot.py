# encoding: utf-8

r"""
Module contains a number of generic helper functions for plotting the
multilayer shallow water equations
"""

def kappa(cd):
    return Solution(cd.frameno,path=plotdata.outdir,read_aux=True).state.aux[4,:]

def wind(cd):
    return Solution(cd.frameno,path=plotdata.outdir,read_aux=True).state.aux[1,:]
    
def h_1(cd):
    return cd.q[0,:] / rho[0]
    
def h_2(cd):
    return cd.q[2,:] / rho[1]
        
def eta_2(cd):
    return h_2(cd) + bathy(cd)
        
def eta_1(cd):
    return h_1(cd) + eta_2(cd)
        
def u_1(cd):
    index = np.nonzero(h_1(cd) > dry_tolerance)
    u_1 = np.zeros(h_1(cd).shape)
    u_1[index] = cd.q[1,index] / cd.q[0,index]
    return u_1
        
def u_2(cd):
    index = np.nonzero(h_2(cd) > dry_tolerance)
    u_2 = np.zeros(h_2(cd).shape)
    u_2[index] = cd.q[3,index] / cd.q[2,index]
    return u_2
