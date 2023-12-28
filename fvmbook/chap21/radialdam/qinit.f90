subroutine qinit(meqn,mbc,mx,my,xlower,ylower,dx,dy,q,maux,aux)

    ! Set initial conditions for the q array.
    ! This default version prints an error message since it should
    ! not be used directly.  Copy this to an application directory and
    ! loop over all grid cells to set values of q(1:meqn, 1:mx, 1:my).

    implicit none
    
    integer, intent(in) :: meqn,mbc,mx,my,maux
    real(kind=8), intent(in) :: xlower,ylower,dx,dy
    real(kind=8), intent(in) :: aux(maux,1-mbc:mx+mbc,1-mbc:my+mbc)
    real(kind=8), intent(inout) :: q(meqn,1-mbc:mx+mbc,1-mbc:my+mbc)

    ! local variables
    integer :: i,j
    real(kind=8) :: h,xlow,ylow,win

    ! Gravity constant 
    real(kind=8) :: grav
    ! initial h outside and inside:
    real(kind=8) :: hout,hin
    ! location of dam:
    real(kind=8) :: r0

    ! these are set in setprob:
    common /cparam/ grav
    common /comic/ hin,hout
    common /cdisc/ r0

    do i=1,mx
        xlow = xlower + (i-1.d0)*dx
        do j=1,my
            ylow = ylower + (j-1.d0)*dy
            call cellave(xlow,ylow,dx,dy,win)
            q(1,i,j) = hin*win + hout*(1.d0-win)
            q(2,i,j) = 0.d0
            q(3,i,j) = 0.d0
        enddo
    enddo

end subroutine qinit
