! =========================================================
subroutine rp1(maxmx,meqn,mwaves,maux,mbc,mx,ql,qr,auxl,auxr,fwave,s,amdq,apdq)
! =========================================================

! Solve Riemann problems for the 1D shallow water equations
! with topography source terms
!   (h)_t + (u h)_x = 0
!   (uh)_t + ( uuh + .5*gh^2 )_x = -ghB_x
! using Roe's approximate Riemann solver and the f-wave formulation
! to incorporate source terms

! fwaves: 2
! equations: 2

! Conserved quantities:
!       1 depth
!       2 momentum

! Auxiliary arrays:
!       1 topography/bathymetry B

! This function solves the Riemann problem at all interfaces in one call

! On input, ql contains the state vector at the left edge of each cell
!           qr contains the state vector at the right edge of each cell
! On output, fwave contains the fwaves,
!            s the speeds,
!            amdq the  left-going flux difference  A^- \Delta q
!            apdq the right-going flux difference  A^+ \Delta q

! Note that the i'th Riemann problem has left state qr(:,i-1)
!                                    and right state ql(:,i)
! From the basic clawpack routine step1, rp is called with ql = qr = q.


    implicit double precision (a-h,o-z)

    dimension   ql(meqn,           1-mbc:maxmx+mbc)
    dimension   qr(meqn,           1-mbc:maxmx+mbc)
    dimension    s(mwaves,         1-mbc:maxmx+mbc)
    dimension fwave(meqn,  mwaves, 1-mbc:maxmx+mbc)
    dimension amdq(meqn,           1-mbc:maxmx+mbc)
    dimension apdq(meqn,           1-mbc:maxmx+mbc)
    dimension auxl(maux,           1-mbc:maxmx+mbc)
    dimension auxr(maux,           1-mbc:maxmx+mbc)

!     # Gravity constant set in the setprob.f
    common /cparam/ grav

!     # Local storage
!     ---------------
    dimension delta(2)

!     # Main loop of the Riemann solver.
    do 30 i=2-mbc,mx+mbc
    
    
    !     # compute  Roe-averaged quantities:
        ubar = (qr(2,i-1)/dsqrt(qr(1,i-1)) + ql(2,i)/dsqrt(ql(1,i)))/ &
        ( dsqrt(qr(1,i-1)) + dsqrt(ql(1,i)) )
        cbar=dsqrt(0.5d0*grav*(qr(1,i-1) + ql(1,i)))
                 
    !     # jump in topography:

    !     # delta = flux difference + source
        delta(1) = ql(2,i) - qr(2,i-1)
        df = (ql(2,i)**2/ql(1,i) + 0.5d0*grav*ql(1,i)**2) - &
             (qr(2,i-1)**2/qr(1,i-1) + 0.5d0*grav*qr(1,i-1)**2) 
        dB = auxl(1,i) - auxr(1,i-1)
        delta(2) = df + 0.5d0*grav*(ql(1,i)+qr(1,i-1))*dB

    !     # Compute coeffs in the evector expansion of delta(1),delta(2)
        a1 = 0.5d0*(-delta(2) + (ubar + cbar) * delta(1))/cbar
        a2 = 0.5d0*( delta(2) - (ubar - cbar) * delta(1))/cbar

    !     # Finally, compute the waves.
        fwave(1,1,i) = a1
        fwave(2,1,i) = a1*(ubar - cbar)
        s(1,i) = ubar - cbar
                 
        fwave(1,2,i) = a2
        fwave(2,2,i) = a2*(ubar + cbar)
        s(2,i) = ubar + cbar
                 
    30 END DO


!     # No entropy fix
!     ----------------------------------------------
!     # amdq = SUM fwave   over left-going waves
!     # apdq = SUM fwave   over right-going waves

    do 100 m=1,2
        do 100 i=2-mbc, mx+mbc
            amdq(m,i) = 0.d0
            apdq(m,i) = 0.d0
            do 90 mw=1,mwaves
                if (s(mw,i) < 0.d0) then
                    amdq(m,i) = amdq(m,i) + fwave(m,mw,i)
                else
                    apdq(m,i) = apdq(m,i) + fwave(m,mw,i)
                endif
            90 END DO
    100 END DO

!    -----------------------------------------------
    return
    end subroutine rp1



