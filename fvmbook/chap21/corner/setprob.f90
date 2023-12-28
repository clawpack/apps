subroutine setprob
    ! Set parameters for shallow water equations, radial dam break

    implicit none

    integer :: iunit

    ! material parameters:
    real(kind=8) :: zl,cl,zr,cr
    common /comaux/ zl,cl,zr,cr


    iunit = 7
    call opendatafile(iunit, 'setprob.data')

    ! data for vc acoustics:
    read(7,*) zl
    read(7,*) cl
    read(7,*) zr
    read(7,*) cr

    close(iunit)

end subroutine setprob
