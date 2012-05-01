#!/usr/bin/env python

import sys
import os
import re
import numpy as np
import pylab

from pyclaw.plotters.data import ClawPlotData
from pyclaw.data import Data

if len(sys.argv) > 1:
    out_dir = sys.argv[1]
else:
    out_dir = "_output"

# Plot settings
claw_data = Data(os.path.join(out_dir,'claw.data'))
prob_data = Data(os.path.join(out_dir,'problem.data'))
pd = ClawPlotData()
pd.outdir = out_dir

# Load the bathymetry
b =  np.loadtxt(os.path.join(pd.outdir,'fort.aux'),
                converters={0:(lambda x:float(re.compile("[Dd]").sub("e",x)))})

def read_data():
    for num_frames in xrange(1000):
        fname = os.path.join(out_dir,'fort.q%s' % str(num_frames).zfill(4))
        if not os.path.exists(fname):
            break
    # num_frames = 301
    mx = claw_data.mx
    eta = np.ndarray((mx,num_frames,2))
    t = np.ndarray((num_frames))
    
    for frameno in xrange(num_frames):
        frame = pd.getframe(frameno)
        q = frame.grids[0].q
        t[frameno] = frame.t / 3600.0
        eta[:,frameno,1] = q[:,2] + b
        eta[:,frameno,0] = q[:,0] + eta[:,frameno,1]
    
    x = frame.p_center[0]
    X,T = np.meshgrid(x,t)
    return X,T,eta

bathy_ref_lines = [-130e3,-30e3]

def contour_plot(X,T,eta):
    pylab.figure(1,figsize=[10,8])
    pylab.clf()
    pylab.subplot(1,2,1)
    # pylab.axes([.1,.1,.6,.8])
    clines = np.linspace(.025,.4,15)
    # clines = np.linspace(.4,.4,15)
    pylab.contour(X,T,eta[:,:,0].T,clines,colors='r')
    # pylab.contour(X,T,eta,-clines,colors='b',linestyles='solid')
    pylab.contour(X,T,-eta[:,:,0].T,clines,colors='b--')
    for ref_line in bathy_ref_lines:
        pylab.plot([ref_line,ref_line],[0,2],'k--')
    pylab.xticks([-300e3,-200e3,-100e3,-30e3],[300,200,100,30],fontsize=15)
    pylab.yticks(fontsize=15)
    pylab.xlabel("Kilometers offshore",fontsize=15)
    pylab.ylabel("Hours",fontsize=20)
    pylab.title("Contours of top surface",fontsize=15)
    pylab.xlim([-200e3,0.0])
    # add_timeslices()
    # fname = "_".join((out_dir,"shelf_top.png"))
    # print "Writing out to %s" % fname
    # pylab.savefig(fname)
    
    # pylab.figure(2,figsize=[7,8])
    # pylab.clf()
    pylab.subplot(1,2,2)
    # pylab.axes([.1,.1,.6,.8])
    clines = np.linspace(.025,0.5,15)
    pylab.contour(X,T,eta[:,:,1].T - prob_data.eta_2,clines,colors='r')
    # # pylab.contour(X,T,eta[:,:,1].T,colors='r')
    # pylab.contour(X,T,eta,-clines,colors='b',linestyles='solid')
    pylab.contour(X,T,-(eta[:,:,1].T - prob_data.eta_2),clines,colors='b--')
    for ref_line in bathy_ref_lines:
        pylab.plot([ref_line,ref_line],[0,2],'k--')
    pylab.xticks([-300e3,-200e3,-100e3,-30e3],[300,200,100,30],fontsize=15)
    pylab.xlim([-200e3,0.0])
    # # pylab.yticks(fontsize=15)
    pylab.xlabel("Kilometers offshore",fontsize=15)
    locs,labels = pylab.yticks()
    # labels = np.flipud(locs)/1.e3
    labels = ['' for i in xrange(len(locs))]
    pylab.yticks(locs,labels)
    # # pylab.ylabel("Hours",fontsize=20)
    pylab.title("Contours of internal surface",fontsize=15)
    # add_timeslices()
    fname = "_".join((out_dir,"shelf_contour.png"))
    print "Writing out to %s" % fname
    pylab.savefig(fname)


def add_timeslices():
    times = pylab.array([0,200,400,600,1000,1400,2000,2800,3400,4800]) 
    for t in times:
        thours = t / 3600.
        pylab.plot([-400e3,0.],[thours,thours],'k')
        pylab.annotate('%s seconds' % t,[0.,thours],[30e3,thours],\
              arrowprops={'width':1,'color':'k','frac':0.2,'shrink':0.1})


def xt_and_frameplots(X,T,eta):
    """
    Unfinished attempt to plot frames with xt plot
    """
    contour_plot(X,T,eta)
    framenos = [0,1,2,3,5,7,10,14,27,24]
    plotdata = ClawPlotData()
    plotdata = setplot(plotdata)
    for frameno in framenos:
        frametools.plotframe(frameno,plotdata)

def mesh_plot(X,T,eta):
    from enthought.mayavi import mlab
    X = 2000*X/np.abs(x.min())
    eta = 1000*eta
    mlab.figure(1)
    mlab.clf()
    mlab.mesh(X,T,eta)

if __name__=="__main__":
    X,T,eta = read_data()
    contour_plot(X,T,eta)
    # pylab.savefig("shelfxt.eps")
