c
c
c =========================================================
       subroutine qinit(meqn,mbc,mx,xlower,dx,q,maux,aux)
c =========================================================
c
c     # Set initial conditions for q.
c
      implicit double precision (a-h,o-z)
      dimension q(1-mbc:mx+mbc, meqn)
      dimension aux(maux,1-mbc:mx+mbc)
c
c
      do 150 i=1,mx
	 xcell = xlower + (i-0.5d0)*dx
	 q(i,1) = 0.0
	 q(i,2) = 0.d0
  150    continue
c
      return
      end
