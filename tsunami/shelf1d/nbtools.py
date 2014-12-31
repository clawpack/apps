
from IPython.core.display import display
try:
    from IPython.display import FileLink
except:
    print "*** Ipython version does not support FileLink"


def make_htmls(outfile=None, verbose=False, readme_link=True):
    """Perform 'make .htmls' and display link."""
    import os,sys
    
    if outfile is None:
        outfile='htmls_output.txt'
    cmd = 'make .htmls &> %s' % outfile

    if verbose:
        print "Making html documentation files... %s" % cmd
        sys.stdout.flush()

    status = os.system(cmd)
    
    if verbose:
        local_file = FileLink(outfile)
        print "Done...  Check this file to see output:" 
        display(local_file)
    if readme_link:
        print "See the README.html file for links to input files..."
        display(FileLink('README.html'))
    

def make_exe(outfile=None, verbose=True):
    """Perform 'make .exe' and display link."""
    import os,sys
    
    if outfile is None:
        outfile='compile_output.txt'
    cmd = 'make .exe &> %s' % outfile

    if verbose:
        print "Compiling code... %s" % cmd
        sys.stdout.flush()

    status = os.system(cmd)
    
    if verbose:
        local_file = FileLink(outfile)
        print "Done...  Check this file to see output:" 
        display(local_file)
    
def make_output(outdir=None, outfile=None, verbose=True):
    """Perform 'make output' and display link."""
    import os,sys
    
    cmd = 'make output'
    if outdir is not None:
        cmd = cmd + ' OUTDIR=%s' % outdir
    if outfile is None:
        outfile = 'run_output.txt'
        cmd = cmd + ' &> %s' % outfile
    else:
        cmd = cmd + ' &> %s' % outfile
    if verbose:
        print "Running code... %s" % cmd
        sys.stdout.flush()
    status = os.system(cmd)
    
    if verbose:
        local_file = FileLink(outfile)
        print "Done... Check this file to see output:"
        display(local_file)
    
def make_plots(outdir=None, plotdir=None, outfile=None, verbose=True):
    """Perform 'make plots' and display links"""
    import os, sys

    cmd = 'make plots'
    if outdir is not None:
        cmd = cmd + ' OUTDIR=%s' % outdir

    if plotdir is None:
        plotdir = '_plots'
    else:
        cmd = cmd + ' PLOTDIR=%s' % plotdir

    if outfile is None:
        outfile = 'plot_output.txt'
        cmd = cmd + ' &> %s' % outfile
    else:
        cmd = cmd + ' &> %s' % outfile


    if verbose:
        print "Making plots... %s" % cmd
        sys.stdout.flush()

    status = os.system(cmd)
    
    if verbose:
        local_file = FileLink(outfile)
        print "Done... Check this file to see output:"
        display(local_file)
    
        index_file = FileLink('%s/_PlotIndex.html' % plotdir)
        print "View plots created at this link:"
        display(index_file)
    

def make_output_and_plots(label=None, verbose=True):

    import sys
    if label is None: 
        label = ''
    else:
        if label[0] != '_':
            label = '_' + label
    outdir = '_output%s' % str(label)
    outfile = 'run_output%s.txt' % str(label)
    make_output(outdir,outfile,verbose)

    plotdir = '_plots%s' % str(label)
    outfile = 'plot_output%s.txt' % str(label)
    make_plots(outdir,plotdir,outfile,verbose)
    return plotdir
