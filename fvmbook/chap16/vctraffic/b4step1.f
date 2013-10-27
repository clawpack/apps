c     ============================================
      subroutine b4step1(mbc,mx,meqn,q,
     &		  xlower,dx,t,dt,maux,aux)
c     ============================================
c
c     # called from claw1 before each call to step1.
c     # use to set time-dependent aux arrays or perform other tasks
c     # which must be done every time step.
c
c
c     
      implicit double precision (a-h,o-z)
      dimension q(meqn,1-mbc:mx+mbc)
      dimension aux(maux,1-mbc:mx+mbc)
      common /comlxf/ alxf

c     # coefficient needed in rp1lxf for Lax-Friedrichs:
      alxf = dx / dt
c
      return
      end

