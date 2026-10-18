     HDATEDIT(*YMD) DFTACTGRP(*YES)
     FPEDCAB    UF   E           K DISK
     FPEDDET    IF   E           K DISK
     FCLIMAE    UF   E           K DISK
     FARTMAE    IF   E           K DISK
     FFACCAB    O    E           K DISK
     FFACDET    O    E           K DISK
     FPARAM     UF A E           K DISK
     FFAC010P   O    E             PRINTER OFLIND(*IN80)
      /COPY QRPGLESRC,FACCPY
     DWKYPED           S              7P 0
     C     *ENTRY        PLIST
     C                   PARM                    WMODO
     C                   EXSR      SRINIC
     C     *LOVAL        SETLL     PEDCAB
     C                   READ      PEDCAB                                 91
     C     *IN91         DOWEQ     *OFF
     C     PCESTA        IFEQ      'S'
     C                   EXSR      SRPEDI
     C                   ENDIF
     C                   READ      PEDCAB                                 91
     C                   ENDDO
     C                   EXSR      SRFINA
     C                   SETON                                        LR
     C                   RETURN
     C     SRINIC        BEGSR
     C     WMODO         IFEQ      *BLANK
     C                   MOVE      'N'           WMODO
     C                   ENDIF
     C                   Z-ADD     0             WCTFAC
     C                   Z-ADD     0             WCTRET
     C                   Z-ADD     0             WCTERR
     C                   Z-ADD     0             WGRTOT
     C     CPFOLI        CHAIN     PARAM                              90
     C     *IN90         IFEQ      *ON
     C                   Z-ADD     1             WFOLIO
     C                   ELSE
     C                   Z-ADD     PRVALN        WFOLIO
     C                   ENDIF
     C                   Z-ADD     WFOLIO        WFOLIN
     C     CPDIAG        CHAIN     PARAM                              90
     C     *IN90         IFEQ      *OFF
     C                   Z-ADD     PRVALN        WDIAGR
     C                   ENDIF
     C     CPPRMV        CHAIN     PARAM                              90
     C     *IN90         IFEQ      *OFF
     C                   Z-ADD     PRVALN        WPRMVI
     C                   ENDIF
     C                   WRITE     ENCABE
     C                   ENDSR
     C     SRPEDI        BEGSR
     C                   MOVE      'N'           WSWERR
     C     PCCLAV        CHAIN     CLIMAE                             90
     C     *IN90         IFEQ      *ON
     C                   EVAL      WMSGER = 'CLIENTE NO EXISTE ' + PCCLAV
     C                   EXSR      SRERRO
     C                   LEAVESR
     C                   ENDIF
     C     CLESTA        IFEQ      'B'
     C                   EVAL      WMSGER = 'CLIENTE DADO DE BAJA ' + PCCLAV
     C                   EXSR      SRERRO
     C                   UNLOCK    CLIMAE
     C                   LEAVESR
     C                   ENDIF
     C                   Z-ADD     0             WSUBTO
     C                   Z-ADD     0             WTODES
     C                   Z-ADD     0             WTOIVA
     C                   Z-ADD     0             WTOTAL
     C                   Z-ADD     0             WRENG
     C                   EXSR      SRPIEZ
     C                   Z-ADD     120           WLIM1
     C                   Z-ADD     600           WLIM2
     C     CLTIPO        IFEQ      'M'
     C     CLZONA        ANDEQ     'N'
     C                   Z-ADD     100           WLIM1
     C                   Z-ADD     500           WLIM2
     C                   ENDIF
     C                   Z-ADD     PCFECH        WFECHA
     C                   Z-ADD     WFMES         WMESP
     C                   ADD       1             WFOLIO
     C     PCNUMP        SETLL     PEDDET
     C     PCNUMP        READE     PEDDET                                 92
     C     *IN92         DOWEQ     *OFF
     C                   EXSR      SRLINE
     C     PCNUMP        READE     PEDDET                                 92
     C                   ENDDO
     C     WRENG         IFEQ      0
     C                   EVAL      WMSGER = 'PEDIDO SIN RENGLONES VALIDOS'
     C                   EXSR      SRERRO
     C                   SUB       1             WFOLIO
     C                   UNLOCK    CLIMAE
     C                   LEAVESR
     C                   ENDIF
     C                   EXSR      SRTOTA
     C                   EXSR      SRFECF
     C                   Z-ADD     WFOLIO        FCNUMF
     C                   Z-ADD     PCNUMP        FCNUMP
     C                   MOVE      PCCLAV        FCCLAV
     C                   Z-ADD     WFECHF        FCFECH
     C                   Z-ADD     WSUBTO        FCSUBT
     C                   Z-ADD     WTODES        FCDESC
     C                   Z-ADD     WTOIVA        FCIVA
     C                   Z-ADD     WTOTAL        FCTOTA
     C                   MOVE      WUSUAR        FCUSUA
     C                   MOVE      'A'           FCESTA
     C     CLCOND        IFEQ      'R'
     C     CLLIMC        ANDGT     0
     C                   IF        CLSALD + WTOTAL > CLLIMC
     C                   MOVE      'R'           FCESTA
     C                   ADD       1             WCTRET
     C                   ENDIF
     C                   ENDIF
     C     WMODO         IFNE      'S'
     C                   WRITE     FCAREG
     C                   ADD       WTOTAL        CLSALD
     C                   UPDATE    CLIREG
     C                   MOVE      'F'           PCESTA
     C                   Z-ADD     WFOLIO        PCNUMF
     C                   UPDATE    PCAREG
     C                   ELSE
     C                   UNLOCK    CLIMAE
     C                   ENDIF
     C                   ADD       1             WCTFAC
     C                   ADD       WTOTAL        WGRTOT
     C     *IN80         IFEQ      *ON
     C                   WRITE     ENCABE
     C                   SETOFF                                       80
     C                   ENDIF
     C                   WRITE     DETALL
     C                   ENDSR
     C     SRPIEZ        BEGSR
     C                   Z-ADD     0             WTOPZA
     C     PCNUMP        SETLL     PEDDET
     C     PCNUMP        READE     PEDDET                                 93
     C     *IN93         DOWEQ     *OFF
     C                   ADD       PDCANS        WTOPZA
     C     PCNUMP        READE     PEDDET                                 93
     C                   ENDDO
     C                   ENDSR
     C     SRLINE        BEGSR
     C     PDCANS        IFLE      0
     C                   LEAVESR
     C                   ENDIF
     C     PDARTI        CHAIN     ARTMAE                             94
     C     *IN94         IFEQ      *ON
     C                   EVAL      WMSGER = 'ARTICULO NO EXISTE ' + PDARTI
     C                   EXSR      SRERRO
     C                   LEAVESR
     C                   ENDIF
     C                   EVAL(H)   WIMPOR = PDCANS * ARPREC
     C                   Z-ADD     0             WPORCD
     C     CLTIPO        IFEQ      'M'
     C                   Z-ADD     WTOPZA        WBASPZ
     C                   ELSE
     C                   Z-ADD     PDCANS        WBASPZ
     C                   ENDIF
     C     WBASPZ        IFGE      WLIM2
     C                   Z-ADD     5.500         WPORCD
     C                   ELSE
     C     WBASPZ        IFGE      WLIM1
     C                   Z-ADD     3.000         WPORCD
     C                   ENDIF
     C                   ENDIF
     C     ARLINE        IFEQ      'MED'
     C     CLTIPO        IFEQ      'H'
     C                   Z-ADD     2.000         WPORCD
     C                   ELSE
     C                   Z-ADD     0             WPORCD
     C                   ENDIF
     C                   ENDIF
     C     CLTIPO        IFEQ      'E'
     C                   Z-ADD     10.000        WPORCD
     C                   ENDIF
     C     *IN77         IFEQ      *ON
     C                   Z-ADD     0             WPORCD
     C                   ENDIF
     C     WMESP         IFEQ      12
     C                   ADD       1.000         WPORCD
     C                   ENDIF
     C     WIMPOR        MULT      WPORCD        WTMP01
     C     WTMP01        DIV       100           WIMDES
     C     ARIVA         IFEQ      '0'
     C                   Z-ADD     0             WTASIV
     C                   ELSE
     C     CLZONA        IFEQ      'F'
     C                   Z-ADD     8             WTASIV
     C                   ELSE
     C                   Z-ADD     16            WTASIV
     C                   ENDIF
     C                   ENDIF
     C                   EVAL(H)   WIMIVA = (WIMPOR - WIMDES) * WTASIV / 100
     C                   ADD       WIMPOR        WSUBTO
     C                   ADD       WIMDES        WTODES
     C                   ADD       WIMIVA        WTOIVA
     C                   ADD       1             WRENG
     C     WMODO         IFNE      'S'
     C                   Z-ADD     WFOLIO        FDNUMF
     C                   Z-ADD     WRENG         FDRENG
     C                   MOVE      PDARTI        FDARTI
     C                   Z-ADD     PDCANS        FDCANT
     C                   Z-ADD     ARPREC        FDPREC
     C                   Z-ADD     WPORCD        FDPDES
     C                   Z-ADD     WIMDES        FDIMPD
     C                   Z-ADD     WIMPOR        FDIMPO
     C                   Z-ADD     WTASIV        FDTIVA
     C                   Z-ADD     WIMIVA        FDIVA
     C                   WRITE     FDEREG
     C                   ENDIF
     C                   ENDSR
     C     SRTOTA        BEGSR
     C                   EVAL      WTOTAL = WSUBTO - WTODES + WTOIVA
     C     CLCOND        IFEQ      'C'
     C                   EVAL(H)   WTMP02 = WTOTAL * 2
     C                   EVAL      WTOTAL = WTMP02 / 2
     C                   ENDIF
     C     WTOTAL        IFLT      0
     C                   Z-ADD     0             WTOTAL
     C                   ENDIF
     C                   ENDSR
     C     SRFECF        BEGSR
     C     UMONTH        IFEQ      1
     C     UDAY          ANDLE     5
     C                   EVAL      WANIOF = 2000 + UYEAR - 1
     C                   EVAL      WFECHF = WANIOF * 10000 + 1231
     C                   ELSE
     C                   EVAL      WANIOF = 2000 + UYEAR
     C                   EVAL      WFECHF = WANIOF * 10000 + UMONTH * 100 + UDAY
     C                   ENDIF
     C                   ENDSR
     C     SRERRO        BEGSR
     C                   MOVE      'S'           WSWERR
     C                   Z-ADD     PCNUMP        WPEDER
     C                   ADD       1             WCTERR
     C     *IN80         IFEQ      *ON
     C                   WRITE     ENCABE
     C                   SETOFF                                       80
     C                   ENDIF
     C                   WRITE     ERRLIN
     C                   ENDSR
     C     SRFINA        BEGSR
     C                   WRITE     TOTALE
     C     CPFOLI        CHAIN     PARAM                              90
     C     *IN90         IFEQ      *ON
     C                   MOVE      CPFOLI        PRCLAV
     C                   Z-ADD     WFOLIO        PRVALN
     C                   MOVE      *BLANKS       PRVALA
     C                   Z-ADD     *DATE         PRFMOD
     C                   WRITE     PARREG
     C                   ELSE
     C                   Z-ADD     WFOLIO        PRVALN
     C                   Z-ADD     *DATE         PRFMOD
     C                   UPDATE    PARREG
     C                   ENDIF
     C                   ENDSR
     C     SRCOMI        BEGSR
     C                   Z-ADD     0             WCOMIS
     C     CLVEND        IFNE      *BLANKS
     C     CLTIPO        ANDNE     'E'
     C                   EVAL(H)   WCOMIS = (WSUBTO - WTODES) * 1.5 / 100
     C     WPRMVI        IFGT      0
     C     WMESP         ANDEQ     12
     C                   EVAL(H)   WCOMIS = WCOMIS + WCOMIS * WPRMVI / 100
     C                   ENDIF
     C                   ENDIF
     C                   ENDSR
