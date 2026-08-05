```{=html}
<!-- Page 1 -->
```
Standard ECMA-48 Fi ft h Edi tion - June 1991 Repri nted June 1998

Standardizing Inform ation and Com m unication System s

Control Functions for Coded Character Sets

Phone: +41 22 849.60.00 - Fax: +41 22 849.60.01 - URL: h ttp://www.
ecma.ch - Internet: helpdesk@ecma.ch

```{=html}
<!-- Page 2 -->
```
.

```{=html}
<!-- Page 3 -->
```
Standard ECMA-48 June 1991

Standardizing Inform ation and Com m unication System s

Control Functions for Coded Character Sets

Phone: +41 22 849.60.00 - Fax: +41 22 849.60.01 - URL: h ttp://www.
ecma.ch - Internet: helpdesk@ecma.ch IW ECMA-048.doc 21-01-03 16,29

```{=html}
<!-- Page 4 -->
```
.

```{=html}
<!-- Page 5 -->
```
Brief History

As part of the work on coded charact er set standards, TC 1, t he codi
ng com mittee of EC MA, worked on t he defi nition and the coding of
control funct ions t o be used wi th the various st andards for coded
graphi c charact er set s produced by\
ECMA, viz. EC MA-6, EC MA-94, EC MA-113, EC MA-114, EC MA-118, EC
MA-121, EC MA-128, and EC MA-144. The first edition of this Standard EC
MA-48 was published in 1976. Further ed itions followed. The fourth
edition, published in 1986 was adopted by ISO/ IEC under the fast-track
procedure as second edition of ISO 6429. It constitutes a repertoire of
a large n umber o f co ntrol fu nctions th e d efinitions an d co ded
rep resentatio ns of wh ich are thus standardized. For each a pplication
the required selecti on of control functions can be made from this
repertoire. This fifth edi tion of St andard EC MA-48 cont ains t he
control funct ions al ready standardi zed i n the fourt h edi tion and,
in ad dition, n ew co ntrol fu nctions n eeded fo r h andling b
i-directio nal tex ts, i.e. tex ts co mprisin g p arts written with a
left-to -right scrip t an d p arts written with a rig ht-to-left scrip
t. ECMA Tech nical Rep ort TR/5 3 g ives fu rther information and exam
ples of handl ing such t exts. The i nclusion of these speci alized cont
rol funct ions has requi red a corresponding adjustm ent of the
definitions of som e of the other control functions. Moreover, the
concept of "device" had t o be revi sed. This fifth edition has been c
ontributed to ISO/IEC for a doption under the fast-track procedure as
third edition of ISO/IEC 6429.

Adopt ed by the General Assem bly of EC MA on 13t h June 1991.

```{=html}
<!-- Page 6 -->
```
```{=html}
<!-- Page 7 -->
```
-   i - . Table of contents 1 Scope 1 2 Conformance 1 2.1 Ty pes of
    conform ance 1 2.2 C onform ance of i nform ation i nterchange 1 2.3
    C onform ance of devi ces 1 2.3.1 Devi ce descri ption 1 2.3.2 Ori
    ginating devi ces 2 2.3.3 Receiving devices 2 3 References 2 4
    Notation and definitions 3 4.1 Not ation 3 4.2 Defi nitions 3 4.2.1
    Active area 3 4.2.2 Act ive fi eld 3 4.2.3 Act ive l ine 3 4.2.4 Act
    ive page 3 4.2.5 Act ive dat a posi tion 3 4.2.6 Act ive present
    ation posi tion 3 4.2.7 Area 3 4.2.8 Au xiliary d evice 3 4.2.9 B
    i-di rect ional dat a 3 4.2.10 B it com bination 3 4.2.11 B yte 4
    4.2.12 To cancel 4 4.2.13 C haract er 4 4.2.14 C haract er-i maging
    devi ce 4 4.2.15 C haract er pat h 4 4.2.16 C haract er posi tion 4
    4.2.17 C haract er progressi on 4 4.2.18 To cl ear 4 4.2.19 C oded
    charact er set ; code 4 4.2.20 Coded-character-data-el ement (CC-d
    ata-elem ent) 4 4.2.21 C ode ext ensi on 4 4.2.22 C ode t able 4
    4.2.23 C ont rol charact er 4 4.2.24 C ont rol funct ion 4 4.2.25 C
    ont rol sequence 5 4.2.26 C ont rol st ring 5 4.2.27 C ursor 5
    4.2.28 Dat a com ponent 5 4.2.29 Deci mal mark 5 4.2.30 Defaul t 5
    4.2.31 To del ete 5 4.2.32 To desi gnat e 5 4.2.33 Devi ce 5 4.2.34
    Di spl ay 5 4.2.35 Edi tor funct ion 5 4.2.36 El igible 5 4.2.37
    Envi ronm ent 5

```{=html}
<!-- Page 8 -->
```
-   ii - 4.2.38 To erase 5 4.2.39 Escape sequence 5 4.2.40 Fi eld 5
    4.2.41 Fi nal Byte 6 4.2.42 Form ator funct ion 6 4.2.43 Graphic
    character 6 4.2.44 Graphi c rendi tion 6 4.2.45 Graphi c sy mbol 6
    4.2.46 Guarded area 6 4.2.47 In itial state 6 4.2.48 In term ediate
    Byte 6 4.2.49 To i nvoke 6 4.2.50 Li ne 6 4.2.51 Li ne hom e posi
    tion 6 4.2.52 Li ne l imit posi tion 6 4.2.53 Li ne ori entation 6
    4.2.54 Li ne progressi on 6 4.2.55 Operat ing sy stem 7 4.2.56 Page
    7 4.2.57 Page hom e posi tion 7 4.2.58 Page l imit posi tion 7
    4.2.59 Param eter B yte 7 4.2.60 Present ation com ponent 7 4.2.61
    Pri vate (or experi mental) use 7 4.2.62 Protected area 7 4.2.63
    Qual ified area 7 4.2.64 R epert oire 7 4.2.65 Scrol l 7 4.2.66
    Selected area 7 4.2.67 Tabul ation 7 4.2.68 Tabul ation st op 7
    4.2.69 User 7 5 Coded representation 8 5.1 General 8 5.2 El ement s
    of t he C 0 set 8 5.3 El ement s of t he C 1 set 8 5.4 C ont rol
    sequences 10 5.4.1 Param eter represent ation 11 5.4.2 Param eter
    string form at 12 5.4.3 Ty pes of param eters 12 5.5 Independent
    cont rol funct ions 12 5.6 C ont rol st rings 13 6 Device concepts
    13 6.1 C omponent s 14 6.1.1 Present ation com ponent 14 6.1.2 The
    act ive present ation posi tion 15 6.1.3 Dat a com ponent 15 6.1.4
    The act ive dat a posi tion 15 6.1.5 R elationshi p bet ween act ive
    dat a posi tion and act ive present ation posi tion 15 6.1.6 Im
    plicit movem ent 16 6.1.7 Expl icit movem ent 17 6.1.8 Indi rect
    movem ent 17 6.2 The dat a st ream 17

```{=html}
<!-- Page 9 -->
```
-   iii - 6.2.1 Dat a organi zat ion 17 6.3 The graphi c i mage out put
    18 6.4 Form ator funct ions and edi tor funct ions 18 6.4.1 Form
    ator funct ions 18 6.4.2 C omposi te graphi c charact ers 18 6.4.3
    Edi tor funct ions 18 6.5 Sel ect ed and qual ified areas 18 6.5.1
    Selected areas 19 6.5.2 Qual ified areas 19 6.6 Auxiliary inpu
    t/output devices 20 6.7 Tabul ation and fi elds 20 7 Modes 20 7.1
    The concept of m odes 20 7.2 Defi nition of m odes 20 7.2.1 BDSM -
    BI-DIRECTIONAL SUPPORT M ODE 21 7.2.2 CRM - CONTROL REPRESENTATION
    MODE 22 7.2.3 DCSM - DEVICE COMPONENT SELECT MODE 22 7.2.4 ER M - ER
    ASUR E M ODE 22 7.2.5 FEAM - FORM AT EFFECTOR ACTION M ODE 22 7.2.6
    FETM - FOR MAT E FFECTOR TRANSFER M ODE 22 7.2.7 GATM - GUARDED AREA
    TRANSFER M ODE 23 7.2.8 GRCM - GRAPHIC RENDITION COM BINATION M ODE
    23 7.2.9 HEM - CHARACTER EDITING M ODE 23 7.2.10 IR M - INSER TION R
    EPLAC EMENT M ODE 24 7.2.11 KAM - KEYBOARD ACTION M ODE 24 7.2.12
    MATM - MULTIPLE AREA TRANSFER MODE 24 7.2.13 PUM - POSITIONING UNIT
    M ODE 24 7.2.14 SATM - SELECTED AREA TRANSFER MODE 24 7.2.15 SR M -
    SEND/ RECEIVE M ODE 24 7.2.16 SR TM - STATUS R EPOR T TR ANSFER MODE
    24 7.2.17 TSM - TAB ULATION STOP M ODE 25 7.2.18 TTM - TRANSFER TERM
    INATION M ODE 25 7.2.19 VEM - LINE EDITING M ODE 25 7.2.20 ZDM - ZER
    O DEFAULT M ODE 25 7.3 Int eract ion bet ween m odes 26 7.3.1
    GUARDED AREA TRANSFER M ODE ( GATM ), MULTIPLE AREA TRANSFER M ODE
    (MATM), SELECTED AREA TRANSFER MODE (SATM), and TRANSFER TERMINATION
    MODE (TTM ) 26 7.3.2 CONTROL REPRESENTATION MODE (CRM ) and FORM AT
    EFFECTOR ACTION MODE (FEAM ) 26 7.3.3 CHARACTER EDITING M ODE (HEM )
    a nd INSERTION REPLACEM ENT M ODE (IRM ) 26 7.3.4 BI-DIRECTIONAL
    SUPPORT MODE (BDSM) and DEVICE COMPONENT SELECT MODE (DCSM ) 27 7.4
    Pri vate m odes 27 8 Control functions 27 8.1 Ty pes of cont rol
    funct ions 27 8.2 C ategori es of cont rol funct ions 28 8.2.1 Del
    imiters 28 8.2.2 Int roducers 28 8.2.3 Shi ft funct ions 28 8.2.4
    Form at effect ors 28 8.2.5 Present ation cont rol funct ions 29

```{=html}
<!-- Page 10 -->
```
-   iv - 8.2.6 Edi tor funct ions 30 8.2.7 C ursor cont rol funct ions
    31 8.2.8 Di spl ay cont rol funct ions 31 8.2.9 Devi ce cont rol
    funct ions 31 8.2.10 Inform ation separat ors 31 8.2.11 Area defi
    nition 32 8.2.12 M ode set ting 32 8.2.13 Transm issi on cont rol
    funct ions 32 8.2.14 M iscel laneous cont rol funct ions 32 8.3 Defi
    nition of cont rol funct ions 33 8.3.1 ACK - ACKNOW LEDGE 33 8.3.2
    APC - APPLICATION PROGRAM COM MAND 33 8.3.3 BEL - BELL 33 8.3.4
    BPH - BREAK PERMITTED HERE 33 8.3.5 BS - BACKSPACE 34 8.3.6 C AN - C
    ANC EL 34 8.3.7 CBT - CURSOR BACKW ARD TABULATION 34 8.3.8 C CH - C
    ANC EL C HAR ACTER 34 8.3.9 C HA - C URSOR CHARACTER ABSOLUTE 34
    8.3.10 CHT - CURSOR FORW ARD TABULATION 34 8.3.11 CM D - CODING M
    ETHOD DELIM ITER 34 8.3.12 C NL - C URSOR NEXT LINE 35 8.3.13 C PL -
    C URSOR PR ECEDING LINE 35 8.3.14 C PR - AC TIVE POSITION R EPOR T
    35 8.3.15 CR - CARRIAGE RETURN 35 8.3.16 CSI - CONTROL SEQUENCE
    INTRODUCER 36 8.3.17 CTC - CURSOR TABULATION CONTROL 36 8.3.18 CUB -
    CURSOR LEFT 36 8.3.19 CUD - CURSOR DOW N 36 8.3.20 C UF - C URSOR
    RIGHT 36 8.3.21 C UP - C URSOR POSITION 36 8.3.22 C UU - C URSOR UP
    37 8.3.23 CVT - CURSOR LINE TABULATION 37 8.3.24 DA - DEVIC E ATTR
    IBUTES 37 8.3.25 DAQ - DEFINE AREA QUALIFICATION 37 8.3.26 DCH -
    DELETE CHARACTER 38 8.3.27 DCS - DEVICE CONTROL STRING 38 8.3.28
    DC1 - DEVICE CONTROL ONE 38 8.3.29 DC 2 - DEVIC E CONTR OL TW O 38
    8.3.30 DC 3 - DEVIC E CONTR OL THR EE 39 8.3.31 DC4 - DEVICE CONTROL
    FOUR 39 8.3.32 DL - DELETE LINE 39 8.3.33 DLE - DATA LINK ESC APE 39
    8.3.34 DM I - DISABLE M ANUAL INPUT 39 8.3.35 DSR - DEVICE STATUS
    REPORT 40 8.3.36 DTA - DIM ENSION TEXT AREA 40 8.3.37 EA - ERASE IN
    AREA 40 8.3.38 EC H - ER ASE C HAR ACTER 41 8.3.39 ED - ER ASE IN
    PAGE 41 8.3.40 EF - ERASE IN FIELD 41 8.3.41 EL - ERASE IN LINE 42
    8.3.42 EM - END OF M EDIUM 42 8.3.43 EM I - ENABLE M ANUAL INPUT 42
    8.3.44 ENQ - ENQUIRY 43 8.3.45 EOT - END OF TRANSM ISSION 43 8.3.46
    EPA - END OF GUARDED AREA 43 8.3.47 ESA - END OF SELECTED AREA 43

```{=html}
<!-- Page 11 -->
```
-   v - 8.3.48 ESC - ESC APE 43 8.3.49 ETB - END OF TRANSM ISSION BLOCK
    43 8.3.50 ETX - END OF TEXT 43 8.3.51 FF - FOR M FEED 44 8.3.52
    FNK - FUNCTION KEY 44 8.3.53 FNT - FONT SELECTION 44 8.3.54 GCC -
    GRAPHIC CHARACTER COM BINATION 44 8.3.55 GSM - GRAPHIC SIZE M
    ODIFICATION 45 8.3.56 GSS - GRAPHIC SIZE SELECTION 45 8.3.57 HPA -
    CHARACTER POSITION ABSOLUTE 45 8.3.58 HPB - CHARACTER POSITION BACKW
    ARD 45 8.3.59 HPR - CHARACTER POSITION FORW ARD 45 8.3.60 HT -
    CHARACTER TABULATION 45 8.3.61 HTJ - C HAR ACTER TAB ULATION W ITH
    JUSTIFICATION 46 8.3.62 HTS - CHARACTER TABULATION SET 46 8.3.63
    HVP - CHARACTER AND LINE POSITION 46 8.3.64 IC H - INSER T CHAR
    ACTER 46 8.3.65 IDCS - IDENTIFY DEVICE CONTROL STRING 47 8.3.66
    IGS - IDENTIFY GR APHIC SUB REPER TOIR E 47 8.3.67 IL - INSER T LINE
    47 8.3.68 INT - INTER RUPT 48 8.3.69 IS1 - INFORMATION SEPARATOR ONE
    (US - UNIT SEPARATOR) 48 8.3.70 IS2 - INFOR MATION SEPAR ATOR TWO
    (RS - RECORD SEPARATOR) 48 8.3.71 IS3 - INFORMATION SEPARATOR THREE
    (GS - GROUP SEPARATOR) 48 8.3.72 IS4 - INFORMATION SEPARATOR FOUR
    (FS - FILE SEPARATOR) 48 8.3.73 JFY - JUSTIFY 48 8.3.74 LF - LINE
    FEED 49 8.3.75 LS0 - LOC KING-SHIFT ZER O 49 8.3.76 LS1 - LOC
    KING-SHIFT ONE 49 8.3.77 LS1R - LOC KING-SHIFT ONE R IGHT 49 8.3.78
    LS2 - LOC KING-SHIFT TW O 49 8.3.79 LS2R - LOC KING-SHIFT TW O R
    IGHT 49 8.3.80 LS3 - LOC KING-SHIFT THR EE 50 8.3.81 LS3R - LOC
    KING-SHIFT THR EE R IGHT 50 8.3.82 M C - M EDIA C OPY 50 8.3.83 M
    W - M ESSAGE W AITING 50 8.3.84 NAK - NEGATIVE ACKNOW LEDGE 50
    8.3.85 NBH - NO BREAK HERE 50 8.3.86 NEL - NEXT LINE 51 8.3.87 NP -
    NEXT PAGE 51 8.3.88 NUL - NULL 51 8.3.89 OSC - OPERATING SYSTEM COM
    MAND 51 8.3.90 PEC - PRESENTATION EXPAND OR CONTRACT 51 8.3.91 PFS -
    PAGE FORMAT SELECTION 52 8.3.92 PLD - PAR TIAL LINE FOR WARD 52
    8.3.93 PLU - PAR TIAL LINE B ACKWARD 53 8.3.94 PM - PR IVAC Y M
    ESSAGE 53 8.3.95 PP - PR ECEDING PAGE 53 8.3.96 PPA - PAGE POSITION
    ABSOLUTE 53 8.3.97 PPB - PAGE POSITION B ACKWARD 53 8.3.98 PPR -
    PAGE POSITION FORW ARD 53 8.3.99 PTX - PARALLEL TEXTS 53 8.3.100
    PU1 - PR IVATE USE ONE 54 8.3.101 PU2 - PR IVATE USE TW O 54 8.3.102
    QUAD - QUAD 55 8.3.103 R EP - R EPEAT 55 8.3.104 R I - R EVER SE
    LINE FEED 55 8.3.105 R IS - R ESET TO INITIAL STATE 55

```{=html}
<!-- Page 12 -->
```
-   vi - 8.3.106 R M - R ESET M ODE 56 8.3.107 SACS - SET ADDITIONAL
    CHARACTER SEPARATION 56 8.3.108 SAPV - SELECT ALTERNATIVE
    PRESENTATION VARIANTS 57 8.3.109 SCI - SINGLE C HARACTER INTRODUCER
    58 8.3.110 SCO - SELECT CHAR ACTER ORIENTATION 58 8.3.111 SCP -
    SELECT CHARACTER PATH 58 8.3.112 SC S - SET C HAR ACTER SPAC ING 59
    8.3.113 SD - SC ROLL DOW N 59 8.3.114 SDS - STAR T DIR ECTED STR ING
    59 8.3.115 SEE - SELECT EDITING EXTENT 60 8.3.116 SEF - SHEET EJECT
    AND FEED 60 8.3.117 SGR - SELECT GRAPHIC RENDITION 61 8.3.118 SHS -
    SELECT CHARACTER SPACING 63 8.3.119 SI - SHIFT-IN 63 8.3.120 SIMD -
    SELECT IMPLIC IT MOVEMENT DIRECTION 63 8.3.121 SL - SC ROLL LEFT 63
    8.3.122 SLH - SET LINE HOM E 64 8.3.123 SLL - SET LINE LIM IT 64
    8.3.124 SLS - SET LINE SPAC ING 64 8.3.125 SM - SET M ODE 65 8.3.126
    SO - SHIFT-OUT 65 8.3.127 SOH - STAR T OF HEADING 65 8.3.128 SOS -
    STAR T OF STR ING 66 8.3.129 SPA - START OF GUARDED AREA 66 8.3.130
    SPD - SELECT PRESENTATION DIRECTIONS 66 8.3.131 SPH - SET PAGE HOM E
    67 8.3.132 SPI - SPAC ING INC REMENT 67 8.3.133 SPL - SET PAGE LIM
    IT 68 8.3.134 SPQR - SELECT PRINT QUALITY AND RAPIDITY 68 8.3.135
    SR - SC ROLL R IGHT 68 8.3.136 SR CS - SET R EDUC ED C HAR ACTER
    SEPAR ATION 68 8.3.137 SR S - STAR T R EVER SED STR ING 69 8.3.138
    SSA - START OF SELECTED AREA 69 8.3.139 SSU - SELECT SIZE UNIT 69
    8.3.140 SSW - SET SPAC E WIDTH 70 8.3.141 SS2 - SINGLE-SHIFT TW O 70
    8.3.142 SS3 - SINGLE-SHIFT THR EE 70 8.3.143 ST - STR ING TER
    MINATOR 70 8.3.144 STAB - SELECTIVE TABULATION 71 8.3.145 STS - SET
    TR ANSM IT STATE 71 8.3.146 STX - STAR T OF TEXT 71 8.3.147 SU - SC
    ROLL UP 71 8.3.148 SUB - SUB STITUTE 71 8.3.149 SVS - SELECT LINE
    SPACING 71 8.3.150 SYN - SYNCHRONOUS IDLE 72 8.3.151 TAC - TAB
    ULATION ALIGNED C ENTR ED 72 8.3.152 TALE - TAB ULATION ALIGNED
    LEADING EDGE 72 8.3.153 TATE - TAB ULATION ALIGNED TR AILING EDGE 72
    8.3.154 TB C - TAB ULATION C LEAR 73 8.3.155 TC C - TAB ULATION C
    ENTR ED ON C HAR ACTER 73 8.3.156 TSR - TAB ULATION STOP R EMOVE 73
    8.3.157 TSS - THIN SPAC E SPEC IFIC ATION 73 8.3.158 VPA - LINE
    POSITION AB SOLUTE 74 8.3.159 VPB - LINE POSITION B ACKWARD 74
    8.3.160 VPR - LINE POSITION FOR WARD 74 8.3.161 VT - LINE TAB
    ULATION 74 8.3.162 VTS - LINE TAB ULATION SET 74

```{=html}
<!-- Page 13 -->
```
-   vii - 9 T ransformati on betw een 7-bi t and 8-bit coded
    representations 74 Annex A - Formator functions and editor functions
    77 Annex B - Coding examples 79 Annex C - Text composition
    considerations 81 Annex D - Implementation-dependent features 83
    Annex E - Text area formats 85 Annex F - Differences between the
    fifth and the fourth edition of ECMA-48 87

```{=html}
<!-- Page 14 -->
```
-   v iii - .

```{=html}
<!-- Page 15 -->
```
1 Scope This EC MA St andard defi nes cont rol funct ions and t heir
coded represent ations for use i n a 7-bi t code, an extended 7-bit
code, an 8-bit code or an extended 8-bit code, if such a c ode is
structured in accordance with Standard EC MA-35. The cont rol funct ions
defi ned i n this St andard are i ntended t o be used em bedded in
charact er-coded data for interchange, i n part icular wi th charact
er-imaging devi ces. In general , the cont rol funct ions are defi ned
by their effect s on a charact er-imaging i nput/output devi ce. It is,
therefore, necessary t o make cert ain assum ptions about the archi
tecture of such a devi ce. These assum ptions are as unrestrictive as
possible; th ey are specified in clause 6. In addi tion to being perform
ed the cont rol funct ions may need t o be represent ed by a graphi c
symbol. The st ructure of t his Standard i s open-ended, so t hat more
cont rol funct ions can be i ncluded i n future edi tions. Other st
andards speci fying cont rol funct ions m ay defi ne m ore restricted
definitions of th em than those in this Standard. The devices to which
this Standard applies can vary greatly from each other depe nding on the
application for which a devi ce has been speci fically desi gned. It is
techni cally and econom ically impract ical for one devi ce to implement
all th e facilities sp ecified in this Stan dard. Th e in tention is
that in any type of device only a limited selectio n of the facilities
ap propriate to the applicatio n will b e implemented. 2 Conformance 2.1
Types of conform ance Full co nformance to a stan dard m eans th at all
o f its req uirements are met. Conformance will only have a unique m
eaning i f t he st andard cont ains no opt ions. If t here are opt ions
wi thin t he st andard t hey m ust be clearly identified, and any claim
of conform ance m ust include a statem ent that identifies th ose
options that have been adopt ed.  This Standard is of a differen t
nature sin ce it sp ecifies a larg e n umber o f facilities fro m wh ich
d ifferen t selectio ns may b e made to su it in dividual ap plicatio
ns. Th ese selectio ns are n ot id entified in th is Stan dard, but m
ust be identified at the tim e that a claim of conform ance i s made. C
onform ance t o such an i dentified selection is known as l imited
conform ance. 2.2 Conformance of information interchange A CC-d ata-elem
ent with in co ded in formation fo r in terch ange is in co nformance
with this Standard if the coded representatio ns of control functions
with in that CC-d ata-elem ent satisfy th e following conditions: a) a
coded represent ation of a cont rol funct ion t hat is specified in this
Stan dard shall always represent that control funct ion; b) a co ntrol
fu nction th at is sp ecified in th is St andard shal l al ways be
represent ed by the coded representatio n that is sp ecified in this
Stan dard for that co ntrol function; c) any coded representation that
is reserved for future standardi zation by this Standard shal l not
appear. Coded represent ations of cont rol funct ions and m odes n ot sp
ecified in th is Standard m ay appear i n interchanged inform ation
subject to the a bove conditions (see 5.4, 5.4.1 and 7.4). 2.3
Conformance of devices A d evice is in co nformance with th is Stan dard
if it c onform s t o t he requi rements of 2.3.1, and ei ther or both
2.3.2 and 2.3.3. Any claim of conform ance shal l identify the docum ent
whi ch cont ains t he descri ption speci fied in 2.3.1. 2.3.1 Devi ce
descri pti on A devi ce that conform s to this Standard shal l be t he
subject of a descri ption that:

```{=html}
<!-- Page 16 -->
```
-   2 -

i.  identifies, b y referen ce to th e clau ses o f, o r to th e co
    ntrol fu nctions sp ecified in this Standard, the selection of cont
    rol funct ions, t he coded represen tations of whi ch t he devi ce
    can ori ginate or can receive and interpret;
ii. identifies t he m eans by whi ch t he user m ay suppl y t he
    correspondi ng cont rol funct ions, or may recogni ze them, as speci
    fied respect ively in 2.3.2 and 2.3.3 bel ow. 2.3.2 Ori ginati ng
    devi ces An o riginating d evice sh all b e cap able o f tran
    smittin g with in a CC-data-elem ent the coded represent ations of
    an i dentified sel ection of cont rol funct ions, and of t heir
    param eter val ues (i ncluding mode sel ection param eters), conform
    ing to this Standard. Such a device shall allow t he user t o suppl
    y any cont rol funct ion t hat he chooses from am ong t he
    identified selection for the purpose of transm itting its coded
    representation over the coding interface. 2.3.3 Receiving devices A
    receiving device shall be capable of receiving with in a
    CC-data-elem ent and interpreting the coded represent ations of an i
    dentified sel ection of cont rol funct ions, and of t heir param
    eter val ues (i ncluding mode sel ection param eters), conform ing
    to this Standard. If t he i dentified sel ection cont ains a cont
    rol seque nce for which a default value for a param eter is
    specified in this Stan dard, th e id entified selectio n sh all in
    clude th e d efault v alue b oth in ex plicit an d in\
    implicit rep resentatio ns. Such a d evice sh all m ake availab le
    to the user an y co ntrol fu nction that is within the identified
    selectio n, and the coded representation of whic h is received over
    the coding interface, in such a form that the user can recogni ze it
    from among t he cont rol funct ions wi thin the identified sel
    ection. 3 References ECMA-6 7-Bit Coded Character Set (1991) ECMA-1
    7 Graphic Rep resentatio n o f th e Co ntrol Characters o f th e
    ECMA 7-Bit Coded Character Set for Inform ation Int erchange (1968)
    ECMA-35 Code Ext ension Techni ques (1985) ECMA-43 8-Bit Code - Stru
    cture and Rules (1991) ECMA-94 8-Bit Single-Byte Coded Graphic
    Character Set - Latin Alphabet No. 1 to No. 4 (1986) ECMA-113 8-Bit
    Single-Byte Code d Graphic Character Sets - Latin/Cyrillic
    Alphabet (1988) ECMA-114 8-Bit Single-Byte Code d Graphic Character
    Sets - Latin/Arabic Alphabet (1986) ECMA-118 8-Bit Single-Byte C
    oded Character Sets - Latin/Greek Alphabet (1986) ECMA-121 8-Bit
    Single-Byte C oded Character Sets - Latin/Hebrew Alphabet (1987)
    ECMA-128 8-Bit Single-Byte C oded Character Sets - Latin Alphabet
    No. 5 (1988) ECMA-144 8-Bit Single-Byte C oded Character Sets -
    Latin Alphabet No. 6 (1990) ECMA TR/53 Handl ing of B i-directional
    Text s (1992) ISO 1745: 1975 Inform ation processi ng - B asic m ode
    control procedures for dat a com munication system s ISO 2375: 1985
    Data processi ng - Procedure for regi stration of escape sequences
    ISO/IEC 7350: 1991 Inform ation Technol ogy - R egistration of
    repert oires of graphi c charact ers from ISO/IEC 10367 ISO
    8613-6:1989 Inform ation processi ng - Text and office systems -
    Office Docum ent Architecture (ODA) and interchange form at - Part
    6: Character content architectures ISO/IEC 10367: 1991 Inform ation
    Technol ogy - R epertoire of st andardi zed coded graphi c charact
    er set s for use i n 8-bi t codes

```{=html}
<!-- Page 17 -->
```
-   3 - ISO/IEC 10538: 1990 Inform ation Technol ogy - Control funct
    ions for t ext communication ISO Int ernational Register of C oded C
    haract er Sets to be Used with Escape Sequences. 4 Notation and
    definitions 4.1 Notation In t his St andard a convent ion has been
    adopt ed to assist t he reader. C apital l etters are used t o refer
    t o a speci fic control funct ion, m ode, m ode set ting, or gr
    aphic charact er i n order t o avoi d confusi on, for example,
    between the concept "s pace" and the character SPACE. It is intended
    t hat this convent ion and t he acrony ms of the m odes and t he
    cont rol funct ions be retained in all tran slatio ns of the tex t.
    This Standard uses t he not ation of t he form xx/ yy, where xx
    represent s the col umn num ber 00 t o 07 i n a 7- bit code t able
    or 00 t o 15 i n an 8-bi t code t able, and y y represent s the row
    num ber 00 t o 15.\
    4.2 Definitions For t he purpose of t his Standard, t he fol lowing
    defi nitions appl y. 4.2.1 Acti ve area The area in the data com
    ponent whic h contains the active data position. The area in the
    presentation com ponent whic h contains the active presentation
    position. 4.2.2 Acti ve field The field in the data com ponent whic
    h contains the active data position. The field in the presentation
    com ponent whic h contains the active presentation position. 4.2.3
    Acti ve line The line in the data com ponent whic h contains the
    active data position. The line in the presentation com ponent whic h
    contains the active presentation position. 4.2.4 Acti ve page The
    page in the data com ponent whic h contains the active data
    position. The page in the presentation com ponent whic h contains
    the active presentation position. 4.2.5 Acti ve data posi tion The
    character position in the data com ponent which is to receive the
    next graphic character or the next control function from the data
    stream and relativ e to which certain control functions are to be
    executed. 4.2.6 Acti ve presentati on posi tion The character
    position in the presentation com ponent wh ich is to receive the
    next graphic character for graphi c image out put and rel ative to
    which cert ain cont rol funct ions are t o be execut ed.  NOTE In
    general , the act ive present ation posi tion is indicated in a di
    splay by a cursor. 4.2.7 Area A series of successive character
    positions th at are not necessarily on the sam e line. 4.2.8 Aux
    ilia ry dev ice A devi ce connect ed t o a charact er-imaging devi
    ce for t he purpose of inputting, storing, retrieving, or imaging
    dat a. 4.2.9 Bi-directional data Data cont aining t ext st rings whi
    ch are t o be presen ted in different wri ting di rections, l ike l
    eft-to-right and ri ght-to-left. Refer t o ECMA Techni cal Report 53
    for furt her expl anations. 4.2.10 B it combi nati on An ordered set
    of bi ts used for t he represent ation of charact ers.

