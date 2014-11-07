

from matplotlib import animation
from clawpack.visclaw.JSAnimation import IPython_display
from IPython.display import display
import ipywidgets
import sympy
import numpy as np
import matplotlib.pyplot as plt


sympy.init_printing(use_latex='mathjax')


def riemann_solution(num_eqn,solver,q_l,q_r,aux_l=None,aux_r=None,t=0.2,problem_data=None):
    if aux_l is None:
        aux_l = np.zeros(num_eqn)
    if aux_r is None:
        aux_r = np.zeros(num_eqn)
    
    wave, s, amdq, apdq = solver(q_l.reshape((num_eqn,1)),q_r.reshape((num_eqn,1)),
                                 aux_l.reshape((num_eqn,1)),aux_r.reshape((num_eqn,1)),problem_data)
    
    wave0 = wave[:,:,0]
    num_waves = wave.shape[1]
    qlwave = np.vstack((q_l,wave0.T)).T
    # Sum to the waves to get the states:
    states = np.cumsum(qlwave,1)  
    
    num_states = num_waves + 1
    
    print 'States in Riemann solution:'
    states_sym = sympy.Matrix(states)
    display([states_sym[:,k] for k in range(num_states)])
    
    print 'Waves (jumps between states):'
    wave_sym = sympy.Matrix(wave[:,:,0])
    display([wave_sym[:,k] for k in range(num_waves)])
    
    print "Speeds: "
    s_sym = sympy.Matrix(s)
    display(s_sym.T)
    
    return states, s

def plot_phase(states, i_h=0, i_v=1, ax=None):
    """
    Plot 2d phase space plot.
    If num_eqns > 2, can specify which component of q to put on horizontal
    and vertical axes via i_h and i_v.
    """
    q0 = states[i_h,:]
    q1 = states[i_v,:]
    
    if ax is None:
        fig, ax = plt.subplots()
    ax.plot(q0,q1,'o-k')
    ax.set_title('phase space: q[%i] vs. q[%i]' % (i_h,i_v))
    ax.axis('equal')
    dq0 = q0.max() - q0.min()
    dq1 = q1.max() - q1.min()
    ax.text(q0[0] + 0.05*dq0,q1[0] + 0.05*dq1,'q_left')
    ax.text(q0[-1] + 0.05*dq0,q1[-1] + 0.05*dq1,'q_right')
    ax.axis([q0.min()-0.1*dq0, q0.max()+0.1*dq0, q1.min()-0.1*dq1, q1.max()+0.1*dq1])
    ax.set_xlabel('q[%s]' % i_h)
    ax.set_ylabel('q[%s]' % i_v)
    
def plot_phase_3d(states):
    """
    3d phase space plot
    """
    from mpl_toolkits.mplot3d import Axes3D
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.plot(states[0,:],states[1,:],states[2,:],'ko-')
    ax.set_xlabel('q[0]')
    ax.set_ylabel('q[1]')
    ax.set_zlabel('q[2]')
    ax.set_title('phase space')
    ax.text(states[0,0]+0.05,states[1,0],states[2,0],'q_left')
    ax.text(states[0,-1]+0.05,states[1,-1],states[2,-1],'q_right')
 
def plot_riemann(states, s, t, fig=None, color='b'):
    """
    Take an array of states and speeds s and plot the solution at time t.
    Plots in the x-t plane and also produces a separate plot for each component of q.
    """
    
    num_eqn,num_states = states.shape
    if fig is None:
        figwidth = 4*(num_eqn+1)
        fig, ax = plt.subplots(1,num_eqn+1,figsize=(figwidth,4))
    else:
        ax = fig.axes
    tmax = 1.0
    xmax = 0.
    for i in range(len(s)):
        x1 = tmax * s[i]
        ax[0].plot([0,x1],[0,tmax],color=color)
        xmax = max(xmax,abs(x1))
    x = np.linspace(-xmax,xmax,1000)
                   
    ax[0].set_xlim(-xmax,xmax)
    ax[0].plot([-xmax,xmax],[t,t],'k',linewidth=2)
    
    for i in range(num_eqn):
        ax[i+1].set_xlim((-1,1))
        qmax = states[i,:].max()  #max([state[i] for state in states])
        qmin = states[i,:].min()  # min([state[i] for state in states])
        qdiff = qmax - qmin
        ax[i+1].set_xlim(-xmax,xmax)
        ax[i+1].set_ylim((qmin-0.1*qdiff,qmax+0.1*qdiff))
        ax[i+1].set_title('q[%s] at t = %6.3f' % (i,t))
    
    q = np.outer(states[:,0],(x<t*s[0]))

    for i in range(len(s)-1):
        q = q + np.outer(states[:,i+1],(x>=t*s[i])*(x<t*s[i+1]))
    q = q + np.outer(states[:,-1],(x>s[-1]*t))

    for i in range(num_eqn):
        ax[i+1].plot(x,q[i,:],color=color)
    return fig
            
            
def make_plot_function(states,s):
    """
    Utility function to create a plot_function that takes a single argument t.
    This function can then be used in a StaticInteract widget.
    """
    def plot_function(t):
        fig = plot_riemann(states,s,t)
        return fig
    return plot_function

def make_plot_function_compare(states,s,states2,s2):
    """
    Utility function to create a plot_function that takes a single argument t.
    This function can then be used in a StaticInteract widget.
    Version that takes two sets of states and speeds in order to make a comparison.
    """
    def plot_function(t):
        fig = plot_riemann(states,s,t)
        fig = plot_riemann(states2,s2,t,fig,'r')
        return fig
    return plot_function
