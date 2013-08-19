c
c
c =========================================================
       subroutine qinit(meqn,mbc,mx,xlower,dx,q,maux,aux)
c =========================================================
c
c     # Set initial conditions for q.
c
c
      implicit double precision (a-h,o-z)
      dimension q(meqn,1-mbc:mx+mbc)
      dimension aux(maux,1-mbc:mx+mbc)
      common /comic/ q0
c
c
      do 150 i=1,mx
	 xcell = xlower + (i-0.5d0)*dx
	 if (xcell .lt. 0.d0) then
	     q(1,i) = q0
	   else
	     q(1,i) = q0
	   endif
  150    continue
c
      return
      end