```{=html}
<!-- Page 18 -->
```
-   4 - 4.2.11 B yte A bit string that is operat ed upon as a uni t.\
    4.2.12 T o cancel\
    To mark dat a in such a way that it can be i gnored i n subsequent
    processi ng.\
    4.2.13 Character A member of a set of el ements used for t he organi
    zation, cont rol or represent ation of dat a.\
    4.2.14 Character-i magi ng devi ce A devi ce t hat gives a vi sual
    represent ation of dat a in the form of graphi c sy mbols usi ng any
    technol ogy, for exam ple cat hode ray tube or pri nter.\
    4.2.15 Character path The sequent ial order of t he charact er posi
    tions al ong a l ine of t he present ation com ponent . 4.2.16
    Character posi tion A position in the data com ponent available for
    r eceiving graphic characters for further presentation processi ng.\
    A position in the presentation com ponent available for receiving
    graphic charact ers for the rendering of the graphi c image out
    put.\
    4.2.17 Character progressi on The sequent ial order of t he charact
    er posi tions al ong a l ine of t he dat a component . 4.2.18 T o
    clear To remove t he di splay of dat a or t he i nformation used for
    t he di splay of dat a, for exam ple t abulation stops m arking the
    boundari es bet ween fi elds.\
    4.2.19 Coded character set; code A set of unam biguous rul es t hat
    est ablishes a charact er set and the one-t o-one rel ationshi p bet
    ween t he characters of the set and their b it co mbinations. 4.2.20
    Coded-character-data-element (CC-data-element) An el ement of i
    nterchanged i nformation t hat i s speci fied t o consi st of a
    sequence of coded representations of characters, in accordance with
    one or m ore identif ied standards for coded character sets. NOTE 1\
    In a communi cation envi ronment accordi ng to the reference model
    for Open Syst ems Int erconnect ion of\
    ISO 7498, a CC-data-element will form all or part of the information
    that corresponds to the Present ation-Prot ocol-Data-Units (PPDU)
    defined in that Standard. NOTE 2\
    When i nformation interchange i s accompl ished by means of
    interchangeabl e medi a, a C C-data-element\
    will form all or part of the informa tion that corresponds to the
    user data, and not that recorded during formatting and
    initialization. 4.2.21 Code extensi on The t echni ques for t he
    encodi ng of ch aracters that are not included in th e character set
    of a given code.\
    4.2.22 Code tabl e A table showing the character allocated to each
    bit com bination in a code.\
    4.2.23 Control character A cont rol funct ion the coded represent
    ation of wh ich consi sts of a si ngle bit combination.\
    4.2.24 Control functi on An elem ent of a character set that effect
    s the recordi ng, processi ng, t ransmission, or i nterpret ation of
    data, and t hat has a coded represent ation cons isting of one or m
    ore bi t combinations.

```{=html}
<!-- Page 19 -->
```
-   5 - 4.2.25 Control sequence A string of bit com binations starting
    with th e control function CONT ROL SEQUENCE INTRODUCER (CSI), and
    used for t he coded represent ation of control funct ions wi th or
    wi thout param eters. 4.2.26 Control stri ng A strin g of bit co
    mbinations which may occur in the data stream as a lo gical en tity
    fo r control purposes.\
    4.2.27 Cursor A special indicator used in a display to mark the
    activ e presentatio n position.\
    4.2.28 Data component The device com ponent which is used for
    storing the received data fo r further presentation processing.
    4.2.29 Decimal mark A graphi c sy mbol, usual ly a FULL STOP or a C
    OMMA, used t o separat e the fract ional part of a deci mal number
    from the integer part of t hat number.\
    4.2.30 Defaul t A value or a state th at is to be assu med when no
    value or state is ex plicitly sp ecified .\
    4.2.31 T o del ete To rem ove the contents from character positions
    and closing the resulting gap by m oving adjacent graphic characters
    into the em pty positions.\
    4.2.32 T o desi gnate To identify a set o f characters that are to
    be repr esented, in som e cases im mediately and in others on the
    occurrence of a furt her cont rol funct ion, i n a prescri bed
    manner.\
    4.2.33 Devi ce A com ponent of inform ation processing equipm ent
    which can tr ansmit, and/or receive, coded information with in CC-d
    ata-elem ents. NOTE It may be an i nput/output devi ce i n the
    convent ional sense, or a process such as an application program or
    gat eway function. 4.2.34 Di spl ay The region for vi sual present
    ation of dat a on any t ype of charact er-imaging devi ce, i
    ncluding pri nter, cathode ray tube and si milar devi ces.\
    4.2.35 E ditor functi on A cont rol funct ion used for edi ting, al
    tering or transposi ng the visual arrangem ent of dat a.\
    4.2.36 E ligible The term used to denote an area consid ered for
    transm ission or transfer.\
    4.2.37 E nvironment The characteristic that id entifies th e number
    of bits u sed for representing a character in a data processing or
    dat a communication sy stem or i n a part of such a sy stem.\
    4.2.38 T o erase To rem ove t he cont ents from charact er posi
    tions and l eaving the resul ting gap open.\
    4.2.39 E scape sequence A st ring of bi t com binations t hat is
    used for cont rol purposes i n code ext ension procedures. The fi
    rst of these b it co mbinations represents th e control function
    ESCAPE.\
    4.2.40 Fi eld An area consisting of the character position at a
    charact er t abulation st op (begi nning of t he fi eld) and t he
    charact er posi tions up t o, but not including, the char acter
    position at the follo wing character tabulation stop (end of t he
    field).

```{=html}
<!-- Page 20 -->
```
-   6 - 4.2.41 Fi nal Byte The bit co mbination that term inates an
    escape sequence or a control sequence.\
    4.2.42 Formator functi on A control funct ion (form at effect or or
    present ation cont rol funct ion) descri bing how t he ori ginator
    of t he data stream wish es th e information to be formatted or
    presented.\
    4.2.43 Graphi c character A character, other th an a co ntrol fu
    nction, that h as a v isual rep resentatio n normally h and-written
    , printed or di splayed, and t hat has a coded represent ation consi
    sting of one or m ore bi t combinations.\
    4.2.44 Graphi c rendi tion The vi sual style of di splaying a set of
    graphi c symbols.\
    4.2.45 Graphi c symbol\
    A visual represent ation of a graphi c charact er or of a cont rol
    funct ion.\
    4.2.46 Guarded area A special case of a qualified area, the contents
    of which m ay be excl uded from transmission as a data stream and
    from transfer to an auxiliary input/ output device.\
    4.2.47 Ini tial state The st ate a devi ce has aft er it is made
    operat ional. It is the recom mended "reset" state of the m odes.\
    4.2.48 Intermediate Byte

a)  In an escape sequence, a bit combination th at m ay o ccur b etween
    th e co ntrol fu nction ESCAPE (ESC) an d the Fin al Byte.\
b)  In a cont rol sequence, a bi t com bination t hat m ay occur between
    the control funct ion CONTROL SEQUENCE INTRODUCER (CSI) and th e
    Final By te, or between a Param eter By te and the Final Byte.\
    4.2.49 T o invoke To cause a designated set of characters to be
    repres ented by the prescribed b it com binations whenever those bit
    co mbinations occur.\
    4.2.50 L ine A set of a consecutive character positions.\
    4.2.51 Line home posi tion A reference position on a line in the
    data com ponent ahead of which the active data position can normally
    not be m oved. A reference position on a l ine i n t he present
    ation com ponent ahead of whi ch t he act ive present ation position
    can norm ally not be m oved. 4.2.52 Line l imit posi tion A
    reference position on a line in the data com ponent beyond which the
    active data position can normally not be m oved. A reference posi
    tion on a l ine i n t he present ation component beyond which the
    active present ation position can norm ally not be m oved. 4.2.53 L
    ine ori entati on The term u sed to d escrib e th e way in wh ich a
    lin e will ap pear in th e g raphic im age o utput. In th is
    Standard, l ine ori entation may only be vert ical or hori zontal.
    4.2.54 L ine progressi on The di rection of present ation of
    successi ve lines.

```{=html}
<!-- Page 21 -->
```
-   7 - 4.2.55 Operati ng system The soft ware t hat cont rols t he
    execut ion of com puter program s and that may provi de schedul ing,
    debugging, input/output control, accounting, com pilation, storag e
    assignm ent, data m anagem ent, and related serv ices.\
    4.2.56 Page A set o f consecutive lin es.\
    4.2.57 Page home posi tion A reference posi tion on a page i n t he
    dat a com ponent ahead of which the active line (the line that
    contains the act ive dat a posi tion) can norm ally not be m oved. A
    reference posi tion on a page i n t he present ation com ponent
    ahead of whi ch t he act ive l ine (t he l ine that cont ains the
    act ive present ation posi tion) can norm ally not be m oved. 4.2.58
    Page l imit posi tion A reference posi tion on a page i n the data
    component bey ond whi ch the act ive line (the line that contains
    the act ive dat a posi tion) can norm ally not be m oved. A
    reference posi tion on a page i n the present ation co mponent
    beyond whi ch the act ive line (t he l ine that contains the act ive
    present ation posi tion) can norm ally not be m oved. 4.2.59
    Parameter Byte In a cont rol sequence, a bi t com bination t hat may
    occur between the control funct ion CONTROL SEQUENCE INTRODUCER
    (CSI) and th e Final By te, or between CSI and an Interm ediate By
    te.\
    4.2.60 Presentati on component The devi ce com ponent which is used
    for produci ng the graphi c image out put. 4.2.61 Private (or
    experimental) use The means of represent ing a non-st andardi zed
    cont rol funct ion or m ode i n a m anner com patible with this
    Standard.\
    4.2.62 Protected area A special case of a qualified area.\
    4.2.63 Qual ified area A string of charact er posi tions wi th which
    certain characteris tics are associated. 4.2.64 Repertoi re A
    specified set of characters that ar e represent ed by one or m ore
    bi t com binations of a coded charact er set.\
    4.2.65 Scrol l The act ion whereby all, or part of, t he graphi c
    symbols of a di splay are m oved i n a speci fied di rection.\
    4.2.66 Sel ected area A strin g of character p ositions, th e co
    ntents o f wh ich may b e elig ible to be tran smitted in th e fo rm
    of a data stream or to be transferred to an auxiliary inpu t/output
    device.\
    4.2.67 T abul ati on The t echni que of i dentifying charact er posi
    tions or l ines i n a di splay for the purpose of arrangi ng
    information system atically.\
    4.2.68 T abul ati on stop The indication that a character position
    or a line is to be used for t abulation; a charact er t abulation st
    op may also serve as a boundary between fi elds.\
    4.2.69 User A person or other entity that invokes the services
    provided by a device.

```{=html}
<!-- Page 22 -->
```
-   8 - NOTE 1\
    This entity may be a process such as an application program if the
    "device" is a code convertor or a gateway function, f or exampl e.
    NOTE 2\
    The charact ers, as suppl ied by t he user or made avai lable to the
    user, ma y be in the form of codes local to the devi ce, or of
    non-convent ional visual represent ations, provi ded that clause 2.3
    above i s satisfied. 5 Coded representation 5.1 General Each cont
    rol funct ion in this Standard belongs t o one of t he fol lowing
    types:

a)  elements of the C0 set;\
b)  elements of the C1 set;\
c)  control sequences;\
d)  independent cont rol funct ions;\
e)  control strings.\
    5.2 Elements of the C0 set\
    These cont rol funct ions are represent ed in 7-bi t and 8-bit codes
    by bit combinations from 00/00 to 01/15. The defi nitions and t he
    coded represent ations of t he cont rol functions are specified in
    8.3 (see also table 1).\
    The 3-charact er escape sequence desi gnating and i nvoki ng this C0
    set is ESC 02/01 04/ 00.\
    NOTE 1\
    The use of this escape sequence i mplies that all cont rol functions
    of this C0 set mu st be implemented. NOTE 2\
    It is assumed that even with no invoked C0 set the control character
    ESCAPE is available and is represent ed by bi t combi nation 01/ 11.
    Table 1 - Bit combinations representing the control functions of the
    C0 set Row number Column number 00 01 00 01 02 03 04 05 06 07 08 09
    10 11 12 13 14 15 NUL SOH STX ETX EOT ENQ ACK BEL BS HT LF VT FF CR
    SO or LS1 SI or LS0 DLE DC1 DC2 DC3 DC4 NAK SYN ETB CAN EM SUB ESC
    IS4 IS3 IS2 IS1

5.3 Elements of the C1 set These control functions are represented a) in
a 7-bit code by 2-character escape sequences of the form ESC Fe , wh ere
ESC is rep resented b y b it combination 01/ 11 and Fe i s represent ed
by a bi t combination from 04/00 to 05/15;

```{=html}
<!-- Page 23 -->
```
-   9 -

b)  in an 8-bi t code by bi t com binations from 08/ 00 t o 09/15;
    however, when the announcer sequence ESC 02/00 04/06 according to
    Standa rd ECMA-35 is used, the control func tions of the C1 set are
    represented by ESC Fe sequences as i n a 7-bi t code.\
    The defi nitions and t he coded represent ations of t he cont rol
    functions are specified in 8.3 (see also table 2a and t able 2b).\
    The unallocated bit com binations are re served for fut ure st
    andardi zation and shal l not be used. For the bit combinations 04/
    04 (see t able 2a) and 08/ 04 (see t able 2b) see F.8.2 i n annex F.
    The 3-charact er escape sequences desi gnating and i nvoki ng t his
    C 1 set are ESC 02/06 04/00 and ESC 02/02 F. NOTE The use of these
    escape sequences i mplies that all cont rol characters o f this C1
    set mu st be implemented. Table 2a - Bit combinations representing
    Fe for the co ntrol functions of the C1 set in the 7-bit code Row
    number Column number 04 05 00 01 02 03 04 05 06 07 08 09 10 11 12 13
    14 15 -- -- BPH NBH -- NEL SSA ESA HTS HTJ VTS PLD PLU RI SS2 SS3
    DCS PU1 PU2 STS CCH MW SPA EPA SOS -- SCI CSI ST OSC PM APC

```{=html}
<!-- Page 24 -->
```
-   10 - Table 2b - Bit combinations representing the cont rol functions
    of the C1 set in an 8-bit code Row number Column number 08 09 00 01
    02 03 04 05 06 07 08 09 10 11 12 13 14 15 -- -- BPH NBH -- NEL SSA
    ESA HTS HTJ VTS PLD PLU RI SS2 SS3 DCS PU1 PU2 STS CCH MW SPA EPA
    SOS -- SCI CSI ST OSC PM APC

5.4 Control sequences A control sequence i s a st ring of bi t com
binations st arting wi th t he cont rol funct ion C ONTROL SEQUENCE
INTRODUCER (CSI) followed by one or m ore bit com binations representing
param eters, if any, and by one or m ore bi t com binations i dentifying
t he cont rol funct ion. The cont rol funct ion C SI itself is an elem
ent of the C1 set.\
The form at of a control sequence is\
CSI P ... P I ... I F\
where\
a) CSI i s represent ed by bi t com binations 01/ 11 (repr esent ing
ESC) and 05/ 11 i n a 7-bi t code or by bi t combination 09/ 11 in an
8-bi t code, see 5.3;\
b) P ... P are Param eter Bytes, which, if present, consist of bit com
binations from 03/00 to 03/15;\
c) I ... I are Interm ediate Bytes, which, if presen t, consist of bit
com binations from 02/00 to 02/15. Together with the Fin al Byte F, th
ey id entify th e control function;\
NOTE The number of Intermediate Bytes is not limited by this Standard;
in practice, one Intermediate Byte will be sufficien t since with
sixteen d ifferen t b it co mbinations a vailable fo r th e In termed
iate Byte o ver o ne thousand control functions may be identified.\
d) F is th e Fin al Byte; it co nsists o f a b it co mbination fro m 0
4/00 to 0 7/14; it terminates the control sequence an d to gether with
the Intermediate Bytes, if p resent, id entifies th e co ntrol fu
nction. Bit combinations 07/ 00 t o 07/ 14 are avai lable as Fi nal B
ytes of cont rol sequences for private (or experi mental) use.\
The definitions and t he coded represent ations of t he cont rol
functions are specified in 8.3 (see also tables 3 and 4). C oding exam
ples are shown i n B.1 in annex B .

```{=html}
<!-- Page 25 -->
```
-   11 - Table 3 - Fina l Bytes o f control sequences w ithout
    Intermediate Bytes Row number Column number 04 05 06 07 00 01 02 03
    04 05 06 07 08 09 10 11 12 13 14 15 ICH CUU CUD CUF CUB CNL CPL CHA
    CUP CHT ED EL IL DL EF EA DCH SSE CPR SU SD NP PP CTC ECH CVT CBT
    SRS PTX SDS SIMD -- HPA HPR REP DA VPA VPR HVP TBC SM MC HPB VPB RM
    SGR DSR DAQ

Private Use

Table 4 - Final Bytes of control sequences with a si ngle Intermedi ate
Byte 02/ 00 Row number Column number 04 05 06 07 00 01 02 03 04 05 06 07
08 09 10 11 12 13 14 15 SL SR GSM GSS FNT TSS JFY SPI QUAD SSU PFS SHS
SVS IGS -- IDCS PPA PPR PPB SPD DTA SHL SLL FNK SPQR SEF PEC SSW SACS
SAPV STAB GCC TATE TALE TAC TCC TSR SCO SRCS SCS SLS -- -- SCP -- -- --
--

Private Use

The unallocated bit combinations are reserved for future standardizati
on and shal l not be used. See al so F.8.3 i n annex F. 5.4.1 Parameter
representation A control sequence m ay contain a string of Param eter
Bytes P ... P repr esenting one or m ore param eters to complete th e
specificatio n of the control function.\
The Param eter Bytes are b it co mbinations fro m 0 3/00 to 0 3/15. Th e
parameter strin g is interpreted as follows:\
a) If t he fi rst bit com bination of t he param eter st ring i s in the
range 03/ 00 t o 03/ 11, t he param eter string is interpreted according
to the format described in 5.4.2.

```{=html}
<!-- Page 26 -->
```
-   12 -

b)  If t he fi rst bit com bination of t he param eter st ring i s in
    the range 03/ 12 t o 03/ 15, t he param eter string is available for
    private (or experi mental) use. It s form at and m eaning are not
    defi ned by t his Standard.\
    5.4.2 Parameter string format\
    A param eter st ring whi ch does not start with a bi t combination i
    n the range 03/ 12 t o 03/ 15 shall have the following form at:\
c)  A param eter string consists of one or m ore param eter sub-strings,
    each of which represents a num ber in deci mal notation.\
d)  Each param eter sub-st ring consi sts of one or more bi t com
    binations from 03/ 00 t o 03/ 10; t he bi t combinations from 03/00
    to 03/09 represent the di gits ZERO to NINE; bit com bination 03/10
    m ay be used as a separator in a param eter sub-string, for ex
    ample, to separate the fractional part of a decim al number from the
    integer part of t hat number.
e)  Param eter sub-st rings are separat ed by one bi t combination 03/
    11.\
f)  Bit co mbinations 03/12 to 03/15 are reserv ed fo r fu ture stan
    dardizatio n ex cept wh en used as the first bit co mbination of the
    parameter strin g.\
g)  An em pty param eter sub-st ring represent s a defa ult value whi ch
    depends on t he cont rol funct ion.\
h)  In each param eter sub-string, leading bit com binations 03/00 are
    not signifi cant and m ay be om itted. If t he param eter sub-st
    ring consi sts of bi t com binations 03/ 00 onl y, at l east one of
    them must be retained to indicate the zer o val ue of t he sub-st
    ring.
i)  If the param eter st ring st arts wi th t he bi t com bination 03/
    11, an em pty param eter sub-st ring i s assum ed preceding the
    separator; if the param eter string terminates with the bit com
    bination 03/11, an em pty param eter sub-st ring i s assum ed fol
    lowing the separat or; if t he param eter st ring cont ains successi
    ve bi t combinations 03/ 11, em pty param eter sub-st rings are
    assum ed bet ween t he separat ors.\
j)  If t he cont rol funct ion has m ore t han one param eter, and som e
    param eter sub-st rings are empty, the separators (b it co mbination
    03/11) must still b e present. However, if the last parameter
    sub-strin g(s) is em pty, the separator preceding it m ay be om
    itted, see B.2 in annex B. 5.4.3 Types of parameters In a control
    sequence with param eters, each para meter sub-string corresponds to
    one param eter and represent s t he val ue of t hat param eter. The
    num ber of param eters i s ei ther fi xed or variable, dependi ng on
    t he cont rol funct ion. If t he num ber of param eters is vari
    able, nei ther t he m aximum num ber of values nor t he order i n
    which the correspondi ng act ions ar e perform ed are defi ned by
    this Standard.\
    A param eter may be purel y numeric or i t may be sel ective,
    i.e. denot ing one of a num bered l ist of act ions the cont rol
    funct ion can perform .\
    In the case of selected param eters a particular param eter val ue m
    ay have t he sam e m eaning as a combination of t wo or m ore
    separat e values.\
    Unassigned selective param eter values are reserved for future
    standardi zation.\
    5.5 Independent control functions These control funct ions are
    represent ed i n 7-bi t and 8-bit codes by 2-charact er escape
    sequences of the form ESC Fs, where ESC is represent ed by bi t com
    bination 01/ 11 and Fs i s represent ed by a bi t combination from
    06/00 to 07/14.\
    The defi nitions and t he coded represent ations of t he cont rol
    functions are specified in 8.3 (see also table 5).

```{=html}
<!-- Page 27 -->
```
-   13 - Table 5 - Independent control functions Row number Column
    number 06 07 00 01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 DMI INT
    EMI RIS CMD -- -- -- -- -- -- -- -- -- LS2 LS3 -- -- -- -- -- -- --
    -- -- -- -- -- LS3R LS2R LS1R --

The unallocated bit com binations ar e reserved for future standard
ization and shal l not be used. NOTE ESC Fs sequences are regi stered i
n t he ISO Int ernational Register of C oded C haract er Set s t o be
Used with Escape Sequences, which is maintained by th e Registration
Authority fo r ISO 2375. Any candidates for ESC Fs sequences have t o be
approved by ISO/ IEC JTC 1/SC2 for regi stration. The coding for the
Final Byte, Fs, will th en be assigned by the Reg istration Authority.\
5.6 Control strings A co ntrol strin g is a strin g o f b it co
mbinations wh ich m ay o ccur in th e data stream as a logical entity
for control purposes. A cont rol string consi sts of an openi ng del
imiter, a com mand st ring or a charact er string, and a term inating
delim iter, the STRING TERM INATOR (ST).\
A com mand st ring is a sequence of bi t combinations i n the range 00/
08 to 00/13 and 02/ 00 to 07/14.\
A character string is a sequence of any bit combination, except those
representing START OF STRING (SOS) or STRING TERM INATOR (ST).\
The interpret ation of t he com mand st ring or t he charact er st ring
i s not defi ned by this Standard, but instead requires prior agreem ent
between the se nder and t he reci pient of t he dat a.\
The openi ng del imiters defi ned i n this Standard are\
a) APPLICATION PROGRAM COMMAND (APC) b) DEVICE CONTROL STRING (DCS) c)
OPERATING SYSTEM COMMAND (OSC) d) PRIVACY MESSAGE (PM ) e) START OF
STRING (SOS) 6 Device concepts The defi nitions of t he cont rol funct
ions i n t his Standard are based on general assum ptions about the
architecture of a character-im aging device. Exam ples of devi ces
confor ming to these concepts are: an alphanum eric display devi ce, a
pri nter or a m icrofi lm output devi ce.\
A character-im aging device is a device which is capable of receiving a
data stream that consists of coded control funct ions and graphi c
charact ers, and i s capabl e of produci ng a graphi c i mage out put.
Thi s out put must be readable by a hum an being according to the
various traditional writing conve ntions such as left-to-

```{=html}
<!-- Page 28 -->
```
-   14 - right, right-to-left, top-to-bottom and bottom-to-top. The
    graphi c i mage out put is, i n general , produced i n the form of
    one or m ore rectangular arrays of ch aracter positions and lines
    which are called pages. If th e device is an input/output device
    rath er th an merely an output device, it is also cap able o f tran
    smittin g a data stream th at co nsists o f co ded control functions
    and graphic ch aracters; th e tran smitted data stream is, in\
    general , com posed of a com bination of dat a whi ch have been sent
    to t he devi ce and dat a whi ch have been entered locally in to the
    device, fo r example by an associated keyboard. A number of
    facilities for the organizatio n o f th e g raphic im age o utput an
    d fo r estab lishing th e d irectio n o f presented text are
    provided by this Standard. A device m ay support all of these
    facilities or only a subset of them appropriate to the applicatio
    n.  The defi nitions i n this St andard assum e a bi-directional
    devi ce whi ch has bot h a present ation com ponent (see 6.1.1) and
    a dat a com ponent (see 6.1.3). In t he case of a uni -directional
    devi ce or a bi -directional devi ce without a data com ponent, all
    references to active data position, data component, character
    progression, etc., are t o be read as referri ng to active present
    ation posi tion, present ation com ponent , charact er pat h, etc.,
    resp. 6.1 Com ponents A devi ce consi sts ei ther of an i nput com
    ponent , a present ation com ponent and a dat a com ponent , or of
    an input component and a present ation com ponent only. The input
    com ponent is capable of receiving the inform ation to be im aged
    from a m anual input device such as a key board or from a dat a
    stream. Thi s Standard does not deal with the input component . The
    present ation com ponent whi ch i s present in uni -directional as
    wel l as i n bi -directional devi ces is used for produci ng the
    graphi c image out put. The out put may, for exam ple, be rendered
    on a di splay or a pri nter. The data com ponent which is generally
    provided in bi-directional devices only is used to store the
    received information for furt her present ation processi ng. 6.1.1
    Presentation component The presentation com ponent is capable of
    presenti ng the inform ation in successive lines; each line
    consisting of successive character positions. The lines , as well as
    the character positions, are identified by the consecutive num bers
    1, 2, 3 ... The l ine ori entation i n the present ation com ponent
    is ei ther hori zontal or vert ical. Thi s defi nes t he way in
    which a line will appear in the produced graphic im age output. For
    hori zontal line ori entation, t he direction of t he line progressi
    on can be:\
    top-t o-bot tom, or − − − − − − bottom-to-top. For vert ical line
    ori entation, t he direction of t he line progressi on can be:\
    left-to-right, or right-to-left. The sequent ial order of t he
    charact er posi tions al ong a l ine of t he present ation component
    is called the character path. The charact er pat h along a l ine can
    be:\
    left-to-right or ri ght-to-left (in the case of hori zontal line ori
    entation), or top-to-bottom or bot tom-to-top (i n the case of vert
    ical line ori entation). The lines are num bered according to the
    established line progression. The character positions are num bered
    accordi ng to the established character path. Each character
    position either is in the erased state or im ages a graphi c sy
    mbol. A graphi c sy mbol represents SPACE, a graphic character, or a
    contro l funct ion for whi ch a graphi cal represent ation i s requi
    red. The initial state o f all ch aracter p ositions is "erased".

```{=html}
<!-- Page 29 -->
```
-   15 - Dependi ng on t he implementation, t here m ay or m ay not be a
    di stinction bet ween a charact er position in the erased state and
    a character position im aging SPACE. 6.1.2 The acti ve presentati on
    posi tion At any time, t here i s a uni que charact er posi tion i n
    the present ation com ponent whi ch is cal led the active present
    ation posi tion. The active presentation position is the character
    position which is to receive the next graphic character of t he dat
    a st ream for graphi c i mage out put or a cont rol funct ion for
    whi ch a graphi cal represent ation is required. The active
    presentation position in the pres entation component is also the
    character position relativ e to which certain control functions are
    to be executed (see 6 .4).\
    The activ e p resentatio n position can be moved ex plicitly (see 6
    .1.7) or in directly (see 6.1.8). In the case where a device has no
    data com ponent, the active pres entation position can also be m
    oved im plicitly (see 6.1.6). NOTE In a display it is common pract
    ice t o mark t he act ive present ation posi tion by means of a
    speci al visible indicator which is ca lled the cursor. The line
    containing the act ive present ation posi tion i s called the active
    line; the field containing the activ e presentatio n position is
    called the activ e field ; the area containing the active
    presentation position is called the active area; the page containing
    the activ e presentatio n position is called the activ e page. 6.1.3
    Data component In the data com ponent the received data stream is st
    ructured into successive lin es; each line consisting of successive
    character positions. The lines, as well as the character positions,
    are id entified b y th e consecutive num bers 1, 2, 3 ... The
    sequent ial order of t he charact er posi tions al ong a l ine of t
    he data component is called the charact er progressi on. In this
    Standard, the line orientation in t he dat a com ponent i s consi
    dered t o be hori zontal, t he l ine progressi on is consi dered t o
    be t op-to-bottom, the charact er progressi on is consi dered t o be
    l eft-to-right. The lines are num bered according to the line
    progression. The character positions are num bered acco rding to the
    character progression. Each character position either is in the
    erased state or contains a gra phic character, or a control
    function. The initial state o f all ch aracter p ositions is
    "erased". Dependi ng on t he implementation, t here m ay or m ay not
    be a di stinction bet ween a charact er position in the erased state
    and a char acter posi tion cont aining SPAC E. 6.1.4 The acti ve
    data posi tion At any t ime, t here i s a uni que charact er posi
    tion i n t he dat a com ponent whi ch i s called the active data
    position. The activ e d ata p osition is th e ch aracter p osition
    wh ich is available for the next graphic character or the next
    control function of the receive d data stream . The active data
    position is also the character position relativ e to which certain
    control functions are to be executed (see 6 .4). The activ e data
    position can b e m oved im plicitly (see 6 .1.6) o r ex plicitly
    (see 6 .1.7) o r in directly (see 6.1.8). The lin e co ntaining th e
    activ e d ata p osition is called th e active line; the field
    containing the active data position is called the active field; the
    area containi ng th e activ e d ata p osition is called th e activ e
    area; the page cont aining the act ive dat a posi tion is called the
    act ive page. 6.1.5 Rel ationshi p betw een acti ve data posi tion
    and acti ve presentati on posi tion In a uni -directional devi ce,
    whet her i t has a present ation com ponent only or a present ation
    component\
    and a data com ponent, there is no difference between the active
    data position and the active presentation position.

```{=html}
<!-- Page 30 -->
```
-   16 - In a bi-directional device, if it has a present ation com
    ponent and a dat a com ponent , t he act ive present ation posi tion
    i s t he charact er posi tion i n t he present ation com ponent that
    corresponds to the active data position in the data com ponent.
    Because of the possible differe nces between character progressi on
    and charact er pat h, as i n some bi-directional environments, the
    coordi nates of t he act ive dat a position in the data com ponent
    and of the active presentation position in the presentation com
    ponent may differ. Some cont rol funct ions act on, and affect , t
    he act ive dat a posi tion whereas ot her cont rol funct ions act
    on, and affect , t he act ive present ation posi tion. W hen one of
    t hese posi tions i s so modified, the other is updated accordingly.
    This is referred to as indirect m ovement (see 6.1.8). In the
    situation where a data component is not present i n a devi ce t hen
    t he charact eristics of t he dat a component, active data position,
    active data position m ovement, character progression, etc., are
    treated as if t hey are i dentical wi th t he respect ive ch aract
    eristics of t he present ation com ponent , act ive present ation
    posi tion, act ive present ation posi tion movement, charact er pat
    h, etc., resp.. 6.1.6 Implicit movement\
    An implicit movement is a m ovement of t he act ive dat a posi tion
    whi ch i s perform ed aft er a graphi c character is received, or a
    control function, for which a graphical representa tion is required.
    In uni- directional devices the direction of t he i mplicit m
    ovement of t he act ive dat a posi tion i n t he dat a component is
    the sam e as t he di rection of t he charact er progressi on; in
    devices wi thout a dat a component\
    the i mplicit m ovement appl ies t o t he act ive present ation posi
    tion in the present ation component and is then the sam e as the
    direction of the character path. In bi-directional devices t he di
    rection of t he implicit movement may be different from the di
    rection of t he charact er progressi on. The di rection i s the sam
    e as the directio n of the character p rogressio n until it is m
    odified by an appropriate co ntrol function. If th e d irectio n of
    th e im plicit m ovement is th e sam e as that of the character
    progressi on and t he active data position is not th e last ch
    aracter p osition of th e activ e lin e, th e activ e d ata p
    osition is m oved to th e following character position of that line.
    If the direction of the i mplicit movement i s opposi te t o t hat
    of t he charact er progressi on and t he act ive data p osition is n
    ot the first ch aracter p osition of the activ e lin e, th e activ e
    data p osition is m oved to the preceding character position of that
    line. When th e activ e d ata p osition h as b een m odified b y an
    implicit movement, the activ e presentatio n position in the
    presentation com ponent is updated accordi ngly; this is referred to
    as indirect m ovement (see 6.1.8). NOTE In the following situation,
    the effect o f an attemp t to mo ve th e a ctive d ata position is n
    ot defined by th is Standard: an attemp t to perform an implicit
    movemen t when th e a ctive d ata p osition is th e la st ch aracter
    position of a l ine and t he di rection of t he i mplicit movement
    is the same as that of the charact er progressi on, or w hen t he
    act ive dat a posi tion is the first charact er posi tion of a line
    and t he direction of the implicit movement is opposi te to that of
    the charact er progressi on; − Dependi ng on t he implement ation,
    an at tempt to perf orm such movement s may

a)  cause a w rap-around movement ;
b)  cause the position to be blocked (a condition in which no graphic
    character can be entered until a valid explicit p osition movemen t
    is p erformed);
c)  cause t he posi tion t o remai n w here i t i s but permi t graphi c
    charact ers t o be entered thereby replacing or overst riking the
    previ ously entered charact er;
