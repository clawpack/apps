
c
c
c     =====================================================
      subroutine bc1(meqn,mbc,mx,xlower,dx,q,maux,aux,t,dt,mthbc)
c     =====================================================
c
c     # Standard boundary condition choices for claw2
c
c     # At each boundary  k = 1 (left),  2 (right):
c     #   mthbc(k) =  0  for user-supplied BC's (must be inserted!)
c     #            =  1  for zero-order extrapolation
c     #            =  2  for periodic boundary coniditions
c     #            =  3  for solid walls, assuming this can be implemented
c     #                  by reflecting the data about the boundary and then
c     #                  negating the 2'nd component of q.
c     ------------------------------------------------
c
c     # Extend the data from the computational region
c     #      i = 1, 2, ..., mx2
c     # to the virtual cells outside the region, with
c     #      i = 1-ibc  and   i = mx+ibc   for ibc=1,...,mbc
c
      implicit double precision (a-h,o-z)
      dimension q(meqn,1-mbc:mx+mbc)
      dimension aux(maux,1-mbc:mx+mbc)

      dimension mthbc(2)

      common /cparam/ rho,bulk,cc,zz
      common /combc/ omega
   

c
c
c-------------------------------------------------------
c     # left boundary:
c-------------------------------------------------------
      go to (100,110,120,130) mthbc(1)+1
c
  100 continue
c     # incoming sine wave

c     # strength of 1-wave (extrapolate the outgoing wave):
      w1 = (-q(1,1) + zz*q(2,1)) / (2.d0*zz)

c     # strength of 2-wave (specify the incoming wave):
      if (omega*t .le. 8.d0*datan(1.d0)) then
           w2 = 0.5d0 * dsin(omega*t) 
	else
	   w2 = 0.d0
	endif

      do 105 ibc=1,mbc
         q(1,1-ibc) = -w1*zz + w2*zz
         q(2,1-ibc) = w1 + w2
  105    continue
      go to 199

c
  110 continue
c     # zero-order extrapolation:
      do 115 m=1,meqn
         do 115 ibc=1,mbc
               q(m,1-ibc) = q(m,1)
  115       continue
      go to 199

  120 continue
c     # periodic:  
      do 125 m=1,meqn
         do 125 ibc=1,mbc
               q(m,1-ibc) = q(m,mx+1-ibc)
  125       continue
      go to 199

  130 continue
c     # solid wall (assumes 2'nd component is velocity or momentum in x):
      do 135 m=1,meqn
         do 135 ibc=1,mbc
               q(m,1-ibc) = q(m,ibc)
  135       continue
c     # negate the normal velocity:
      do 136 ibc=1,mbc
            q(2,1-ibc) = -q(2,ibc)
  136    continue
      go to 199

  199 continue

c
c-------------------------------------------------------
c     # right boundary:
c-------------------------------------------------------
      go to (200,210,220,230) mthbc(2)+1
c
  200 continue
c     # user-specified boundary conditions go here in place of error output
      write(6,*) '*** ERROR *** mthbc(2)=0 and no BCs specified in bc2'
      stop
      go to 299

  210 continue
c     # zero-order extrapolation:
      do 215 m=1,meqn
         do 215 ibc=1,mbc
               q(m,mx+ibc) = q(m,mx)
  215       continue
      go to 299

  220 continue
c     # periodic:  
      do 225 m=1,meqn
         do 225 ibc=1,mbc
               q(m,mx+ibc) = q(m,ibc)
  225       continue
      go to 299

  230 continue
c     # solid wall (assumes 2'nd component is velocity or momentum in x):
      do 235 m=1,meqn
         do 235 ibc=1,mbc
               q(m,mx+ibc) = q(m,mx+1-ibc)
  235       continue
      do 236 ibc=1,mbc
            q(2,mx+ibc) = -q(2,mx+1-ibc)
  236    continue
      go to 299

  299 continue
c
      return
      end

