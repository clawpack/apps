
def output_link(fname='output.txt'):
    """Display a link to file where system call output is saved"""
    from IPython.display import FileLink
    from IPython.core.display import display
    local_file = FileLink(fname)
    print "Check this file to see results from running code:"
    display(local_file)

def run_and_make_plots(label=None,verbose=True):
    import os
    from IPython.display import FileLink
    from IPython.core.display import display
    if label is None: 
        label = ''
    else:
        if label[0] != '_':
            label = '_' + label
    outdir = '_output%s' % str(label)
    plotdir = '_plots%s' % str(label)
    outfile = 'output%s.txt' % str(label)
    os.system('make output OUTDIR=%s > %s' % (outdir,outfile))
    os.system('make plots OUTDIR=%s PLOTDIR=%s >> %s' % (outdir,plotdir,outfile))
    if verbose:
        print "Output in %s and plots in %s" % (outdir,plotdir)
        output_link(outfile)
        index_file = FileLink('%s/_PlotIndex.html' % plotdir)
        print "View all plots created at this link:"
        display(index_file)

    return plotdir

