
c
c
c     =====================================================
      subroutine rpn2(ixy,maxm,meqn,mwaves,maux, mbc,mx,ql,qr,
     &                  auxl,auxr,wave,s,amdq,apdq)
c     =====================================================
c
c     # Riemann solver for Burgers' equation in 2d:
c     #  u_t + cos(theta)*(0.5*u^2)_x + sin(theta)*(0.5*u^2)_y = 0
c     
c     # On input, ql contains the state vector at the left edge of each cell
c     #           qr contains the state vector at the right edge of each cell
c
c     # This data is along a slice in the x-direction if ixy=1 
c     #                            or the y-direction if ixy=2.
c     # On output, wave contains the waves,
c     #            s the speeds,
c     #            amdq the  left-going flux difference  A^- \Delta q
c     #            apdq the right-going flux difference  A^+ \Delta q
c
c     # Note that the i'th Riemann problem has left state qr(i-1,:)
c     #                                    and right state ql(i,:)
c     # From the basic clawpack routines, this routine is called with ql = qr
c
c
      implicit double precision (a-h,o-z)
c
      dimension wave(meqn, mwaves,1-mbc:maxm+mbc)
      dimension    s(mwaves, 1-mbc:maxm+mbc)
      dimension   ql(meqn, 1-mbc:maxm+mbc)
      dimension   qr(meqn, 1-mbc:maxm+mbc)
      dimension  apdq(meqn, 1-mbc:maxm+mbc)
      dimension  amdq(meqn, 1-mbc:maxm+mbc)
      logical efix
      common /comrp/ theta
c
c
      if (ixy .eq. 1) then
          a = 0.5d0*dcos(theta)
        else
          a = 0.5d0*dsin(theta)
        endif
c
      efix = .true.
c
      do 10 i = 2-mbc, mx+mbc
c        # wave is jump in q, speed comes from R-H condition:
         wave(1,1,i) = ql(1,i) - qr(1,i-1)
         s(1,i) = a*(qr(1,i-1) + ql(1,i))
c
c        # compute left-going and right-going flux differences:
c        ------------------------------------------------------
c
         amdq(1,i) = dmin1(s(1,i), 0.d0) * wave(1,1,i)
         apdq(1,i) = dmax1(s(1,i), 0.d0) * wave(1,1,i)
c
         if (efix) then
c           # entropy fix for transonic rarefactions:
            if (qr(1,i-1).lt.0.d0 .and. ql(1,i).gt.0.d0) then
               amdq(1,i) = - a*qr(1,i-1)**2
               apdq(1,i) =   a*ql(1,i)**2
               endif
            endif
   10   continue
c
      return
      end

