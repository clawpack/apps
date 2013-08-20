c
c
c =========================================================
       subroutine qinit(meqn,mbc,mx,xlower,dx,q,maux,aux)
c =========================================================
c
c     # Set initial conditions for q.
c     # Standing wave for the acoustics equations.
c
c
      implicit double precision (a-h,o-z)
      dimension q(meqn,1-mbc:mx+mbc)
      dimension aux(maux,1-mbc:mx+mbc)
      common /cqinit/ beta
c
c
      pi = 4.d0*datan(1.d0)
      do 150 i=1,mx
	 xcell = xlower + (i-0.5d0)*dx
	 q(1,i) = dcos(2.d0*pi*xcell)
	 q(2,i) = 0.d0
  150    continue
c
      return
      end

