subroutine src1(meqn,mbc,mx,xlower,dx,q,maux,aux,t,dt)

    ! Called to update q by solving source term equation 
    ! $q_t = \psi(q)$ over time dt starting at time t.
    !
    ! source terms for radial symmetry in shallow water equations
    ! Solve ODEs with 2-stage Runge-Kutta method
 
    implicit none

    integer, intent(in) :: mbc,mx,meqn,maux
    real(kind=8), intent(in) :: xlower,dx,t,dt
    real(kind=8), intent(in) ::  aux(maux,1-mbc:mx+mbc)
    real(kind=8), intent(inout) ::  q(meqn,1-mbc:mx+mbc)

    ! local variables
    integer :: i
    real(kind=8) :: xcell,qstar1,qstar2

    ! Gravity constant 
    real(kind=8) :: grav
    common /cparam/ grav


    do i=1,mx
        xcell = xlower + (i-0.5d0)*dx
        qstar1 = q(1,i) - 0.5d0*dt/xcell * q(2,i)
        qstar2 = q(2,i) - 0.5d0*dt/xcell * q(2,i)**2 / q(1,i)
        q(1,i) = q(1,i) - dt/xcell * qstar2
        q(2,i) = q(2,i) - dt/xcell * qstar2**2 / qstar1
    enddo


end subroutine src1