d)  cause t he cursor t o disappear f rom the operat or's vi ew;
e)  cause t he cursor t o move t o the opposi te end of the display but
    one col umn or row offset;
f)  cause scro lling to occur;
g)  cause ot her i mplement ation-dependent action.

```{=html}
<!-- Page 31 -->
```
-   17 - 6.1.7 Explicit movement In the data com ponent an explicit m
    ovement is a movement of the active data position that is perform ed
    when a cont rol funct ion i s execut ed whi ch causes t he act ive
    dat a posi tion t o be m oved t o a speci fied character position in
    the data com ponent. W hen the active data position has been m
    odified by an explicit movement, the active presentation position in
    the presentation com ponent is updated accordingly; this is referred
    t o as i ndirect movement (see 6.1.8). In the presentation com
    ponent an explicit m ovement is a m ovement of the active
    presentation position that is p erformed when a co ntrol fu nction
    is ex ecuted which causes the activ e presentatio n position to be
    moved t o a speci fied charact er posi tion i n t he present ation
    com ponent . W hen t he act ive present ation position has been m
    odified by an expl icit m ovement, t he act ive data position in the
    data component is updated accordingly; this is referred to as
    indirect m ovement (see 6.1.8). NOTE In th e fo llowing situ ation,
    th e effect o f a n a ttemp t to mo ve th e a ctive d ata p osition
    o r the active present ation posi tion is not defined by t his
    Standard: an attempt to perform an explicit movement to a non-
    existing character position, for example beyond the last charact er
    posi tion of a line, or beyond t he last line of a page. − Dependi
    ng on t he implement ation, an at tempt to perf orm such movement s
    may

a)  cause a w rap-around movement ;
b)  cause the position to be blocked (a condition in which no graphic
    character can be entered until a valid explicit p osition movemen t
    is p erformed);
c)  cause t he posi tion t o remai n w here i t i s but permi t graphi c
    charact ers t o be entered thereby replacing or overst riking the
    previ ously entered charact er;
d)  cause t he cursor t o disappear f rom the operat or's vi ew;
e)  cause t he cursor t o move t o the opposi te end of the display but
    one col umn or row offset;
f)  cause scro lling to occur;
g)  cause ot her i mplement ation-dependent action. 6.1.8 Indirect
    movement In the data com ponent an indir ect m ovement is the m
    ovement by which the active data position is modified t o refl ect a
    m odification of t he act ive present ation posi tion by an expl
    icit movement (see 6.1.7) in the present ation com ponent . In t he
    present ation com ponent an i ndirect m ovement i s t he m ovement
    by which the active present ation position i s m odified t o refl
    ect a m odification of t he act ive dat a posi tion by an implicit
    movement (see 6.1.6) or by an expl icit movement (see 6.1.7) i n the
    dat a component . 6.2 The data stream The data stream is consi dered
    t o be a cont inuous st ream. It may be st ructured i n messages,
    records and/ or blocks, but this does not affect t he operat ion of
    t he de vices at th e ab stract lev el o f d escrip tion in th is
    Standard; the l ogical or phy sical uni ts of dat a are re garded as
    bei ng concat enated t o form one cont inuous data stream . 6.2.1
    Data organi zati on Text within a data stream can be viewed as bei
    ng const ructed from charact er st rings. Each such string may cont
    ain nest ed st rings. C haract ers within a string are organized in
    th e o rder in wh ich th ey are intended t o be read. Each string
    has a direction associated with it. The direction m ay be associ
    ated wi th t he st ring usi ng a control funct ion or a hi gher-l
    evel prot ocol. If t he di rection i s not det ermined i n t his way
    , t hen t he directio n is th e sam e as th at of the currently
    established character path.

```{=html}
<!-- Page 32 -->
```
-   18 - 6.3 The graphic im age output In t his St andard, t he graphi c
    i mage out put i s regarded as bei ng produced in the form of a
    continuous stream , but it m ay eventually be m ade available ch
    aracter-by-character, line-by -line, or page-by -page. The graphi c
    image out put may consi st of one or m ore pages of a predet ermined
    si ze. A page is com posed of a predeterm ined num ber of lines,
    each com posed of a predeterm ined num ber of charact er posi tions.
    Duri ng t he operat ion of t he devi ce, t he num ber of l ines per
    page, t he number of character positions per line, the line spacing,
    and th e character spacing m ay be changed by appropriate control
    funct ions. The graphi c i mage out put i s const ructed i n t he
    present ation com ponent from t he dat a st ream st ored i n t he
    data com ponent, and according to the line orientati on and line
    progression of the presentation com ponent. The present ation of
    charact ers along a line in t he present ation com ponent i s
    dependent on t he charact er path, the character progression and the
    di rection associated with the string. The size of a charact er
    position may be fi xed or m ay depend on t he graphi c sy mbol of t
    he charact er bei ng imaged. The font desi gn of t he graphi c
    symbols is not defi ned by this Standard. 6.4 Form ator functions
    and editor functions Two cl asses of cont rol funct ions have an act
    ion on t he l ayout or posi tioning of i nformation in charact er-
    imaging devices. They are form ator funct ions and ed itor funct
    ions. The pri ncipal difference bet ween edi tor functions and form
    ator functions is that the la tter are sensitive to the FORMAT
    EFFECTOR ACTION MODE (FEAM); whereas the form er are not (see annex
    A).\
    6.4.1 Formator functi ons They are form at effectors and presen
    tation control funct ions. Form ator funct ions m ay be part of t he
    dat a stream. They descri be how t he ori ginator of t he dat a st
    ream wi shes t he i nformation t o be form atted or presented.\
    Therefore, if form ator functions are not stored by the receiving
    device they sha ll be regenerated by the device for subsequent
    transmission to addi tional recipients in order to preserv e data in
    tegrity. In u ni-directio nal d evices th e activ e p resentatio n p
    osition (o r th e activ e lin e, wh ere ap plicab le) is the
    reference posi tion agai nst whi ch formator funct ions are perform
    ed. In bi-directional devices certain formator functions are perform
    ed against the active da ta position (or th e activ e lin e, wh ere
    ap plicab le) in\
    the data com ponent, dependent on the setting of the DEVICE CO
    MPONENT SELECT MODE (DCSM). Formator functions are proce ssed
    depending on the setting of the FORMAT EFFECTOR ACTION MODE (FEAM )
    of t he devi ce.\
    6.4.2 Composi te graphi c characters Composite graphi c charact ers
    m ay be obt ained by usi ng form ator funct ions onl y; edi tor
    funct ions shall not be used for t his purpose (see A.2 i n annex
    A). 6.4.3 E ditor functi ons The m ain purpose of edi tor funct ions
    i s to edit, alter or t ranspose t he visual arrangem ent of dat a.\
    Editor funct ions are perform ed immediately and do not becom e part
    of t he dat a stream.\
    In uni -directional devi ces t he act ive present ation pos ition (o
    r th e activ e lin e, wh ere applicable) is the reference posi tion
    agai nst whi ch editor funct ions are performed. In b i-directio nal
    d evices certain ed itor funct ions are perform ed agai nst the
    active data position (or the active line, where applicab le) in the
    data component, depending on the setting of the DEVICE COMPONENT
    SELECT MODE (DCSM). 6.5 Selected and qualified areas This clause is
    applicable pri marily to buffered i nput/output devi ces. It may
    also be appl icable to unbuffered input/output devi ces when t he
    SEND/ RECEIVE MODE (SRM ) is set to SIM ULTANEOUS.

```{=html}
<!-- Page 33 -->
```
-   19 - 6.5.1 Selected areas A sel ected area i s a st ring of charact
    er posi tions i n t he present ation com ponent , t he contents of
    which may b e elig ible (see 7 .3.1) to b e tran smitted in th e fo
    rm o f a d ata stream o r to b e tran sferred to an auxiliary
    input/output device (see 6.6).\
    The beginning of a selected area is established by START OF SELECTED
    AREA (SSA). The character position in the presentation com ponent
    which is the active presentation position after the receipt of SSA
    is the first character positi on of the selected area.\
    The end of a selected area is established by E ND OF SELECTED AREA
    (ESA). The character position in the presentation com ponent which
    is the active pr esentation position before the receipt of ESA is
    the last character position of the selected area. The character
    positions in a line of a selected area are ordered according to the
    character path of this line. 6.5.2 Qual ified areas A qual ified
    area i s a st ring of charact er posi tions i n t he present ation
    component with which certain characteristics are associated, such as
    one or a com bination of t he fol lowing:\

a)  the contents are protected against m anual alteration;\
b)  the kind of characters which are p ermitted to b e en tered is
    restricted (fo r ex ample, to n umeric o r alphabetic characters
    only);\
c)  the contents are prot ected against erasure;\
d)  a tabulation st op is associ ated with the first character
    position;\
e)  the contents are to be excluded, i.e. guarded (see 6.5.2.2) from
    transmission as a dat a stream, or from\
    transfer to an auxiliary i nput/output device (see 6.6).\
    The beginning of a qualified area is establis hed by DEFINE AREA
    QUALIFICATION (DAQ). The character position in the presentation com
    ponent which is the active presentation position after receipt of
    DAQ is the first character position of the qualified area. The type
    of area qualifica tion is specified by the param eter value of DAQ.
    The end of a qualified area is established by the beginning of the
    following qualified area.\
    The order of the charact er posi tions i n a l ine of a qual ified
    area can be t he sam e as, or opposi te to, t he character path of
    this line. 6.5.2.1 Protected areas A protected area is a special
    case of a qualified area. It is a string of character positions, the
    contents of whi ch are prot ected agai nst manual al teration and m
    ay al so be prot ected agai nst erasure dependi ng on the setting of
    the ERASURE M ODE (ERM ). A protected area m ay, in general , be ei
    ther guarded or unguarded.\
    6.5.2.2 Guarded areas A guarded area is a special case of a
    qualified area. It is a protected area the contents of which are
    excluded from transm ission as a data stream and fro m transfer to
    an auxilia ry input/output device, depending on the setting of the
    GUARDE D AREA TRANSFER M ODE (GATM ).\
    Alternatively to using DEFINE AREA QUALIFICATION (DAQ), STAR T OF
    GUARDED AREA (SPA) com bined with END OF GUARDED AREA (EPA) can be
    used. The start of a guarded area is then established by START OF
    GUARDED AREA ( SPA). The end of the guarded area is then established
    by END OF GUARDED AREA (EPA). The character position which is the
    active presentation position after receipt of SPA is the first
    character position of the guarded area. The character position which
    is the active presentation position before the receipt of EPA is the
    last character position of the guarded area.\
    NOTE Interaction between guarded areas established by SPA and EPA,
    and those established by DAQ is not defined by t his Standard.

```{=html}
<!-- Page 34 -->
```
-   20 - 6.6 Auxiliary input/output devices This clause is applicable
    pri marily to buffered i nput/output devi ces. It may also be appl
    icable to unbuffered input/output devi ces when t he SEND/ RECEIVE
    MODE (SRM ) is set to SIM ULTANEOUS.\
    Data transfer from , or to, an auxiliary input/output device is
    initiated either by the operation of an appropriate key on a
    keyboard or by the control function MEDIA COPY (MC) appearing in the
    received data stream .\
    If there is m ore than one auxiliary input/output device, the
    relevant device is specified by the param eter value of M C.\
    An input data stream which is received from an auxilia ry device is
    processed in the sam e way as any other received data stream . The m
    ethod of terminating the input from the auxiliary device depends on
    the implementatio n.\
    6.7 Tabulation and fields Tabul ation i s t he t echni que of i
    dentifying charact er posi tions or l ines, as related to the
    present ation component, for the purpose of arrangi ng inform ation
    system atically. A ch aracter position or a line which is identified
    for t abulation is indicated by a tabulation st op. Tabul ation
    stops in the present ation component introduce fi elds and act as
    boundari es bet ween fi elds. The field i s defi ned as a st ring of
    charact er posi tions st arting at t he posi tion of the charact er
    tabulation stop (begi nning of t he fi eld) up t o, but not
    including, t he posi tion of the following charact er tabulation
    stop (end of t he fi eld). The order of charact er posi tions wi
    thin the fi eld as wel l as t he order of tabulation stops within a
    line in the present ation com ponent is determined by the charact er
    pat h of t his line. A charact er t abulation st op i s assi gned t
    o a charact er posi tion by t he cont rol funct ions C URSOR
    TABULATION CONTROL (CTC), CHARACTER TABULATION SET (HTS), TABULATION
    ALIGNED CENTRED (TAC), TABULATION ALIGNED LE ADING EDGE (TALE),
    TABULATION ALIGNED TRAILING EDGE (TATE), TABULAT ION CENTRED ON
    CHARACTER (TCC). A line tabulation stop is assigned to a line by the
    control function LINE TABULATION SET (VTS). 7 Modes 7.1 The concept
    of modes This Standard is in tended to b e ap plicab le to a v ery l
    arge range of devi ces, i n whi ch t here are vari ations. Some of t
    hese vari ations have been form alized i n t he form of m odes. They
    deal with th e way in which a device transm its, receives,
    processes, or im ages data. Each m ode has two states. The reset
    state is shown first in the definitions in 7.2. The states o f th e
    m odes m ay b e estab lished ex plicitly in th e data stream by the
    control functions SET MODE (SM) and RESET MODE (RM) or m ay be est
    ablished by agreem ent bet ween sender and reci pient. In an i
    mplementation, som e or al l of t he modes m ay have one st ate
    onl y. To en sure d ata co mpatibility an d ease o f in terch ange
    with a v ariety o f eq uipment th e use of modes is deprecated. If
    modes have to be im plemented for back ward com patibility it is r
    ecommended that the reset state of the modes be the in itial state.
    Oth erwise, ex plicit ag reements will h ave to b e n egotiated b
    etween\
    sender and reci pient, to the det riment of "bl ind" i nterchange.
    7.2 Definition of m odes The modes are set and reset by t he cont
    rol funct ions SET M ODE (SM ) and R ESET M ODE (R M). The param
    eters of SM or RM specify the m odes which are affected. In each of
    the mode definitions below, the first state is caused by RM, the
    second one by SM.\
    The m odes are l isted i n t he al phabet ical order of t heir
    acrony ms. It i s intended that the acrony ms be retain ed in all
    tran slatio ns of the tex t. See also table 6.

```{=html}
<!-- Page 35 -->
```
-   21 - Table 6 - Mode summary Acronym Reset-state\
    set-state Name Defined in BDSM EXPLICIT IMPLICIT BI-DIRECTIONAL
    SUPPORT M ODE 7.2.1 CRM CONTROL GRAPHIC CONTROL REPRESENTATION M ODE
    7.2.2 DCSM PRESENTATION DATA DEVICE COMPONENT SELECT MODE 7.2.3 ERM
    PROTECT ALL ERASURE MODE 7.2.4 FEAM EXECUTE STORE FORMAT EFFECTOR
    ACTION M ODE 7.2.5 FETM INSERT EXCLUDE FORMAT EFFECTOR TRANSFER M
    ODE 7.2.6 GATM GUARD ALL GUARDED AREA TRANSFER M ODE 7.2.7 GRCM
    REPLACING CUMULATIVE GRAPHIC RENDITION COM BINATION MODE 7.2.8 HEM
    FOLLOWING PRECEDING CHARACTER EDITING M ODE 7.2.9 IRM REPLACE INSERT
    INSERTION REPLACEM ENT M ODE 7.2.10 KAM ENABLED DISABLED KEYBOARD
    ACTION M ODE 7.2.11 MATM SINGLE MULTIPLE MULTIPLE AREA TRANSFER MODE
    7.2.12 PUM CHARACTER SIZE POSITIONING UNIT M ODE F.4.1 of annex F
    SATM SELECT ALL SELECTED AREA TRANSFER MODE 7.2.14 SRM MONITOR
    SIMULTANEOUS SEND/RECEIVE M ODE 7.2.15 SRTM NORMAL DIAGNOSTIC STATUS
    REPORT TRANSFER M ODE 7.2.16 TSM MULTIPLE SINGLE TABULATION STOP M
    ODE 7.2.17 TIM CURSOR ALL TRANSFER TERM INATION M ODE 7.2.18 VEM
    FOLLOWING PRECEDING LINE EDITING M ODE 7.2.19 ZDM ZERO DEFAULT ZERO
    DEFAULT M ODE F.4.2 of annex F

The defi nitions of t he m odes cover bi -directional de vices whi ch
have bot h a present ation component (see 6.1.1) and a dat a com ponent
(see 6.1.3). In t he case of a uni -directional devi ce or a
bi-directional device without a data com ponent, all references to
active data position, data com ponent, character progression, etc., are
t o be read as referri ng t o act ive present ation posi tion, present
ation com ponent , charact er path, etc., resp. 7.2.1 BDSM -
BI-DIRECTIONAL SUPPORT MODE EXPLICIT: Control funct ions are perform ed
i n the dat a com ponent or i n the present ation com ponent , dependi
ng on the setting of the DEVICE COMP ONENT SELECT MODE (DCSM).

```{=html}
<!-- Page 36 -->
```
-   22 - IMPLICIT: Control funct ions are perform ed i n the data
    component . Al l bi-directional aspect s of dat a are handl ed by\
    the device itself. 7.2.2 CRM - CONTROL REPRESENTATION MODE CONTROL:
    All cont rol funct ions are perform ed as defi ned; the way form
    ator funct ions are processed depends on the setting of the FORM AT
    EFFECTOR ACTION M ODE (FEAM ). A device m ay choose to im age the
    graphi cal represent ations of cont rol func tions i n addi tion to
    perform ing them.\
    GRAPHIC: All co ntrol fu nctions, ex cept RESET MODE (RM), are
    treated as graphic characters. A device m ay choose to perform som e
    control functions in add ition to storing them and imaging their
    graphical represent ations.\
    NOTE All control functions, except RM, are affected. 7.2.3 DCSM -
    DEVICE COMPONENT SELECT MODE PRESENTATION: Certain control functions
    are perform ed in the pr esentation com ponent. The active
    presentation position (or the active line, where applicab le) in the
    presentation com ponent is the reference position against which the
    rel evant cont rol funct ions are perform ed.  DATA: Certain control
    functions are perform ed in the da ta com ponent. The active data
    position (or the active line, where applicable) in the data com
    ponent is the reference pos ition against which the relevant control
    funct ions are perform ed.  NOTE Control functions af fected are: C
    PR, C R, DC H, DL, EA, ECH, ED, EF, EL, ICH, IL, LF, NEL, RI, SLH,
    SLL, SPH, SPL. 7.2.4 ERM - ERASURE MODE PROTECT: Only the cont ents
    of unprot ected areas are affect ed by an erasure cont rol funct
    ion.\
    ALL: The cont ents of prot ected as wel l as of unprot ected ar eas
    are affect ed by an erasure cont rol funct ion.\
    NOTE Control functions af fected are: EA, EC H, ED, EF, EL.\
    7.2.5 FEAM - FORMAT EFFECTOR ACTION MODE EXECUTE: Formator funct
    ions are perform ed immediately and m ay be st ored i n addi tion to
    being perform ed.\
    STORE: Formator funct ions are st ored but not perform ed. In t his
    case, t he speci fied action is intended to be performed by another
    device wh en the asso ciated data are tran smitted or tran sferred
    .\
    NOTE Control functions affected are: BPH, BS, C R, DTA, FF, FNT,
    GCC, GSM, GSS, HPA, HPB, HPR, HT, HTJ, HTS, HVP, JFY, NEL, PEC, PFS,
    PLD, PLU, PPA, PPB, PPR, PTX, QUAD, RI, SACS, SAPV, SCO, SCS, SGR,
    SHS, SLH, SLL, SLS, SPD, SPI, SPQR, SRC S, SRS, SSU, SSW, STAB, SVS,
    TAC , TALE, TATE, TBC, TCC, TSS, VPA, VPB, VPR, VTS.\
    7.2.6 FETM - FORMAT E FFECTOR TRANSFER MODE INSERT: Formator
    functions may be inserted in a d ata stream to b e tran smitted o r
    in d ata to b e tran sferred to an\
    auxiliary input/ output device.

```{=html}
<!-- Page 37 -->
```
-   23 - EXCLUDE: No form ator functions other than those recei ved
    while the FORMAT EFFECTOR ACTION MODE (FEAM) is set to STORE are
    included in a transmitted data stream or in data tran sferred to an
    au xiliary input/output devi ce.\
    NOTE No cont rol functions are af fected.\
    7.2.7 GATM - GUARDED AREA TRANSFER MODE GUARD: Only the contents of
    unguarded areas in an eligible area are transm itted or transferred.
    ALL: The contents of guarded as well as of unguarded areas in an
    eligible area are tr ansmitted or transferred.\
    NOTE No cont rol functions are af fected.\
    7.2.8 GRCM - GRAPHIC RENDI TION COMBINATION MODE REPLACING: Each
    occurrence of the control function SELEC T GRAPHIC RENDITION (SGR)
    cancels the effect of any preceding occurrence. Any gra phic
    rendition aspects that are to rem ain unchanged after an occurrence
    of SGR have t o be re-speci fied by that SGR.\
    CUMULATIVE: Each occurrence of the control function S ELECT GRAPHIC
    RENDITION (S GR) causes only those graphi c rendi tion aspect s t o
    be changed t hat are speci fied by t hat SGR . Al l ot her graphi c
    rendi tion aspect s rem ain unchanged.\
    NOTE Control function af fected is SGR.\
    7.2.9 HEM - CHARACTER EDITING MODE FOLLOWING: If the DEVICE
    COMPONENT SELECT MODE (DCSM) is set to PRESENTATION, a character
    insertion causes t he cont ents of t he act ive present ation posi
    tion and of the following charact er positions in the present ation
    com ponent t o be shi fted i n t he di rection of t he charact er
    pat h; a charact er del etion causes th e co ntents o f th e ch
    aracter p ositions fo llowing th e activ e p resentatio n position
    to be shifted in the direction opposi te to that of t he charact er
    pat h. If the DEVICE COMPONENT SELECT MODE (DCSM) is set to DATA, a
    character insertion causes the contents of the active data position
    and of t he fol lowing charact er posi tions i n the dat a com
    ponent to be shi fted i n t he di rection of t he charact er progre
    ssion; a character deletion causes the contents of the charact er
    positions fol lowing t he act ive dat a posi tion t o be shi fted in
    the di rection opposi te to that of t he character progression.
    PRECEDING: If the DEVICE COMPONENT SELECT MODE (DCSM) is set to
    PRESENTATION, a character insertion causes t he cont ents of t he
    act ive present ation posi tion and of the following charact er
    positions in the present ation com ponent t o be shi fted i n t he
    di rection opposi te t o t hat of t he charact er pat h; a character
    deletion causes the cont ents of the character positions following
    th e activ e p resentatio n position to be shi fted in the direction
    of t he charact er pat h. If the DEVICE COMPONENT SELECT MODE (DCSM)
    is set to DATA, a character insertion causes the contents of the
    active data position and of precedi ng character positions in the
    data com ponent to be shifted in t he di rection opposi te t o t hat
    of t he charact er progressi on; a charact er del etion causes t he
    contents of the character positions preceding the active data
    position to be shifted in the direction of the character
    progression.\
    NOTE Control functions af fected are: DC H, IC H.

```{=html}
<!-- Page 38 -->
```
-   24 - 7.2.10 IRM - INSE RTION REPLACEMENT MODE REPLACE: The graphi c
    sy mbol of a graphi c charact er or of a cont rol funct ion, for whi
    ch a graphi cal represent ation is required, replaces (or, dependi
    ng upon the im plementation, is combined with) the graphic sym bol
    imaged at the active presentation position.\
    INSERT: The graphi c sy mbol of a graphi c charact er or of a cont
    rol funct ion, for whi ch a graphi cal represent ation is req uired,
    is in serted at th e activ e presentatio n position.\
    NOTE Only cont rol functions f or which a graphi cal represent ation
    is requi red are af fected.\
    7.2.11 KAM - KEYBOARD ACTION MODE ENABLED: All or part of the m
    anual input f acilities are enabled to be used.\
    DISABLED: All or part of the m anual input facilities are disabled.\
    NOTE No cont rol functions are af fected.\
    7.2.12 MATM - MULTIPLE AREA TRANSFER MODE SINGLE: Only the contents
    of the selected area which contains the active pres entatio n p
    osition are elig ible to b e transmitted or tran sferred . MULTIPLE:
    The contents of all selected areas are elig ible to be tran smitted
    or tran sferred .\
    NOTE No cont rol functions are af fected.\
    7.2.13 PUM - POSIT IONING UNIT MODE\
    See F.4.1 i n annex F. 7.2.14 SATM - SELECTED AREA TRANSFER MODE
    SELECT: Only th e contents of selected areas are elig ible to be
    tran smitted or tran sferred .\
    ALL: The co ntents o f all ch aracter p ositions, irresp ectiv e o f
    any explicitly defined selected areas, are eligible to be tran
    smitted or tran sferred .\
    NOTE No cont rol functions are af fected.\
    7.2.15 SRM - SEND/RECEIVE MODE MONITOR: Data which are locally
    entered are im mediately im aged.\
    SIMULTANEOUS: Local input facilities are logically disconnected from
    the output m echanis m; only data which are sent to the device are
    im aged.\
    NOTE No cont rol functions are af fected.\
    7.2.16 SRTM - STATUS REPORT TRANSFER MODE NORMAL: Status reports in
    the form of DEVICE CONTROL STRINGs (DCS) are not generated autom
    atically .

```{=html}
<!-- Page 39 -->
```
-   25 - DIAGNOSTIC: Status reports in the form of DEVICE CONTROL ST
    RINGs (DCS) are included in every data stream\
    transmitted or tran sferred .\
    NOTE No cont rol functions are af fected.\
    7.2.17 TSM - TABULATION STOP MODE MULTIPLE: Charact er tabulation
    stops in the present ation component are set or cl eared i n t he
    act ive l ine (t he l ine that contains the active presentation
    position) and in the corresponding character positions of the
    preceding lines and of the following lines.\
    SINGLE: Charact er tabulation st ops i n the present ation com
    ponent are set or cl eared i n the act ive line onl y.\
    NOTE Control functions af fected are: C TC, DL, HTS, IL, TBC .\
    7.2.18 TTM - TRANSFER TERMINATION MODE CURSOR: Only the contents of
    the charact er positions preceding the active pres entation position
    in the presentation component are eligible to be transm itted or
    transferred.\
    ALL: The contents of character positions preceding, fo llowing, and
    at the active presentation position are eligible to be tran smitted
    or tran sferred .\
    NOTE No cont rol functions are af fected.\
    7.2.19 VEM - L INE EDITING MODE\
    FOLLOWING: If the DEVICE COMPONENT SELECT MODE (DCSM) is set to
    PRESENTATION, a line insertion causes the contents of the active lin
    e (t he l ine t hat cont ains t he act ive present ation posi tion)
    and of t he following l ines i n the present ation com ponent to be
    shi fted in the di rection of the line progressi on; a line deletion
    causes the contents of the l ines fol lowing t he act ive l ine t o
    be shi fted i n the di rection opposi te to that of t he line
    progressi on.\
    If the DEVICE COMPONENT SELECT MODE (DCSM) is set to DATA, a line
    insertion causes the contents o f th e activ e lin e (th e lin e th
    at co ntains th e activ e d ata position) and of the following lines
    in the dat a com ponent t o be shi fted i n t he di rection of t he
    l ine progressi on; a line deletion causes the contents of t he l
    ines fol lowing t he act ive l ine t o be shi fted in the direction
    opposi te to that of the line progressi on.\
    PRECEDING: If the DEVICE COMPONENT SELECT MODE (DCSM) is set to
    PRESENTATION, a line insertion causes the contents of the active lin
    e (t he l ine t hat cont ains t he act ive present ation posi tion)
    and of t he preceding lines to be shifted in the direction opposite
    to that of the line progression; a line deletion causes the contents
    of the lines preceding the active line to be shif ted in the
    direction of the line progressi on.\
    If the DEVICE COMPONENT SELECT MODE (DCSM) is set to DATA, a line
    insertion causes the contents of the active line (the line that
    contains the active data position) and of the preceding lines to be
    shifted i n the di rection opposi te to that of t he l ine progressi
    on; a l ine del etion causes the contents of the lines preceding the
    active line to be shifted in the direction of the line progression.\
    NOTE Control functions af fected are: DL, IL.\
    7.2.20 ZDM - Z ERO DEFAULT MODE See F.4.2 i n annex F.

```{=html}
<!-- Page 40 -->
```
-   26 - 7.3 Interaction between modes Four groups of m odes are speci
    fied bel ow. Each group c ontains t wo or m ore modes which interact
    with one another.\

a)  GUARDED AREA TRANSFER M ODE (GATM ), MULTIPLE AREA TRANSFER M ODE (M
    ATM), SELECTED AREA TRANSFER MODE (SATM), and TRANSFER TERMINAT ION
    MODE (TTM)\
b)  CONTROL REPRESENTATION M ODE (CRM ), and FORM AT EFFECTOR ACTION M
    ODE (FEAM )\
c)  CHARACTER EDITING M ODE (HEM ), and INSERTION REPLACEM ENT M ODE
    (IRM )\
d)  BI-DIRECTIONAL SUPPORT MODE (BDSM) , and DEVICE COMPONENT SELECT
    MODE (DCSM ) 7.3.1 GUARDED AREA TRANSFE R MODE (GATM), MULTIPLE AREA
    TRANSFER MODE (MATM), SELECTED AREA TRANSFER MODE (SATM), and
    TRANSFER TERMINATION MODE (TTM)\
    These m odes h ave a co mbined effect o n th e fo rmat o f a tran
    smitted d ata stream or of a data stream\
    transferred to an auxiliary input/output device, as described
    hereafter.\
    The t erm "act ive sel ected area" i s used t o denot e t he sel
    ected area in the present ation component\
    containing t he act ive present ation posi tion. The t erm "el
    igible" i s used for denot ing any area whi ch may be considered for
    tran smittin g or tran sferrin g.\
e)  If the TTM is set to CURSOR, the SATM to SELECT, and the MATM to
    SINGLE, then the contents of the active selected area, up to but
    excluding the activ e presentatio n position, are elig ible.\
f)  If the TTM is set to CURSOR, the SATM to SELECT, and the MATM to
    MULTIPLE, then the contents of any selected area, up to but excludi
    ng the activ e presentatio n position, are elig ible.\
g)  If the TTM is set to CURSOR and the SATM to ALL, th en th e co
    ntents o f th e b uffer u p to b ut excluding the active presentati
    on position, are elig ible.\
h)  If the TTM is set to ALL, the SATM to SELEC T, and the MATM to SING
    LE, then the com plete contents of the active sel ected area are
    eligible.\
i)  If the TTM is set to ALL, th e SATM to SELECT, and the MATM to
    MULTIPLE, then the com plete contents of all selected areas are
    eligible.\
j)  If th e TTM an d the SATM are b oth set to ALL, th en the complete
    co ntents of the buffer are elig ible.\
k)  If the GATM is set to GUARD, the contents of the eligible area or
    areas are transm itted or transferred, except for the conten ts of
    guarded areas which are co mpletely co ntained with in an\
    eligible area. In the case where a guarded area is only partly cont
    ained with in an elig ible area, th e contents of the part co
    ntained in th e elig ible area m ay b e tran smitted o r n ot, d
    epending o n th e implementatio n.\
l)  If the GATM is set to ALL, guarded as well as ungua rded data in an
    eligib le area are transm itted or transferred. If th e activ e p
    resentatio n position is n ot with in a selected area, the form at
    of the data stream in th e first and fourt h case above i s not defi
    ned by this Standard.\
    7.3.2 CONTROL REPRESENTATION MODE ( CRM) and FORMAT EFFE CTOR ACTION
    MODE (FEAM)
m)  If th e CRM is set to CONTROL, an d th e FEAM is set to EXECUTE, all
    co ntrol fu nctions are perform ed as defi ned.\
n)  If th e CRM is set to CONTROL, an d th e FEAM is set to STORE, fo
    rmator functions are treated as graphic characters.\
o)  If th e CRM is set to GRAPHIC, all co ntrol functions except RM are
    treated as graphic characters.\
    7.3.3 CHARACTER EDITING MODE (HEM) a nd INSERTION REPLACE MENT MODE
    (IRM)
p)  If the IRM is set to REPLACE, the HEM in fluences the control f
    unctions DELETE CHARACTER (DCH) and INSERT CHAR ACTER (ICH) only .

```{=html}
<!-- Page 41 -->
```
-   27 -

b)  If the IRM is set to INSERT, then , in addition, the effect of the r
    eceipt of a graphic character or a control funct ion for whi ch a
    graphi cal represent ation i s requi red, depends on t he set ting
    of t he HEM. If the HEM is set to FOLLOW ING, the im plicit movement
    of the active position is perform ed normally; if it is set to
    PRECEDING, the active position does not m ove.\
    Whether the active position referred to above is the active data
    position in the data com ponent or the active presentation position
    in the presentation component, depends on the setting of the DEVICE
    COMPONENT SELECT MODE (DCSM). 7.3.4 BI-DIRECTIONAL SUPPORT MODE (B
    DSM) a nd DEVICE COMPONENT SELECT MODE (DCSM)
