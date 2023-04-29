

c
c
c =========================================================
      subroutine src1(meqn,mbc,mx,xlower,dx,q,maux,aux,t,dt)
c =========================================================
      implicit real*8(a-h,o-z)
      dimension q(meqn,1-mbc:mx+mbc)
c
      common /comsrc/ ndim
c
c     # source terms for radial symmetry in shallow water equations
c
c     # ndim should be set in setprob.f
c     # ndim = 2  for cylindrical symmetry
c     # ndim = 3  for spherical symmetry
c
c     # 2-stage Runge-Kutta method
c
c     do i=-1,3
c        write(6,*) 'i, q(1,i), q(2,i): ',i, q(1,i), q(2,i)
c        enddo 

      do 10 i=1,mx+mbc
         xcell = xlower + (i-0.5d0)*dx
         qstar1 = q(1,i) - 0.5d0*dt*(ndim-1)/xcell * q(2,i)
         qstar2 = q(2,i) - 0.5d0*dt*(ndim-1)/xcell * q(2,i)**2 / q(1,i)
c
         q(1,i) = q(1,i) - dt*(ndim-1)/xcell * qstar2
         q(2,i) = q(2,i) - dt*(ndim-1)/xcell * qstar2**2 / qstar1
   10    continue
c
      return
      end

