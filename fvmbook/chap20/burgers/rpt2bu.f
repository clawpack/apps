c
c
c     =====================================================
      subroutine rpt2(ixy,maxm,meqn,mwaves,mbc,mx,
     &                  ql,qr,aux1,aux2,aux3,
     &                  imp,asdq,bmasdq,bpasdq,num_aux)
c     =====================================================
      implicit double precision (a-h,o-z)
c
c     # Riemann solver in the transverse direction for 2D Burgers' equation
c     #  u_t + cos(theta)*(0.5*u^2)_x + sin(theta)*(0.5*u^2)_y = 0
c
c     # Split asdq into eigenvectors of Roe matrix B.
c     # For the scalar equation, this simply amounts to computing the
c     # transverse wave speed from the opposite Riemann problem.
c
      dimension    ql(meqn, 1-mbc:maxm+mbc)
      dimension    qr(meqn, 1-mbc:maxm+mbc)
      dimension   asdq(meqn, 1-mbc:maxm+mbc)
      dimension bmasdq(meqn, 1-mbc:maxm+mbc)
      dimension bpasdq(meqn, 1-mbc:maxm+mbc)
      common /comrp/ theta
c
      if (ixy .eq. 1) then
          b = 0.5d0*dsin(theta)
        else
          b = 0.5d0*dcos(theta)
        endif
c
          do 10 i = 2-mbc, mx+mbc
             sb = b*(qr(1,i-1) + ql(1,i))
             bmasdq(1,i) = dmin1(sb, 0.d0) * asdq(1,i)
             bpasdq(1,i) = dmax1(sb, 0.d0) * asdq(1,i)
   10        continue
c
      return
      end