c)  If the BDSM is set to EXPLICIT an d th e DCSM is set to DATA,
    certain co ntrol fu nctions are perform ed in the dat a component .
d)  If the BDSM is set to EXPLICIT and the DCSM is set to PRESENTATION,
    certain control functions are perform ed in the present ation com
    ponent . NOTE Control functions af fected are: C PR, C R, DC H, DL,
    EA, ECH, ED, EF, EL, ICH, IL , LF, NEL, RI, SLH, SLL, SPH, SPL.
e)  If t he BDSM is set to IMPLICIT, al l rel evant control funct ions
    are perform ed i n the dat a com ponent ; all bi-directional aspect
    s of t he dat a are handl ed by the devi ce i tself. The set ting of
    t he DC SM has no effect; it is co nsidered to be set to DATA (th e
    reset state). 7.4 Private modes A devi ce m ay i mplement m odes ot
    her than those speci fied in 7.2. Such m odes are called Private
    Modes. See SET M ODE (SM ) and RESET M ODE (RM ).\
    The reset state of a private m ode shall perm it the sel ection of
    coded represent ations of cont rol funct ions (including param eters
    for control of m odes) that are identified in accordance with 2.3.1
    to have the meanings specified in this Standard. 8 Control functions
    8.1 Types of control functions This Standard provi des for four t
    ypes of cont rol funct ions:
f)  Control funct ions t hat are elem ents of the C0 set
g)  Control functions that are elem ents of the C1 set
h)  C ontrol sequences
i)  Independent cont rol func tions, represent ed either

-   by ESC Fs sequences, or
-   by ESC 02/03 F sequences. There are al so several different form s
    of cont rol seque nces, vi z. wi th param eters or wi th no param
    eter. The not ations used for t he di fferent t ypes of cont rol
    funct ions and for t he di fferent form s of cont rol sequences are
    shown below. They are used in the defin itions of t he cont rol
    funct ions i n clause 8.3, and in the l isting of cont rol funct ion
    cat egori es i n cl ause 8.2. For independent control funct ions of
    t he t ype ESC\
    02/03 F no notation is in dicated as it is n ot expected that th ey
    will b e included in this Stan dard.

a)  (C0): Element of the C0 set
b)  (C1): Element of the C1 set
c)  (NP): Control sequence wi th no param eter (see F.9 i n annex F)
d)  (Pn): Control sequence wi th a si ngle num eric param eter
e)  (Pn1; Pn2): Control sequence wi th two num eric param eters

```{=html}
<!-- Page 42 -->
```
-   28 -

f)  (Pn...): Control sequence with any num ber of num eric param eters
g)  (Ps): Control sequence wi th a si ngle sel ective param eter
h)  (Ps1;Ps2): Control seq uence with two selectiv e parameters
i)  (Ps...): Control sequence with an y num ber of selective param eters
j)  (Fs): Independent cont rol funct ion, represent ed by an ESC Fs
    sequence 8.2 Categories of control functions The following list
    groups t he cont rol funct ions defi ned i n this Standard. Thi s
    groupi ng i s intended t o aid in underst anding the Standard and
    does not rest rict the use of the cont rol funct ions t o the
    indicated cat egori es. 8.2.1 Del imiters Acronym Notation Name
    Defined in APC (C1) APPLICATION PROGRAM COMMAND 8.3.2\
    CMD (Fs) CODING METHOD DELIM ITER 8.3.11\
    DCS (C1) DEVICE CONTRO L STRING 8.3.27\
    OSC (C1) OPERATING SYSTEM COMMAND 8.3.90 PM (C1) PRIVACY MESSAGE
    8.3.94 SOS (C1) START OF STRING 8.3.128 ST (C1) STRING TERMINATOR
    8.3.143 8.2.2 Introducers Acronym Notation Name Defined in CSI (C1)
    CONTROL SEQUENC E INTRODUCER 8.3.16\
    ESC (C0) ESC APE 8.3.48 SCI (C1) SINGLE CHARAC TER INTRODUCER
    8.3.109 8.2.3 Shi ft functi ons Acronym Notation Name Defined in LS0
    (C0) LOCKING-SHIFT ZERO 8.3.75\
    LS1 (C0) LOCKING-SHIFT ONE 8.3.76\
    LS1R (Fs) LOCKING-SHIFT ONE RIGHT 8.3.77\
    LS2 (Fs) LOCKING-SHIFT TWO 8.3.78\
    LS2R (Fs) LOCKING-SHIFT TWO RIGHT 8.3.79\
    LS3 (Fs) LOCKING-SHIFT THREE 8.3.80\
    LS3R (Fs) LOCKING-SHIFT THREE RIGHT 8.3.81\
    SI (C0) SHIFT-IN 8.3.119 SO (C0) SHIFT-OUT 8.3.126 SS2 (C1)
    SINGLE-SHIFT TWO 8.3.141 SS3 (C1) SINGLE-SHIFT THREE 8.3.142 8.2.4
    Format effectors Acronym Notation Name Defined in BS (C0 ) BACKSPACE
    8 .3.5\
    CR (C0) CARRIAGE RETURN 8.3.15

```{=html}
<!-- Page 43 -->
```
-   29 - FF (C 0) FOR M FEED 8.3.51\
    HPA (Pn) CHARACTER POSITION ABSOLUTE 8.3.57\
    HPB (Pn) CHARACTER POSITION BACKW ARD 8.3.58\
    HPR (Pn) CHARACTER POSITION FORW ARD 8.3.59\
    HT (C0) CHARACTER TABULATION 8.3.60\
    HTJ (C1) CHARACTER TABULATION W ITH JUSTIFICATION 8.3.61\
    HTS (C1) CHARACTER TABULATION SET 8.3.62 HVP (Pn1;Pn2) CHARACTER AND
    LINE POSITION 8.3.63\
    LF (C 0) LINE FEED 8.3.74\
    NEL (C1) NEXT LINE 8.3.86\
    PLD (C1) PARTIAL LINE FORW ARD 8.3.92\
    PLU (C1) PARTIAL LINE BACKW ARD 8.3.93\
    PPA (Pn) PAGE POSITION ABSOLUTE 8.3.96\
    PPB (Pn) PAGE POSITION BACKW ARD 8.3.97\
    PPR (Pn) PAGE POSITION FORW ARD 8.3.98 RI (C 1) R EVERSE LINE FEED
    8.3.104 TBC (Ps) TABULATION CLEAR 8.3.154 TSR (Pn) TABULATION STOP
    REMOVE 8.3.156 VPA (Pn) LINE POSITION ABSOLUTE 8.3.158 VPB (Pn) LINE
    POSITION BACKW ARD 8.3.159 VPR (Pn) LINE POSITION FORW ARD 8.3.160
    VT (C0) LINE TABULATION 8.3.161 VTS (C1) LINE TABULATION SET 8.3.162
    8.2.5 Presentati on control functi ons Acronym Notation Name Defined
    in BPH (C1) BREAK PERMITTED HERE 8.3.4\
    DTA (Pn1;Pn2) DIMENSION TEXT AREA 8.3.36\
    FNT (Ps1;Ps2) FONT SELECTION 8.3.53\
    GCC (Ps) GRAPHIC CHARACTER COM BINATION 8.3.54\
    GSM (Pn1;Pn2) GRAPHIC SIZE MODIFICATION 8.3.55 GSS (Pn) GRAPHIC SIZE
    SELECTION 8.3.56\
    JFY (Ps...) JUSTIFY 8.3.73\
    NBH (C1) NO BREAK HERE 8.3.85\
    PEC (Ps) PRESENTATION EXPAND OR CONTRACT 8.3.90\
    PFS (Ps) PAGE FORMAT SELECTION 8.3.91\
    PTX (Ps) PARALLEL TEXTS 8.3.99 QUAD (Ps...) QUAD 8.3.102 SACS (Pn)
    SET ADDITIONAL C HARACTER SEPARATION 8.3.107

```{=html}
<!-- Page 44 -->
```
-   30 - SAPV (Ps...) SELECT ALTERNATIVE PRESENTATION VARIANTS 8.3.108
    SCO (Ps) SET CHARACTER ORIENTATION 8.3.110 SCP (Ps1;Ps2) SELECT
    CHARACTER PATH 8.3.111 SCS (Pn) SET CHARAC TER SPACING 8.3.112 SDS
    (Ps) START DIRECTED STRING 8.3.114 SGR (Ps...) SELECT GRAPHIC
    RENDITION 8.3.117 SHS (Ps) SELECT CHARACTER SPACING 8.3.118 SIMD
    (Ps) SELECT IMPLICIT MOVEMENT DIRECTION 8.3.120 SLH (Pn) SET LINE
    HOME 8.3.122 SLL (Pn) SET LINE LIMIT 8.3.123 SLS (Pn) SET LINE
    SPACING 8.3.124 SPD (Ps1;Ps2) SELECT PRESENTATION DIRECTIONS 8.3.126
    SPH (Pn) SET PAGE HOME 8.3.131 SPI (Pn1;Pn2) SPACING INCREM ENT
    8.3.132 SPL (Pn) SET PAGE LIMIT 8.3.133 SPQR (Ps) SELECT PRINT
    QUALITY AND RAPIDITY 8.3.134 SRCS (Pn) SET REDUCED CHARACTER
    SEPARATION 8.3.136 SRS (Ps) START REVERSED STRING 8.3.137 SSU (Ps)
    SELECT SIZE UNIT 8.3.139 SSW (Pn) SELECT SPACE WIDTH 8.3.140 STAB
    (Ps) SELECTIVE TABULATION 8.3.144 SVS (Ps) SELECT LINE SPACING
    8.3.149 TAC (Pn) TABULATION ALIGNED CENTRED 8.3.151 TALE (Pn)
    TABULATION ALIGNED LEADING EDGE 8.3.152 TATE (Pn) TABULATION ALIGNED
    TRAILING EDGE 8.3.153 TCC (Pn1;Pn2) TABULATION CENTRED ON CHARACTER
    8.3.155 TSS (Pn) THIN SPACE SPECIFICATION 8.3.157 8.2.6 E ditor
    functi ons Acronym Notation Name Defined in DCH (Pn) DELETE
    CHARACTER 8.3.26\
    DL (Pn) DELETE LINE 8.3.32\
    EA (Ps) ERASE IN AREA 8.3.37\
    ECH (Pn) ERASE CHARACTER 8.3.38\
    ED (Ps) ERASE IN PAGE 8.3.39\
    EF (Ps) ERASE IN FIELD 8.3.40\
    EL (Ps) ERASE IN LINE 8.3.41 ICH (Pn) INSERT CHARACTER 8.3.64\
    IL (Pn) INSERT LINE 8.3.67

```{=html}
<!-- Page 45 -->
```
-   31 - 8.2.7 Cursor control functi ons Acronym Notation Name Defined
    in CBT (Pn) CURSOR BACKW ARD TABULATION 8.3.7\
    CHA (Pn) CURSOR CHARACTER ABSOLUTE 8.3.9 CHT (Pn) CURSOR FORW ARD
    TABULATION 8.3.10\
    CNL (Pn) CURSOR NEXT LINE 8.3.12\
    CPL (Pn) CURSOR PRECEDING LINE 8.3.13\
    CTC (Ps...) CURSOR TABULATION CONTROL 8.3.17\
    CUB (Pn) C URSOR LEFT 8.3.18\
    CUD (Pn) CURSOR DOWN 8.3.19\
    CUF (Pn) CURSOR RIGHT 8.3.20\
    CUP (Pn1;Pn2) CURSOR POSITION 8.3.21\
    CUU (Pn) CURSOR UP 8.3.22\
    CVT (Pn) CURSOR LINE TABULATION 8.3.23 8.2.8 Displ ay control functi
    ons Acronym Notation Name Defined in NP (Pn) NEXT PAGE 8.3.87\
    PP (Pn) PRECEDING PAGE 8.3.95\
    SD (Pn) SC ROLL DOWN 8.3.113 SL (Pn) SC ROLL LEFT 8.3.121 SR (Pn)
    SCROLL RIGHT 8.3.135 SU (Pn) SC ROLL UP 8.3.147 8.2.9 Devi ce
    control functi ons Acronym Notation Name Defined in DC1 (C0) DEVICE
    CONTROL ONE 8.3.28\
    DC2 (C0) DEVICE CONTROL TWO 8.3.29 DC3 (C0) DEVICE CONTROL THREE
    8.3.30\
    DC4 (C0) DEVICE CONTRO L FOUR 8.3.31\
    8.2.10 Informati on separators Acronym Notation Name Defined in IS1
    (C0) INFORM ATION SEPARATOR ONE 8.3.69\
    IS2 (C0) INFORM ATION SEPARATOR TWO 8.3.70\
    IS3 (C0) INFORM ATION SEPARATOR THREE 8.3.71\
    IS4 (C0) INFORM ATION SEPARATOR FOUR 8.3.72\
    NOTE Each information separator is given two names . The names,
    INFORMATION SEPARATOR FOUR (IS4) , INFORMATION SEPARATOR THREE (
    IS3), IN FORMATION SEPARATOR TWO ( IS2), and INFORMATION SEPARATOR
    ONE (IS1) are the gene ral names. The names FILE SEPARATOR (FS) ,
    GROUP SEPARATOR (GS), RECORD SEPARATOR (RS) , and UNIT SEPARATOR
    (US) are the specific names and are intended mai nly f or appl
    ications w here t he i nformation separat ors are used hierarchi
    cally. The ascendi ng order is then US, RS, GS, FS. In t his case,
    dat a normal ly del imited by a

```{=html}
<!-- Page 46 -->
```
-   32 - particular separator cannot be split by a higher-order
    separator but will be considered as delimited by any ot her hi
    gher-order separat or.\
    In ISO/IEC 10538, IS3 and IS4 are gi ven t he names PAGE TERMIN ATOR
    ( PT) and DOC UMENT TERMIN ATOR ( DT), respect ively and may be used
    t o reset present ation at tributes to the def ault state.\
    8.2.11 Area defi nition Acronym Notation Name Defined in DAQ (Ps...)
    DEFINE AREA QUALIFICATION 8.3.25\
    EPA (C1) END OF GUARDED AREA 8.3.46\
    ESA (C1) END OF SELECTED AREA 8.3.47\
    SPA (C1) START OF GUARDED AREA 8.3.129 SSA (C1) START OF SELECTED
    AREA 8.3.138 8.2.12 Mode setti ng Acronym Notation Name Defined in
    RM (Ps...) RESET MODE 8.3.106 SM (Ps...) SET MODE 8.3.125 8.2.13
    Transmi ssi on control functi ons Acronym Notation Name Defined in
    ACK (C0) ACKNOW LEDGE 8.3.1\
    DLE (C0) DATA LINK ESCAPE 8.3.33\
    ENQ (C0) ENQUIRY 8.3.44\
    EOT (C0) END OF TRANSM ISSION 8.3.45\
    ETB (C0) END OF TRANSM ISSION BLOCK 8.3.49\
    ETX (C0) END OF TEXT 8.3.50 NAK (C0) NEGATIVE ACKNOW LEDGE 8.3.84
    SOH (C0) START OF HEADING 8.3.127 STX (C0) STAR T OF TEXT 8.3.146
    SYN (C0) SYNCHRONOUS IDLE 8.3.150 8.2.14 Miscel laneous control
    functi ons Acronym Notation Name Defined in BEL (C0) BELL 8.3.3\
    CAN (C0) CANCEL 8.3.6\
    CCH (C1) CANCEL CHARACTER 8.3.8\
    CPR (Pn1;Pn2) ACTIVE POSITION REPORT 8.3.14 DA (Ps) DEVICE
    ATTRIBUTES 8.3.24\
    DMI (Fs) DISABLE MANUAL INPUT 8.3.34\
    DSR (Ps) DEVICE STATUS REPORT 8.3.35 EM (C0) END OF MEDIUM 8.3.42\
    EMI (Fs) ENABLE MANUAL INPUT 8.3.43\
    FNK (Pn) FUNCTION KEY 8.3.52\
    IDCS (Ps) IDENTIFY DEVIC E CONTROL STRING 8.3.65

```{=html}
<!-- Page 47 -->
```
-   33 - IGS (Ps) IDENTIFY GRAPHIC SUBREPERTOIRE 8.3.66\
    INT (Fs) INTERRUPT 8.3.68\
    MC (Ps) M EDIA COPY 8.3.82 MW (C1) M ESSAGE WAITING 8.3.83 NUL (C0)
    NULL 8.3.88\
    PU1 (C1) PR IVATE USE ONE 8.3.100 PU2 (C1) PR IVATE USE TWO 8.3.101
    REP (Pn) R EPEAT 8.3.103 RIS (Fs) RESET TO INITIAL STATE 8.3.105 SEE
    (Ps1;Ps2) SELECT EDITING EXTENT 8.3.115 SEF (Ps1;Ps2) SHEET EJECT
    AND FEED 8.3.116 STS (C1) SET TRANSMIT STATE 8.3.145 SUB (C0) SUB
    STITUTE 8.3.148 8.3 Definition of control functions The control
    funct ions are listed in the alphabet ical order of t heir acrony
    ms. It is intended t hat the acrony ms be retain ed in all tran
    slatio ns of the tex t. The definitions of t he cont rol funct ions
    cover bi -directional devi ces whi ch have bot h a present ation
    component (see 6.1.1) and a data com ponent (see 6.1.3). In t he
    case of a uni -directional devi ce or a bi - directional device
    without a data component, all references to activ e data position,
    data com ponent, character progression, etc., are to be read as
    referri ng t o act ive present ation posi tion, present ation
    component , charact er pat h, et c., resp. Thi s al so m eans t hat
    t he use of t he cont rol funct ions in implementations of earlier
    versi ons of t his St andard i s not affect ed by t he i nclusion of
    bi -directional capabilities in the Stan dard. 8.3.1 ACK -
    ACKNOWLEDGE Notation: (C0) Represent ation: 00/06 ACK is transm
    itted by a receiver as an affirm ative response to the sender.\
    The use of AC K is defi ned i n ISO 1745.\
    8.3.2 APC - APPLICATION PROGRAM COMMAND Notation: (C1) Represent
    ation: 09/15 or ESC 05/15 APC is used as the openi ng delimiter of a
    cont rol st ring for appl ication program use. The com mand string
    following may consi st of bit com binations i n t he range 00/ 08 t
    o 00/ 13 and 02/ 00 t o 07/ 14. The control string is closed by the
    term inating delim iter STRING TERM INATOR (ST). The interpretation
    of the com mand st ring depends on t he rel evant appl ication
    program .\
    8.3.3 BEL - BELL Notation: (C0) Represent ation: 00/07 BEL is u sed
    when there is a n eed to call fo r atten tion; it m ay control alarm
    or atten tion devices.\
    8.3.4 BPH - BREAK PERMITTED HERE Notation: (C1) Represent ation:
    08/02 or ESC 04/02 BPH is used to indicate a point where a line
    break may occur when text is form atted. BPH m ay occur between t wo
    graphi c charact ers, ei ther or bot h of whi ch may be SPAC E.

```{=html}
<!-- Page 48 -->
```
-   34 - 8.3.5 BS - B ACKSPACE\
    Notation: (C0) Represent ation: 00/08 BS causes t he act ive dat a
    posi tion t o be m oved one charact er posi tion i n t he dat a
    component in the direction opposi te to that of t he implicit
    movement.\
    The direction of the im plicit movement depends on the param eter
    value of SELECT IMPLICIT MOVEMENT DIRECTION (SIM D). 8.3.6 CAN -
    CANCEL Notation: (C0) Represent ation: 01/08 CAN is used to indicate
    that the data preceding it in th e data stream is in error. As a
    result, this data shall be ignored. The specific m eaning of this
    control function shall be defi ned for each application and/or bet
    ween sender and reci pient. 8.3.7 CBT - CURSOR BACKWARD TABULATION
    Notation: (Pn) Represent ation: CSI Pn 05/ 10 Param eter d efault
    value: Pn = 1\
    CBT causes t he act ive present ation posi tion t o be m oved t o t
    he charact er posi tion correspondi ng t o t he n-th preceding
    character tabulation stop in the pres entation com ponent, according
    to the character path, where n equals the value of Pn.\
    8.3.8 CCH - CANCEL CHARACTER Notation: (C1) Represent ation: 09/04
    or ESC 05/04\
    CCH is used to indicate that both the preceding graphi c character
    in the data stream , (represented by one or more bit com binations)
    i ncluding SPAC E, and t he cont rol funct ion C CH i tself are t o
    be i gnored for further interpretatio n of the data stream .\
    If the character preceding CCH in the data stream is a control
    function (represented by one or m ore bit combinations), t he effect
    of C CH is not defi ned by this Standard.\
    8.3.9 CHA - CURSOR CHARACTER ABSOLUTE Notation: (Pn) Represent
    ation: CSI Pn 04/ 07 Param eter d efault value: Pn = 1\
    CHA cau ses th e activ e p resentatio n position to be moved to ch
    aracter p osition n in th e activ e lin e in th e present ation com
    ponent , where n equal s the val ue of Pn.\
    8.3.10 CHT - CURSOR FORWARD TABULATION Notation: (Pn) Represent
    ation: CSI Pn 04/ 09 Param eter d efault value: Pn = 1\
    CHT causes the active present ation position to be m oved t o the
    charact er posi tion correspondi ng t o the n-th following character
    tabulation stop in the presentation com ponent, according to the
    character path, where n equals the value of Pn.\
    8.3.11 CMD - CODING METHOD DELIMITER Notatio n: (Fs) Represent
    ation: ESC 06/04\
    CMD is used as the delim iter of a string of data c oded according
    to Standard EC MA-35 and to switch to a general level of cont rol.

```{=html}
<!-- Page 49 -->
```
-   35 - The use of C MD is not mandatory if the hi gher l evel prot
    ocol defi nes m eans of del imiting t he st ring, for instance, by
    speci fying the length of t he string.\
    8.3.12 CNL - CURSOR NEX T LINE Notation: (Pn) Represent ation: CSI
    Pn 04/ 05 Param eter d efault value: Pn = 1\
    CNL cau ses th e activ e p resentatio n p osition to b e m oved to
    th e first character position of the n-th following line in the
    present ation com ponent , where n equal s the val ue of Pn. 8.3.13
    CPL - CURSOR PRECEDING LINE Notation: (Pn) Represent ation: CSI Pn
    04/ 06 Param eter d efault value: Pn = 1\
    CPL causes the activ e presentatio n position to b e m oved to th e
    first ch aracter p osition o f th e n -th preceding line in the
    presentation com ponent, where n equals the value of Pn. 8.3.14
    CPR - ACTIVE POSITION REPORT Notation: (Pn1; Pn2) Represent ation:
    CSI Pn1; Pn2 05/ 02 Param eter defaul t values: Pn1 = 1; Pn2 = 1\
    If the DEVICE COMPONENT SELECT MODE (DCSM) is set to PRESENTATION,
    CPR is used to report the active present ation position of t he
    sendi ng devi ce as resi ding i n the present ation com ponent at
    the n-th line position according to the line progression and at the
    m -th character position according to the charact er pat h, where n
    equal s the val ue of Pn1 and m equal s the val ue of Pn2. If the
    DEVICE COMPONENT SELECT MODE (DCSM) is set to DATA, CPR is used to
    report the active data position of the sending de vice as residing
    in the data co mponent at the n-th line position according to the
    line progression and at the m-th character position accord ing to
    the character progressi on, where n equal s the val ue of Pn1 and m
    equal s the val ue of Pn2. CPR m ay be solicited by a DEVICE STATUS
    REPORT (DSR) o r be sent unsolicited .\
    8.3.15 CR - CARRIAGE RETURN Notation: (C0) Represent ation: 00/13\
    The effect of CR depends on the setting of the DEVICE COMPONENT
    SELECT MODE (DCSM) and on the param eter value of SELECT IM PLICIT
    MOVEMENT DIRECTION (SIMD). If the DEVICE COMPONENT SELECT MODE
    (DCSM) is set to PRESENTATION and with the parameter value of SIMD
    eq ual to 0, CR cau ses th e activ e p resentatio n position to be
    moved to th e lin e home position of the sam e line in the
    presentation component. The line hom e position is established by
    the param eter value of SET LINE HOM E (SLH). With a parameter value
    of SIMD eq ual to 1 , CR cau ses th e activ e p resentatio n p
    osition to b e moved to\
    the line lim it position of the sam e line in the presentation com
    ponent. The line lim it position is established by the param eter
    val ue of SET LINE LIM IT (SLL). If the DEVICE COMPONENT SELECT MODE
    (DCSM) is set to DATA and with a param eter value of SIMD equal to
    0, C R causes t he act ive dat a posi tion t o be m oved t o the l
    ine hom e posi tion of t he sam e line in the data com ponent. The
    line home position is established by the param eter value of SET
    LINE HOME (SLH).\
    With a p arameter v alue o f SIMD eq ual to 1, CR cau ses th e activ
    e d ata p osition to be moved to the line limit position of the sam
    e line in the data com ponent. The line lim it position is
    established by the param eter value of SET LINE LIMIT (SLL).

```{=html}
<!-- Page 50 -->
```
-   36 - 8.3.16 CSI - CONTROL SEQUENCE INTRODUCER Notation: (C1)
    Represent ation: 09/11 or ESC 05/11\
    CSI is used as the first character of a cont rol sequence, see 5.4.\
    8.3.17 CTC - CURSOR TABULATION CONTROL\
    Notation: (Ps...) Representation: CSI Ps... 05/07 Param eter d
    efault value: Ps = 0\
    CTC causes one or m ore t abulation st ops t o be set or cl eared i
    n the present ation component , dependi ng on the parameter v
    alues:\
    0 a character tabulation stop is se t at th e activ e presentatio n
    position 1 a lin e tab ulation stop is set at th e activ e lin e (th
    e line that co ntains the activ e presentatio n position) 2 the
    character tabulation stop at the active presentation position is
    cleared 3 the line tabulation stop at the active line is cleared 4
    all character tabulation stops in the activ e lin e are cleared 5
    all character tabulation stops are cleared 6 all line tabulation
    stops are cleared In the case of param eter val ues 0, 2 or 4 t he
    num ber of l ines affect ed depends on t he set ting of t he
    TABULATION STOP M ODE (TSM ). 8.3.18 CUB - CURSOR LEFT Notation:
    (Pn) Represent ation: CSI Pn 04/ 04 Param eter d efault value: Pn =
    1\
    CUB causes the active present ation posi tion t o be m oved l
    eftwards i n t he present ation com ponent by n character positions
    if the character path i s hori zontal, or by n l ine posi tions i f
    t he charact er pat h i s vertical, where n equals the value of Pn.
    8.3.19 CUD - CURSOR DOWN Notation: (Pn) Represent ation: CSI Pn 04/
    02 Param eter d efault value: Pn = 1\
    CUD causes t he act ive present ation posi tion t o be m oved
    downwards i n the present ation com ponent by n line p ositions if
    th e ch aracter p ath is h orizontal, o r by n charact er posi tions
    i f the character path is vertical, where n equals the value of Pn.
    8.3.20 CUF - CURSOR RIGHT Notation: (Pn) Represent ation: CSI Pn 04/
    03 Param eter d efault value: Pn = 1\
    CUF causes t he act ive present ation posi tion t o be m oved ri
    ghtwards i n the present ation com ponent by n character positions
    if the character path i s hori zontal, or by n l ine posi tions i f
    t he charact er pat h i s vertical, where n equals the value of Pn.
    8.3.21 CUP - CURSOR POSITION Notation: (Pn1; Pn2) Represent ation:
    CSI Pn1; Pn2 04/ 08 Param eter defaul t values: Pn1 = 1; Pn2 = 1 CUP
    causes t he act ive present ation posi tion t o be m oved i n the
    present ation component to the n-th line position according to the
    line progression and to the m-th character position acco rding to
    the character path, where n equal s the val ue of Pn1 and m equal s
    the val ue of Pn2.

```{=html}
<!-- Page 51 -->
```
-   37 - 8.3.22 CUU - CURSOR UP Notation: (Pn) Represent ation: CSI Pn
    04/ 01 Param eter d efault value: Pn = 1\
    CUU causes t he act ive present ation posi tion t o be m oved
    upwards i n t he present ation com ponent by n line p ositions if th
    e ch aracter p ath is h orizontal, o r by n charact er posi tions i
    f the character path is vertical, where n equals the value of Pn.
    8.3.23 CVT - CURSOR LINE TABULATION Notation: (Pn) Represent ation:
    CSI Pn 05/ 09 Param eter d efault value: Pn = 1\
    CVT causes the active presentation position to be m oved to the
    corresponding character position of the line correspondi ng to the
    n-th fol lowing l ine t abulation st op i n t he present ation com
    ponent , where n equal s the val ue of Pn.\
    8.3.24 DA - DEVICE ATTRIBUTES Notatio n: (Ps) Represent ation: CSI
    Ps 06/ 03 Param eter d efault value: Ps = 0\
    With a parameter v alue n ot eq ual to 0 , DA is u sed to id entify
    th e d evice wh ich sen ds th e DA. Th e param eter value is a
    device type identification code acco rding to a register which is to
    be established. If the param eter val ue is 0, DA i s used t o
    request an i dentifying DA from a devi ce.\
    8.3.25 DAQ - DE FINE AREA QUALIFICATION Notation: (Ps...)
    Representation: CSI Ps... 06/15 Param eter d efault value: Ps = 0\
    DAQ is used to indicate that the active presentation position in the
    presentation com ponent is the first character position of a
    qualified area. The last character posi tion of t he qual ified area
    is the character position in the presentation com ponent im mediatel
    y preceding the first character position of the following qualified
    area.\
    The param eter val ue desi gnates the type of qual ified area:\
    0 unprot ected and unguarded 1 protected and guarded 2 graphi c
    charact er input 3 num eric input 4 al phabet ic input 5 input
    aligned on the last char acter position of the qualified area 6 fill
    with ZEROs 7 set a character tabulation stop at the active pres
    entation posi tion (t he fi rst charact er position of the qualified
    area) t o indicate the begi nning of a fi eld 8 protected and
    unguarded 9 fill with SPACEs 10 input aligned on the first char
    acter position of the qualified area 11 the order of the character
    positions in the input fi eld is reversed, i.e. the last position in
    each line becom es the first and vice versa; input begins at the new
    first position.

```{=html}
<!-- Page 52 -->
```
-   38 - This control function operates i ndependently of the setting of
    the TABULATION STOP MODE (TSM). The character tab ulation stop set b
    y parameter v alue 7 applies to the activ e lin e only. NOTE The
    control functions for area definition (DAQ, EPA, ESA, SPA, SSA)
    should not be used within an SRS string or an SDS st ring. 8.3.26
    DCH - DELETE CHARACTER Notation: (Pn) Represent ation: CSI Pn 05/ 00
    Param eter d efault value: Pn = 1\
    If the DEVICE COMPONENT SELECT MODE (DCSM) is set to PRESENTATION,
    DCH causes the contents of t he act ive present ation posi tion and,
    dependi ng on the setting of the CHARACTER EDITING MODE (HEM), the
    contents of the n-1 pr eceding or following character positions to
    be removed from the presentation com ponent, where n equa ls the
    value of Pn. The resulting gap is closed by shifting the contents of
    the adjacent character positions towards the active presentation
    position. At the other end of t he shi fted part , n charact er
    positions are put into the erased state. The extent of the shifted
    part is es tablished by SELECT EDITING EXTENT (SEE).\
    The effect of DCH on the start or end of a selected area, the start
    or end of a qualified area, or a tabulation st op in the shi fted
    part is not defi ned by this Standard.\
    If the DEVICE COMPONENT SELECT MODE (DCSM) is set to DATA, DCH
    causes the contents of the active data position and, depending on
    the setting of the CHARACTER EDITING M ODE (HEM ), the contents of
    the n-1 preceding or following character positions to be rem oved
    from the data component, where n equals the value of Pn. The resulti
    ng gap is closed by shifting the contents of the adjacent character
    positions towards the active data position. At the other end of the
    shifted part, n character positions are put into the erased state.
    8.3.27 DCS - DEVICE CONTROL STRING Notation: (C1) Represent ation:
    09/00 or ESC 05/00\
    DCS i s used as t he openi ng del imiter of a cont rol st ring for
    devi ce cont rol use. The command string following m ay co nsist o f
    b it co mbinations in th e range 00/08 t o 00/ 13 and 02/ 00 t o
    07/ 14. The cont rol string is closed by the term inati ng delim
    iter STRING TERM INATOR (ST).\
    The com mand string represents either one or m ore commands for the
    receiving device, or one or m ore status report s from the sendi ng
    devi ce. The purpose and the format of the command string are speci
    fied by the most recent occurrence of IDENTIFY DEVIC E CONTROL
    STRING (IDCS), if any, or depend on the sending and/or the receiving
    device. 8.3.28 DC1 - DEVICE CONTROL ONE Notation: (C0) Represent
    ation: 01/01\
    DC1 is p rimarily in tended fo r tu rning o n o r startin g an an
    cillary d evice. If it is n ot required for this purpose, i t may be
    used t o rest ore a devi ce t o t he basi c m ode of operat ion (see
    also DC2 and DC3), or any other devi ce cont rol funct ion not provi
    ded by other DC s.\
    NOTE When used for data flow control, DC1 is so metimes ca lled
    "X-ON".\
    8.3.29 DC2 - DEVICE CONTROL TWO Notation: (C0) Represent ation:
    01/02\
    DC2 is p rimarily in tended fo r tu rning o n o r startin g an an
    cillary d evice. If it is n ot required for this purpose, it may be
    used t o set a devi ce t o a speci al m ode of operat ion (i n whi
    ch case DC 1 i s used t o restore t he devi ce t o t he basi c m
    ode), or for any other devi ce cont rol funct ion not provi ded by
    other DCs.

