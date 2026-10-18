000010 01  REG-MOVTO.
000020     05  MV-NUM-CRED           PIC 9(10).
000030     05  MV-TIPO               PIC X(01).
000040         88  MV-ORDINARIO         VALUE 'I'.
000050         88  MV-MORATORIO         VALUE 'M'.
000060         88  MV-ORDEN             VALUE 'O'.
000070     05  MV-FECHA              PIC 9(08).
000080     05  MV-DIAS               PIC 9(03).
000090     05  MV-TASA-APLIC         PIC 9(03)V9999.
000100     05  MV-IMPORTE            PIC S9(11)V99.
000110     05  MV-SALDO-BASE         PIC S9(11)V99.
000120     05  FILLER                PIC X(25).
