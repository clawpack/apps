subroutine qinit(meqn,mbc,mx,my,xlower,ylower,dx,dy,q,maux,aux)

    ! Set initial conditions for the q array.

    ! Right-going plane wave in acoustics, assuming Z=1

    implicit none
    
    integer, intent(in) :: meqn,mbc,mx,my,maux
    real(kind=8), intent(in) :: xlower,ylower,dx,dy
    real(kind=8), intent(in) :: aux(maux,1-mbc:mx+mbc,1-mbc:my+mbc)
    real(kind=8), intent(inout) :: q(meqn,1-mbc:mx+mbc,1-mbc:my+mbc)

    ! local variables
    integer :: i,j
    real(kind=8) :: xi,yj


    do i=1,mx
        xi = xlower + (i-0.5d0)*dx
        do j=1,my
            yj = ylower + (j-0.5d0)*dy
            if (xi .gt. -0.35d0 .and. xi.lt.-0.2d0) then
                q(1,i,j) = 1.d0
            else
                q(1,i,j) = 0.d0
            endif
            q(2,i,j) = q(1,i,j)
            q(3,i,j) = 0.d0
        enddo
    enddo

end subroutine qinit