```{=html}
<!-- Page 53 -->
```
-   39 - 8.3.30 DC3 - DEVICE CONTROL THREE Notation: (C0) Represent
    ation: 01/03\
    DC3 is prim arily intended for turning off or stoppi ng an ancillary
    device. This function m ay be a secondary l evel st op, for exam ple
    wai t, pause, st and-by or hal t (i n whi ch case DC 1 i s used to
    restore normal operat ion). If i t i s not requi red for t his
    purpos e, it may be used for any ot her devi ce cont rol funct ion
    not provi ded by other DC s.\
    NOTE When used for data flow control, DC3 is so metimes ca lled
    "X-OFF" .\
    8.3.31 DC4 - DEVICE CONTROL FOUR Notation: (C0) Represent ation:
    01/04\
    DC4 is prim arily intended for turn ing off, stopping or
    interrupting an ancillary device. If it is not requi red for this
    purpose, i t m ay be used for any other devi ce cont rol funct ion
    not provi ded by ot her DCs.\
    8.3.32 DL - DELETE LINE Notation: (Pn) Represent ation: CSI Pn 04/
    13 Param eter d efault value: Pn = 1\
    If the DEVICE COMPONENT SELECT MODE (DCSM) is set to PRESENTATION,
    DL causes the contents of the active line (the line t hat cont ains
    t he act ive present ation posi tion) and, dependi ng on t he
    setting of the LINE EDITING MODE (VEM), the contents of the n-1
    preceding or following lines to be removed from the presentation com
    ponent, where n equa ls the value of Pn. The resulting gap is closed
    by shifting the contents of a number of adjacent lines towa rds the
    active line. At the other end of the shifted part , n l ines are put
    into the erased state. The activ e presentatio n position is moved
    to the lin e h ome p osition in th e activ e lin e. Th e lin e h ome
    position is established by the param eter value of SET LINE HOM E
    (SLH). If the TABULATION STOP MODE (TSM ) is set to SINGLE,
    character tabulation st ops are cleared in the lines th at are p ut
    in to th e erased state. The extent of the shifted part is es
    tablished by SELECT EDITING EXTENT (SEE).\
    Any occurrences of the start or end of a selected area, the start or
    e nd of a qual ified area, or a t abulation stop in the shifted
    part, are also shifted .\
    If the DEVICE COMPONENT SELECT MODE (DCSM) is se t to DATA, DL
    causes the contents of the active line (the line that contains the
    active data position) and, dependi ng on t he set ting of t he LINE
    EDITING MODE (VEM), the contents of the n-1 preced ing or following
    lines to be removed from the data com ponent, where n equals the
    value of Pn. The re sulting gap is closed by shifting the contents
    of a number of adjacent lines towards the ac tive line. At the other
    end of the shifted part, n lines are put into the erased state. The
    active data position is m oved to th e lin e h ome p osition in th e
    activ e line. The line home posi tion is established by the param
    eter val ue of SET LINE HOM E (SLH). 8.3.33 DLE - DATA LINK ESCAPE
    Notation: (C0) Represent ation: 01/00\
    DLE i s used excl usively to provi de suppl ementary transmission
    cont rol funct ions.\
    The use of DLE i s defi ned i n ISO 1745.\
    8.3.34 DMI - DISABLE MANUAL INPUT Notatio n: (Fs) Represent ation:
    ESC 06/00\
    DMI causes the m anual input facilities of a device to be disabled.

```{=html}
<!-- Page 54 -->
```
-   40 - 8.3.35 DSR - DEVICE STATUS REPORT\
    Notatio n: (Ps) Represent ation: CSI Ps 06/ 14 Param eter d efault
    value: Ps = 0\
    DSR i s used ei ther t o report t he st atus of t he sendi ng devi
    ce or t o request a st atus report from the receiving device,
    depending on the param eter values:\
    0 ready , no m alfunction det ected 1 busy, anot her DSR must be
    request ed later 2 busy, an other DSR will b e sent later 3 some
    malfunction det ected, anot her DSR must be request ed later 4 some
    malfunction detected , another DSR will b e sent later 5 a DSR is
    request ed 6 a report of t he act ive present ation posi tion or of
    t he act ive dat a posi tion i n t he form of ACTIVE POSITION REPORT
    (CPR) is requested\
    DSR with param eter val ue 0, 1, 2, 3 or 4 may be sent either unsol
    icited or as a response t o a request such as a DSR with a param
    eter value 5 or M ESSAGE W AITING (M W).\
    8.3.36 DTA - DIMENSION TEX T AREA Notation: (Pn1; Pn2) Represent
    ation: CSI Pn1; Pn2 02/ 00 05/ 04 No param eter default value.\
    DTA i s used t o establish the dimensions of t he text area for
    subsequent pages.\
    The estab lished dimensions remain in effect u ntil th e next
    occurrence of DTA in the data stream .\
    Pn1 speci fies the dimension in the direction perpendi cular to the
    line ori entation Pn2 specifies th e dimension in the directio n
    parallel to the lin e orientation The unit in which the param eter
    value is expressed is that established by the param eter value of
    SELECT SIZE UNIT (SSU).\
    8.3.37 EA - ERASE IN AREA Notatio n: (Ps) Represent ation: CSI Ps
    04/ 15 Param eter d efault value: Ps = 0\
    If the DEVICE COMPONENT SELECT MODE (DCSM) is set to PRESENTATION,
    EA causes som e or all charact er positions i n t he act ive qual
    ified area (t he qual ified area i n t he present ation com ponent\
    which contains the active present ation posi tion) t o be put i nto
    t he erased st ate, dependi ng on t he parameter v alues:\
    0 the active present ation position and the charact er posi tions up
    t o the end of t he qual ified area are put\
    into the erased state 1 the charact er posi tions from t he begi
    nning of t he qual ified area up to and including the active
    presentation position are put into the erased state 2 all charact er
    posi tions of t he qual ified area are put into the erased state\
    If the DEVICE COMPONENT SELECT MODE (DCSM) is set to DATA, EA causes
    som e or all charact er posi tions i n the act ive qual ified area
    (t he qual ified area i n the dat a component which contains the act
    ive dat a posi tion) t o be put into the erased st ate, dependi ng
    on t he param eter val ues: 0 the act ive dat a posi tion and t he
    charact er posi tions up t o the end of t he qual ified area are put
    into the erased state

```{=html}
<!-- Page 55 -->
```
-   41 - 1 the charact er posi tions from t he begi nning of t he qual
    ified area up to and including the active data position are put into
    the erased state 2 all charact er posi tions of t he qual ified area
    are put into the erased state Whether the character positions of
    protected areas are put into the erased state, or the character
    positions of unprotected areas only, depends on the setting of the
    ERASURE MODE (ERM).\
    8.3.38 ECH - ERASE CHARACTER Notation: (Pn) Represent ation: CSI Pn
    05/ 08 Param eter d efault value: Pn = 1\
    If the DEVICE COMPONENT SELECT MODE (DCSM) is set to PRESENTATION,
    ECH causes the active present ation position and t he n-1 fol lowing
    charact er posi tions i n t he present ation com ponent t o be put
    into the erased state, wh ere n equals the value of Pn.\
    If the DEVICE COMPONENT SELECT MODE (DCSM) is set to DATA, ECH
    causes the active data position and t he n-1 fol lowing charact er
    posi tions i n the dat a com ponent to be put into the erased state,
    where n equals the value of Pn. Whether the character positions of
    protected areas are put into the erased state, or the character
    positions of unprotected areas only, depends on the setting of the
    ERASURE MODE (ERM).\
    8.3.39 ED - E RASE IN PAGE\
    Notatio n: (Ps) Represent ation: CSI Ps 04/ 10 Param eter d efault
    value: Ps = 0\
    If the DEVICE COMPONENT SELECT MODE (DCSM) is set to PRESENTATION,
    ED causes som e or all charact er posi tions of t he act ive page (t
    he page whi ch cont ains t he act ive present ation posi tion in the
    present ation com ponent ) to be put into the erased st ate, dependi
    ng on t he param eter val ues:\
    0 the active present ation posi tion and t he charact er posi tions
    up t o the end of t he page are put into the erased state 1 the
    charact er positions from t he begi nning of t he page up t o and i
    ncluding t he act ive present ation position are put into the erased
    state 2 all charact er posi tions of t he page are put into the
    erased state\
    If the DEVICE COMPONENT SELECT MODE (DCSM) is set to DATA, ED causes
    som e or all charact er posi tions of t he act ive page (t he page
    wh ich cont ains t he act ive dat a position in the data component )
    to be put into the erased st ate, dependi ng on t he param eter val
    ues: 0 the act ive dat a posi tion and t he charact er posi tions up
    to the end of t he page are put into the erased state 1 the charact
    er positions from the begi nning of t he pa ge up t o and i ncluding
    t he act ive dat a posi tion are put into the erased state 2 all
    charact er posi tions of t he page are put into the erased state
    Whether the character positions of protected areas are put into the
    erased state, or the character positions of unprotected areas only,
    depends on the setting of the ERASURE MODE (ERM).\
    8.3.40 EF - ERASE IN FIELD Notatio n: (Ps) Represent ation: CSI Ps
    04/ 14 Param eter d efault value: Ps = 0\
    If the DEVICE COMPONENT SELECT MODE (DCSM) is set to PRESENTATION,
    EF causes som e or all character positions of the active field (the
    field whi ch cont ains t he act ive present ation posi tion i n the
    present ation com ponent ) to be put into the erased st ate, dependi
    ng on t he param eter val ues:

```{=html}
<!-- Page 56 -->
```
-   42 - 0 the active present ation position and the charact er posi
    tions up t o the end of t he fi eld are put into the erased state 1
    the charact er posi tions from t he begi nning of t he fi eld up to
    and including the active present ation position are put into the
    erased state 2 all character positions of the fiel d are put into
    the erased state\
    If the DEVICE COMPONENT SELECT MODE (DCSM) is set to DATA, EF causes
    som e or all charact er positions of the active field (the fi eld
    whi ch cont ains t he act ive dat a posi tion i n t he dat a
    component ) to be put into the erased st ate, dependi ng on t he
    param eter val ues: 0 the act ive dat a posi tion and t he charact
    er posi tions up to the end of the field are put into the erased
    state 1 the charact er positions from the beginning of the field up
    t o and i ncluding t he act ive dat a posi tion are put into the
    erased state 2 all character positions of the fiel d are put into
    the erased state Whether the character positions of protected areas
    are put into the erased state, or the character positions of
    unprotected areas only, depends on the setting of the ERASURE MODE
    (ERM).\
    8.3.41 EL - ERASE IN LINE Notatio n: (Ps) Represent ation: CSI Ps
    04/ 11 Param eter d efault value: Ps = 0\
    If the DEVICE COMPONENT SELECT MODE (DCSM) is set to PRESENTATION,
    EL causes som e or all character positions of the activ e lin e (th
    e lin e wh ich co ntains th e active presentation position in the
    present ation com ponent ) to be put into the erased st ate, dependi
    ng on t he param eter val ues:\
    0 the active presentation position and the character pos itions up t
    o t he end of t he line are put into the erased state 1 the charact
    er posi tions from t he begi nning of t he l ine up to and including
    the active present ation position are put into the erased state 2
    all character positions of the line are put into the erased state\
    If the DEVICE COMPONENT SELECT MODE (DCSM) is set to DATA, EL causes
    some or all character p ositions o f th e activ e lin e (th e lin e
    wh ich co ntains th e activ e d ata p osition in th e d ata
    component ) to be put into the erased st ate, dependi ng on t he
    param eter val ues: 0 the active dat a posi tion and t he charact er
    posi tions up to th e en d o f th e lin e ar e put into the erased
    state 1 the charact er posi tions from the begi nning of t he line
    up t o and i ncluding t he act ive dat a posi tion are put into the
    erased state 2 all character positions of the lin e are put into the
    erased state Whether the character positions of protected areas are
    put into the erased state, or the character positions of unprotected
    areas only, depends on the setting of the ERASURE MODE (ERM).\
    8.3.42 EM - E ND OF ME DIUM Notation: (C0) Represent ation: 01/09\
    EM is used to identify the phy sical end of a m edium, or t he end
    of t he used port ion of a m edium, or t he end of t he want ed port
    ion of dat a recorded on a m edium.\
    8.3.43 EMI - ENABLE MANUAL INPUT Notatio n: (Fs) Represent ation:
    ESC 06/02\
    EMI is used to enable the m anual input facilities of a device.

```{=html}
<!-- Page 57 -->
```
-   43 - 8.3.44 ENQ - E NQUIRY Notation: (C0) Represent ation: 00/05\
    ENQ is transm itted by a sender as a re quest for a response from a
    receiver.\
    The use of ENQ i s defi ned i n ISO 1745.\
    8.3.45 EOT - END OF TRANSMISSION Notation: (C0) Represent ation:
    00/04\
    EOT i s used t o indicate the concl usion of t he transmission of
    one or m ore texts.\
    The use of EOT i s defi ned i n ISO 1745.\
    8.3.46 EPA - END OF GUARDED AREA Notation: (C1) Represent ation:
    09/07 or ESC 05/07\
    EPA is used to indicate that the active present ation posi tion i s
    the l ast of a st ring of charact er posi tions in t he present
    ation com ponent , t he cont ents of whi ch are protected against
    manual alteration, are guarded against transm ission or transfer,
    depending on the setting of the GUARDED AREA TRANSFER MODE (GATM),
    and m ay be protected against er asure, depending on the setting of
    the ERASURE MODE (ERM ). The beginning of this string is indicated
    by START OF GUARDED AREA (SPA).\
    NOTE The control functions for area definition ( DAQ, EPA, ESA, SPA,
    SSA) should not be used within an SRS string or an SDS st ring.
    8.3.47 ESA - END OF SELECTED AREA Notation: (C1) Represent ation:
    08/07 or ESC 04/07\
    ESA is used to indicate that the active present ation posi tion i s
    the l ast of a st ring of charact er posi tions in the presentation
    com ponent, the contents of which ar e eligible to be transm itted
    in the form of a data stream or transferred to an aux iliary
    input/output device. The beginning of this string is indicated by
    START OF SELECTED AREA (SSA).\
    NOTE The control function for area definition (DAQ, EPA, ESA, SPA,
    SSA) should not be used within an SRS string or an SDS st ring.
    8.3.48 ESC - E SCAPE\
    Notation: (C0) Represent ation: 01/11\
    ESC is used for code ext ension purposes. It causes the meanings of
    a l imited num ber of bi t combinations following it in the data
    stream to be changed.\
    The use of ESC is defi ned i n Standard EC MA-35.\
    8.3.49 ETB - END OF TRANSMISSION BLOCK Notation: (C0) Represent
    ation: 01/07\
    ETB i s used t o i ndicate t he end of a bl ock of dat a where the
    data are divided into such blocks for transmission purposes.\
    The use of ETB is defi ned i n ISO 1745.\
    8.3.50 ETX - END OF TEX T Notation: (C0) Represent ation: 00/03

```{=html}
<!-- Page 58 -->
```
-   44 - ETX is used to indicate the end of a text.\
    The use of ETX i s defi ned i n ISO 1745.\
    8.3.51 FF - FORM FE ED Notation: (C0) Represent ation: 00/12\
    FF causes the active presentation position to be m oved to the
    corresponding character position of the line at t he page hom e posi
    tion of t he next form or page i n t he present ation component .
    The page home position is established by the param eter val ue of
    SET PAGE HOM E (SPH). 8.3.52 FNK - FUNCTION KEY Notation: (Pn)
    Represent ation: CSI Pn 02/ 00 05/ 07 No param eter default value.\
    FNK is a co ntrol fu nction in wh ich th e p arameter v alue id
    entifies th e function key which has been operat ed.\
    8.3.53 FNT - FONT SELECTION Notatio n: (Ps1 ;Ps2) Represent ation:
    CSI Ps1; Ps2 02/ 00 04/ 04 Param eter defaul t values: Ps1 = 0; Ps2
    =0\
    FNT is u sed to id entify th e character font to be selected as
    primary or al ternative font by subsequent\
    occurrences of SELECT GRAPHIC RENDITION (SGR) in the data stream .
    Ps1 specifies the prim ary or alternative font concerned:\
    0 primary font\
    1 first altern ative font\
    2 second al ternative font\
    3 third altern ative font\
    4 fourth altern ative font\
    5 fifth alternative font\
    6 sixth alternative font\
    7 sevent h alternative font\
    8 eighth alternative font\
    9 ninth alternative font\
    Ps2 identifies the character font according to a register which is
    to be established.\
    8.3.54 GCC - GRAPHIC CHARACTER COMBINATION Notatio n: (Ps) Represent
    ation: CSI Ps 02/ 00 05/ 15 Param eter d efault value: Ps = 0\
    GCC i s used t o i ndicate t hat t wo or m ore graphi c characters
    are to be im aged as one single graphic symbol. GC C wi th a param
    eter val ue of 0 i ndicates that th e fo llowing two g raphic
    characters are to be imaged as one si ngle graphi c sy mbol; GCC
    with a param eter val ue of 1 and GC C with a param eter value of 2
    indicate respect ively t he begi nning and t he end of a st ring of
    graphi c charact ers whi ch are t o be imaged as one si ngle graphi
    c symbol.\
    NOTE GCC does not explicitly specify the relative sizes or pl
    acements of the component parts of a composite graphi c symbol . In
    the simplest case, t wo component s may be "hal f-width" and si
    de-by-si de. For

```{=html}
<!-- Page 59 -->
```
-   45 - exampl e, in Japanese t ext a pai r of charact ers may be
    present ed si de-by-si de, and occupy t he space of a normal -size
    Kanji charact er.\
    8.3.55 GSM - GRAPHIC SIZ E MODIFICATION Notation: (Pn1; Pn2)
    Represent ation: CSI Pn1; Pn2 02/ 00 04/ 02 Param eter defaul t
    values: Pn1 = 100; Pn2 = 100\
    GSM i s used t o m odify for subsequent t ext t he hei ght and/or t
    he wi dth of al l pri mary and al ternative fonts identified by FONT
    SELECTION (FNT) and established by GRAPHIC SIZE SELECTION (GSS). The
    estab lished values rem ain in effect u ntil th e next occurrence of
    GSM o r GSS in the data steam .\
    Pn1 speci fies the hei ght as a percent age of t he hei ght
    established by GSS Pn2 speci fies the width as a percent age of t he
    width est ablished by GSS 8.3.56 GSS - GRAPHIC SIZ E SELECTION
    Notation: (Pn) Represent ation: CSI Pn 02/ 00 04/ 03 No param eter
    default value.\
    GSS i s used t o est ablish for subsequent text the hei ght and t he
    wi dth of al l pri mary and al ternative font s identified by FONT
    SELECTION (FNT). The establis hed values rem ain in effect until the
    next occurrence of GSS in the data stream .\
    Pn specifies th e height, the wid th is im plicitly d efined by the
    height.\
    The unit in which the param eter value is expressed is that
    established by the param eter value of SELECT SIZE UNIT (SSU).\
    8.3.57 HPA - CHARACTER POSITION ABSOLUTE Notation: (Pn) Represent
    ation: CSI Pn 06/ 00 Param eter d efault value: Pn = 1\
    HPA causes th e activ e data p osition to be moved to character p
    osition n in the activ e lin e (th e lin e in the data com ponent
    that contains the active data position), where n equals the value of
    Pn.\
    8.3.58 HPB - CHARACTER POSITION BACKWARD Notation: (Pn) Represent
    ation: CSI Pn 06/ 10 Param eter d efault value: Pn = 1\
    HPB causes the active data position t o be m oved by n charact er
    posi tions i n t he dat a com ponent i n t he direction opposi te to
    that of t he charact er progressi on, where n equal s the val ue of
    Pn.\
    8.3.59 HPR - CHARACTER POSITION FORWARD Notation: (Pn) Represent
    ation: CSI Pn 06/ 01 Param eter d efault value: Pn = 1\
    HPR causes the active data position t o be m oved by n charact er
    posi tions i n t he dat a com ponent i n t he direction of t he
    charact er progressi on, where n equal s the val ue of Pn.\
    8.3.60 HT - CHARACTER TABULATION Notation: (C0) Represent ation:
    00/09\
    HT causes the act ive present ation posi tion t o be m oved t o the
    fol lowing charact er t abulation st op i n the present ation com
    ponent .

```{=html}
<!-- Page 60 -->
```
-   46 - In addition, if that following character tabulation stop has
    been set by TABULATION ALIGN CENTRE (TAC), TABULATION ALIGN LEADING
    EDGE (T ALE), TABULATION ALIGN TRAILING EDGE (TATE) or TABULATION
    CENTRED ON CHARACTER (T CC), HT indicates the beginning of a string
    of text which is to be positioned w ithin a line according to the
    properties of that tabulation stop. The end of the string is
    indicated by th e next occurrence of HT or CARRIAGE RETURN (CR) or
    NEXT LINE (NEL) in the data stream .\
    8.3.61 HTJ - CHARACTER TABULATION WITH JUSTIFICATION Notation: (C1)
    Represent ation: 08/09 or ESC 04/09\
    HTJ causes the contents of the active fi eld (t he fi eld i n t he
    present ation com ponent t hat cont ains t he active presentation
    position) to be shifted forward so that it ends at the character
    position preceding the following charact er t abulation st op. The
    act ive present ation posi tion i s moved to that following charact
    er tabulation stop. The character positions which precede the
    beginning of the shifted string are put into the erased state.\
    8.3.62 HTS - CHARACTER TABULATION SET Notation: (C1) Represent
    ation: 08/08 or ESC 04/08\
    HTS causes a character tabulation stop to be set at th e activ e p
    resentatio n p osition in th e p resentatio n component .\
    The num ber of lines affected depends on the se tting of the
    TABULATION STOP M ODE (TSM ).\
    8.3.63 HVP - CHARACTER AND LINE POSITION Notation: (Pn1; Pn2)
    Represent ation: CSI Pn1; Pn2 06/ 06 Param eter defaul t values: Pn1
    = 1; Pn2 = 1\
    HVP causes the active data position to be m oved in the data com
    ponent to the n-th line position according to the line progression
    and to the m -th character position accord ing to the character
    progressi on, where n equal s the val ue of Pn1 and m equal s the
    val ue of Pn2.\
    8.3.64 ICH - INSERT CHARACTER Notation: (Pn) Represent ation: CSI Pn
    04/ 00 Param eter d efault value: Pn = 1\
    If the DEVICE COMPONENT SELECT MODE (DCSM) is set to PRESENTATION,
    ICH is used to prepare the insertion of n character s, by putting
    into the erased stat e the active present ation posi tion and,
    depending on the setting of the CHARACTER EDITING MODE (HEM), the
    n-1 preceding or following charact er positions in the present ation
    com ponent , where n equal s the val ue of Pn. The previ ous cont
    ents of the active presentation position and an adjacent string of
    character positions are shifted away from the active present ation
    posi tion. The cont ents of n charact er posi tions at the ot her
    end of the shifted part are removed. The activ e presentatio n
    position is m oved to the lin e home position in the activ e lin e.
    Th e lin e home posi tion is established by the param eter val ue of
    SET LINE HOM E (SLH). The extent of the shifted part is es tablished
    by SELECT EDITING EXTENT (SEE).\
    The effect of ICH on the start or end of a selected area, the start
    or end of a qualified area, or a tabulation st op in the shi fted
    part , is not defi ned by this Standard.\
    If the DEVICE COMPONENT SELECT MODE (DCSM) is set to DATA, ICH is
    used to prepare the insertion of n charact ers, by putting into the
    erased st ate t he act ive dat a posi tion and, dependi ng on t he
    setting of the CHARACTER EDIT ING MODE (HEM), the n-1 preceding or
    following character positions in the dat a component , where n equal
    s the val ue of Pn. The previ ous cont ents of t he act ive dat a
    position and an adj acent string of character positions are shifted
    away from the active data position. The contents of n charact er
    positions at the ot her end of t he shi fted part are rem oved. The
    act ive dat a

```{=html}
<!-- Page 61 -->
```
-   47 - position is moved to the line home position in th e activ e
    lin e. Th e lin e h ome p osition is estab lished b y the param eter
    value of SET LINE HOM E (SLH). 8.3.65 IDCS - IDENTIFY DEVICE CONTROL
    STRING Notatio n: (Ps) Represent ation: CSI Ps 02/ 00 04/ 15 No
    param eter default value.\
    IDCS i s used t o speci fy t he purpose and form at of the command
    string of subsequent DEVIC E CONTROL STRINGs (DCS). The specified
    purpose a nd form at rem ain in effect until the next occurrence of
    IDCS in the data stream .\
    The param eter values are\
    1 reserved for use with the DIAGNOSTIC state of the STATUS REPORT
    TRANSFER M ODE (SRTM ) 2 reserved for Dynam ically Rede finable
    Character Sets (DRCS) acco rding to Standard ECMA-35. The form at
    and i nterpret ation of t he com mand st ring correspondi ng t o t
    hese param eter val ues are t o be defined in appropri ate st
    andards. If t his cont rol funct ion i s used t o identify a pri
    vate com mand st ring, a private param eter val ue shal l be used.\
    8.3.66 IGS - IDENTIFY GRAPHIC SUBREPERTOIRE Notatio n: (Ps)
    Represent ation: CSI Ps 02/ 00 04/ 13 No param eter default value.
    IGS i s used t o i ndicate t hat a repert oire of t he graphi c
    charact ers of ISO/IEC 10367 is used in the subsequent text.\
    The param eter value of IGS identifies a graphic ch aracter
    repertoire regist ered in accordance with ISO/IEC 7350.\
    8.3.67 IL - INSE RT LINE Notation: (Pn) Represent ation: CSI Pn 04/
    12 Param eter d efault value: Pn = 1\
    If the DEVICE COMPONENT SELECT MODE (DCSM) is set to PRESENTATION,
    IL is used to prepare the insertion of n l ines, by put ting i nto
    the erased st ate i n the present ation com ponent the act ive line
    (the line that contains the active present ation posi tion) and,
    dependi ng on t he set ting of t he LINE EDITING MODE (VEM), the n-1
    preceding or following lines, where n equals the value of Pn. The
    previous contents of the active line and of adjacent lines are
    shifted away from the active line. The contents of n lines at the
    other end of t he shi fted part are rem oved. The act ive present
    ation posi tion i s moved to the line h ome p osition in th e activ
    e lin e. Th e lin e h ome p osition is estab lished b y th e param
    eter value of SET LINE HOM E (SLH). The extent of the shifted part
    is es tablished by SELECT EDITING EXTENT (SEE).\
    Any occurrences of the start or end of a selected area, the start or
    e nd of a qual ified area, or a t abulation stop in the shifted
    part, are also shifted .\
    If the TABULATION STOP M ODE (TSM ) is set to S INGLE, character
    tabulation stops are cleared in the lines that are put in to the
    erased state. If the DEVICE COMPONENT SELECT MODE (DCSM) is set to
    DATA, IL is used to prepare the insertion of n l ines, by put ting i
    nto t he erased st ate i n the data component the active line (the
    line that contains the active data position) and, dependi ng on the
    setting of the LINE EDITING M ODE (VEM ), the n-1 preceding or
    following lines, where n equals the value of Pn. The previous
    contents of the active line and of adjacent lines ar e shifted away
    from the activ e line. The contents of n lines at the other end of
    the shi fted part are rem oved. The act ive dat a posi tion i s
    moved t o the line hom e posi tion i n the act ive line. Th e lin e
    home position is estab lished by the parameter v alue of SET LINE
    HOME (SLH).

```{=html}
<!-- Page 62 -->
```
-   48 - 8.3.68 INT - INTERRUPT Notatio n: (Fs) Represent ation: ESC
    06/01\
    INT is used to indicate to the receiving device that the current
    process is to be interrupted and an agreed procedure is to be
    initiated . This co ntrol function is ap plicab le to eith er
    directio n of tran smissio n.\
    8.3.69 IS1 - INFORMATION SEPARAT OR ONE (US - UNIT SEPARATOR)
    Notation: (C0) Represent ation: 01/15\
    IS1 is used to separate and qualify data logically ; its specific m
    eaning has to be defined for each applicatio n. If th is co ntrol fu
    nction is u sed in hierarch ical o rder, it m ay delimit a data item
    called a unit, see 8.2.10.\
    8.3.70 IS2 - INFORMATION SEPARAT OR TWO (RS - RECORD SEPARATOR)
    Notation: (C0) Represent ation: 01/14\
    IS2 is used to separate and qualify data logically ; its specific m
    eaning has to be defined for each applicatio n. If th is co ntrol fu
    nction is u sed in h ierarch ical o rder, it m ay d elimit a d ata
    item called a record, see 8.2.10.\
    8.3.71 IS3 - INFORMATION SEPARATOR THREE (GS - GROUP SEPARATOR)
    Notation: (C0) Represent ation: 01/13\
    IS3 is used to separate and qualify data logically ; its specific m
    eaning has to be defined for each applicatio n. If th is co ntrol fu
    nction is u sed in h ierarch ical o rder, it m ay d elimit a d ata
    item called a group, see 8.2.10.\
    8.3.72 IS4 - INFORMATION SEPARAT OR FOUR (FS - FILE SEPARATOR)
    Notation: (C0) Represent ation: 01/12\
    IS4 is used to separate and qualify data logically ; its specific m
    eaning has to be defined for each application. If t his cont rol
    funct ion i s used i n hi erarchical o rder, it m ay d elimit a d
    ata item called a file, see 8.2.10.\
    8.3.73 JFY - JUST IFY Notation: (Ps...) Representation: CSI Ps...
    02/00 04/06 Param eter d efault value: Ps = 0\
    JFY i s used t o indicate the begi nning of a st ring of graphi c
    charact ers in the present ation component that are to be justified
    according to the layout sp ecified by the param eter values, see
    annex C:\
    0 no justification, end of jus tification of preceding text\
    1 word fill\
    2 word space\
    3 letter space\
    4 hy phenat ion\
    5 flush t o line hom e posi tion margin\
    6 centre b etween line home position and line lim it position
    margins 7 flush to line lim it position margin\
    8 Italian hyphenat ion\
    The end of t he string to be just ified is indicated by the next
    occurrence of JFY i n the dat a stream.

```{=html}
<!-- Page 63 -->
```
-   49 - The lin e home position is estab lished by the parameter v alue
    of SET LINE HOME (SLH). The line limit position is established by
    the param eter val ue of SET LINE LIM IT (SLL).\
    8.3.74 LF - L INE FE ED Notation: (C0) Represent ation: 00/10\
    If the DEVICE COMPONENT SELECT MODE (DCSM) is set to PRESENTATION,
    LF causes the active presentation position to be m oved to the co
    rresponding character position of the following line in the present
    ation com ponent . If the DEVICE COMPONENT SELECT MODE (DCSM) is set
    to DATA, LF causes the active data position to be m oved to the
    corresponding charact er position of the following line in the data
    component . 8.3.75 LS0 - L OCKING-SHIFT ZERO Notation: (C0)
    Represent ation: 00/15\
    LS0 i s used for code ext ension purposes. It causes t he m eanings
    of t he bi t com binations fol lowing i t in the dat a stream to be
    changed.\
    The use of LS0 i s defi ned i n Standard EC MA-35.\
    NOTE LS0 i s used i n 8-bi t envi ronment s only; in 7-bi t envi
    ronment s SHIFT-IN (SI) is used i nstead.\
    8.3.76 LS1 - L OCKING-SHIFT ONE\
    Notation: (C0) Represent ation: 00/14\
    LS1 i s used for code ext ension purposes. It causes t he m eanings
    of t he bi t com binations fol lowing i t in the dat a stream to be
    changed.\
    The use of LS1 i s defi ned i n Standard EC MA-35.\
    NOTE LS1 is used in 8-bit environments only; in 7-bit environments
    SHIFT-OUT ( SO) is used instead.\
    8.3.77 LS1R - L OCKING-SHIFT ONE RIGHT\
    Notatio n: (Fs) Represent ation: ESC 07/14\
    LS1R is used for code ext ension purposes. It causes t he meanings
    of t he bi t com binations fol lowing i t in the dat a stream to be
    changed.\
    The use of LS1R is defi ned i n Standard EC MA-35. 8.3.78 LS2 - L
    OCKING-SHIFT TWO Notatio n: (Fs) Represent ation: ESC 06/14\
    LS2 i s used for code ext ension purposes. It causes t he m eanings
    of t he bi t com binations fol lowing i t in the dat a stream to be
    changed.\
    The use of LS2 i s defi ned i n Standard EC MA-35.\
    8.3.79 LS2R - L OCKING-SHIFT TWO RIGHT\
    Notatio n: (Fs) Represent ation: ESC 07/13\
    LS2R is used for code ext ension purposes. It causes t he meanings
    of t he bi t com binations fol lowing i t in the dat a stream to be
    changed.\
    The use of LS2R is defi ned i n Standard EC MA-35.

