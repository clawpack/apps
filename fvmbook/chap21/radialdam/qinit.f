
c
c
c
c     =====================================================
       subroutine qinit(meqn,mbc,mx,my,xlower,ylower,
     &                   dx,dy,q,maux,aux)
c     =====================================================
c
c     # Set initial conditions for q.
c     # Shallow water with radial dam break problem, h = hin inside
c     # circle specified in fdisc.f
c
       implicit double precision (a-h,o-z)
       dimension q(meqn,1-mbc:mx+mbc,1-mbc:my+mbc)
       common /comic/ hin,hout
c

       do 20 i=1,mx
          xlow = xlower + (i-1.d0)*dx
          do 20 j=1,my
             ylow = ylower + (j-1.d0)*dy
             call cellave(xlow,ylow,dx,dy,win)
             q(1,i,j) = hin*win + hout*(1.d0-win)
             q(2,i,j) = 0.d0
             q(3,i,j) = 0.d0
  20         continue
       return
       end

