      subroutine setprob
      implicit double precision (a-h,o-z)
      character*12 fname
      common /cparam/ grav
      common /comeps/ eps
      common /ctopo/ Bocean, Bshelf, width, start
c
c     # Shallow water equations
c
c
      iunit = 7
      fname = 'setprob.data'
c     # open the unit with new routine from Clawpack 4.4 to skip over
c     # comment lines starting with #:
      call opendatafile(iunit, fname)
                

c     # Graviational constant g:
      grav = 9.81d0
c
c     # initial data has pulse of height eps
      read(7,*) eps

c     # topography data:
      read(7,*) Bocean
      read(7,*) Bshelf
      read(7,*) width
      read(7,*) start

      return
      end

