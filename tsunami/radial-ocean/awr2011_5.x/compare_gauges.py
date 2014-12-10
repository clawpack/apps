
import pylab
from clawpack.visclaw.data import ClawPlotData

outdir1 = '_output_260'
outdir2 = '_output_220'
gaugenos = [1,2]

plotdata = ClawPlotData()
    
pylab.figure(301)
pylab.clf()

plotdata.outdir = outdir1
for gaugeno in gaugenos:
    gs = plotdata.getgauge(gaugeno)
    pylab.plot(gs.t, gs.q[3,:], 'b',linewidth=2)


plotdata.outdir = outdir2
for gaugeno in gaugenos:
    gs = plotdata.getgauge(gaugeno)
    pylab.plot(gs.t, gs.q[3,:], 'r--',linewidth=2)

pylab.xlim([7500,14000])
pylab.ylim([-2.5,4])
pylab.xticks(fontsize=15)
pylab.yticks(fontsize=15)

pylab.annotate('Gauge 1',[8200,1.9],[7700,2.5],arrowprops={'width':1,'color':'k'})
pylab.annotate('Gauge 2',[9300,2.7] ,[9700,3.1],arrowprops={'width':1,'color':'k'})

pylab.savefig('gauges1-2.png')

print "Created gauges1-2.png"

#===============================

gaugenos = [3,4]
pylab.figure(302)
pylab.clf()

plotdata.outdir = outdir1
for gaugeno in gaugenos:
    gs = plotdata.getgauge(gaugeno)
    pylab.plot(gs.t, gs.q[3,:], 'b',linewidth=2)


plotdata.outdir = outdir2
for gaugeno in gaugenos:
    gs = plotdata.getgauge(gaugeno)
    pylab.plot(gs.t, gs.q[3,:], 'r--',linewidth=2)

pylab.xlim([7500,14000])
pylab.ylim([-2.5,4])
pylab.xticks(fontsize=15)
pylab.yticks(fontsize=15)

pylab.annotate('Gauge 3',[12500,2.6],[13000,3.1],arrowprops={'width':1,'color':'k'})
pylab.annotate('Gauge 4',[11550,1.0] ,[11200,2.0],arrowprops={'width':1,'color':'k'})

pylab.savefig('gauges3-4.png')

print "Created gauges3-4.png"