```{=html}
<!-- Page 64 -->
```
-   50 - 8.3.80 LS3 - LOCKING-SHIFT THREE Notatio n: (Fs) Represent
    ation: ESC 06/15\
    LS3 i s used for code ext ension purposes. It causes t he m eanings
    of t he bi t com binations fol lowing i t in the dat a stream to be
    changed.\
    The use of LS3 i s defi ned i n Standard EC MA-35.\
    8.3.81 LS3 R - LOCKING-SHIFT THREE RIGHT Notatio n: (Fs) Represent
    ation: ESC 07/12\
    LS3R is used for code ext ension purposes. It causes t he meanings
    of t he bi t com binations fol lowing i t in the dat a stream to be
    changed.\
    The use of LS3R is defi ned i n Standard EC MA-35.\
    8.3.82 MC - ME DIA COPY Notatio n: (Ps) Represent ation: CSI Ps 06/
    09 Param eter d efault value: Ps = 0\
    MC is used either to initia te a transfer of data from or to an aux
    iliary input/output devi ce or to enable or disable the relay of the
    received data stream to an auxiliary input/output device, depending
    on the param eter value:\
    0 initiate tran sfer to a primary au xiliary d evice\
    1 initiate tran sfer fro m a p rimary au xiliary d evice\
    2 initiate transfer to a secondary auxiliary device\
    3 initiate transfer from a secondary auxiliary device\
    4 stop relay to a primary au xiliary d evice\
    5 start relay to a primary au xiliary d evice\
    6 stop relay to a secondary auxiliary device\
    7 start relay to a secondary auxiliary device\
    This co ntrol function may not be used to switch on or off an
    auxiliary d evice.\
    8.3.83 MW - ME SSAGE WAIT ING Notation: (C1) Represent ation: 09/05
    or ESC 05/05\
    MW is used to set a message waiting indicator in the receiving
    device. An a ppropriate acknowledgem ent to the receipt of MW may be
    given by using DEVICE STATUS REPORT (DSR). 8.3.84 NAK - NEGATIVE
    ACKNOWLEDGE Notation: (C0) Represent ation: 01/05\
    NAK is transm itted by a receiver as a negative response to the
    sender.\
    The use of NAK is defined in ISO 1745.\
    8.3.85 NBH - NO B REAK HE RE Notation: (C1) Represent ation: 08/03
    or ESC 04/03\
    NBH is used to indicate a point where a line break shall not occur
    when text is form atted. NBH m ay occur bet ween t wo graphi c
    charact ers ei ther or bot h of whi ch may be SPAC E.

```{=html}
<!-- Page 65 -->
```
-   51 - 8.3.86 NEL - NE XT LINE Notation: (C1) Represent ation: 08/05
    or ESC 04/05\
    The effect of NEL depends on the setting of the DEVICE COMPONENT
    SELECT MODE (DCSM) and on the param eter value of SELECT IM PLICIT
    MOVEMENT DIRECTION (SIMD). If the DEVICE COMPONENT SELECT MODE (DCSM
    ) is set to PRESENTATION and with a param eter value of SIMD equal
    to 0, NEL causes t he act ive present ation posi tion t o be m oved
    t o the line home position of the following line in the presentation
    com ponent. The line hom e position is established by the param eter
    value of SET LINE HOM E (SLH). With a param eter value of SIM D
    equal to 1, NEL causes t he act ive present ation posi tion t o be m
    oved t o the line lim it position of the follo wing line in the
    presentation co mponent. The line lim it position is established by
    the param eter val ue of SET LINE LIM IT (SLL).\
    If the DEVICE COMPONENT SELECT MODE (DCSM) is set to DATA and with a
    param eter value of SIMD equal to 0, NEL causes the act ive dat a
    posi tion t o be m oved t o t he l ine hom e posi tion of t he
    following line in the data com ponent. The line hom e pos ition is
    established by the param eter value of SET LINE HOM E (SLH).\
    With a p arameter v alue of SIMD eq ual to 1, NEL cau ses the activ
    e data position to be moved to the line limit position of the
    following line in the data com ponent. The line lim it position is
    established by the param eter value of SET LINE LIMIT (SLL).\
    8.3.87 NP - NE XT PAGE\
    Notation: (Pn) Represent ation: CSI Pn 05/ 05 Param eter d efault
    value: Pn = 1\
    NP causes t he n-t h fol lowing page i n t he present ation com
    ponent t o be displayed, where n equal s the value of Pn.\
    The effect of t his cont rol funct ion on t he act ive pres entation
    posi tion is not defi ned by this Standard.\
    8.3.88 NUL - NUL L Notation: (C0) Represent ation: 00/00\
    NUL is used for media-fill or time-fill. NUL characters m ay b e in
    serted in to, o r rem oved fro m, a d ata stream wi thout affect ing
    t he i nformation cont ent of t hat stream, but such action may
    affect the information layout and/ or the cont rol of equi pment.\
    8.3.89 OSC - OPERATING SYSTEM COMMAND Notation: (C1) Represent
    ation: 09/13 or ESC 05/13\
    OSC is used as the openi ng delimiter of a cont rol st ring for
    operat ing sy stem use. The com mand st ring following m ay consi st
    of a sequence of bi t com binations i n the range 00/ 08 t o 00/ 13
    and 02/00 to 07/14. The control string is closed by the terminating
    delim iter STRING TERM INATOR (ST). The interpret ation of t he com
    mand st ring depends on t he rel evant operat ing sy stem. 8.3.90
    PEC - PRESENTATION EX PAND OR CONTRACT Notatio n: (Ps) Represent
    ation: CSI Ps 02/ 00 05/ 10 Param eter d efault value: Ps = 0\
    PEC is u sed to estab lish th e sp acing an d the extent of t he
    graphi c charact ers for subsequent t ext. The spacing is specified
    in the line as multiples of the spacing established by the m ost
    recent occurrence of SET CHARACTER SPACING (SCS) or of SELEC T
    CHARACTER SPACING (S HS) or of SPACING INCREMENT (SPI) in th e d ata
    stream . Th e ex tent o f th e ch aracters is im plicitly estab
    lished by these

```{=html}
<!-- Page 66 -->
```
-   52 - control fu nctions. Th e estab lished sp acing an d th e ex
    tent rem ain in effect until the next occurrence of PEC, of SC S, of
    SHS or of SPI i n the dat a stream. The param eter val ues are\
    0 normal (as specified by SCS, SHS or SPI)\
    1 expanded (multiplied by a facto r not greater th an 2)\
    2 condensed (m ultiplied by a factor not less than 0,5)\
    8.3.91 PFS - PAGE FORMAT SELECTION Notatio n: (Ps) Represent ation:
    CSI Ps 02/ 00 04/ 10 Param eter d efault value: Ps = 0\
    PFS is used to establish the availa ble area for the im aging of
    pages of text based on paper size. The pages are i ntroduced by the
    subsequent occurrence of FOR M FEED (FF) i n the dat a stream.\
    The established im age area remains in effect until the next
    occurren ce of PFS in the data stream . The param eter values are
    (see also annex E): 0 tall basi c text communication form at\
    1 wide basi c text communication form at\
    2 tall basic A4 form at\
    3 wide basic A4 form at\
    4 tall North Am erican letter form at\
    5 wide North Am erican letter form at\
    6 tall ex tended A4 format\
    7 wide ext ended A4 form at\
    8 tall No rth American legal format\
    9 wide North Am erican legal form at\
    10 A4 short lines form at\
    11 A4 long l ines form at\
    12 B5 short lin es fo rmat\
    13 B5 long l ines form at\
    14 B4 short lin es fo rmat\
    15 B4 long l ines form at\
    The page home posi tion i s est ablished by t he para meter value of
    SET PAGE HOM E (SPH), the page limit position is estab lished by the
    parameter v alue of SET PAGE LIMIT (SPL). 8.3.92 PLD - PARTIAL LINE
    FORWARD Notation: (C1) Represent ation: 08/11 or ESC 04/11\
    PLD causes the active present ation position to be m oved i n t he
    present ation com ponent t o t he corresponding position of an im
    aginary lin e with a partial offset in the direction of the line
    progression. This offset should be sufficient either to im age
    following characters as s ubscripts until the first following
    occurrence of PARTIAL LINE BACKW ARD (PLU) in the data stream , or,
    if preceding characters were im aged as superscr ipts, to resto re
    im aging of fo llowing ch aracters to the activ e line (the line
    that contains the active presentation position).\
    Any interactions between PLD and form at effectors ot her t han PLU
    are not defi ned by this Standard.

```{=html}
<!-- Page 67 -->
```
-   53 - 8.3.93 PLU - PARTIAL LINE BACKWARD Notation: (C1) Represent
    ation: 08/12 or ESC 04/12\
    PLU causes the active present ation position to be m oved i n t he
    present ation com ponent t o t he corresponding position of an im
    aginary lin e with a partial offset in the direction opposite to
    that of the line progressi on. This offset shoul d be suffi cient ei
    ther t o i mage fol lowing charact ers as superscri pts until the
    first following occurrence of PARTIAL LINE FORW ARD (PLD) in th e d
    ata stream , o r, if preceding characters were im aged as
    subscripts, to restore im aging of following character s to the
    active line (th e line that co ntains the activ e presentatio n
    position).\
    Any interactions between PLU and form at effectors ot her t han PLD
    are not defi ned by this Standard.\
    8.3.94 PM - PRIVACY MESSAGE Notation: (C1) Represent ation: 09/14 or
    ESC 05/14\
    PM i s used as t he openi ng del imiter of a cont rol st ring for
    privacy message use. The command string following m ay consi st of a
    sequence of bi t com binations i n the range 00/ 08 t o 00/ 13 and
    02/00 to 07/14. The control string is closed by the terminating
    delim iter STRING TERM INATOR (ST). The interpret ation of t he com
    mand st ring depends on t he rel evant privacy discipline.\
    8.3.95 PP - PRE CEDING PAGE\
    Notation: (Pn) Represent ation: CSI Pn 05/ 06 Param eter d efault
    value: Pn = 1\
    PP causes the n-th preceding page in the presentation com ponent to
    be displayed, where n equals the value of Pn. The effect of this
    control funct ion on t he act ive present ation posi tion i s not
    defi ned by this Standard.\
    8.3.96 PPA - PAGE POSIT ION AB SOL UTE Notation: (Pn) Represent
    ation: CSI Pn 02/ 00 05/ 00 Param eter d efault value: Pn = 1\
    PPA causes t he act ive dat a posi tion t o be m oved i n t he dat a
    com ponent t o t he correspondi ng charact er position on t he n-t h
    page, where n equal s the val ue of Pn.\
    8.3.97 PPB - PAGE POSITION BACKWARD Notation: (Pn) Represent ation:
    CSI Pn 02/ 00 05/ 02 Param eter d efault value: Pn = 1\
    PPB causes t he act ive dat a posi tion t o be m oved i n t he data
    component to the correspondi ng charact er position on the n-th
    preceding page, where n equals the value of Pn.\
    8.3.98 PPR - PAGE POSITION FORWARD Notation: (Pn) Represent ation:
    CSI Pn 02/ 00 05/ 01 Param eter d efault value: Pn = 1\
    PPR causes t he act ive dat a posi tion t o be m oved i n t he data
    component to the correspondi ng charact er position on t he n-t h
    following page, where n equal s the val ue of Pn.\
    8.3.99 PTX - PARALLEL TEX TS Notatio n: (Ps) Represent ation: CSI Ps
    05/ 12 Param eter d efault value: Ps = 0

```{=html}
<!-- Page 68 -->
```
-   54 - PTX i s used t o del imit st rings of graphi c charact ers that
    are communicated one after another in the data stream but that are
    intended to be presented in pa rallel with one another, us ually in
    adjacent lines.\
    The param eter values are\
    0 end of paral lel texts\
    1 beginning of a st ring of pri ncipal paral lel text\
    2 beginning of a st ring of suppl ementary paral lel text\
    3 beginning of a st ring of suppl ementary Japanese phonet ic annot
    ation\
    4 beginning of a st ring of suppl ementary Chinese phonet ic annot
    ation\
    5 end of a st ring of suppl ementary phonet ic annot ations\
    PTX with a param eter value of 1 indicates the begi nning of t he st
    ring of pri ncipal t ext i ntended t o be present ed in paral lel
    with one or m ore st rings of suppl ementary text.\
    PTX wi th a param eter val ue of 2, 3 or 4 i ndicates the beginning
    of a string of suppl ementary text that is intended to be presented
    in paralle l with either a string of principa l text or the im
    mediately preceding string of supplem entary text, if an y; at the
    sam e time it indicates the end of the preceding string of principal
    text or of the im mediatel y preceding string of supplem entary text
    , if any. The end of a string of suppl ementary text is indicated by
    a subsequent occurrence of PTX wi th a param eter val ue other t han
    1.\
    PTX wi th a param eter val ue of 0 i ndicates t he end of t he st
    rings of text intended to be present ed in paral lel with one anot
    her.\
    NOTE PTX does not explicitly specify the relative placemen t of the
    strings of pr incipal and supplementary paral lel t exts, or t he
    rel ative si zes of graphi c charact ers i n t he strings of paral
    lel text. A string of suppl ement ary t ext is normal ly present ed
    i n a l ine adj acent to the line containing the string of principal
    text, or adjacent to the line cont aining the immediately preceding
    string of suppl ementary text, if any. The f irst graphi c charact
    er of t he st ring of pri ncipal t ext and t he f irst graphi c
    charact er of a string of supplementary text are normally presented
    in the same position of their respective lines. However, a string of
    suppl ement ary text longer (when present ed) than t he associ ated
    st ring of pri ncipal text may be centred on that string. In the
    case of long strings of t ext, such as paragraphs in different
    languages, the strin gs ma y b e presented in su ccessive lin es in
    parallel co lumns, with their beginnings aligned with one another
    and t he short er of the paragraphs f ollowed by an appropri ate
    amount of "white space".\
    Japanese phonet ic annot ation t ypically consi sts of a few hal
    f-size or smal ler K ana charact ers w hich indicate t he pronunci
    ation or interpret ation of one or more K anji charact ers and are
    present ed above those Kanji charact ers if the charact er pat h is
    hori zontal, or t o the ri ght of them i f the charact er pat h is
    vertical.\
    Chinese phonet ic annot ation typically consi sts of a f ew Pi nyin
    charact ers w hich i ndicate t he pronunci ation of one or more
    Hanzi charact ers and are present ed above t hose Hanzi charact ers.
    Alternatively, t he Pi nyin charact ers may be present ed i n t he
    same l ine as the Hanzi charact ers and following the resp ective Ha
    nzi ch aracters. Th e Pin yin characters will then be presented
    within enclosing pairs of parent heses. 8.3.100 PU1 - PRIVAT E USE
    ONE\
    Notation: (C1) Represent ation: 09/01 or ESC 05/01\
    PU1 i s reserved for a funct ion wi thout st andardi zed m eaning
    for pri vate use as requi red, subject t o t he prior agreem ent
    between the sender and the recipient of the data.\
    8.3.101 PU2 - PRIVAT E USE TWO Notation: (C1) Represent ation: 09/02
    or ESC 05/02\
    PU2 i s reserved for a funct ion wi thout st andardi zed m eaning
    for pri vate use as requi red, subject t o t he prior agreem ent
    between the sender and the recipient of the data.

```{=html}
<!-- Page 69 -->
```
-   55 - 8.3.102 QUAD - QUAD Notation: (Ps...) Representation: CSI Ps...
    02/00 04/08 Param eter d efault value: Ps = 0\
    QUAD is used to indicate the end of a string of gra phic characters
    that are to be positioned on a single line according to the layout
    specified by the param eter values, see annex C:\
    0 flush t o line hom e posi tion margin\
    1 flush to line home position margin and fill with lead er\
    2 centre b etween line home position and line lim it position
    margins\
    3 centre b etween line home position and line lim it position
    margins and fill with lead er\
    4 flush to line lim it position margin\
    5 flush to line lim it position margin and fill with lead er\
    6 flush t o both margins\
    The beginning of the string to be positioned is indicated by the
    precedi ng occurrence in the data stream\
    of either QUAD or one of the following form ator functions: FORM
    FEED (FF), CHARACTER AND LINE POSITION (HVP), LINE FEED (LF), NEXT
    LINE (NEL), PAGE POSITION ABSOLUTE (PPA), PAGE POSITION BACKW ARD
    (PPB), PAGE POSITION FORW ARD (PPR), REVERSE LINE FEED (RI), LINE
    POSITION ABSOLUTE (VPA), LINE POSITION BACKW ARD (VPB), LINE
    POSITION FORW ARD (VPR), or LINE TABULATION (VT).\
    The lin e home position is estab lished by the parameter v alue of
    SET LINE HOME (SLH). The line limit position is established by the
    param eter val ue of SET LINE LIM IT (SLL).\
    8.3.103 REP - RE PEAT Notation: (Pn) Represent ation: CSI Pn 06/ 02
    Param eter d efault value: Pn = 1\
    REP is used to indicate that the preceding character in the data str
    eam, if it is a graphic character (represent ed by one or m ore bi t
    com binations) i ncluding SPAC E, i s t o be repeat ed n t imes,
    where n equals the value of Pn. If the charact er preceding REP is a
    control functi on or part of a control function, the effect of R EP
    is not defi ned by this Standard.\
    8.3.104 RI - RE VERSE LINE FE ED Notation: (C1) Represent ation:
    08/13 or ESC 04/13\
    If the DEVICE COMPONENT SELECT MODE (DCSM) is set to PRESENTATION,
    RI causes the active present ation position to be moved in t he
    present ation com ponent t o t he correspondi ng charact er position
    of the preceding line. If the DEVICE COMPONENT SELECT MODE (DCSM) is
    set to DATA, RI causes the active data position to be m oved in the
    data component to the corresponding character position of the
    preceding line. 8.3.105 RIS - RE SET TO INIT IAL ST ATE Notatio n:
    (Fs) Represent ation: ESC 06/03\
    RIS cau ses a d evice to b e reset to its in itial state, i. e. the
    state it h as after it is m ade o peratio nal. Th is may im ply, if
    ap plicab le: clear tab ulation sto ps, re move qual ified areas,
    reset graphi c rendi tion, put all character positions into the
    erased state, move the activ e presentatio n position to the first p
    osition of the first line in the presentation com ponent, m ove the
    ac tive data position to the first character position of the first
    line in the dat a component , set the modes i nto the reset state,
    et c. 

```{=html}
<!-- Page 70 -->
```
-   56 - 8.3.106 RM - RE SET MODE\
    Notation: (Ps...) Representation: CSI Ps... 06/12 No param eter
    default value.\
    RM causes the m odes of the receiving device to be reset as
    specified by the param eter values:\
    1 GUARDED AREA TRANSFER M ODE (GATM )\
    2 KEYBOARD ACTION M ODE (KAM )\
    3 CONTROL REPRESENTATION M ODE (CRM )\
    4 INSERTION REPLACEM ENT M ODE (IRM )\
    5 STATUS REPORT TRANSFER M ODE (SRTM )\
    6 ERASURE M ODE (ERM )\
    7 LINE EDITING M ODE (VEM )\
    8 BI-DIRECTIONAL SUPPORT M ODE (BDSM ) 9 DEVICE COMPONENT SELECT
    MODE (DCSM) 10 CHARACTER EDITING M ODE (HEM )\
    11 POSITIONING UNIT M ODE (PUM ) (see F.4.1 in annex F) 12
    SEND/RECEIVE M ODE (SRM )\
    13 FORMAT EFFECTOR ACTION M ODE (FEAM )\
    14 FORMAT EFFECTOR TRANSFER M ODE (FETM )\
    15 MULTIPLE AREA TRANSFER M ODE (M ATM)\
    16 TRANSFER TERM INATION M ODE (TTM )\
    17 SELECTED AREA TRANSFER MODE (SATM)\
    18 TABULATION STOP M ODE (TSM )\
    19 (Shal l not be used; see F.5.1 i n annex F) 20 (Shal l not be
    used; see F.5.2 i n annex F) 21 GRAPHIC RENDITION COM BINATION M ODE
    (GRCM ) 22 ZERO DEFAULT M ODE (ZDM ) (see F.4.2 in annex F) NOTE
    Private modes may be i mplement ed usi ng pri vate paramet ers, see
    5.4.1 and 7.4.\
    8.3.107 SACS - SET ADDITIONAL CHARACTER SEPARATION Notation: (Pn)
    Represent ation: CSI Pn 02/ 00 05/ 12 Param eter d efault value: Pn
    = 0\
    SACS is u sed to estab lish ex tra in ter-ch aracter escapem ent for
    subsequent text. The established extra escap ement remains in effect
    u ntil th e n ext o ccurrence o f SACS o r o f SET REDUCED CHARACTER
    SEPARATION (SRCS) in the data stream or until it is reset to the
    default value by a subsequent occurrence of CARRIAGE RETURN/LINE
    FEED (CR LF) or of NEXT LINE (NEL) in the data stream , see annex C
    .\
    Pn speci fies the num ber of uni ts by which the inter-character
    escap ement is enlarged.\
    The unit in which the param eter value is expressed is that
    established by the param eter value of SELECT SIZE UNIT (SSU).

```{=html}
<!-- Page 71 -->
```
-   57 - 8.3.108 SAPV - SELECT ALTERNATIVE PRESENTATION VARIANTS
    Notation: (Ps...) Representation: CSI Ps... 02/00 05/13 Param eter d
    efault value: Ps = 0\
    SAPV i s used t o speci fy one or m ore vari ants fo r the present
    ation of subsequent t ext. The param eter values are\
    0 default presentation (implementation-defined); cancels the effect
    of any preceding occurrence of SAPV in the data stream\
    1 the deci mal digits are present ed by means of t he graphi c
    symbols used i n the Lat in scri pt 2 the decim al digits are
    presented by m eans of t he graphi c sy mbols used i n t he Arabi c
    script, i.e. the Hindi symbols 3 when the direction of the character
    path is right-to-left, each of th e graphic characters in the
    graphic character set(s) in u se wh ich is one of a left/ri
    ght-handed pair (parentheses, square brackets, curly brackets,
    greater-than/less-than signs, etc.) is presented as "m irrored",
    i.e. as the other member of the pair. For exam ple, the coded
    graphic character gi ven the nam e LEFT PAR ENTHESIS i s present ed
    as RIGHT PARENTHESIS, and vice versa 4 when the direction of the
    char acter p ath is rig ht-to-left, all graphic characters which
    represent operat ors and delimiters in mathematical formulae and whi
    ch are not sy mmetrical about a vert ical axis are present ed as m
    irrored about that vert ical axis 5 the following graphic character
    is presented in its iso lated form 6 the following graphic character
    is p resented in its in itial fo rm 7 the following graphic
    character is presented in its m edial fo rm 8 the following graphic
    character is presented in its fin al form 9 where th e bit co
    mbination 02/14 is in tended to rep resent a d ecimal mark in a d
    ecimal number it shall be present ed by means of t he graphi c
    symbol FULL STOP 10 where th e bit co mbination 02/14 is in tended
    to rep resent a d ecimal mark in a d ecimal number it shall be
    present ed by means of t he graphi c symbol COMMA 11 vowels are
    presented above or below the preceding character 12 vowels are
    presented after the preceding character 13 contextual shape det
    ermination of Arabi c scri pts, i ncluding t he LAM -ALEPH ligature
    but excluding all other Arabi c ligatures 14 contextual shape det
    ermination of Arabi c scri pts, excl uding al l Arabi c ligatures 15
    cancel s the effect of param eter val ues 3 and 4 16 vowel s are not
    present ed 17 when t he st ring di rection i s ri ght-to-left, the
    italicized characters are slante d to th e left; wh en th e strin g
    directio n is left-to -right, the italic ized characters are slanted
    to the right 18 contextual shape determination of Arabi c scri pts i
    s not used, t he graphi c charact ers - including t he digits - are
    present ed in the form they are st ored (Pass-t hrough) 19
    contextual shape det ermination of Arabi c scri pts is not used, the
    graphic characters- excluding the digits - are present ed in the
    form they are st ored (Pass-t hrough) 20 the graphi c symbols used t
    o present the deci mal digits are devi ce dependent\
    21 establishes the effect of param eter val ues 5, 6, 7, and 8 for t
    he fol lowing graphi c charact ers unt il cancelled 22 cancels the
    effect of param eter value 21, i.e. re-estab lishes the effect of
    param eter val ues 5, 6, 7, and 8 for t he next single graphi c
    charact er onl y.

```{=html}
<!-- Page 72 -->
```
-   58 - 8.3.109 SCI - SINGLE CHARACTER INTRODUCER Notation: (C1)
    Represent ation: 09/10 or ESC 05/10\
    SCI an d th e b it co mbination fo llowing it are u sed to represent
    a control function or a graphic character. The bi t com bination fol
    lowing SC I m ust be from 00/ 08 t o 00/ 13 or 02/ 00 t o 07/ 14.
    The use of SCI is reserved for future standardi zation.\
    8.3.110 SCO - SELECT CHARACTER ORIENTATION Notatio n: (Ps) Represent
    ation: CSI Ps 02/ 00 06/ 05 Param eter d efault value: Ps = 0\
    SCO i s used t o est ablish t he am ount of rot ation of t he graphi
    c charact ers fol lowing i n t he dat a st ream. The estab lished
    value rem ains in effect u ntil th e next occurrence of SCO in the
    data stream .\
    The param eter values are\
    0 0° 1 45° 2 90° 3 135° 4 180° 5 225° 6 270° 7 315° Rotation is
    positive, i.e. counter-clockwise and a pplies to the norm al
    presentation of the graphic charact ers al ong t he charact er
    pat h. The centre of rotation of t he affect ed graphi c charact ers
    i s not\
    defined by this Standard.\
    8.3.111 SCP - SELECT CHARACTER PATH Notatio n: (Ps1 ;Ps2) Represent
    ation: CSI Ps1; Ps2 02/ 00 06/ 11 No param eter default values. SCP
    is u sed to select th e ch aracter p ath, relativ e to th e lin e o
    rientation, for the activ e line (the line that contains t he act
    ive present ation position) and subsequent lines i n the present
    ation com ponent . It is al so used to updat e the content of the
    active line i n the present ation com ponent and t he cont ent of t
    he act ive line (the line that cont ains the act ive dat a posi
    tion) i n the dat a component . Thi s takes effect immediately. Ps1
    specifies the character path: 1 left-to-right (i n t he case of hori
    zontal l ine ori entation), or t op-to-bottom (i n t he case of vert
    ical l ine orientation) 2 right-to-left (i n t he case of hori
    zontal l ine ori entation), or bot tom-to-top (i n t he case of vert
    ical l ine orientation) Ps2 speci fies t he effect on t he cont ent
    of t he present ation component and the content of the data
    component : 0 undefi ned (implementation-dependent ) NOTE This ma y
    a lso p ermit th e effect to ta ke p lace a fter t he next
    occurrence of C R, N EL or any cont rol function wh ich in itiates a
    n a bsolute mo vemen t o f th e a ctive p resentation p osition o r
    th e a ctive data position.

```{=html}
<!-- Page 73 -->
```
-   59 - 1 the cont ent of t he act ive l ine i n t he present ation com
    ponent (t he l ine t hat contains the active present ation position)
    is updat ed to correspond t o the cont ent of t he act ive line in
    the dat a component\
    (the line that contains the active data position) according to the
    newly established character path characteristics in the presentation
    component; the active data position is moved to the first character
    position in the active line in the data com ponent, the active
    presentation position in the presentation component is updated
    accordingly 2 the content of the active line in the data com ponent
    (the line that contains the active data position) is updat ed to
    correspond t o t he cont ent of t he act ive l ine i n t he present
    ation com ponent (t he l ine t hat contains the active presentation
    position) accordi ng to the newly established character path
    characteristics of the presentati on com ponent; the active
    presentation position is moved to the first character position in
    the active line in the presentation com ponent, the active data
    position in the data component is updated accordingly. 8.3.112 SCS -
    SET CHARACTER SPACING Notation: (Pn) Represent ation: CSI Pn 02/ 00
    06/ 07 No param eter default value.\
    SCS is u sed to estab lish th e ch aracter spaci ng for subsequent t
    ext. The est ablished spaci ng rem ains i n effect until the next
    occurrence of SCS, or of SELECT CHARACTER SPAC ING (SHS) or of
    SPACING INCREMENT (SPI) in the data stream , see an nex C.\
    Pn specifies the character spacing.\
    The unit in which the param eter value is expressed is that
    established by the param eter value of SELECT SIZE UNIT (SSU).
    8.3.113 SD - SCROL L DOWN Notation: (Pn) Represent ation: CSI Pn 05/
    04 Param eter d efault value: Pn = 1\
    SD causes the data in the presenta tion com ponent to be m oved by n
    lin e positions if the line orientation is horizontal, or by n
    charact er positions if t he l ine ori entation i s vert ical, such
    t hat t he dat a appear t o move down; where n equal s the val ue of
    Pn.\
    The act ive present ation posi tion is not affect ed by this cont
    rol funct ion.\
    8.3.114 SDS - ST ART DIRE CTED ST RING Notatio n: (Ps) Represent
    ation: CSI Ps 05/ 13 Param eter d efault value: Ps = 0\
    SDS is used to establish in the data component t he begi nning and t
    he end of a st ring of charact ers as well as t he di rection of t
    he st ring. Thi s di rection m ay be di fferent from t hat current
    ly est ablished. The indicated string follows the preced ing text.
    The established charact er progression is not affected. The begi
    nning of a di rected st ring i s indicated by SDS wi th a param eter
    val ue not equal to 0. A directed string may contain one or m ore
    nest ed st rings. These nest ed st rings m ay be di rected st rings
    t he beginnings of whi ch are i ndicated by SDS wi th a param eter
    val ue not equal to 0, or reversed st rings t he beginnings of which
    are indicated by START REVERSED STRING (SRS) with a param eter value
    of 1. Every begi nning of such a st ring invokes t he next deeper l
    evel of nest ing. This Standard does not defi ne the location of t
    he activ e data position with in any such nested strin g. The end of
    a di rected st ring i s indicated by SDS wi th a param eter value
    of 0. Every end of such a string re-est ablishes t he next hi gher l
    evel of nest ing (t he one i n effect pri or t o t he st ring just
    ended). The directio n is re-estab lished to th at in effect p rior
    to th e strin g just ended. The activ e data position is moved t o
    the charact er posi tion fol lowing the characters of the string
    just ended.

```{=html}
<!-- Page 74 -->
```
-   60 - The param eter values are: 0 end of a di rected st ring; re-est
    ablish the previ ous di rection 1 start of a di rected st ring;
    establish the direction left-to-right 2 start of a di rected st
    ring; establish the direction ri ght-to-left NOTE 1\
    The effect of receiving a CVT, HT, SCP, SPD or VT control function
    within an SDS string is not defined by this Standard. NOTE 2\
    The control functions for area definition (DAQ, EPA, ESA, SPA, SSA)
    should not be used within an SDS string. 8.3.115 SEE - SELECT
    EDITING EX TENT Notatio n: (Ps) Represent ation: CSI Ps 05/ 01 Param
    eter d efault value: Ps = 0\
    SEE i s used t o est ablish t he edi ting ext ent for subsequent
    charact er or line insertion or deletion. The estab lished extent
    remains in effect until th e n ext o ccurrence o f SEE in th e d ata
    stream . Th e ed iting extent depends on t he param eter val ue:\
    0 the shi fted part is limited to the act ive page i n the present
    ation com ponent\
    1 the shi fted part is limited to the act ive line in the present
    ation com ponent\
    2 the shi fted part is limited to the act ive fi eld in the present
    ation com ponent\
    3 the shifted part is lim ited to the activ e qualified area\
    4 the shi fted part consi sts of t he rel evant part of t he ent ire
    present ation com ponent .\
    8.3.116 SEF - SHEET EJECT AND FEED Notatio n: (Ps1 ;Ps2) Represent
    ation: CSI Ps1; Ps2 02/ 00 05/ 09 Param eter defaul t values: Ps1 =
    0; Ps2 = 0 SEF causes a sheet of paper to be ejected from a printing
    device into a speci fied out put st acker and another sheet to be l
    oaded i nto the pri nting devi ce from a speci fied paper bi n. 
    Param eter val ues of Ps1 are:\
    0 eject sheet, no new sheet loaded 1 eject sheet and l oad anot her
    from bin 1\
    2 eject sheet and l oad anot her from bin 2\
    .\
    .\
    .\
    n eject sheet and l oad anot her from bin n Param eter val ues of
    Ps2 are:\
    0 eject sheet, no stacker specified 1 eject sheet into stacker 1 2
    eject sheet into stacker 2 . . .

