subroutine qinit(meqn,mbc,mx,xlower,dx,q,maux,aux)

    ! Set initial conditions for the q array.
    ! This default version prints an error message since it should
    ! not be used directly.  Copy this to an application directory and
    ! loop over all grid cells to set values of q(1:meqn, 1:mx).

    implicit none
    
    integer, intent(in) :: meqn,mbc,mx,maux
    real(kind=8), intent(in) :: xlower,dx
    real(kind=8), intent(in) :: aux(maux,1-mbc:mx+mbc)
    real(kind=8), intent(inout) :: q(meqn,1-mbc:mx+mbc)

    ! local variables
    integer :: i
    real(kind=8) :: h,xcell

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
        xcell = xlower + (i-0.5d0)*dx
        if (xcell .lt. r0) then
            h = hin
        else
            h = hout
        endif
        q(1,i) = h
        q(2,i) = 0.d0
    enddo

end subroutine qinit
