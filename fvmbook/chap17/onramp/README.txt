

begin_html [use: jsMath] [use: doc/doc.css]
<!--   For a more readable version of this file, execute
                  unix>  make .htmls
       in this directory and then point your browser to README.html
     --------------------------------------------------------------  -->

<h2>
CLAWPACK Sample Code
</h2>

    
Traffic flow equations with a delta function source term representing
an on ramp at x=0.  This is implemented using the fractional step approach
in src1.f

Set D = 0.008 or 0.012 for Figure 17.6 in setprob.data
Example [book/chap17/onramp]
to accompany the book <br> &nbsp;&nbsp;
  [www.clawpack.org/book.html Finite Volume Methods for Hyperbolic Problems]
  by R. J. LeVeque.

Converted to [www.clawpack.org Clawpack 4.6] form in 2011.
        
<h4>
Plots of results
</h4>
After running this code and creating plots via "make .plots", you should be
able to view the plots in [link: _plots/_PlotIndex.html].


<h4>
Fortran files
</h4>

<dl>
<dt>[code: Makefile]
<dd> Determines which version of fortran files
are used when compiling the code with make and specifies where output and
plots should be directed.  Type "make .help" at the Unix prompt for options.

<dt>[code: driver.f]
<dd>
The driver routine allocates storage and then calls the main Clawpack
routine.

<dt>[code: setprob.f]
<dd>
A routine by this name is called by the library routine
[clawcode: clawpack/1d/lib/claw1ez.f]
and is generally used to set any values needed for the specific problem
being solved.
    
    
<dt>[code: rp1.f]
<dd>
This is the Riemann solver, which takes the $q$ values stored in the
arrays <tt>ql</tt> and <tt>qr</tt> and returns the waves in the array
<tt>wave</tt> and speeds in the array <tt>s</tt> that result in solving the
Riemann problem at each cell interface, and the fluctuations <tt>amdq</tt>
and <tt>apdq</tt>.  See [claw:doc/rp1.html] for more information about 1d
Riemann solvers.
         
<dt>[code: qinit.f]
<dd>
This subroutine sets the initial data at time $t=0$.

</dl>

<h4>
Python files
</h4>
<dl>

<dt>[code: setrun.py]
<dd> This file contains a function that
specifies what run-time parameters will be used.

Some parameters that you might want to modify are described in the
[www.clawpack.org/doc.html documentation].

<dt>[code: setplot.py]
<dd> This file contains a function that
specifies what plots will be done and
sets various plotting parameters.

</dl>


<h4>
Data files
</h4>
<font color='red'>Warning:</font> These files are generally changed
when setting up a run, usually in [code: setrun.py].

<dl>
<dt>[code: claw.data]
<dd> This file contains a number of
parameter values that are used by CLAWPACK.
The values in this file are read by the library routine
[clawcode: clawpack/1d/lib/claw1ez.f].


<dt> [code: setprob.data]
<dd> This file may contain various
parameters used in setting the initial conditions or otherwise setting up
the problem.


</dl>

<h4>Library routines</h3>

In addition to the Fortran routines in this library, several library
routines from [claw:clawpack/1d/lib] are used.  See the [code: Makefile]
to determine which ones are used.

end_html

    
