      subroutine setprob
      implicit double precision (a-h,o-z)
      character*12 fname
      common /cparam/ grav

      common/cdisc/ x0,y0,alf,beta,r0,idisc
      common /comic/ hin,hout
c
c
c
      iunit = 7
      fname = 'setprob.data'
c     # open the unit with new routine from Clawpack 4.4 to skip over
c     # comment lines starting with #:
      call opendatafile(iunit, fname)
c
c     # gravitational constant:
      read(7,*) grav

c     # data for radial dam-break problem:
      idisc = 2
      read(7,*) x0
      read(7,*) y0
      read(7,*) r0
      read(7,*) hin
      read(7,*) hout
c

      return
      end

