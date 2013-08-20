c     ============================================
      subroutine setaux(mbc,mx,xlower,dx,maux,aux)
c     ============================================
c
c     # set auxiliary arrays 
c     # for traffic flow with variable speed limit umax stored in aux(1,i)
c
c     
      implicit double precision (a-h,o-z)
      dimension aux(maux,1-mbc:mx+mbc)
      common /cout/ umax(-1:20002)
c
      pi = 4.d0*datan(1.d0)
      do 150 i=1-mbc,mx+mbc
	 xcell = xlower + (i-0.5d0)*dx
	 if (xcell .lt. 0.d0) then
	     aux(1,i) = 2.0d0
	    else
	     aux(1,i) = 1.0d0
	    endif

c        # pass aux array to out1.f in order to plot velocities:
         umax(i) = aux(1,i)

  150    continue

       return
       end

