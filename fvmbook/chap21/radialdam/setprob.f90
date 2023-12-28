subroutine setprob
    ! Set parameters for shallow water equations, radial dam break

    implicit none

    integer :: iunit

    ! Gravity constant 
    real(kind=8) :: grav
    common /cparam/ grav

    ! initial h outside and inside:
    real(kind=8) :: hout,hin
    common /comic/ hin,hout

    ! location of dam:
    real(kind=8) :: r0
    common /cdisc/ r0

    iunit = 7
    call opendatafile(iunit, 'setprob.data')

    ! data for radial dam-break problem:
    read(7,*) grav
    read(7,*) r0
    read(7,*) hin
    read(7,*) hout

    close(iunit)

end subroutine setprob