```{=html}
<!-- Page 75 -->
```
-   61 - n eject sheet into stacker n 8.3.117 SGR - SELECT GRAPHIC
    RENDITION Notation: (Ps...) Representation: CSI Ps... 06/13 Param
    eter d efault value: Ps = 0\
    SGR i s used t o est ablish one or m ore graphi c re ndition aspect
    s for subsequent t ext. The est ablished aspects remain in effect u
    ntil th e next occurrence o f SGR in the data stream , depending on
    the settin g of the GRAPHIC RENDITION COMBINATION MODE (GRCM). Each
    graphic rendition aspect is specified by a param eter value:\
    0 default rendition (implementation- defined), cancels the effect of
    an y preceding occurrence of SGR in the data stream regardless of
    the setti ng of the GRAPHIC RENDITION COM BINATION M ODE (GRCM ) 1
    bold or i ncreased i ntensity 2 faint, decreased i ntensity or
    second col our 3 italicized\
    4 si ngly underl ined 5 slowly blinking (l ess t hen 150 per m
    inute) 6 rapidly blinking (150 per m inute or m ore) 7 negat ive
    image 8 concealed characters 9 crossed-out (characters still leg
    ible but marked as to be deleted ) 10 primary (defaul t) font\
    11 first altern ative font 12 second al ternative font\
    13 third altern ative font 14 fourt h alternative font\
    15 fifth alternative font\
    16 sixth alternative font\
    17 sevent h alternative font\
    18 eighth alternative font\
    19 ninth alternative font\
    20 Fraktur (Gothic) 21 doubl y underl ined 22 normal colour or norm
    al intensity (nei ther bol d nor fai nt) 23 not italicized, not
    frakt ur 24 not underl ined (nei ther si ngly nor doubl y) 25 steady
    (not blinking) 26 (reserved for proport ional spaci ng as speci fied
    in CCITT Recommendation T.61) 27 p ositive image 28 revealed
    characters

```{=html}
<!-- Page 76 -->
```
-   62 - 29 not crossed out\
    30 bl ack display 31 red display 32 green display 33 y ellow display
    34 bl ue display 35 m agenta display 36 cy an display 37 whi te
    display 38 (reserved for fut ure st andardi zation; intended for set
    ting charact er foreground col our as speci fied i n ISO 8613-6 \[C
    CITT Recommendation T.416\] ) 39 defaul t display colour (i
    mplementation-defi ned) 40 bl ack background 41 red background 42
    green background 43 y ellow background 44 bl ue background 45 m
    agenta background 46 cy an background 47 whi te background 48
    (reserved for fut ure st andardi zation; intended fo r set ting
    charact er background col our as speci fied i n ISO 8613-6 \[C CITT
    Recommendation T.416\] ) 49 defaul t background col our (i
    mplementation-defi ned) 50 (reserved for cancelling the effect of
    the rende ring aspect established by param eter val ue 26) 51 fram
    ed 52 enci rcled 53 overl ined 54 not fram ed, not enci rcled 55 not
    overl ined 56 (reserved for future standardi zation) 57 (reserved
    for future standardi zation) 58 (reserved for future standardi
    zation) 59 (reserved for future standardi zation) 60 ideogram underl
    ine or ri ght side line\
    61 ideogram doubl e underl ine or doubl e line on t he right side\
    62 ideogram overl ine or l eft side line 63 ideogram doubl e overl
    ine or doubl e line on t he left side 64 ideogram stress m arking 65
    cancel s the effect of t he rendi tion aspect s est ablished by
    param eter val ues 60 t o 64

```{=html}
<!-- Page 77 -->
```
-   63 - NOTE The usabl e combi nations of paramet er val ues are det
    ermined by t he implement ation.\
    8.3.118 SHS - SELECT CHARACTER SPACING Notatio n: (Ps) Represent
    ation: CSI Ps 02/ 00 04/ 11 Param eter d efault value: Ps = 0\
    SHS is u sed to estab lish th e ch aracter spaci ng for subsequent t
    ext. The established spaci ng remains in effect until the next
    occurrence of SHS or of SET CHARACTER SPAC ING (SCS) or of SPACING
    INCREM ENT (SPI) in the data stream . The param eter values are\
    0 10 charact ers per 25,4 m m\
    1 12 charact ers per 25,4 m m\
    2 15 charact ers per 25,4 m m\
    3 6 charact ers per 25,4 m m\
    4 3 charact ers per 25,4 m m\
    5 9 charact ers per 50,8 m m\
    6 4 charact ers per 25,4 m m\
    8.3.119 SI - SHIFT -IN Notation: (C0) Represent ation: 00/15\
    SI is used for code ext ension purposes. It causes t he meanings of
    t he bi t combinations fol lowing i t in the data stream to be
    changed.\
    The use of SI i s defi ned i n Standard EC MA-35.\
    NOTE SI is used in 7-bit environment s only; i n 8-bi t envi ronment
    s LOC KING-SHIFT ZERO ( LS0) i s used instead.\
    8.3.120 SIMD - SELECT IMPLIC IT MOVEMENT DIRECTION Notatio n: (Ps)
    Represent ation: CSI Ps 05/ 14 Param eter d efault value: Ps = 0\
    SIMD is u sed to select th e d irectio n o f im plicit m ovement o f
    th e d ata p osition relativ e to the character progressio n. The
    directio n selected remains in effect u ntil th e next occurrence of
    SIMD. The param eter values are: 0 the direction of i mplicit
    movement is the sam e as t hat of t he charact er progressi on 1 the
    direction of i mplicit movement is opposi te to that of t he charact
    er progressi on. 8.3.121 SL - SCROL L LEFT Notation: (Pn) Represent
    ation: CSI Pn 02/ 00 04/ 00 Param eter d efault value: Pn = 1\
    SL causes the data in the presentation com ponent to be moved by n
    character positions if the line orientation is horizontal, or by n
    line positions i f the line ori entation i s vert ical, such t hat
    the dat a appear to move to the left; wh ere n equals th e value of
    Pn.\
    The act ive present ation posi tion is not affect ed by this cont
    rol funct ion.

```{=html}
<!-- Page 78 -->
```
-   64 - 8.3.122 SLH - SE T LINE HOME\
    Notation: (Pn) Represent ation: CSI Pn 02/ 00 05/ 05 No param eter
    default value.\
    If the DEVICE COMPONENT SELECT MODE is set to PRESENTATION, SLH is
    used to establish at character position n in the active line (the l
    ine that cont ains t he act ive present ation posi tion) and l ines
    of subsequent text in the presentation component the position to
    which the active presentation position will be moved by subsequent
    occurrences of CA RRIAGE RETURN (CR), DELETE LINE (DL), INSERT LINE
    (IL) or NEXT LINE (NEL) in the data stream ; where n equals the
    value of Pn. In the case of a device without data com ponent, it is
    also the position ahead of which no im plicit m ovement of the
    active present ation posi tion shal l occur. If the DEVICE COMPONENT
    SELECT MODE is set to DAT A, SLH is used to establish at character
    position n in th e activ e lin e (th e lin e th at co ntains th e
    active data position) and l ines of subsequent text in the data com
    ponent the position to which the active data position will be m oved
    by subsequent occurrences of CARRIAGE RETURN (CR), DELETE L INE
    (DL), INSERT LINE (IL) or NEXT LINE (NEL) in the data stream; where
    n equal s the value of Pn. It i s al so t he posi tion ahead of whi
    ch no implicit m ovement of the activ e data position shall o ccur.
    The estab lished position is called th e lin e h ome p osition an d
    rem ains in effect until the next occurrence of SLH in the data
    stream .\
    8.3.123 SLL - SE T LINE LIMIT\
    Notation: (Pn) Represent ation: CSI Pn 02/ 00 05/ 06 No param eter
    default value.\
    If the DEVICE COMPONENT SELECT MODE is set to PRESENTATION, SLL is
    used to establish at character position n in the active line (the l
    ine that cont ains t he act ive present ation posi tion) and l ines
    of subsequent text in the presentation component the position to
    which the active presentation position will be m oved by subsequent
    occurren ces of CARRIAGE RETURN (CR), or NEXT LINE (NEL) in the data
    stream if the param eter value of SELECT IMPLIC IT MOVEMENT
    DIRECTION (S IMD) is equal to 1; where n equals the value of Pn. In
    the case of a device without data com ponent, it is also the
    position beyond which no im plicit m ovement of the active
    presentation position shall occur. If the DEVICE COMPONENT SELECT
    MODE is set to DAT A, SLL is used to establish at character position
    n in th e activ e lin e (th e lin e th at co ntains th e active data
    position) and l ines of subsequent text in the data com ponent the
    position beyond which no implicit m ovement of the active data
    position shall occur. It is also the position in the data com ponent
    to which the active data position will be m oved by subsequent
    occurrences of CR or NEL in the data stream , if the param eter
    value of SELECT IMPLICIT MOVEMENT DIRECTION (SIM D) is equal to 1.\
    The estab lished p osition is called th e lin e lim it p osition an
    d rem ains in effect u ntil th e n ext occurrence of SLL in the data
    stream .\
    8.3.124 SLS - SE T LINE SPACING Notation: (Pn) Represent ation: CSI
    Pn 02/ 00 06/ 08 No param eter default value.\
    SLS i s used t o est ablish t he l ine spaci ng for subsequent text.
    The established spaci ng remains in effect\
    until the next occurrence of SLS or of SELEC T LINE SPACING (SVS) or
    of SPACING INCREMENT (SPI) in the data stream .\
    Pn specifies the line spacing.\
    The unit in which the param eter value is expressed is that
    established by the param eter value of SELECT SIZE UNIT (SSU).

```{=html}
<!-- Page 79 -->
```
-   65 - 8.3.125 SM - SE T MODE\
    Notation: (Ps...) Representation: CSI Ps... 06/08 No param eter
    default value.\
    SM causes the m odes of the receiving device to be set as specified
    by the param eter values:\
    1 GUARDED AREA TRANSFER M ODE (GATM )\
    2 KEYBOARD ACTION M ODE (KAM )\
    3 CONTROL REPRESENTATION M ODE (CRM )\
    4 INSERTION REPLACEM ENT M ODE (IRM )\
    5 STATUS REPORT TRANSFER M ODE (SRTM )\
    6 ERASURE M ODE (ERM )\
    7 LINE EDITING M ODE (VEM )\
    8 BI-DIRECTIONAL SUPPORT M ODE (BDSM ) 9 DEVICE COMPONENT SELECT
    MODE (DCSM) 10 CHARACTER EDITING M ODE (HEM )\
    11 POSITIONING UNIT M ODE (PUM ) (see F.4.1 in annex F) 12
    SEND/RECEIVE M ODE (SRM )\
    13 FORMAT EFFECTOR ACTION M ODE (FEAM )\
    14 FORMAT EFFECTOR TRANSFER M ODE (FETM )\
    15 MULTIPLE AREA TRANSFER M ODE (M ATM)\
    16 TRANSFER TERM INATION M ODE (TTM )\
    17 SELECTED AREA TRANSFER MODE (SATM)\
    18 TABULATION STOP M ODE (TSM )\
    19 (Shal l not be used; see F.5.1 i n annex F) 20 (Shal l not be
    used; see F.5.2 i n annex F) 21 GRAPHIC RENDITION COM BINATION (GRCM
    ) 22 ZERO DEFAULT M ODE (ZDM ) (see F.4.2 in annex F) NOTE Private
    modes may be i mplement ed usi ng pri vate paramet ers, see 5.4.1
    and 7.4.\
    8.3.126 SO - SHIFT -OUT\
    Notation: (C0) Represent ation: 00/14\
    SO is used for code ext ension purposes. It causes t he m eanings of
    t he bi t com binations fol lowing i t i n the dat a stream to be
    changed.\
    The use of SO i s defi ned i n Standard EC MA-35.\
    NOTE SO is used i n 7-bi t envi ronment s onl y; i n 8-bi t envi
    ronment s LOC KING-SHIFT ON E ( LS1) i s used instead.\
    8.3.127 SOH - ST ART OF HE ADING Notation: (C0) Represent ation:
    00/01

```{=html}
<!-- Page 80 -->
```
-   66 - SOH i s used t o indicate the begi nning of a headi ng.\
    The use of SOH i s defi ned i n ISO 1745.\
    8.3.128 SOS - ST ART OF ST RING\
    Notation: (C1) Represent ation: 09/08 or ESC 05/08\
    SOS i s used as t he openi ng del imiter of a cont rol st ring. The
    charact er st ring fol lowing may consi st of any bit com bination,
    except thos e representing SOS or STRING TERM INATOR (ST). The
    control string is closed by the term inating delim iter STRING
    TERMINATOR (ST). The interpretation of the character string depends
    on t he appl ication.\
    8.3.129 SPA - START OF GUARDED AREA Notation: (C1) Represent ation:
    09/06 or ESC 05/06\
    SPA is used to indicate that the active present ation posi tion i s
    the fi rst of a st ring of charact er posi tions in t he present
    ation com ponent , t he cont ents of whi ch are protected against
    manual alteration, are guarded against transm ission or transfer,
    depending on the setting of the GUARDED AREA TRANSFER MODE (GATM)
    and m ay be protected against er asure, depending on the setting of
    the ERASURE MODE (ERM ). The end of this string is i ndicated by END
    OF GUARDED AREA (EPA).\
    NOTE The control functions for area definition (DAQ, EPA, ESA, SPA,
    SSA) should not be used within an SRS string or an SDS st ring.
    8.3.130 SPD - SELECT PRESENTATION DIRECTIONS Notatio n: (Ps1 ;Ps2)
    Represent ation: CSI Ps1; Ps2 02/ 00 05/ 03 Param eter defaul t
    value: Ps1 = 0; Ps2 = 0 SPD is u sed to select th e lin e
    orientation, the line progression, and the character path in the
    presentatio n component . It is also used t o updat e t he cont ent
    of t he present ation com ponent and t he cont ent of t he data
    component . Thi s takes effect immediately. Ps1 specifies the line
    orientation, the line progression and the character path: 0 l ine
    orientation: horizontal l ine progressi on: top-to-bottom character
    path: left-to-right 1 l ine orientation: vertical l ine progressi
    on: right-to-left ch aracter path: top-to-bottom 2 l ine
    orientation: vertical l ine progressi on: left-to-right ch aracter
    path: top-to-bottom 3 l ine orientation: horizontal l ine progressi
    on: top-to-bottom character path: right-to-left 4 l ine orientation:
    vertical l ine progressi on: left-to-right character path: bottom
    -to-top 5 l ine orientation: horizontal l ine progressi on:
    bottom-to-top character path: right-to-left

```{=html}
<!-- Page 81 -->
```
-   67 - 6 l ine orientation: horizontal l ine progressi on:
    bottom-to-top character path: left-to-right 7 l ine orientation:
    vertical l ine progressi on: right-to-left character path: bottom
    -to-top Ps2 speci fies t he effect on t he cont ent of t he present
    ation component and the content of the data component : 0 undefi ned
    (implementation-dependent ) NOTE This ma y a lso p ermit th e effect
    to ta ke p lace after the next occurrence of C R, FF or any cont rol
    function wh ich in itiates a n a bsolute mo vemen t o f th e a ctive
    p resentation p osition o r th e a ctive data position. 1 the
    content of the present ation com ponent i s updat ed t o correspond
    t o t he cont ent of t he dat a component according to the newly
    established ch aracteristics of the pres entation com ponent; the
    active dat a posi tion i s moved t o the fi rst charact er posi tion
    i n the fi rst line in the data component , the active presentation
    position in the presen tation com ponent is updated accordingly 2
    the content of the data com ponent i s updat ed t o correspond t o t
    he cont ent of t he present ation component according to the newly
    established ch aracteristics of the pres entation com ponent; the
    activ e presentatio n position is moved to the first ch aracter p
    osition in the first lin e in the presentatio n component, the
    active data position in the data com ponent is updated accordingly.
    8.3.131 SPH - SE T PAGE HOME\
    Notation: (Pn) Represent ation: CSI Pn 02/ 00 06/ 09 No param eter
    default value. If the DEVICE COMPONENT SELECT MODE is set to
    PRESENTATION, SPH is used to establish at line posi tion n i n the
    act ive page (t he page t hat cont ains t he act ive present ation
    posi tion) and subsequent\
    pages in the presentation com ponent the position to which the
    active presentation position will be m oved by subsequent
    occurrences of FOR M FEED (FF) i n the data stream ; where n equals
    the value of Pn. In the case of a device without data com ponent, it
    is al so the position ahead of which no im plicit m ovement of the
    activ e presentatio n position shall o ccur. If the DEVICE COMPONENT
    SELECT MODE is set to DAT A, SPH is used to establish at line
    position n i n t he act ive page (t he page t hat cont ains t he ac
    tive data position) and subsequent pages i n t he dat a component
    the position to which the active data positi on will be m oved by
    subsequent occurrences of FORM FEED (FF) in th e d ata stream ; wh
    ere n eq uals th e v alue o f Pn . It is also the position ahead of
    which no implicit m ovement of the activ e presentatio n position
    shall o ccur. The estab lished position is called the page home
    position and remains in effect until the next occurrence of SPH in
    the data stream . 8.3.132 SPI - SPACING INCREMENT Notation: (Pn1;
    Pn2) Represent ation: CSI Pn1; Pn2 02/ 00 04/ 07 No param eter
    default values.\
    SPI is u sed to estab lish th e lin e sp acing an d th e ch aract er
    spaci ng for subsequent t ext. The est ablished line spacing rem
    ains in effect until the next occurrence of SPI or of SET LINE
    SPACING (SLS) or of SELECT LINE SPACING (SVS) in the data stream .
    The established character spacing rem ains in effect until the next
    occurrence of SET CHARACTER SPACING (SCS) or of SELECT CHARACTER
    SPACING (SHS) in the data stream , see annex C.\
    Pn1 specifies the line spacing\
    Pn2 specifies the character spacing

```{=html}
<!-- Page 82 -->
```
-   68 - The unit in which the parameter values are ex pressed is th at
    estab lished b y th e p arameter v alue o f SELECT SIZE UNIT (SSU).\
    8.3.133 SPL - SE T PAGE LIMIT\
    Notation: (Pn) Represent ation: CSI Pn 02/ 00 06/ 10 No param eter
    default value. If the DEVICE COMPONENT SELECT MODE is set to
    PRESENTATION, SPL is used to establish at line position n i n t he
    act ive page (t he page t hat c ontains t he act ive present ation
    posi tion) and pages of subsequent text in the presentation
    component the position beyond which the active presentation position
    can normally not be m oved; where n equal s t he val ue of Pn. In t
    he case of a devi ce wi thout dat a component, it is also the
    position beyond which no im plicit m ovement of the active
    presentation position shall occur. If the DEVICE COMPONENT SELECT
    MODE is set to DAT A, SPL is used to establish at line position n i
    n the act ive page (t he page t hat cont ains t he act ive dat a
    posi tion) and pages of subsequent text in the data com ponent the
    position beyond which no im plicit m ovement of the active data
    position shall occur.\
    The estab lished position is called th e p age lim it p osition an d
    rem ains in effect u ntil the next occurrence of SPL in the data
    stream . 8.3.134 SPQR - SELECT PRINT QUALITY AND RAPIDITY Notatio n:
    (Ps) Represent ation: CSI Ps 02/ 00 05/ 08 Param eter d efault
    value: Ps = 0\
    SPQR is used to select the relativ e print quality an d th e p rint
    sp eed fo r d evices th e o utput q uality an d speed of which are
    inversely related . The selected v alues rem ain in effect u ntil th
    e n ext o ccurrence o f SPQR in the data stream . The param eter
    values are\
    0 highest av ailab le print quality, lo w print speed\
    1 medium print quality, m edium print speed\
    2 draft p rint quality, h ighest av ailab le print speed\
    8.3.135 SR - SCROL L RIGHT\
    Notation: (Pn) Represent ation: CSI Pn 02/ 00 04/ 01 Param eter d
    efault value: Pn = 1\
    SR causes the data in the presentation com ponent to be m oved by n
    character positions if the line orientation is horizontal, or by n
    line positions i f the line ori entation i s vert ical, such t hat
    the dat a appear to move to the rig ht; wh ere n equals th e value
    of Pn.\
    The act ive present ation posi tion is not affect ed by this cont
    rol funct ion.\
    8.3.136 SRCS - SET REDUCED CHARACTER SEPARATION Notation: (Pn)
    Represent ation: CSI Pn 02/ 00 06/ 06 Param eter d efault value: Pn
    = 0\
    SRCS is u sed to estab lish red uced in ter-ch aracter escapem ent
    for subsequent t ext. The established reduced escapem ent rem ains
    in effect until the next occurrence of SRCS or of SET ADDITIONAL
    CHARACTER SEPARATION (SACS) in the data stream or until it is reset
    to the default value by a subsequent occurrence of CARRIAGE
    RETURN/LINE F EED (CR/LF) or of NEXT LINE (NEL) in the data stream ,
    see annex C.\
    Pn speci fies the num ber of uni ts by which the inter-character es
    capem ent is reduced.

```{=html}
<!-- Page 83 -->
```
-   69 - The unit in which the parameter values are ex pressed is th at
    estab lished b y th e p arameter v alue o f SELECT SIZE UNIT (SSU).\
    8.3.137 SRS - ST ART RE VERSE D ST RING Notatio n: (Ps) Represent
    ation: CSI Ps 05/ 11 Param eter d efault value: Ps = 0\
    SRS is used to establish in the dat a component the begi nning and t
    he end of a st ring of charact ers as wel l as t he di rection of t
    he st ring. Thi s direction i s opposi te to that current ly
    established. The indicated string follows the preceding text. The
    establishe d character progression is not affected. The begi nning
    of a reversed st ring i s i ndicated by SR S with a param eter value
    of 1. A reversed string may cont ain one or m ore nest ed st rings.
    These nest ed strings may be reversed st rings t he begi nnings of
    which are i ndicated by SR S wi th a param eter val ue of 1, or
    directed strings the beginnings of which are indicated by START
    DIRECTED STRING (SDS) with a param eter value not equal to 0. Every\
    beginning of such a st ring invokes t he next deeper l evel of nest
    ing. This Standard does not defi ne the location of t he activ e
    data position with in any such nested strin g. The end of a reversed
    st ring i s indicated by SRS wi th a param eter val ue of 0. Every
    end of such a string re-est ablishes t he next hi gher l evel of
    nest ing (t he one i n effect pri or t o t he st ring just ended).
    The directio n is re-estab lished to th at in effect p rior to th e
    strin g just ended. The activ e data position is moved t o the
    charact er posi tion fol lowing the characters of the string just
    ended. The param eter values are: 0 end of a reversed st ring;
    re-est ablish the previ ous di rection 1 beginning of a reversed st
    ring; reverse t he direction. NOTE 1\
    The effect of receiving a CVT, HT, SCP, SPD or VT control function
    within an SRS string is not defined by this Standard. NOTE 2\
    The control functions for area definition ( DAQ, EPA, ESA, SPA, SSA)
    should not be used within an SRS string. 8.3.138 SSA - START OF
    SELECTED AREA Notation: (C1) Represent ation: 08/06 or ESC 04/06\
    SSA is used to indicate that the active present ation posi tion i s
    the fi rst of a st ring of charact er posi tions in the presentation
    com ponent, the contents of which ar e eligible to be transm itted
    in the form of a data stream or transferred to an auxiliary input/
    output device.\
    The end of this string is indi cated by END OF SELECTED AREA (ESA).
    The string of characters actually transm itted or transferred
    depends on the setting of the GUARDED AREA TRANSFER MODE (GATM ) and
    on any guarded areas established by DEFINE AREA QUALIFICATION (DAQ),
    or by\
    START OF GUARDED AREA (SPA) and END OF GUARDED AREA (EPA).\
    NOTE The control functions for area definition (DAQ, EPA, ESA, SPA,
    SSA) should not be used within an SRS string or an SDS st ring.
    8.3.139 SSU - SELECT SIZ E UNIT Notatio n: (Ps) Represent ation: CSI
    Ps 02/ 00 04/ 09 Param eter d efault value: Ps = 0\
    SSU is used to estab lish th e u nit in wh ich th e n umeric p
    arameters o f certain co ntrol fu nctions are expressed . The estab
    lished unit rem ains in effect u ntil th e next occurrence of SSU in
    the data stream .

```{=html}
<!-- Page 84 -->
```
-   70 - The param eter values are\
    0 CHARACTER - The di mensions of t his unit are devi ce-dependent\
    1 MILLIMETRE\
    2 COMPUTER DECIPOINT - 0,035 28 m m (1/720 of 25,4 m m)\
    3 DECIDIDOT - 0,037 59 m m (10/266 m m)\
    4 MIL - 0,025 4 m m (1/1 000 of 25,4 m m)\
    5 BASIC M EASURING UNIT (BM U) - 0,021 17 m m (1/1 200 of 25,4 m m)\
    6 MICROMETRE - 0,001 m m\
    7 PIXEL - The sm allest increm ent th at can be specified in a
    device\
    8 DECIPOINT - 0,035 14 m m (35/996 m m)\
    8.3.140 SSW - SE T SPACE WIDT H Notation: (Pn) Represent ation: CSI
    Pn 02/ 00 05/ 11 No param eter default value.\
    SSW i s used t o est ablish for subsequent t ext t he character
    escapem ent associ ated with the character SPACE. The estab lished
    escap ement remains in effect until th e n ext o ccurrence o f SSW
    in th e d ata stream or until it is reset to th e default value by a
    subsequent occurrence of CARRIAGE RETURN/LINE FEED (CR/LF), CARRIAGE
    RETURN/F ORM FEED (CR/FF), or of NEXT LINE (NEL) in the data stream
    , see annex C.\
    Pn specifies the escapem ent.\
    The unit in which the param eter value is expressed is that
    established by the param eter value of SELECT SIZE UNIT (SSU). The
    default character escapem ent of SPACE is specified by the most
    recent occurrence of SET CHARACTER SPACING (SCS) or of SELECT
    CHARACTER SPACING (SHS) or of SELECT SPACING INCREM ENT (SPI) in the
    data stream if the cu rrent font has constant spacing, or is
    specified by the nom inal width of t he charact er SPAC E in the
    current font if that font has proport ional spaci ng.\
    8.3.141 SS2 - SINGL E-SHIFT TWO Notation: (C1) Represent ation:
    08/14 or ESC 04/14\
    SS2 is used for code extension purposes. It causes t he m eanings of
    t he bi t com binations fol lowing i t in the dat a stream to be
    changed. The use of SS2 i s defi ned i n Standard EC MA-35. 8.3.142
    SS3 - SINGL E-SHIFT THREE Notation: (C1) Represent ation: 08/15 or
    ESC 04/15\
    SS3 is used for code extension purposes. It causes t he m eanings of
    t he bi t com binations fol lowing i t in the dat a stream to be
    changed. The use of SS3 i s defi ned i n Standard EC MA-35. 8.3.143
    ST - ST RING T ERMINAT OR Notation: (C1) Represent ation: 09/12 or
    ESC 05/12\
    ST is used as the closing delim iter of a control string opened by
    APPLICATION PROGRAM\
    COMMAND (APC), DEVICE CONTROL STRING (DCS), OPERATING SYSTEM COM
    MAND (OSC), PRIVACY M ESSAGE (PM ), or START OF STRING (SOS).

```{=html}
<!-- Page 85 -->
```
-   71 - 8.3.144 STAB - SELECTIVE TABULATION Notatio n: (Ps) Represent
    ation: CSI Ps 02/ 00 05/ 14 No param eter default value.\
    STAB causes subsequent text in the presentation co mponent to be
    aligned acco rding to the position and the properties of a
    tabulation stop which is selected from a list accordi ng to the
    value of the param eter Ps.\
    The use of t his cont rol funct ion and m eans of speci fying a l
    ist of t abulation st ops to be referenced by the control funct ion
    are speci fied in other st andards, for exam ple ISO 8613-6.\
    8.3.145 STS - SET TRANSMIT STATE Notation: (C1) Represent ation:
    09/03 or ESC 05/03\
    STS is used to establish the transm it state in the receiving
    device. In this state the transm ission of data from the devi ce is
    possi ble.\
    The actual initiation of transm ission of data is pe rform ed by a
    data communication or input/output interface control procedure which
    is out side the scope of this Standard.\
    The transm it state is established eith er by STS appearing in the
    receive d data stream or by the operation of an appropri ate key on
    a key board. 8.3.146 STX - ST ART OF T EXT Notation: (C0) Represent
    ation: 00/02\
    STX i s used t o indicate the begi nning of a t ext and t he end of
    a headi ng.\
    The use of STX i s defi ned i n ISO 1745.\
    8.3.147 SU - SCROL L UP Notation: (Pn) Represent ation: CSI Pn 05/
    03 Param eter d efault value: Pn = 1\
    SU causes the data in the presenta tion com ponent to be m oved by n
    lin e positions if the line orientation is horizontal, or by n
    charact er positions if t he l ine ori entation i s vert ical, such
    t hat t he dat a appear t o move up; where n equal s the val ue of
    Pn.\
    The act ive present ation posi tion is not affect ed by this cont
    rol funct ion.\
    8.3.148 SUB - SUB STITUTE Notation: (C0) Represent ation: 01/10\
    SUB is used in the place of a charact er that has been found to be
    invalid or in error. SUB is intended to be introduced by automatic m
    eans.\
    8.3.149 SVS - SELECT LINE SPACING Notatio n: (Ps) Represent ation:
    CSI Ps 02/ 00 04/ 12 Param eter d efault value: Ps = 0\
    SVS is used to establish the l ine spaci ng for subsequent text. The
    est ablished spaci ng rem ains i n effect\
    until the next occurrence of SVS or of SET LINE SPACING (SLS) or of
    SPACING INCREMENT (SPI) in the data stream . The param eter values
    are:\
    0 6 lines per 25,4 m m\
    1 4 lines per 25,4 m m

```{=html}
<!-- Page 86 -->
```
-   72 - 2 3 lines per 25,4 m m\
    3 12 lines per 25,4 m m\
    4 8 lines per 25,4 m m\
    5 6 lines per 30,0 m m\
    6 4 lines per 30,0 m m\
    7 3 lines per 30,0 m m\
    8 12 lines per 30,0 m m\
    9 2 lines per 25,4 m m\
    8.3.150 SYN - SYNCHRONOUS IDLE\
    Notation: (C0) Represent ation: 01/06 SYN is used by a synchronous
    transm ission system in the absence of any other character (idle
    condition) to provi de a si gnal from which synchroni sm may be achi
    eved or retain ed between data term inal eq uipment.\
    The use of SYN i s defi ned i n ISO 1745.\
    8.3.151 TAC - T ABULATION AL IGNE D CE NTRED Notation: (Pn)
    Represent ation: CSI Pn 02/ 00 06/ 02 No param eter default value.\
    TAC causes a character tabulation stop calling for centri ng to be
    set at character position n in the active line (t he l ine t hat
    cont ains t he act ive present ation posi tion) and lines of
    subsequent text in the presentation com ponent, where n equals the
    value of Pn. TAC causes the replacem ent of any tabulation stop
    previ ously set at that charact er posi tion, but does not affect
    other t abulation st ops.\
    A text string centred upon a tabulati on stop set by TAC will be
    positioned so that the (trailing edge of the) first graphic
    character and the (leading edge of t he) last graphi c character are
    at approxim ately equal distances from the tabulation st op.\
    8.3.152 TALE - T ABULATION AL IGNE D L EADING E DGE Notation: (Pn)
    Represent ation: CSI Pn 02/ 00 06/ 01 No param eter default value.\
    TALE causes a character tabulation stop calling for leading edge
    alignm ent to be set at character position n in th e activ e lin e
    (th e lin e th at co ntains th e activ e p resentatio n p osition)
    an d lin es o f subsequent text in the present ation com ponent ,
    where n equal s t he val ue of Pn. TALE causes t he replacem ent of
    any tabulation stop pr eviously set at that character position, but
    does not affect other tabulation st ops.\
    A text strin g aligned with a tabulation stop set b y TALE will b e
    positioned so th at th e (lead ing ed ge of the) last graphic
    character of the st ring is placed at the tabulation stop.\
    8.3.153 TATE - T ABULATION AL IGNE D T RAIL ING E DGE Notation: (Pn)
    Represent ation: CSI Pn 02/ 00 06/ 00 No param eter default value.\
    TATE causes a character tabulation stop calling for tr ailing edge
    alignm ent to be set at character position n in th e activ e lin e
    (th e lin e th at co ntains th e activ e p resentatio n p osition)
    an d lin es o f subsequent text in the present ation com ponent ,
    where n equal s t he val ue of Pn. TATE causes t he replacem ent of
    any tabulation stop pr eviously set at that character position, but
    does not affect other tabulation st ops.

