#!/usr/bin/env python3
"""DataViral: 500 propuestas, Reels/feed/Stories; edición de retención y fondo monocromático.

Las referencias son opcionales; la ausencia de fuentes no impide publicar.
Los datos generados por IA no están verificados independientemente.
Para contenido sensible, mantener revisión humana antes de publicar.
Python 3.11+. Dependencias en requirements.txt; ffmpeg instalado por workflow.
"""
from __future__ import annotations

import argparse
import asyncio
import base64
import hashlib
import io
import json
import math
import os
import random
import re
import subprocess
import sys
import time
import urllib.parse
import wave
import zlib
from datetime import datetime, timezone
from pathlib import Path

import requests
from PIL import Image, ImageDraw, ImageFont

CATALOG_B85 = """c-pmnOONC@lIC9#`dpP2??>-p&|BTTvp~<FXR0xa#bOV1iSEH@N>osiS7t8u$K){&aTw&SE(47Ju{ASF9*^{g{4?&QJ2NZ7j2}fB?QQ?-
|NPEXzx(~~{`hY{o}Hcl?uXx%rnjpQKheMawR2_gVYPWS#iybSbsJ)DYG<21&`<WR_m+Pw#Nuh#d@X$Fir#j;ThSld!B(~@qAf$LOe`u#{~`Ti
S4P+N^qc(WFvQZPKYQDCp`kzj>0|3%NxxJEqCn(g(VoPFmdk$~8p9+yTMo7<ohd>wbb<e=jJ6LSe)oTWcn$vog8%d8TOEqd7RwN8Lp+P6@x&!E
*I1!|%Ohklh?lxA9Q@i<rly^5LcNH#<K?)`*QT&tIg}5k3Z3=?&*6cAzk<O33oq)yl$Mrf`8&|>#KM%lTifl|Kv6%<B96hm)_v<}y|po2v4R-
T0{8?PI+Lp*(kH64U-~!)4ET-W9-B`?WnKhI=bEB+k^W@bp&_}Wy3NOkV{mWrV@)hQ@fzaV6qWVq?gh<R-
c1n$cBebQd~sSEX}zYK?viQfjab@9zhkH6tm$VANtkbq_CTM`5!;x1#Q}HC(hr|(LEoku?B?G?K@TYN4&L!nv=Xg6jSI8^=Vw~cHr~L7*7Y>Fw
ehy#i`m9d4W&!#Sw*wRb1qKhhi!^dd!x0{*)83|@!Q)6{y3~`m8M=e`v0}-+`?P+`#zTswh0%wFbpKMB7GM>3S~OG_2%2!@!#p^qmebbhIJE-
h&+W4wh2ltkGVCWcS~A*I*+7N+Zczsl^fmKrhEBy)nPb+6}A;uc|>I#_!T1=#_W4Tx(ZA6&2#B|E;)IC1qNNI{}D~gCy=$%C{LR#s*_*!_L2T%
_^n^t&)QRP0xN7QG#cS@AO`fJ%W)j|AeN2@CGF-
>XWkv5je)(@eRmShm3$4+<LIXhi>mFlbg|LfcyoAQ;O|t*Fm1bC+LFG*FMSN5RcgZT$zhN*+8*m!wAtyES%#92R@c(<I{JewWZd*tqv(_fFK9C
^l$sx{tTgnb@U<%pe;W}j%uSx&Eb87YCK&v4?eXqxC-
Q|kEM2Tsh@Xzp#XxHOa4a}%vof217ol2)j&9$>&{R(8i919XgQ?ciik3ZNtVB5C=3ibD`eizJP3etZKbye>gMX!UTNpN@<&??wYBygaeGH@bUh
E-
^!Ms)+=H$*^4UQK|HiI8;6<;$mbjB;ZaOHds81Ngt5fa9if{$Z0zNA}?xuI)lOFoNwoAe}R*mm4zQcQ@~V5(@dsU{Oa43^SI=Sj7<U2m$*GabZ
|{>DyGV%FP_y>KOYQ(5(sJeLo)3HNG;v)H+j&slFeTHV5QHiN5q7g-
46C8l@%JZ!!+l~7&Nf3sxU#hPS|5pOpMnTp<)%0(3FO!63Hr9aJdfq1ZyV<y4DEBC{SY+JR&I!qk{tni(6Zq<krM|gIYv?R|T;9>J+;d)g>;Rt
CA>ZQu2N<Q0VbY(fJ2_t*@52WjFe(RNPp?NGY=vPX&&~(>GFKo?d?ePzj&93$X9iWYYz0TndX0x^FdCBae<}?Fao6bofdOU@h9Kv%rVH=Ul1ID
3QH#%frE@79=3$}+o23qL}bLj^-
PGfr)#}Jli3`v{F5e}Kf1cQI4Gd)<+CY~I>szsOJ=uJg7uxpIg?l?jogM6<`@nDt0utq^@QsgzI^_lX)XcIgRkcOaMo$2kX+S0*mY-
u~!ONvqJO|xZ~!>BsU0Rw)n2X5=|5^dshXMAs?So=h{$>If^%Lm(p3%$ufN@E;ztk}^JBn7FX-
*9!vk>_%l0S5b0>okgXZTv8LIm$q)W$)G*d`7$JVj!>7K5lw9BKzHw8X?v%n?hX{XUQ@880hO93W|J)u62`--
Lp28M>p9?8iRV1!DqsPMK+t(&u*&l%H>Xv=;m9jY=&=r3NLIk)P6D6mdwh9X`ROFU1Q(V#K5V&W3=6*I`pm@M2faCtOHrX{Fvl;qmDAbVBhEQd
DBl+Vg*De(WTl}oEenM;k}1E1o`?bhwr2heu|&g#<TJt^LS2n5XN9CbuY5(SA!V1ru1as7xm^#m(+qm)CF~7!7&CHY>l>6*`6c7iRZLFdO73DR
7xZ25M>OgTE7}|^iv9Z2EFPnJq*;9He0kC*sE;UY{T&VVP&4<zMVcXbT4TPsz!^FQ^Y~P$x7jWAbD91ojNz<2yG1PjY8(Kubgz7>DF|GSvYzJj
mnX?pDG6MR<9_w#+wDFl(MG28YH)rK7-icO9Ih{EIQ&0HrN(ud|0im(%q^OCl2|U-jwjGS{@;bLA+PVTxPa39Ji;tRTU4Rc8#r-
f_FDj2;R+^P8lpE6d;>yKbn=OF`SeUx_%%zVjivD6*-
3o241Nz+1HEihu8OvT`X!#{xEqA@<k>?zKxqNCCBRNK(>4mt9+LH4%!&lORYX^WEmt*VhkL(O~r6zeTjQquMQukkAYTaZb=?!X<j88k=;qASFL
+~j}ph=UhAu(?W3(*DRLQkbW_}?$x#n|fIJ3S6D{QbOdHN3G!%wZp_C#iuVjWA%H!lQ$hq>f=)A2g8Jf8gYj={xAS%64mR`fkNpQO94DER@v3k
FGu3ewOt$dg~23h5avP;*vch)rvPg!VCn(hZ_Ltt<9x$#SDtA#25&d;JPH_uC=kV(}zL>z;w)UDQ1fa3fxMlCkqTFDI5BHc$91F6xbMn`taa7>
Y!fh{s0bOz7?x){hy^}!9B=PHclVsw)TKo0lJUcwkmwcbQViY4~mWpJ#$(89o6>!a|lCR?j{R}|gG!7faW;QImc7~~su#X@D;etf|@(!oP?>S)
zIvKYi$mAhqI)h#AgSW0z_vO-}mRSe*rzJAO`yNF!+LSo&u+r);o%~3bDmpBIZK9@00U%|GMMdgb+tevU?ygY#g1pV$z-
#tX0G`eH#(e!rPZi+>x6e^G1rn($`L+0|rHbYT2ICd{#9%N;jo_{B4s*;~t7*(6ArxRFU(3M@im{T9Q2uLa$P4ii}Z`1Cz?Y)lC$3S1^$$Tvb(
tF5EA+cLqE+A>?DP_-5wzSv%95CQl%9s#8Gn2(Rw(`M~e4mbx#UN^8d=hAkg-KyY$x6&{jQ3K-0A|RKlF*`W=}%MgDR&9vnu0P<-po-
J7<7&PWk0s`fQ&rTnpjO5S?QeTM`&YU@05YB?YpqHQSw~y<e;a6L@{{Ez73%X{P5F?Ugrg9J2dR33IV*=)dZ$6YV!ZskG+kYFWn?h!Wc7FmIcn
>fB`?x;vQ$F=2fqRwTs4Q@{RALje)&Tw<#FI6Ksid%QM?a>a4gv!@`?P+4i&8U|VpRt?Nd|9a7eAEnG8p-
FQP61F7khC4D>xsh#H*C+5+nV0!A85tX&fN2z0gGkCC8aq~qIEK^vOjkFNi@2d~p9wCoGzR6<-Zc|@qQPPXK4vouZ0q&-
b0oLeKyo}VDF0ow>(!;Zjt~Sx>^r<7XF|c>J>bL8G3p|X77o+Q_a*!|vQ=?bC)YTTDb<J3<(-h5M*RPJA?iHTL0|9@2c9yxKVBxs8Nz(4=gH-
0l4UxUL-~cadGv4W8Kf7sT8^eiP-
U^6m6aHcfKYS*8+!H6VS1Ue~WSEEYAr!T12C29uW8K@;TlqcyCVM4+34V0Qc7=Hee3p%;Pn?=~e@E{_@fRc2Qr1f{bHDjgjBLx~+bn61QU|=+c
`rsY9h|>APiM*YF?7GD$6eTO%P4zCicVnH;Mhz$+US`Ve`ec-A6^=Z5);yhi01ZR$Y3>9_)z>$sYj&+NQOK&S!^V-
7Z#7S(?6ttW;gU|FjHnt3aBuA?g=GM`46v8#zWt?-S2<;sbg%V{m>Av538{L$(q<d{IoP>-
~IIZ`26CSE`v+o!?LDo9!>m#*3pqhLu*b8nwHqT4(4oshIVMg_3ngRoOD87E3Jl`7W2w#H$J^aAsO1^l(8#ti2)q@;mEP<=s@+(ORf+*s<=ega
?WyXn>^XU^EhD}aCOoKjBZ`CkRUyuWIBI;b2iddTG18Jd2{!Y#h_hd-`0MlBW0Uy&!apovUXF&fZdz~OcWGJCl}^R(<K>6Tl|-
yQE4apsbauxu`iZVMmiSjksGgdA{J}c)l$yG5;B8DF^>xd{O<HGn!Ihc^sW^P?sbFkZYX6Y1gi<P?etE)S!^)q_t-c8Cwda?7~U%)-
blFJOAvzdzP0|GFZs%NW51&9ZHOWDd>#L$YymZk0S5OR`+A*Z6<2hAnu2@U($&fk2i{E;19oxxcNBeuMS|h>1w%FNa7PkC_4y9b#lR`Fp3qd>{
crQ!)smGb`X=|+8YArdPoy)K9N)-
OKYtoWY(o$&XiB~qYu3Es#c@R`8LWy#$Z{5O3?`@%J(y3$I{4DC#zJ;Pke9yX(meX(BE$?|dJYc^G@vcHrjp_oU)a`3(`nTO-
a!t70_sP`uLc>Z6ZqtiK`LW)mYZ*#%g}-
AFm(**9b%P?v)<B`sksG(BGaNgL=yvbj~dfbOz5S%*H~P*iq1;*hw)_2+n6Qc^C%Mt_Qe@&t?(d=j<}JI{UZBxy#fzY#sHqH4=eki*qxP3DE9A
_CgZu?MIM6+`h(anR&Ktsi!4>8)H0tWM}GMZvKX{WjZr-^Uc0sF@)*>wDPn-G;BRHvXW1Fgb{+dZ*_Byw|FsMsY%gsL<TY^jN*Bw)r!fSEi!N-
+FdNU3vcB#JaSSG)!%WQ-KFc({dPsc~I6T(m>C&*1Fb3}yKB_h6%`LhR7wih&eEaB9Pa<0PBIrBn9_N4o#{4~WthyntMh2zbd|_KaUjVU#C<g0
Z{SpSBRbyjv5R}U^^-DLplFaA9XME^hQN@6P9-A>}_Ngent3^vpiMiqcRo}D2)G?qJio=-lG>3)FHGMi!!+>0>T#Aje3opqa3Or8-
iDIy>;Mig`pTacu*x1x~#QS0G%(hW1)2ees8)x&vHsKn62$*%s$?G>?W1Z(A_?{>R>qd9?3KPq)d5*5jHvN4|5d(CKdQ6Llp|+CiJ@tAm?Ap)?
%auuggaHN@jYrX?=#pGW%I^>trZE}1DeWSQK|^#D>50;Erap%NQ`3R4FbkLFJF$CSM1pdb={zP7>?>Vds;6sY#~uq0^y4LIiJ6{~U8FIH=dj9F
(rx)HQcv6n<zU!FTbgyAD8_LP7+@eq)ko8GsdS7*hpofPhlSJK(Y-`5SYULj8!EXulGkOMWppOTtkpeaF=)y-6S0kUDbbN!(WO@;F-
U+0)0&p9gxrL*f|cKVTMYas(kdIJi}yHn4CoCkUN~>@TWwZh3QrfCFC|`#)XpG{LA-
^YeRh(#lHMv8>ZBEOTsB7^@ttHbXm^mKkbWb&&#AuNS!H$6dukYvdpvgE4y}`TfM|-
++l`bB&Zo@M!*nlo2<Wv=V_Ca6NVsERO46%z)k25pV&K4-
QII$eXFrTVSF@Jn<W)31w=GfIOGg=CaKX5dB)Ja0<#1h+=L=G!I17*a>*p9Bb({kR_!9WO((u=EJpx%dBqzo}8G)Vbk^b`4lbqLm;dv}D$XB>v
G7I}CamspN=QFK&=uMX7q1}`*fY;caC3!e3{itg>=B6F^wvQ+V3y3XAvBu`NMmo@W5*m%`ImS%Nm3Ge89<mrT&}$>&E(H)4#(Uf7&*Bb}7$iiG
83!G3amXT0ndc(lS^9BVOpZAU2gqYkK~3kC{*ij>O-W>>T^ce4+K{2O-
7F>$>>EJuakZ>el0?OS6qliMT}l)+5}TzLPNf3PWPw3GSD3}Tq9y0~Zl2jha9y^JT5qUgz%KAN@gY2#tx`g!PpI>}h`Z=w;1C_B<8YDWfbgQo2
Kwl@wY2Uz+)Wb$bp^hLT(p!1EOQ;ADONUe(|`4IxQ8wV?pl#QO5$wuB`$(AS0iD^-PPnQWyv4iOC19W#-
A$Jad#=xOxvBNg0J<R`i>FDU;_Rc5pY{abkZLmLc>~r?Kn|z^IU3^Ea&pTK;PkMw9#yyKXXlesxTy#Y;Exdo9ztJ7{q%#7qM9SkfC|{4ssBb+c
