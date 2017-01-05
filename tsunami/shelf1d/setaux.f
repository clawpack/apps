c     ============================================
      subroutine setaux(mbc,mx,xlower,dx,maux,aux)
c     ============================================
c
c     # set auxiliary arrays 
c     # aux(1,i) = B in cell i, bottom topography
c
c     
      implicit double precision (a-h,o-z)
      dimension aux(1,1-mbc:mx+mbc)
      common /ctopo/ Bocean, Bshelf, width, start

      open(unit=17,file='fort.H',status='unknown',form='formatted')
      pi = 4.d0*datan(1.d0)
c

      slope = (Bshelf - Bocean)/width
      do 50 i=1-mbc,mx+mbc
         xcell = xlower + (i-0.5d0)*dx
         aux(1,i) = Bocean
         if (xcell.gt.start) aux(1,i) = Bocean +(xcell-start)*slope
         if (xcell.gt.(start+width)) aux(1,i) = Bshelf
   50    continue

      do i=1,mx
         write(17,701) aux(1,i)
  701    format(e22.12)
         enddo

       close(17)
       return
       end