```{=html}
<!-- Page 87 -->
```
-   73 - A tex t strin g alig ned with a tab ulation sto p set b y TATE
    will b e positioned so that the (trailin g edge of the) first
    graphic character of the st ring is placed at the tabulation stop.\
    8.3.154 TBC - T ABULATION CL EAR Notatio n: (Ps) Represent ation:
    CSI Ps 06/ 07 Param eter d efault value: Ps = 0\
    TBC causes one or m ore t abulation st ops i n the pr esent ation
    com ponent to be cl eared, dependi ng on the param eter value:\
    0 the character tabulation stop at the active presentation position
    is cleared\
    1 the line tabulation stop at the active line is cleared\
    2 all character tabulation stops in the activ e lin e are cleared\
    3 all character tabulation stops are cleared\
    4 all line tabulation stops are cleared\
    5 all tabulation stops are cleared In t he case of param eter val ue
    0 or 2 t he num ber of l ines affect ed depends on t he setting of
    the TABULATION STOP M ODE (TSM )\
    8.3.155 TCC - TABULATION CENTRED ON CHARACTER Notation: (Pn1; Pn2)
    Represent ation: CSI Pn1; Pn2 02/ 00 06/ 03 No param eter default
    value for Pn1 Param eter defaul t value: Pn2 = 32\
    TCC causes a character tabulation stop callin g fo r alig nment o f
    a targ et graphic character to be set at character position n in the
    active line (the l ine that cont ains t he act ive present ation
    posi tion) and l ines of subsequent text in the present ation
    component , where n equal s the val ue of Pn1, and t he target
    charact er about which centring is to be perform ed is speci fied by
    Pn2. TCC causes the replacem ent of any tabulation st op previ ously
    set at that charact er posi tion, but does not affect other t
    abulation st ops.\
    The positioning of a text strin g alig ned with a tab ulation sto p
    set b y TCC will b e determined by the first occurrence in the
    string of the target graphic character; that character will be
    centred upon the tabulation stop. If the target character does not
    occur with in th e strin g, th en th e tr ailing edge of the first
    character of the strin g will b e positioned at th e tab ulation
    stop.\
    The val ue of Pn2 i ndicates t he code table position (binary value)
    of the target ch aracter in the currently invoked code. For a 7-bi t
    code, t he perm issible range of val ues i s 32 t o 127; for an 8-bi
    t code, t he permissible range of val ues is 32 t o 127 and 160 t o
    255.\
    8.3.156 TSR - T ABULATION ST OP RE MOVE\
    Notation: (Pn) Represent ation: CSI Pn 02/ 00 06/ 04 No param eter
    default value.\
    TSR causes any character tabulation st op at character position n in
    the ac tive lin e (th e lin e th at co ntains the act ive present
    ation posi tion) and l ines of subse quent t ext i n t he present
    ation com ponent t o be cleared, but does not affect other t
    abulation st ops. n equal s the val ue of Pn.\
    8.3.157 TSS - T HIN SPACE SPE CIFICAT ION Notation: (Pn) Represent
    ation: CSI Pn 02/ 00 04/ 05 No param eter default value.

```{=html}
<!-- Page 88 -->
```
-   74 - TSS is used to establish the width of a thin space fo r
    subsequent text. The esta blished width rem ains in effect u ntil th
    e next occurrence of TSS in the data stream , see an nex C.\
    Pn specifies the width of the thin space.\
    The unit in which the param eter value is expressed is that
    established by the param eter value of SELECT SIZE UNIT (SSU).\
    8.3.158 VPA - L INE POSIT ION AB SOL UTE Notation: (Pn) Represent
    ation: CSI Pn 06/ 04 Param eter d efault value: Pn = 1\
    VPA causes the active data position to be m oved t o line posi tion
    n i n the dat a com ponent in a di rection paral lel to the line
    progressi on, where n equal s the val ue of Pn.\
    8.3.159 VPB - LINE POSITION BACKWARD Notation: (Pn) Represent ation:
    CSI Pn 06/ 11 Param eter d efault value: Pn = 1\
    VPB causes t he act ive dat a posi tion to be moved by n line posi
    tions i n the dat a com ponent in a di rection opposi te to that of
    t he line progressi on, where n equal s the val ue of Pn.\
    8.3.160 VPR - LINE POSITION FORWARD Notation: (Pn) Represent ation:
    CSI Pn 06/ 05 Param eter d efault value: Pn = 1\
    VPR causes t he act ive dat a posi tion to be moved by n line posi
    tions i n the dat a com ponent in a di rection paral lel to the line
    progressi on, where n equal s the val ue of Pn.\
    8.3.161 VT - L INE TABULATION Notation: (C0) Represent ation: 00/11\
    VT causes t he act ive present ation posi tion t o be moved in the
    present ation component to the corresponding character position on
    the line at whic h the following line tabulation stop is set.\
    8.3.162 VTS - L INE TABULATION SE T Notation: (C1) Represent ation:
    08/10 or ESC 04/10\
    VTS cau ses a lin e tab ulation sto p to be set at the activ e line
    (the line that contains the active presentation position).\
    9 Transformation betw een 7-bit and 8-bit coded representations The
    cont rol funct ions defi ned i n this St andard can be c oded i n a
    7-bi t code as wel l as i n an 8-bi t code; both forms of coded
    representation are equivalent and in accordan ce with Standard
    ECMA-35.\
    However, when dat a cont aining t hese cont rol funct ions are t
    ransform ed from a 7-bi t t o an 8-bi t coded represent ation or vi
    ce versa, t he t ransform ation al gorithm speci fied i n St andard
    EC MA-35 m ay produce results wh ich are fo rmally in disagreement
    with this Stan dard.\
    In order t o make al lowance for such unintended but unavoidable
    devi ations, t he form al rul es are ext ended i n the manner descri
    bed bel ow.\
    In an 8-bit co de, the bit co mbinations of columns 10 to 15 are p
    ermitted to represent\
    Param eter Bytes, In termediate Bytes, an d Final Bytes o f a co
    ntrol seq uence − − the cont ents of t he com mand st ring or t he
    charact er st ring as part of a cont rol string (see 5.6)

```{=html}
<!-- Page 89 -->
```
-   75 - the operand of a si ngle-shi ft cont rol funct ion. − − − − In
    these situations, the bit co mbinations in th e ran ge 1 0/00 to 1
    5/14 sh all h ave th e sam e m eanings as th e correspondi ng bi t
    combinations i n the range 02/ 00 to 07/14.\
    In a 7-bit code, the control functions SHIFT-OUT (SO) and SHIFT-IN
    (SI) are perm itted to occur\
    between the CONTROL SEQUENCE INT RODUCER (CSI) and the Final By te
    of a control sequence, between the opening delim iter of a contro l
    string and the STRING TERM INATOR (ST), between a si ngle-shi ft
    cont rol funct ion and i ts operand.\
    SO and SI have no effect on t he i nterpret ation of a control
    sequence, a cont rol st ring or the operand of a single-shi ft
    control funct ion, but t hey m ay, i ndeed, affect t he m eanings of
    bi t com binations fol lowing i n t he data stream .

```{=html}
<!-- Page 90 -->
```
-   76 -

```{=html}
<!-- Page 91 -->
```
-   77 - Annex A (informative)

Formator functions and editor functions

A.1 Differences betw een editor functions and formator functions The
cont rast bet ween edi tor funct ions and formator functions, to gether
with th eir in teractio n with certain\
modes, is illu strated b y th e fo llowing ex ample o f th e u se o f
the control functions CURSOR NEXT LINE (CNL) and NEXT LINE (NEL).\
In the exam ple it is assum ed that the direction of t he charact er pat
h is from left to ri ght and t he di rection of the line progressi on is
from top to bottom.\
Furthermore, it is assu med that th e strin g of capital letters\
A B C D E F\
has been entered or received, and th at the active presentation position
has b een m oved back to the letter D, for example, by m eans of CURSOR
LEFT (CUB). Starting fro m th is situ ation, th e fo llowing cases are
considered:\
a) A CURSOR NEXT LINE (CNL) is received. In this case, the active
presentation position is m oved to the beginning of the next line
without affecting the prev iously received data.\
b) With the FORM AT EFFECTOR ACTION M ODE (FEA M) set to EXECUTE, a NEXT
LINE (NEL) is received. This has the sam e effect as in case a).\
c) With the FORM AT EFFECTOR ACTION M ODE (FEAM ) set to STORE and the
INSERTION REPLACEMENT MODE (IRM) set to REPLACE, a NEXT L INE (NEL) is
received. In this case, the letter D is replaced by NEL.\
If the data is subsequently forwarded to anothe r device operating with
the FORM AT EFFECTOR ACTION MODE (FEAM) set to EXECUTE, th e effect is:\
A B C\
E F d) With the FORM AT EFFECTOR ACTION M ODE (FEAM ) set to STORE and
the INSERTION REPLACEMENT MODE (IRM) set to INSERT, a NEXT LINE (NEL) is
received. In this case, the NEL is inserted b etween th e letters C an d
D. If th e d ata is subsequent ly forwarded to another devi ce operat
ing with the FORM AT EFFECTOR ACTION M ODE (F EAM) set to EXECUTE, the
effect is:\
A B C D E F\
Formator functions which have been received while the FORMAT EFFECTOR
ACTION MODE (FEAM) is set to STOR E can be operat ed upon wi th editor
funct ions.\
For exam ple, the NEL which has been i nserted bet ween A B C and D E F
i n case d) can be del eted usi ng DELETE CHARACTER (DCH), resulting in
the initial situation being restored.\
A.2 Composite graphic characters Because the form ator functions can be
stored in a receiving device, as opposed to the editor functions which
are i mmediately perform ed, form ator funct ions m ay be used but edi
tor funct ions shal l not be used for the const ruction of composite
graphi c charact ers. For example, i f t he sy mbol = i s t o be com
posed usi ng = (EQUALS SIGN) and / (SOLIDUS), the sequence:\
= CUB /

```{=html}
<!-- Page 92 -->
```
-   78 - does not produce the desired effect if received by a device
    which has no overstrike capability. Such a device may, however,
    process the sequence:\
    = BS /\
    in such a way that it is preserved and can be forwa rded to a device
    which can indeed produce t he i ntended composite symbol. This
    example serv es o nly th e p urpose o f illu stratin g th e d
    ifferen ce b etween th e effects o f ed itor an d fo rmator funct
    ions. W here t wo or m ore graphi c charact ers are t o be i maged
    by a single graphi c symbol, this shoul d be done by using the
    control function GRAPHIC CHARACTER COM BINATION (GCC).

```{=html}
<!-- Page 93 -->
```
-   79 - Annex B (informative)

Coding examples

B.1 Examples of complete control sequences The general form at of a cont
rol sequence i s:\
CSI P ... P I ... I F\
In an 8-bit environm ent the control function CURSOR RIGHT (CUF) by one
positi on can be represented by 09/11 03/ 01 04/ 03 or 01/ 11 05/ 11 03/
01 04/ 03. Other exam ples are 09/11 03/ 00 03/ 01 04/ 03\
09/11 04/ 03\
The fi rst exam ple shows t hat l eading ZER Os (03/ 00) are not si
gnificant. The second example uses the fact that a defaul t value for C
UF is defi ned and i s equal to 1. In a 7-bi t envi ronment the
represent ation is 01/11 05/ 11 03/ 01 04/ 03\
The represent ation of t he two exam ples above i s then 01/11 05/ 11
03/ 00 03/ 01 04/ 03\
01/11 05/ 11 04/ 03\
In an 8-bit environm ent the cont rol function SCROLL RIGHT (SR) by 28
positions can be represented for instance by\
09/11 03/ 02 03/ 08 02/ 00 04/ 01 or 01/ 11 05/ 11 03/ 02 03/ 08 02/ 00
04/ 01 In a 7-bi t envi ronment the correspondi ng represent ation is\
01/11 05/ 11 03/ 02 03/ 08 02/ 00 04/ 01\
In an 8-bit environm ent the control functi on DEFINE AREA QUALIFIC
ATION (DAQ) perm itting num eric and al phabet ic data to be ent ered i
nto an i nput area can be represent ed by\
09/11 03/ 03 03/ 11 03/ 04 06/ 15 or 01/ 11 05/ 11 03/ 03 03/ 11 03/ 04
06/ 15 In a 7-bi t envi ronment the correspondi ng represent ation is\
01/11 05/ 11 03/ 03 03/ 11 03/ 04 06/ 15

```{=html}
<!-- Page 94 -->
```
-   80 - B.2 Examples of parameter strings Character Bit combina tion
    Explanation 7 03/07 A param eter havi ng the val ue 7. 98 03/09 03/
    08 A param eter havi ng the val ue 98. 4;2 03/04 03/ 11 03/ 08 Two
    param eters havi ng the val ues 4 and 2, respectively. =3 03/13 03/
    03 A pri vate param eter string. 6; 03/06 03/ 11 Two param eters, t
    he first havi ng the val ue 6 and the second t aking the defaul t
    value. NOTE - The bi t combination 03/ 11 may be omitted (see 5 .4.2
    h). ;5 03/11 03/ 05 Two param eters, t he first taking the defaul t
    value and t he second havi ng the val ue 5. 1;;4 03/01 03/ 11 03/11
    03/ 04 Three param eters, t he first havi ng the val ue 1, t he
    second t aking the defaul t value, and t he third having the val
    ue 4. 0007 03/00 03/ 00 03/00 03/ 07 A param eter havi ng the val ue
    7.

```{=html}
<!-- Page 95 -->
```
-   81 - Annex C (informative)

Text composition considerations

Display devices and system s involvi ng text com position m ay use the
cont rol functions JUSTIFY (JFY) and QUAD (QUAD). W hen working in the
field of te xt composition several words are used with quite specialized
m eaning. Those words have been used in this St andard wi th t he m
eaning from t he t echnol ogy of t he pri nting and publ ishing indust
ry. Explanation is provi ded i n t his annex i n t erms com patible wi
th coded i nformation i nterchange and t he concepts of character-im
aging devices.\
Both QUAD and JFY deal with the positioning of text (g raphic characters
and free spaces) between "m argins". Margins are areas prot ected agai
nst di splay at t he boundari es of whi ch l ines of t ext m ay st art
and t erminate. In t he general case of a display device with a m
ultiple-page buffer (capable of th e QUAD or JFY functions) the m
argin(s) would be set at arbitrary absolute character positions. The
QUAD function deals with single lines of text from the data stream , wh
ile th e JFY fu nction m ay d eal with m ore th an o ne lin e. In b oth
cases it is possible to "flush" text. When text is flush, it starts or
ends, as applicable, against a m arginal boundary. Flush to line hom e
position m argin means start tex t at th e ap propriate m argin (o r
first m argin lin e home position in columnar texts). Similarly, flush
to line l imit posi tion m argin m eans t o end t ext at t hat appropri
ate m argin. In t he process of making text flush, open spaces m ay be
generated.\
The action to "fill" open spaces involves a concept partic ular to the
JFY and QUAD functions. The open spaces m ay be filled with a "leader"
in the QUAD function. A leader is a pattern (m ost often a repeated
string of graphic characters) wh ich is in serted in to th e o pen area.
In th e u se of the JFY fu nction th e fill o peratio n is m ore co
mplicated\
and will b e describ ed below.\
Having consi dered m argins and fl ush t ext i t is necessary to consi
der t ext whi ch i s not i ntended t o be fl ush t o t he margins. Tex t
wh ich m eets th is criterio n falls in to two cla sses. They are
"centred" text and "ragged" text. This\
Standard deals explicitly with ragged te xt. Centred text is arranged
between m argins such that th e open space to the line home position
margin and to the line limit p osition margin are as eq ual as p
ossible. Rag ged is th e term ap plied when text is n either cen tred
nor flush to a margin.\
The process using the JFY function invol ves the arrangem ent of text
between margins either being flush (explicitly) or ragged (im plicitly).
In order to accom plish flush to line hom e position m argin and to line
lim it position m argin, "fill" m ay be required. The fill m ay consist
of spaces of diffe rent width, words, or parts of words. For the purpose
of this descri ption a word is consi dered as including the graphi c
charact ers of t he word i tself and t he punct uation m ark or SPACE
terminating the word. The rul es regardi ng a speci fic just ification
process depend on t he com bination of t he parameter values used. A
line which is to be justified to lin e home position margin and lin e
lim it p osition margin with\
word fill will first be adjusted in len gth b y th e ad dition o r rem
oval o f tex t in th e fo rm o f wo rds u ntil th e rem aining words fit
between the estab lished margins. Words added to a lin e b y su ch a p
rocess will b e o btained fro m th e d ata stream from its following
line(s). Words rem oved fro m th e lin e will b e retu rned to th e d
ata stream in its fo llowing lines. Subsequent to having sufficient
words to fit betw een m argins the open spaces (b etween words or
graphic characters) m ay be adj usted to accom plish the com bined
flush-to-line hom e position m argin and flush-to-line limit position m
argin action. This spacing is adjusted by intervals, or variable-si ze
spaces according to the im plementation. When the word space param eter
value ha s been used the spacing adjustm ent o ccurs between words. W
hen the letter space param eter value has been used the spacing adjustm
ent occurs between adjacent gr aphic characters. W hen both word space
and letter space param eter values have been used the strategy for
selecti ng which spacings are to be adjusted is im
plementation-dependent. Speci al cases of the above involve the use of
partial words in the fill process. In t hese cases a hy phenat ion
process i s used. If t he hy phenation param eter val ue i s used, words
may be subdi vided according to an im plementation strate gy at language
intervals, often co rresponding to syllables. If the Italian hyphenation
parameter v alue is u sed th e first wo rd wh ich will n ot fit b etween
th e m argins is tru ncated , th e last charact er of t he line is
underl ined and t he rem ainder of t he word i s inserted in the dat a
stream for use i n the next line.

```{=html}
<!-- Page 96 -->
```
-   82 -

```{=html}
<!-- Page 97 -->
```
-   83 - Annex D (informative)

Implementation-dependent features

The following introduces, b ut does not exhaustively list th ose matters
left to the implementors. 1) The control functions which will b e
selected for implementatio n.\
2) The number of bits, num ber of charact ers, and form of the b it co
mbination or bit co mbinations generated by a single or multiple key
depressio n.\
3) Whether characters entered becom e immediately visible or are
processed (part ially or ful ly) pri or t o becom ing visible.\
4) If there is a buffer, whether it has a capacity larger than, id
entical with , or smaller than, the display area.\
5) Whether a control function occupies buffer space, display space or
both.\
6) At what point(s) i n the processi ng of t he dat a stream cont rol
funct ions are t o be execut ed.\
7) What the representation of an erased state m ay be.\
8) Whether certain control sequences rem ain in their encode d state or
are transform ed into data in special registers and t ables.\
9) Whether or not t here are i mplementation-defi ned values for param
etric funct ions when t he St andard does not\
specify a standardized default value.\
10) What actio n will b e taken in erro r reco very.\
11) The initial state of a device upon power-up, including the settings
of the m odes.\
12) Whether t he wi dth of a di splayed charact er posi tion i s fixed
or variable (dependi ng on the charact er occupy ing the posi tion). 13)
The action to be taken by a devi ce if a control function or a graphic
character is received which the device cannot im plement, because of
design lim itati on or tem porary functional disablem ent. 14) Whether a
change of the setting of the CONTRO L REPRESENTATION M ODE (CRM )
affects the appearance of control functions already entered into, or
received by, the device or whether only those control functions are
affected that are entered or received subsequently.\
15) Whether or not the characters in that part of a gua rded area which
is containe d in an eligible area are transmitted or tran sferred .

```{=html}
<!-- Page 98 -->
```
-   84 -

```{=html}
<!-- Page 99 -->
```
-   85 - Annex E (informative)

Text area formats

E.1 General The purpose of t his annex i s to provi de suppl ementary
information for t he cont rol funct ion PAGE FOR MAT SELECTION (PFS)
defined in 8.3.91. E.2 Dimension of the text area Table E.1 shows the
dim ensions of the text area corre sponding to various values of the
param eter of PFS. NOTE 1\
When det ermining t he number of l ines per page f or t he paramet er
val ues 0 t o 9, account i s t aken of any additional space needed for
an optional "call identification lin e" (see CCITT Rec. T.60) . This
space is not included in the text area. NOTE 2\
This annex does not speci fy t he number of l ines per page f or l ine
spaci ngs of 6 per 30,0 mm used in conjunction with the North American
page formats, or for line spacings of 2 or 12 lines per 25,4 mm or 3, 4
of 12 lines per 30,0 mm used in conj unction with any of the page
formats. NOTE 3\
This annex does not speci fy t he number of charact ers pe r l ine f or
spaci ngs of 10 or 15 charact ers per 25,4 mm used in conjunction with
page formats specified by PFS with parameter values 10 to 15, or for
spacings of 3 characters per 25,4 mm used in conjunction with the page
format s specified by PFS with parameter values 0 to 9. E.3 Line home
position For the page form ats specified by PFS with param eter values 0
to 9, the line hom e position is, depending on the character spacing, 6
characters per 25,4 m m: the 4th character position of each line; 10
charact ers per 25,4 m m: the 6th character position of each line; 12
charact ers per 25,4 m m: the 7th character position of each line; 15
charact ers per 25,4 m m: the 8th character position of each line. NOTE
For the page formats specified by PFS with parameter values 0 to 9, the
line home position is specified so as to provide a margin of
approximately 20 mm between the line home position and the edge of the
paper. For the page formats specified by PFS with param eter values 10
to 15, the line hom e position is, depending on the character spacing, 3
characters per 25,4 m m: the 3rd character position of each line; 6
characters per 25,4 m m: the 5th character position of each line; 12
charact ers per 25,4 m m: the 9th character position of each line.

```{=html}
<!-- Page 100 -->
```
-   86 - NOTE For the page formats specified by PFS with parameter
    values 10 to 15, the line home position is specified so as to
    provide a margin of approximately 25 mm betw een the line home
    position and the edge of the paper. Table E.1 - Dimensions of the
    text area Number of l ines per page for spaci ngs of Number of
    characters per line for spaci ngs of PFS param eter value Meaning 8
    6 4 3 6 per 3 6 10 12 15 per 25 ,4 mm 30 mm per 25 ,4 mm 0 Tall basi
    c text communication 73 55 37 28 46 46 77 92 115 1 Wide basi c text
    communication 50 38 25 19 32 62 105 125 156 2 Tall basic A4 78 59 39
    30 49 46 77 92 115 3 Wide basi c A4 50 38 25 19 32 66 110 132 165 4
    Tall North Am erican letter 74 56 37 28 48 80 96 120 5 Wide Nort h
    American letter 53 40 27 20 62 105 125 156 6 Tall extended A4 88 66
    44 33 55 46 77 92 115 7 Wide ext ended A4 58 44 29 22 36 66 110 132
    165 8 Tall North Am erican legal 98 74 49 37 48 80 96 120 9 Wide
    Nort h American legal 53 40 27 20 80 135 161 201 10 A4 short lines
    59 39 30 22 45 89\
    11 A4 long lines 38 25 19 32 66 131\
    12 B5 short lines 49 33 24 18 38 75\
    13 B5 long lines 32 21 16 27 56 111\
    14 B4 short lines 57 50 38 27 56 111\
    15 B4 long lines 49 33 25 39 79 157

```{=html}
<!-- Page 101 -->
```
-   87 - Annex F (informative)

Differences betw een the fifth and the fourth edition of ECMA-48

F.1 General In t his fi fth Edi tion of Standard ECMA-48 a number of t
echni cal addi tions and i mprovem ents have been introduced; they are
listed h ereafter. Also ed itorial im provements h ave b een m ade lik e
th e can cellatio n o f unnecessary repeat ed references. The el
imination of the Lat in scri pt bi as was al ready done i n t he fourt h
Edition, where som e of the term s like "horizontal" and "v ertical" or
"up" and "down" have been replaced by terms like "character" and "line"
or "backward" and "forward". As t he acrony ms coul d not be changed
because they were already widely im plemented and referenced in other
standa rds, some of them are not really acrony ms any m ore, like VPR
for LINE POSIT ION FORW ARD (used to be VERTICAL POSITION RELATIVE) or
PLU for PARTIAL LINE BACK WARD (used to be PARTIAL LINE UP). The m ain t
echni cal addi tions concern modes and control funct ions for handl ing
bi -directional t exts and t ext communication. The m ain cancellations
concern the m odes and cont rol funct ions l isted i n annex E of t he
fourth Edition the use of whic h was already then deprecated. As almost
all parts of the text of t his versi on were m odified i n one way or t
he ot her com pared t o the form er versi on of t his Standard, t he Edi
tor has refrai ned from putting change bars i n the margins. F.2 Device
concepts Clause 6 on devi ce concept s has been ent irely revi sed i n
order to cope with the speci fic requi rements for bi - directional
texts. F.3 New modes Two new m odes, the BI-DIRECTIONAL SUPPORT MODE
(BDSM ) and the DEVICE COM PONENT SELECT MODE (DCSM) have been
introduced. F.4 Deprecated modes The use of the POSITIONING UNIT MODE
(PUM) and the ZERO DEFAULT MODE (ZDM) is deprecated. Their speci
fications have been m oved from the main text to this annex. F.4.1 PUM -
Positioning unit mode CHARACTER: The uni t for num eric param eters of t
he posi tioning form at effect ors i s one charact er posi tion. SIZE:
The uni t for num eric param eters of t he posi tioning form at effect
ors is that established by the param eter value of SELECT SIZE UNIT
(SSU). NOTE 1\
Control functions affected are: CUB, CUD, CUF, CUU, HPA, HPB, HPR, HVP,
SLH, SLL, SSU, VPA, VPB, VPR.. NOTE 2\
As the default parameter value of the control func tion SELECT SIZE UNIT
(SSU) is CHARACTER, this mode i s redundant and shoul d no l onger be
used. F.4.2 ZDM - Z ero default mode ZERO: A param eter val ue of 0 of a
cont rol funct ion means t he num ber 0.

```{=html}
<!-- Page 102 -->
```
-   88 - DEFAULT: A param eter val ue of 0 represent s a defaul t
    parameter value which m ay be different from 0. NOTE 1\
    This mode was provided for implem entations of the first edition of
    this Standard which specified that "an empty paramet er sub-st ring
    or a paramet er sub-st ring w hich consi sts of bi t combi nations
    03/ 00 onl y represent s a def ault value which depends on t he cont
    rol function". For numeri c paramet ers which are expressed i n uni
    ts est ablished by t he paramet er val ue of SELEC T SIZE UNIT (SSU)
    the value 0 could then be sp ecified . Fo r n umeric p arameters wh
    ich a re effectively rep eat count s, a 0 paramet er val ue
    corresponded t o a "no-op". In ei ther i nstance, non-negat ive
    comput ed numeri c paramet er val ues mi ght have been used w ithout
    treating 0 as a speci al (unusabl e) case. Where an explicit paramet
    er value was not used, i mplement ors w ere urged t o omi t a
    paramet er val ue ( use an empt y paramet er sub-st ring) to imply a
    def ault paramet er val ue. Control fu nctions a ffected a re: CBT,
    CHA, CHT, CNL, CPL, CPR, CUB, CUD, CUF, CUP, CUU, CVT, DCH, DL, ECH,
    GSM, HPA, HPB, HPR, HVP, ICH, IL, NP, PP, PPA, PPB, PPR, REP, SD,
    SL, SR, SU, TCC, VPA, VPB, VPR. NOTE 2\
    Since t he publ ication of the f irst edi tion of this St andard i n
    1976 almost 15 years have expired. The use of this mode should no
    longer be requi red because the definition of def ault parameter
    values has been changed. F.5 Eliminated modes F.5.1 Editing Boundary
    Mode (EBM) The m ode EDITING BOUNDARY MODE (EBM ) the use of which
    was alread y declared deprecated in the fourt h Edition of t his
    Standard has now been rem oved. F.5.2 LINE FEED/NEW LINE MODE
    (LF/NL) The m ode LINE FEED/NEW LINE MODE (LF/NL) the use of which
    was already declared deprecated in the fourt h Edition of t his
    Standard has now been rem oved. F.6 New control functions Five new
    cont rol funct ions have been i ntroduced, vi z.: three cont rol
    funct ions for bi -directional texts: − − . SELECT CHARACTER PATH
    (SCP) . START DIRECTED STRING (SDS) . SELECT IMPLICIT MOVE MENT
    DIRECTION (SIMD) and t wo cont rol funct ions for t ext
    communication: . SET PAGE HOM E (SPH) . SET PAGE LIMIT (SPL) F.7
    Modified control functions The control functions SELECT ALTERNATIVE
    PRESENTATION VARIANTS (SAPV), SELECT PRESENTATION DIRECTIONS (SPD)
    and START REVERSED STRING (SRS) have been am ended to take into
    account their interaction wi th new cont rol funct ions. A second
    param eter has been added to the cont rol function SHEET EJECT AND
    FEED (SEF) for the selection of t he out put stacker. Whether the
    control functions CARRIAGE RETURN ( CR) and NEXT LINE (NEL) m ove
    the active position (the active presentation position in the
    presentati on com ponent, the active data position in the data
    component) to the line hom e position or to the line lim it
    position, has been m ade dependent on the param eter value of the
    control function SELECT IMPLICIT MOVEMENT DIRECTION (SIMD).

```{=html}
<!-- Page 103 -->
```
-   89 - In t he defi nition of m any ot her cont rol funct ions sm all
    adjustm ents have been m ade; for exam ple, references to SPD have
    been cancel led when no more pertinent or requi red, dependenci es
    on new m odes have been included i n the defi nitions of t he affect
    ed cont rol funct ions, et c.  For bi -directional devi ces t he
    cursor cont rol funct ions are act ive i n t he present ation com
    ponent ; t hey are independent of the setting of the DEVICE COMPONE
    NT SELECT MODE (DCSM). The control functions for character position
    or line position m ovements are activ e in the data com ponent; they
    depend on the setting of the DEVICE COMPONENT SELECT MODE (DCSM).
    Their dependency on SELECT SIZE UNIT (SSU) was rem oved.\
    F.8 Eliminated control functions F.8.1 DELETE (DEL) The character
    DELETE (bit com bination 07/15, see ISO/IE C 646, clause 6.5), not
    being a control function in the strict sense, has been rem oved from
    the body of t he Standard. DEL was originally used to erase or
    obliterate an erroneous or unwan ted character in punched tape. DEL
    charact ers may be inserted into, or rem oved from , a C
    C-data-element wi thout affect ing i ts i nformation content, but
    such act ion may affect the information layout and/ or the cont rol
    of equi pment. F.8.2 INDEX (IND) The control function INDEX (IND)
    which wa s coded as an elem ent of the C1 set (08/04) and the use of
    which was already declared deprecated in the fourth Edition of this
    Standard has now been rem oved. F.8.3 CHARACTER TABULATION SET
    ABSOLUTE (HTSA) The control function CHARACTER TABULATION SET
    ABSOLUTE (HTSA) which was coded as a control sequence with any num
    ber of num eric param eters (CSI Pn ... 02/00 04/14) and the use of
    which was already declared deprecated in the fourth Edition of this
    Standard has now been rem oved. F.9 New type of control functions
    representing control sequences w ith no parameter The earlier
    editions of this Standard have im plicitly perm itted control
    sequences with no param eter although this typ e o f co ntrol seq
    uences was n ot ex plicitly sp ecified in clau se 8. Moreover, no
    control functions were defined whi ch woul d have been repr esent ed
    by such cont rol sequences. The t ype of cont rol sequences wi th no
    param eter i s introduced in this Edi tion of t his St andard. W hen
    cont rol functions rep resented by co ntrol seq uences o f th is n
    ew typ e will h ave to be defined in future Editions of this
    Standard, it is in tended that th ey be control seq uences with the
    sin gle Intermediate Byte 0 2/01.

```{=html}
<!-- Page 104 -->
```
```{=html}
<!-- Page 105 -->
```
```{=html}
<!-- Page 106 -->
```
.

```{=html}
<!-- Page 107 -->
```
Free pri nted copi es can be ordered from : ECMA 114 R ue du R hône
CH-1204 Geneva Switzerlan d Fax: +41 22 849.60.01 Email: d ocuments@ecm
a.ch Files of this Standard can be freel y downloaded from the ECM A web
site (www.ecm a.ch). This site gives full information on ECMA, ECMA
activ ities, ECMA Stan dards and Tech nical Rep orts.

```{=html}
<!-- Page 108 -->
```
ECMA 114 R ue du R hône CH-1204 Geneva Switzerlan d See inside cover
page for obtaining further soft or hard copies.
