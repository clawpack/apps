subroutine setaux(mbc,mx,my,xlower,ylower,dx,dy,maux,aux)

    ! Called at start of computation before calling qinit, and
    ! when AMR is used, also called every time a new grid patch is created.
    ! Use to set auxiliary arrays aux(1,1:maux, 1-mbc:mx+mbc, 1-mbc:my+mbc).
    ! Note that ghost cell values may need to be set if the aux arrays
    ! are used by the Riemann solver(s).
    !
    ! For variable-coefficient acoustics in a heterogeneous medium
 
    implicit none
    integer, intent(in) :: mbc,mx,my,maux
    real(kind=8), intent(in) :: xlower,ylower,dx,dy
    real(kind=8), intent(inout) ::  aux(1:maux,1-mbc:mx+mbc,1-mbc:my+mbc)

    ! local variables:
    integer :: i,j
    real(kind=8) :: rhol,rhor,bulkl,bulkr,wl,wr,xl,yl,rho,bulk

    ! global variables:
    real(kind=8) :: zl,cl,zr,cr
    common /comaux/ zl,cl,zr,cr

    ! density and bulk moduli:
    rhol = zl/cl
    rhor = zr/cr
    bulkl = cl**2 * rhol
    bulkr = cr**2 * rhor

    do j=1-mbc,my+mbc
        do i=1-mbc,mx+mbc
            xl = xlower + (i-1.0d0)*dx
            yl = ylower + (j-1.0d0)*dy

            ! determine what fraction wl of this cell lies to the 
            ! "left" of the interface:
            call cellave(xl,yl,dx,dy,wl)
            wr = 1.d0 - wl

            ! average density:
            rho = wl*rhol + wr*rhor

            ! harmonic average bulk modulus:
            bulk = 1.d0 / (wl/bulkl + wr/bulkr)

            ! average sound speed:
            aux(2,i,j) = dsqrt(bulk/rho)

            ! average impedance:
            aux(1,i,j) = rho*aux(2,i,j)
        enddo
    enddo

end subroutine setaux
