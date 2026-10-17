#!/usr/bin/env python3
"""DataViral: catálogo integrado (500 propuestas), previews y publicación de VIDEO en Reels y feed de IG.

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
WSc+9myDCFRoG_>J@}>F_YQCAjpp*SkArvcaI^@u&wWJEyJhbEI6pqJ{yvP<i4=zmVWwYr9-
kY_CaTkS=i{A_LW;nKH2|ZjO{{?^y@QAxjQ(zyNC^Pn<vDYCPmy?xuzTxrWn*I4CK%zO^e;n5m0*2Jyd_GzRfTrGpk`E#g|{U2tnFt~>AbPr^(
V7-T#HIJK1LltC#BoNR!#DL2nKB5VigV_-oI=7C$3abKL4pRBRip1Z;1NF+K)9D{kU6FEj^MB7|4XCwzfxjRGC^vG0;G6l{TOM1M7b72Oux;Nj
}&gU4{bdUiC7q99LA6;cer6b0Wp`!a8MGVjd8rW|Ck$!0Ecff_%`k?lABr!;ru*7^c3%=9Q)`MMJHdV4z_Us~yLA%llj%d04H?JmTL;ScfT}DB
&lRO6X8qO>2=*BPjLE<AdG-<{au~}K4Ew%J04-7P*--L3Ak?k^RwNhISUdF<F-
uzbThI}6+jKRCrdD+;#&TcRwpITX1Z_7Tq(q(W}%wmGUzSG{?1^sf|JezzMb)tv?x`!p~+BIesc>+VeOt0@~LZI%?K-
+@5KAT>W2C5L%cEnq97?g9BTjIgBn{O$!BaKpn;^;lip^bsWJMh_$t&Of0@A9_yArBsl!RKffeSka$^%7OGxm`6UKe{njUawWZr-
%UpGh(D8<@CUkjyQ#0#V4x{TpuEi!Ms*gREWVMe_b0tDHy5_s^xqR7~mVYTiZCEa%{XQ50%f*ooyFc4B9Ph`K8pdrZb-cXMb497i8(4qpjC|;u
uVzzUieCbF^!h+#<Y0_VaalT0HL{jKM=ZFH=T~Bm;)Zj`NWJKeTo}$^!v?aRz8Msjl<I8c%=U&VZO2$g9E@b9rE(-
|0Yqvt{$r&$?pg(7ri*FD=wr0h8)7Q=7_6GtQUBcd5gAmt!*DDeSPVxHxGm-ektfhp>%j&6GdRgX<n#v&xYbw}&(a@e=#mL~bo*XG1rhInMiu<
4f2_(`A`SHj@no{puv>a=Xp8B+U#QpP+SbXWH}2!Tq#@Qh3khfq}lpzPB{<3jHK&=vlGcvwc`htIN_Y><|MC?#=1ncq|Vty;<8d>agUPaBI5m@
AgxM!s9)ZF@U$H17vGCawGYa2DWs*k1t0o!}WbSjSB|+4m-%M>3YK_i*C^{7A#11@i_iaJw@>deGKe9@DRNoEoO>e?Sc*-Y4MfGHn8jsRS4Mo-
o|r|@7BBwHR-dxlXrm@SGhEJX_^wJj!vJ%2!nrqI{c|uRvE(IU24DA+0~$%{rhyBG6wMCbbzm%UM**)cFDfpe5sA}i{uK<&9^1qitFh#E*S7j{
GByzTeKX+TiLf&RXN_+y~Ht?fDXl?UvxSNz;=C_jm}B`>8)3cMtGV_9|L<0NMTRcM`k9Qah6TA+?=5c#Lg?LWRB3rKw=t`47OQDlN#CCk3DxvF
U<5OeTe%Ibqwe&enZR9reSC-AES74qm_oXVuq8ImhHaIWQA?P9jqNc3^G26o<cf-Ugj`0q}8spk(?RiF{qdZwRUWGjt@j9>*%fDd{w+Y<qXmg#
0x-|icZE=zDlYe^_#Bvmw%--
b)xLKN|(Gpp9=>39KXr`{STwT>6$g?8^$pkV^R)sT;XFpFwlr^YSLJz6?836|1&A+QfnC;BaXqmR4I_$7~eMI^u2<=fbzpW&1QhXy+V)j==|P>
8Eu+G+hqvL?xBnUM0BWknNnnr*`^w`R^wM33hx!&3d@t2V6ag?6iG+hF3sOFOi`aGVE}Gb9th8sFsWI*pZ<BWE0>1V)l5!_<BTx)pts43^q09-
9sS4Qlg&7{wmppt2K*j6xU?d9>KZdS`$$y}`Xq`SL?Kw0fUfisRJCj4hZK((Wg{;(Sz(gY-}NC={B{;AYzqM2(@SQfWo!$Vm{u-
MX2`F0ktcQX00Ru}1!~v+@t=Ruo3BI!TlS^qp#J0E{`S{j@*G4Vg+aK2Wv8d#5(bm=T&B@hHcXM;43hIG4-7P-
=Zs^>*g)F4bXxN?*k0)<Iz$+QccW6v|A+hW&#n-QsJF4PeI{-EJGvM+*fT`;rFY>a{lJTb-
|=ANo~<C}Xg}t04bA6;Z36Ba`uUIloWTV|RIr8LD=dsD0Mc?>I?D;g<-_J{#<6?vNkb5?&aj}b#IJbzd&-%a+-
q4fufHdYK|4oMZe(iXY9MWa2f(L6r0i^onmWdE4s8tNh2~Kg*|zyA9q7cx67sz8-
_ymwUBb`3YnD?QakS!TXi4WCvwi9|<}j3w^1wh}!P2rH8xL%^-
!5(0yLFBh_j_q$Affn|wJ~)o=L6M;evHMD$e<NfPT2(KIC%`}4R(ktCxRilL3!*Uhv@i21d@x%4X!=IGgx4dZ&4T3GBjgguD0XUC%w072T=^x9
dKw<#)mAec3p}XFHBP!bwAvLlrez!DpfqPM`bEWX+k}=!;V&`7tG@T0lq#%ADE6KrnT*i<hHB~DP_!UMIWT;IrpDy-
g)+1lcjm}OkUU~oNH8wBrR!Oflc0_(N;Jeri=l+&;$zTp$|)&((Po*OKqCUWNYKNgEj^d)RnkBVZ*I7Xhj`Q{$N>YyV7*lNU%abq2dSw3@)H0N
jC#}4>r#{@j4~Er)6ml?0%{kuxphJ=Gmo@Z23hTL|<uapDVX*7ikP47Qsp(LsB_K5O}i)QC*(4lO_fViE5c;YE7KlWb^EGx8@QuIz;98q^ktY4
Eh*Y)T2`@91DZZZws$1T-rengK`hsn5=-=(c_zZXWWe<Duqfrp92K=<_xwk?MHTnno<3-
E0f8#+({P$cdoE2)2_+~Q0Xz{VX7Fg3;39h8V09CrA0`)u#RV%M!PMG%5YleF~Z;jv8yRB&P=1_yI~9jcB&MJLv%54SCFG}dYI#A38WuygWo)J
p_kNn*>&(knZa{;8Z&Ggt~GWDy>t&#FuxmWo;a1V;(D9M967)MgL|Va#3@?SN8aqvl|u|12pF^SvsLBnXMsV!MJq%{Pscd1Np78O*4)=BQ?1nu
78v9^TyTxMJ^GTzylu7*$w~}4B-lX)7~FeJnRB#b6<-
&+mabdqOqZw1c^72};O%MJ)6c`^3){PCUg}^M(tEofxEl?fto301n(RfMkVp596IK*GB@tfOCY&om6w%62GrpJhE?j|}B|Nc%E(Q+Nw4z<Pu8&
f#IoQZr5M47)0*O&k$KB4QkAb}e?ki6^tXWjDW|y+a=&viQ(=ql^#eiLDl!-Pv>EM#Kf0%*>+owPqmpF|RwgJ~z^qa-xly*<{inNjZt#@7<`QA
qt1Bb@cLOIl_ZlaB(<5XilZ<hk{W;}fAxY|5681!4b%(=3jjO(;y!p8$5*(K{u)VV<C(8s_c5jWDylPWjz;uz=DEx;{#xQFgA&!CTi1wBzUoiF
JTFnTdLklT&_O7Ftpd!ujhIEx7c`wsU<5w$4#ocN1U-=a@8k3zARHU{!sSG>;gKklLSNw(ZHxoVESCyc=Zb*AZ&69+Z7zhgaSti)9-
Ob3Z$FjX1UGKh|op<?RbNG1tA5n31O9Qqj8E7X<BEu|jWPZAZ9r`$&m19PoQs^UXca-hBBfJ5zku8gYh2xIUNU(&l4lqLJA$MPmx6$gt3Wi8b#
4j5pqCrNq$baZ>Tm@Q?Ja6PzfR)!SSY~G~9Y%u6|Xc-
k*kkiDBaZ+ZbPOsWW7K5hDKS~*EX3+(oLe$(#mP4Mo(vS8sfZ*Pr>3RZkTU_~N{)Jky6_<`fOu0G(?qz_%J=fLi7OiPy;*E!U>X(OTVxW{=i9$
c+BXXg|DqoZD9h5PEh=<7d+K_lRFRZh5&_7HXgLs8EeOQEgk)lGZV2(lhjw8RMlR1Sqw>^yu1{~FjWJYKj&d_IQ((;xZ1_jc9YA$F_70&!;+Xd
2{FaM}hdiD^-
VBIQ=<Er2$FfunIm1KCg(#AuN631ZPDW3*1b!eNXaZ^6q^YD%?2JT*E92cqkfGfRul<dMZ3x(7z#UR}FBqj*#%d<1p%P2#_O#iB-
9RCZc(D|OoLo6`J?=+l$99zb*cV%d*uxpeoQ}5&OiFTur$c_lXu84tyu<8-
AN62F^FJ{9`eayKrRqtd8?2GB>=WU&`*`+q08=$M2n9pH=LA^Zji%!C0VQ7UzFJ+o_5*{QvIbVM@D1+MbSYU9kPW!UUL0Th@`&~3cz4;nB6SFp
-jBZBv0m2xx>)FuWlzEhHs0_D46z_!`u}7ITMvvg;IY*Y~aUK}po729f^a|g6laxi%(*LHu;Z;o*U)N_C+C7T_2KDxIxf|ljG$i`@7MWN+q{L{
sJbI~nkT?eM?zFFIV=|1=(fX0Qr&YSJ$S#5ylzUL7PU4-6AnvCn!9}y88&Z<_o=2u0W&y!{-
<SH>my;<ZbWKWWp`1qH4RNLO)a@mTK?3xg+Eu&&PHK0t9A0|ck>MUWXkoRN?l=bw>;)!AIU#zQc*KH@EF{uJHs4yjyWG=U`WVntb)7~yOD`?bE
Sqs1+*>L(Iw#LT${4sS)h(Qc<Z&zSu+Rozj}pfqUY~v|xnb(Ch~sASB_Z=*kYrF_`~hyhQqHB10X<Q(d2pXO;MBQ=w`0lzcgTIoGm{dHPCbEsJ
{t@+pylv0P0JaT%2a>C10<xU(Kw3Ds@0u&Trkil>OFPn*li(7=H_ct4QZs_pTkg^!K<1>9U+auy9XYZt(Nj?$fel2e>U74_mh5N&=Cd@)Qhtdk
FQyq=5yNbH@!D`Iv3Z(dsEW?aj;6<R7wr-WNz3doT@pIUDR~T5bGpC#i87!kxrFc4&5{a$5mFj0Vi?7z@O?jqSw%~`OiLdzjo>CM7yMAa~o(~<
l#7V4CLkMeg?LMeQ7vh)OpW#Rc#*w%bLkEkYU8#5e^vGs}qm&SRxjhwA<39eihA9mnF29DhBFWp<Xb1zDV*r*|do_R54IDCw{3(M@{mO+W_*7s
15h7cD(0)ayth7(9L;#FyOb4vwB?7%Y>$diBUJj>@Z~v+}(*^Rc`(EdG}UISjlGW6|to9IAsjnJtRq^_2H40Q*OR+@Jd|C+qX^eXtbyBfB;{f!
JdYtTaZzewmX-
1;SEg;(D`YAUd84(t*RfmR^EqZ#ed8c^!uJL2JPbX!})r?@Wa59S|0eyWM~z!pE3sS@<eCzIE<2M8+y5_7{<B5Il4paB8$PgI{lkHkhMeF5m~l
u0*z4_Uxae=6)(bV=TXN%0$w1IT4}C>?~T?Q@Rk||;s!W?1^rN+p{I<H!IpgsyjUMO#@Qt2U+G<~??k?XBnIaWa`RgW>-
k<Gw97r@Fc|mnD^#17-
oedtm%0m0?JjcV6YnDr!Mr*{0^DO+Q*yBX6RFuoW@5|lc9I3v4WzhAnqiKPMyIgDw&7F{3;jna)lA7U^xDLA${cCj+UhdN4wJ^<o#;b(HU6V34
add|y)`*r=fjjSaG39;A(hp>ZZ%}Pepu5>8lzj74C?-21{l;UFbFOIBl^K+HF%@%?6aRN2J0Hq9A8U?YzOohZ4BV4eiW%-
D?^BtZDa(<%5GQC>1*TmQO3Xl`pbX&>n}xPOHyL{ZC!f`bg8xD1Eeu{cZgOgk92SA&6hq)%fh$xFd(O9&`i^r<LhBwZ!ZI}S~`y6>CWT{j3DUO
XUI34@(AhaeKjld)qTlO!f=cQ2KOAdDAELHZi%xRq#j7|b=z6QF^DH>G}D-
nR~!B|w2@;5$zI|ZL^O+dOlM|cK~^>ArLnk|BGN9`B$>SoFsOi!h1BELo1{!Obe&ow%}v)fW{7+pB#uEmUB@vczhYD4`k|4z3+m>@d#GZdZca6
l(<~b@(ZhONLB&pR5q3%g`5<Ww9*{fpl9|lP@xpYRw=~3sY1A&V1Eeu{kY>}S=h^g*J9=vKgLjj};Gh}8+dye67Mmm>)uGB&5Vnsx1oGxgS&+c
KF*a$Y8{!M&qRm>5u$u)2_goh+ag_@he4{%^VsI`nL)Uo2Q8g|L?eQt;PX|b1aDd$3RN_j!?b;bd30Jw7AO__McJ~^;G>bIVpmVgV96`%fYq*0
n2JadRVvWZ{vNEHohLRIYx-<^AH+7Cm^_gri*f-F9^R{98M5^Vv|7(W(_MRjL2hc~PF>@;BY__s1SH;pn;uyp`=!;p-
`WefF+t3bpvyZ34R54IMP6|IY+_GYvv+a0H481_xn)x!r)b`^nAh@?@U@*BUn!$3gW0D71g38}f#XteoOPm4QR8#KO;HBpe>qE8KJbzYKNgSk(
fxLk1aC)z#acM&j)|mI5!2sVu6$5pN)z@>8l+?d(xlgkje6i#TTfQ+v$MFxJqu~A&e%MARs+njFV!6n_F$W*$54wi(bLeA0fozshzPmA-zgG@j
-boPya|1=_*`*`(@a!)j-YeW+-5w!}!Mas>H#xUg+>NX+x-
2D0a~NPy?~rmGNnlw;$C90`8rw)os`;$bM~@Q6Al?J7BTuK~EKwGErR8y)`l7O(L?K9bXOJd3HEb-W%9p^EAx#EtbPr_=+&P-x-k9~aTep-
)d!H-8eJ5!Q-
UaFkl)h<k^V=hd?p*z#UMON<E>%UyV;t2i*@_9JmE`lBg~+=ZU{J44y>tCgO^!KB%MDV3#UmQIH=|Wr?nj7Y5U=s{$TkL1`6st(t!!y|m^20t^
SE%yD8I6jZo}zso99f4JbNf(;BG<Zdx(<L$I&;Lt;ro;NUvDij_ypJW<ZBoU~o^=TcTZCzb)ojJM%bNFaOn=mDf(sJ470T2k0zYSvQ*9X-
NDe^n%(9JWL*fd4C3JpPbIX3ch!}wDx=5H6(-
nd5Am)Q&BZ!xi*~#hY$54+FT_=Z>eISF7QMi@yxnjDqMMlfpoOXS0=EBJO=ah$|1{br5COWX;x0BjY5A%4+8?^vApV~DXAIUzs)t`xlFfV98_#
FHtjsj2!nnN+w&#2OO>>+HY{?cC+{YW!Mi~-
=y@2Xt3$(Htz>QcOhdrFCyYS@qDn+Z@}hbk9w@qS=H@U*8DLPMj2C{HoJ?cRHi7&*k{BF7gCX%oKQHNuV~@e&fqrfCEoRVP4iZNoUY(sm#U0WV
;A5KUC_<0!hGf1^L)P?d8(WYawhiyJn_ui|h~rpr9<4<?zxh&*W!&E-zP_5-I$8-S;kYwzUzPv-k3S{LkCU;uy?~^e*~cV7*-
G^0llh0@pVN>Qu{KtwF_AQIE+$}Q^-
av4_a$YkZ8?7^{)q=ce;r*1zBWG;OCNaJs3YZmo4U{Y#54;YiQ=sfsqtr!j9U3e_C>px+D?1(q4>pd6jQp~i#}rLhkhtpHgL_Sp<*O!PA^N-
PK!k}pTmdZFVi$d-b`+$Iz?i(qXIs>J`@jq-
*&(M>8D?R{q@7I*7OfHeprR|Pvt}R6Yb(SAhmmac4)W!P(Gx?^L{)23s>^ewtkj+ueVrPcjR*++r#E~o5raznD^)70yrPv4~OQg!ltrmtgn3RY
(t^HCyiZ%O91FrGVpA9!%Vy2)rBT+h+$x^;IB4xvZ(m#vhl2>2Rc3^Y3XLH4O7s)!*iKn;IDNejl_lVtAPh#rDk%QFFYu7CHI?0CwbGzt<q-
ppTG*+h#Sq3X6KKQ*4^ASQF@S7GO?QUc~0YqigDQONlY;Cx9BOD#*t4!@+o|fW5oG;ni#Y@g-qrgxHyiE>Za$rbzSKitxP^d8UuQ-Il!bo1#ia
z5;4?mQc%*g8hS9eST;xZo#RX(@b4Qn&-=>b&~+Kb&6-
A<(Cy`tDF?alq=`XODxKB9>HP9$^tN7j8DW>~I2V+`nRy&A*cY1POmE|(JOy;H){?$t#!JTKVYOQ8I7T0Xd<lyx)A7#|$9k}mv}=5?Of20^5(9
RH9$~sPu`*lBsSae$dQo0&ZKEmy^Jy-94DvPnExB%^7w1w;WjSLj(`oj)Zo<_O;uu(!?zAQ`krtFDqVVQ(>u{9|vYkgAgL|u#$Yg8M-
()RYfw3HH>@#S|2Z&=}?@+MQxUtRGG-
1BmJa=`TaPoIFF=#4{i6<MkjuW>d_j7pUre9|BTeF?;NB0c3d)gD(KpSvzmcd_<8U=LQPtg^DTL7uu&$BpSu+P;tZ#URx?32cArGq%Y9)>z(F?
07)$KYNloi*Zs5dD>&N%|P6^(igZ>FbV;kjDVydK8zNTf-jXP8^$+83n1Kud^VPULO{l#{vU>r8VP6J;*g(Z>B)q%dE&8M*U$980>4E1CK@Q$D
ZsJTB~VeXdPZpT^=Ee0aWQ%C8rc8mM!Z6W_&u9k)%x2NUin+78r1)rX^-+V1v{YE0e+0eMb-jb*FxQcyfDa4f{b|L%M--7W^T)7(|t3<y}p8h2
DMV`zR)7YyH5!%`vd2cBCF-0D->L`JmV)5%IXTpJiM$&y6PCE<K5Achq6>7~t~^>LX`Tq{yZzOR-
L^R17R)SevdKv;*T$;)HF(g;GfQ*C9m`EHAEy91`mQbquaH_E!h8$w|IQjM+pt#<WD?B~YAMQsoE>&f<e@0jy_@@+FP7bGES~XPGsgbRo_gc56
|F|Mlm;Y7W53%&^V4RyhdRVZq(%otNJGq%qmZCN9r+&egW>C<_eu4eqWj`(X@l3Dc*+)`s2aoE@R-
;&+%d2J}|vCn3Ye)`2uco>@5^%AS3WPlF=?TukRt?<<+j3fqXgO!*zrnz5^?A=4*H`R0nt1TrRi?B#($zt5H@&^qql_I_Ab*8G6oEFj=lXPUz=
dA*WTMCVSp`Sc3$B6&I+tDk20=zNAr5+^akHsf3wWA<jvk1l<iG{Rou;3-
3mu56Ypz+)^h;INMOk}1q_Lg!x!N4Nb9^Tc9LVuWpiO7pYbYk|zcMN&#%&uZpS>dVAf^+`C59kwA?8Qz08$^Z4{E4P0ss-
X&9uC%`c95C1#jnB)_KB-=j-dc22^9<%aMjL~w^1Sf^xJEb4(Q0H)BX?3+yEv#t-9h3Q*xP(&4Jq0+=QmmINgp*W%ARI3z(C_V-
I!+|rH#WdmA7&|WE`B*gM5TG22~gDWS_PyOCnMoS6{zPOI54yM>#;SuQh%-
W;1wB<r2RE7icHfftN0F#^ZBx=5xSct8_K9h=H@^yQD>v<}gIDCAgKZUUnU%j={xq?^CI^OsuzFl4`4BoSoZ^GG~fqC~x&ioUm=URBGt;=G)qN
Sx_|GL7h2CvT6q1d_Qpv?3F?h;Zfj{{ZzU!<UFu*{9*H44n9L6>jB~zSUk#Uy<Lg++m(S`-YEf0d6xGP#lYQU2=sYBtl90uMNysjG-
=($%tn(b@^^p(23zG>tBuUujc=ugm^vz-N;{hY1{&A6Qa%hv?o97iQsB2HEdkd($|GbkfcN?A<SA{UvBT)A?($m3I~YKqZ}42QG7da-hKzHcO8
@BKePRW0BB2{neT+H=SD8ar4pO$n6Ok4vNHI;7=22yVptwH6Je1jtuuZ^qu9vi2>C5a*%~hs6Dq`Rg#kWzP|NM`?+4M785AV|;b(*$hc@($5^$
*3Le9>%vV_#=c2UasU`b}yz*PKetYD!EozDxW&`++NIIVxr%CkU6G+w~NUn>MQZfs0^e6PBB2&O_u%Lz}u~ZqupB9{o`KJXpWtrywo1-
~7h1WLnRdwJ2*}I@&7n%+k_H^gLQAGBxrk#n}5${M&Yqwv|w0bSHrrYfPlS63OS~?iyLKFNpt#WnW5>EWvaoot~c_!mmHFmuS_v&-
O<;CO?{WaMh3PgX<n#v-+_sP5q{b_7783Y5HKUv0Y2AUuAxH^+{RO@If<d#7wANQ`weNN~Hey-
9frkM;Giz?z1FambQv!mYBjW!q{!O(t8?8&LWeOunb&{u{5>wPSInnoJ${re4VYXa7-
9XD|mHHvKAWdV}gOdQ6@@^GRaLP>toM)zFjrzpO5+pOY^v3@NX4rUc<d(QVwP6aS)PWY=%m!>K!7D0oCX8O{3C#nY&l?p;pcpIZPRYd7mlx&2K
O9T1uX%R9dy(hK!N#-
3%bmw`a;bY!;DouTmS9t}vAhitk<?&XD5{&)|Z=Ki4@}>d<VyeRL@tOUqw`CWB{X7gY?Nsxo4FJ>G{~CCJ#PCZ*bMJBJ4b{Zem)r!k=`GmVnWV
}rk^iov_m$Lo{g97vqdPIqabr1e$`6%<zK(`j5V_}3~AM6xToupqf=;!5&{%ZFj9KhFn9V?Y%-
c)sSbE5tITgQvSxg?jU~)A(7+dDJnuaD<lgVeRMAr)C6G0z3&*ZlI#-
)^V6J1{3!XO24mhY7p7kNdXwUqv$7g?;(tVyw?>?%Yz_$o*D!>Qg`TBkttUVWro==$2mZ-
?=;a^Qx1~KF0CduUrTAn%T;q;<1H)aQODq_qOemriZp5CQSr%C**u3_ZAibTjKRE6D2kGr_cBvK9JcE5io1zo;BZ~3v)oKBzM3XP3#n4}S;+xl
_4K!+^fAa+>QoUPuu5yRT(>?hPcf6RokJUgdYz?ccKZqFuWQpOefLL5V?b{dk~i8V&pC;s@`ksx+eZ(BbgOIH#tkM@mhjdE$hW4^x4Jq+8-
uEensT?emG$FN^TgHmQpMoi>kT$>+WN`sLrh#utpt?g@SaX&18u;)*3(34*+Q0GyRly@Es9<Mm!cS5`amXww`nFPY#YuMVPrdn6FFTWT{wCeL{
-hvF{(U~4YmOnS$bu0B6Mqf@{zstKhD-GYY%-
4vZ7x{92KDSJyLV>j30XjeGIZnznYxg_9eFLLzxmr^~J;OiEOY9z_Zzw?(tpoGU7L+21!%AQa89@1_KOqjx4t_a4Rp8!Jb~<vC_#8pEG5+?V*m
rz0Kg9GvmPSOc(kPVGQJ5h8&orPUPyGb$~7gQRS&>qmlm>Q|F^@%xZU)S{2z(8G(6yhG(!zZ-ppLs4KS~JUc$$R9#6(Qg?7?v6v0~fB!%6wD2t"""
# VALORES HARDCODE PARA PRUEBAS LOCALES (ficticios, nunca credenciales reales).
# Los secretos de GitHub prevalecen sobre estos valores.
# Para pruebas locales se puede sustituir el valor de demostración.
# No introduzcas credenciales reales en un repositorio público.
TEST_OPENROUTER_API_KEY = "PON_AQUI_TU_CLAVE_DE_PRUEBA"
TEST_INSTAGRAM_TOKEN = "PON_AQUI_TU_TOKEN_DE_PRUEBA"
TEST_INSTAGRAM_USER_ID = "00000000000000000"

# Únicamente se acepta el router gratuito o un modelo con sufijo :free.
OPENROUTER_MODEL = os.getenv('OPENROUTER_MODEL', 'openrouter/free').strip() or 'openrouter/free'
if OPENROUTER_MODEL != 'openrouter/free' and not OPENROUTER_MODEL.endswith(':free'):
    raise RuntimeError('Modelo no gratuito rechazado: configura openrouter/free o un modelo :free')
OPENROUTER_URL = 'https://openrouter.ai/api/v1/chat/completions'

GRAPH_VERSION = os.getenv('IG_GRAPH_VERSION', 'v25.0')

def credential(name, demo):
    value = os.getenv(name, '').strip() or demo
    if not value or value.startswith('PON_AQUI_') or value == '00000000000000000':
        raise RuntimeError(f'Configura {name} como secreto de GitHub o valor de prueba local')
    return value

BRAND = 'DATAVIRAL'


def catalog():
    return json.loads(zlib.decompress(base64.b85decode(''.join(CATALOG_B85.split()))))


def _parse_ai_json(text):
    """Parsea un objeto JSON completo; admite fences y texto envolvente.

    No intenta cerrar comillas ni fabricar campos de un JSON truncado.
    """
    if not isinstance(text, str) or not text.strip():
        raise ValueError('Respuesta sin texto JSON')
    cleaned = text.strip()
    fenced = re.fullmatch(r'```(?:json)?\s*([\s\S]*?)\s*```', cleaned, flags=re.I)
    if fenced:
        cleaned = fenced.group(1).strip()
    try:
        value = json.loads(cleaned)
    except json.JSONDecodeError:
        start = cleaned.find('{')
        if start < 0:
            raise
        value, end = json.JSONDecoder().raw_decode(cleaned[start:])
        rest = cleaned[start + end:].strip()
        if rest and not rest.startswith('```'):
            raise ValueError('Texto inesperado después del JSON')
    if not isinstance(value, dict):
        raise ValueError('OpenRouter debe devolver un objeto JSON')
    return value


def _validate_ai_data(data):
    for field in ('title', 'script', 'lesson', 'fact'):
        if not isinstance(data.get(field), str) or not data[field].strip():
            raise ValueError(f'Guion de IA sin campo requerido: {field}')
    words = len(data['script'].split())
    if not 38 <= words <= 54:
        raise ValueError(f'Duración incompatible: {words} palabras (38-54 requeridas)')
    return data


def ajustar_texto_visual(texto, max_caracteres=40, max_palabras=6):
    """Obtiene una microfrase SIN cortar letras ni añadir puntos suspensivos.

    Si la entrada excede seis palabras, se utiliza una frase breve completa
    cuando sea posible. En caso contrario, se elige un grupo de palabras
    recortado en frontera léxica y se quita un conector final colgante.
    """
    texto = re.sub(r'\s+', ' ', str(texto or '')).strip(' \t\n.,;:')
    texto = re.sub(r'https?://\S+', '', texto).strip()
    # Si una pregunta original queda demasiado larga, presentar la afirmación central.
    if len(texto.split()) > max_palabras:
        texto = re.sub(r'^[¿¡]?\s*(?:sab[ií]as que|sab[ií]as|te imaginas que)\s+', '', texto, flags=re.I)
    texto = texto.lstrip('¿¡')
    if not texto:
        return 'DESCUBRE ALGO NUEVO'
    candidatos = re.split(r'(?<=[.!?;:])\s+|\s+[—–]\s+|,\s+', texto)
    candidatos = [x.strip(' .,:;!?') for x in candidatos if x.strip(' .,:;!?')]
    candidato = next((x for x in candidatos if len(x.split()) <= max_palabras
                      and len(x) <= max_caracteres), candidatos[0] if candidatos else texto)
    palabras = candidato.split()
    elegidas = []
    for palabra in palabras:
        if len(elegidas) >= max_palabras or len(' '.join(elegidas + [palabra])) > max_caracteres:
            break
        elegidas.append(palabra)
    conectores = {'de', 'del', 'la', 'el', 'los', 'las', 'un', 'una', 'y', 'o', 'que',
                  'para', 'por', 'con', 'sin', 'en', 'a', 'al', 'su', 'sus', 'es'}
    while len(elegidas) > 2 and elegidas[-1].lower().strip('.,:;') in conectores:
        elegidas.pop()
    return ' '.join(elegidas).strip(' .,:;!?¿¡') or 'DATO SORPRENDENTE'


def microfrases(ep):
    """Cinco titulares, nunca el texto completo de la narración."""
    ai = ep.get('visuals')
    if isinstance(ai, list) and len(ai) == 5 and all(isinstance(v, str) and v.strip() for v in ai):
        raw = ai
    else:
        raw = [ep.get('title', ''), '¿SABÍAS ESTO?',
               ep.get('fact', '') or 'UN DATO REAL',
               ep.get('lesson', '') or 'UNA IDEA ÚTIL',
               'AHORA YA LO SABES']
    return [ajustar_texto_visual(v, 38, 6).upper() for v in raw]


def texto_centrado_seguro(draw, texto, *, centro_y, ancho=550, max_lineas=2):
    """Dibuja en el rectángulo central sin salirse ni cortar renglones."""
    texto = ajustar_texto_visual(texto, 38, 6).upper()
    for tam in range(66, 30, -2):
        fuente = font(tam, True)
        lineas = wrap_text(draw, texto, fuente, ancho)
        if len(lineas) > max_lineas:
            continue
        medidas = [draw.textbbox((0, 0), lin, font=fuente, stroke_width=1) for lin in lineas]
        if any((b[2] - b[0]) > ancho for b in medidas):
            continue
        salto = tam + 18
        alto = len(lineas) * salto
        if alto > 240:
            continue
        y = centro_y - alto // 2
        for linea in lineas:
            caja = draw.textbbox((0, 0), linea, font=fuente, stroke_width=1)
            x = (720 - (caja[2] - caja[0])) / 2
            draw.text((x, y), linea, font=fuente, fill=(255,255,255),
                      stroke_width=1, stroke_fill=(4, 7, 22))
            y += salto
        return
    raise ValueError('No es posible componer un titular dentro de la zona segura')



OPENROUTER_MODELS_URL = 'https://openrouter.ai/api/v1/models'


def _free_price(value):
    try:
        return float(value) == 0.0
    except (TypeError, ValueError, OverflowError):
        return False


def select_free_json_models(key, count=5):
    """Selecciona modelos de texto gratuitos; response_format es OPCIONAL.

    El listado de parámetros es informativo: el proveedor concreto puede no
    aceptar json_schema, por lo que se utiliza un segundo modo sin restricciones.
    """
    response = requests.get(OPENROUTER_MODELS_URL,
                            headers={'Authorization': f'Bearer {key}'}, timeout=30)
    response.raise_for_status()
    items = response.json().get('data', [])
    candidates = []
    forbidden = ('safety', 'moderation', 'guard', 'omni', 'embedding',
                 'audio', 'speech', 'image', 'reasoning', 'vision-only')
    for item in items:
        mid = item.get('id', '')
        if not isinstance(mid, str) or not mid.endswith(':free'):
            continue
        price = item.get('pricing') or {}
        if not (_free_price(price.get('prompt')) and _free_price(price.get('completion'))):
            continue
        description = (mid + ' ' + str(item.get('name', ''))).lower()
        if any(term in description for term in forbidden):
            continue
        context = item.get('context_length') or 0
        if not isinstance(context, int) or context < 4000:
            continue
        params = item.get('supported_parameters') or []
        can_format = 'response_format' in params
        # Preferir modelos de instrucciones conocidos, no modelos de razonamiento.
        familiar = any(term in description for term in ('instruct', 'chat', 'qwen', 'llama', 'mistral', 'gemma'))
        candidates.append((0 if familiar else 1, 0 if can_format else 1, mid, can_format))
    candidates.sort()
    # La clave de usuario nunca debe habilitar automáticamente un modelo pagado.
    if OPENROUTER_MODEL != 'openrouter/free':
        selected = [x for x in candidates if x[2] == OPENROUTER_MODEL]
        if not selected:
            raise RuntimeError('Modelo configurado sin cuota gratuita de texto: ' + OPENROUTER_MODEL)
        candidates = selected + [x for x in candidates if x[2] != OPENROUTER_MODEL]
    if not candidates:
        raise RuntimeError('No hay modelos gratuitos de texto en el catálogo de OpenRouter.')
    return [(item[2], item[3]) for item in candidates[:count]]


def _normalize_ai_fields(data):
    """Valida contenido, sin inventar ni reconstruir un JSON truncado."""
    if not isinstance(data, dict):
        raise ValueError('La IA no devolvió un objeto JSON')
    # No exigir metadatos que no afectan al relato; reducir tokens de salida.
    if not data.get('fact') and data.get('lesson'):
        data['fact'] = data['lesson']
    if not data.get('lesson') and data.get('fact'):
        data['lesson'] = data['fact']
    for field in ('title', 'script', 'lesson', 'fact'):
        if not isinstance(data.get(field), str) or not data[field].strip():
            raise ValueError('Falta ' + field)
    words = len(data['script'].split())
    if not 38 <= words <= 54:
        raise ValueError(f'Guion de {words} palabras; requiere entre 38 y 54')
    visuals = data.get('visuals')
    if not isinstance(visuals, list) or len(visuals) != 5 or not all(isinstance(v, str) and v.strip() for v in visuals):
        raise ValueError('Deben existir cinco frases visuales')
    # El renderizador controla la composición, no altera la narración.
    data['visuals'] = [ajustar_texto_visual(v, 38, 6) for v in visuals]
    if not isinstance(data.get('sources'), list):
        data['sources'] = []
    return data


def classify_openrouter_429(response):
    """Distingue saturación del proveedor y cuota global sin asumir que todo 429 es global.

    Devuelve 'provider', 'account' o 'unknown'. Nunca imprime credenciales.
    """
    try:
        body = response.json()
    except (ValueError, TypeError):
        body = {}
    error = body.get('error') if isinstance(body, dict) else None
    if not isinstance(error, dict):
        error = {}
    meta = error.get('metadata')
    if not isinstance(meta, dict):
        meta = {}
    details = ' '.join(str(x) for x in (
        error.get('message', ''), meta.get('raw', ''),
        meta.get('provider_name', ''), meta.get('reason', ''),
    )).lower()
    provider_clues = (
        'temporarily rate-limited upstream', 'rate-limited upstream',
        'upstream', 'provider returned error', 'provider rate limit',
        'provider rate-limit', 'provider is rate limited',
    )
    if any(phrase in details for phrase in provider_clues):
        return 'provider'
    account_clues = (
        'free-models-per-day', 'free model requests per day',
        'daily free requests', 'daily limit', 'daily quota',
        'insufficient credits', 'not enough credits',
        'account rate limit', 'your account', 'your quota',
    )
    if any(phrase in details for phrase in account_clues):
        return 'account'
    return 'unknown'


def create_ai_episode(ep):
    """Texto JSON compacto con modelos gratuitos: rígido y luego flexible.

    Un 404 de proveedor por parámetros no invalida el modelo: se reintenta
    sin json_schema ni require_parameters. Nunca se usa el router de pago.
    """
    key = credential('OPENROUTER_API_KEY', TEST_OPENROUTER_API_KEY)
    candidates = select_free_json_models(key, 5)
    print('Modelos gratuitos de texto: ' + ', '.join(mid for mid, _ in candidates), flush=True)
    prompt = (
        'Responde SOLO un JSON compacto y válido, sin Markdown ni texto externo. '
        'Idioma español. NO inventes estadísticas ni afirmaciones dudosas. '
        'Usa exactamente estas claves: title, script, lesson, fact, visuals, sources. '
        'title: título muy corto. script: 38 a 54 palabras en un párrafo. '
        'lesson y fact: una frase breve cada uno. '
        'visuals: arreglo de EXACTAMENTE 5 frases, 2 a 6 palabras, máximo 38 caracteres por frase. '
        'sources: [] si no tienes referencias comprobables; no inventes URLs. '
        'Evita consejos médicos, legales o de emergencia no corroborados. '
        'No agregues otros campos. '
        f"Tema: {ep.get('title', '')}. Categoría: {ep.get('category', '')}. "
        f"Objetivo: {ep.get('lesson', '')}."
    )
    headers = {
        'Authorization': f'Bearer {key}',
        'Content-Type': 'application/json',
        'HTTP-Referer': 'https://github.com',
        'X-Title': 'Dato Wow - DataViral',
    }
    last_problem = 'sin respuesta'
    data = None
    used_model = None
    # 5 modelos, hasta 2 configuraciones c/u; cuotas free pueden ser menores.
    for model, supports_format in candidates:
        # El formato estricto se intenta solo donde está anunciado; el modo
        # flexible no exige parámetros y funciona con proveedores más variados.
        modes = ('structured', 'prompt') if supports_format else ('prompt',)
        for mode in modes:
            payload = {
                'model': model,
                'messages': [
                    {'role': 'system', 'content': 'Eres un guionista educativo conciso. Responde solo JSON.'},
                    {'role': 'user', 'content': prompt},
                ],
                'temperature': 0.25,
                'max_tokens': 2500,
                'stream': False,
            }
            if mode == 'structured':
                payload['response_format'] = {'type': 'json_object'}
                payload['provider'] = {'require_parameters': True}
            try:
                response = requests.post(OPENROUTER_URL, headers=headers,
                                         json=payload, timeout=150)
            except requests.RequestException as exc:
                last_problem = 'error de red: ' + type(exc).__name__
                print(f'OpenRouter {model} [{mode}]: {last_problem}', flush=True)
                break
            if not response.ok:
                last_problem = f'HTTP {response.status_code}: {response.text[:170]}'
                print(f'OpenRouter {model} [{mode}]: {last_problem}', flush=True)
                if response.status_code in (401, 403):
                    raise RuntimeError('Credenciales OpenRouter rechazadas')
                if response.status_code == 429:
                    category = classify_openrouter_429(response)
                    if category == 'provider':
                        print(f'OpenRouter {model}: proveedor gratuito saturado; '
                              'se probará el siguiente modelo gratuito.', flush=True)
                        # Un cambio de parámetros no resuelve el límite upstream.
                        break
                    if category == 'account':
                        raise RuntimeError('Límite de la cuenta o cuota gratuita '
                                           'de OpenRouter agotada; se conserva el episodio pendiente.')
                    # Si se desconoce el origen, no afirmar que la cuota de la cuenta
                    # está agotada. Continuar con otro modelo gratuito como máximo.
                    print(f'OpenRouter {model}: HTTP 429 de origen desconocido; '
                          'se probará otro modelo gratuito.', flush=True)
                    break
                # 404 por require_parameters => probar modo prompt del MISMO modelo.
                if response.status_code in (400, 404, 422) and mode == 'structured':
                    continue
                break
            try:
                body = response.json()
                choice = (body.get('choices') or [])[0]
                content = (choice.get('message') or {}).get('content') or ''
                if isinstance(content, list):
                    content = ''.join(part.get('text', '') for part in content
                                      if isinstance(part, dict))
                finish = choice.get('finish_reason')
                if finish == 'length':
                    raise ValueError('respuesta truncada')
                data = _normalize_ai_fields(_parse_ai_json(content))
                used_model = body.get('model') or model
                print(f'Guion válido con {model} [{mode}]', flush=True)
                break
            except (ValueError, TypeError, KeyError, IndexError, json.JSONDecodeError) as exc:
                last_problem = f'JSON/guion inválido: {str(exc)[:140]}'
                print(f'OpenRouter {model} [{mode}]: {last_problem}', flush=True)
                # Si el JSON estaba corrupto, no repetir en el mismo modelo:
                # escoger siguiente modelo para preservar cuota gratuita.
                break
        if data is not None:
            break
    if data is None:
        raise RuntimeError('Los modelos gratuitos no entregaron un guion válido. '
                           f'Último diagnóstico: {last_problem}. No se publicó nada.')

    sources = []
    for item in data['sources'][:3]:
        if isinstance(item, str) and item.startswith('https://'):
            host = urllib.parse.urlparse(item).hostname or ''
            if host and host not in ('example.com', 'www.example.com'):
                sources.append(item)
    result = dict(ep)
    result.update(
        title=data['title'].strip(), script=data['script'].strip(),
        lesson=data['lesson'].strip(), fact=data['fact'].strip(),
        visual_title=ajustar_texto_visual(data['title'], 38, 6),
        visual_lesson=ajustar_texto_visual(data['lesson'], 38, 6),
        visuals=data['visuals'], source=' | '.join(sources),
        suggested_sources=sources, ai_model=used_model,
        generated_at=now(), verified=False,
        verification_note='Fuentes no verificadas independientemente',
    )
    print(f"Guion OpenRouter creado: {ep['id']}; referencias propuestas: " +
          (' | '.join(sources) if sources else 'ninguna'), flush=True)
    return result


def select_episode(episodes, gh=None, requested=None):
    """Selecciona un episodio pendiente con variedad de categorias y azar real.

    - Un ID explicito respeta la eleccion manual (publish() aplica antidualidad).
    - El historial remoto impide reutilizar publicaciones o envios inciertos.
    - Entre categorias con episodios disponibles, prioriza las menos publicadas;
      entre empates evita la ultima categoria usada, si existe alternativa.
    - Sortea tanto la categoria como el episodio usando SystemRandom.
    No altera el schema ni la ubicacion del estado previo.
    """
    if requested:
        return next((e for e in episodes if e['id'] == requested), None)

    states = {}
    if gh is not None:
        raw, _ = gh.read('dataviral/state.json')
        if raw is not None:
            document = json.loads(raw)
            if not isinstance(document, dict) or not isinstance(document.get('episodes'), dict):
                raise RuntimeError('Estado remoto de DataViral invalido; no se seleccionara episodio')
            states = document['episodes']

    blocked = {'publicado', 'enviando', 'incierto'}
    by_category = {}
    published_counts = {}
    recent = []
    for ep in episodes:
        category = ep['category']
        row = states.get(ep['id'], {})
        if not isinstance(row, dict):
            raise RuntimeError('Registro de estado invalido para ' + ep['id'])
        statuses = [row.get(field) for field in ('reel', 'foto', 'feed_video')]
        if any(status in blocked for status in statuses):
            if 'publicado' in statuses:
                published_counts[category] = published_counts.get(category, 0) + 1
                if row.get('updated_at'):
                    recent.append((str(row['updated_at']), category))
            continue
        by_category.setdefault(category, []).append(ep)
        published_counts.setdefault(category, 0)

    if not by_category:
        raise RuntimeError('Los 500 episodios ya estan publicados o bloqueados por incertidumbre')

    # Equilibrio entre categorias; no completar cien episodios de una sola.
    minimum = min(published_counts[category] for category in by_category)
    eligible_categories = [category for category in by_category
                           if published_counts[category] == minimum]
    if recent and len(eligible_categories) > 1:
        last_category = max(recent, key=lambda pair: pair[0])[1]
        others = [category for category in eligible_categories if category != last_category]
        if others:
            eligible_categories = others

    rng = random.SystemRandom()
    chosen_category = rng.choice(eligible_categories)
    selected = rng.choice(by_category[chosen_category])
    print(f'Episodio aleatorio equilibrado: {selected["id"]} | '
          f'categoria: {chosen_category} | '
          f'publicados de esa categoria: {published_counts[chosen_category]}', flush=True)
    return selected


def now():
    return datetime.now(timezone.utc).isoformat()


def font(size, bold=False):
    filenames = (['/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',
                  '/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf'] if bold else
                 ['/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
                  '/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf'])
    for filename in filenames:
        if Path(filename).exists():
            return ImageFont.truetype(filename, size)
    return ImageFont.load_default()


def wrap_text(draw, text, text_font, width):
    words = text.split()
    result, current = [], ''
    for word in words:
        trial = f'{current} {word}'.strip()
        if draw.textbbox((0, 0), trial, font=text_font)[2] <= width:
            current = trial
        else:
            if current:
                result.append(current)
            current = word
    if current:
        result.append(current)
    return result


def palette(i):
    return [(12, 12, 32), (9, 23, 38), (27, 15, 28), (14, 26, 25), (20, 17, 45)][i % 5], [
        (186, 93, 253), (39, 217, 241), (255, 193, 92), (69, 231, 169), (252, 105, 174)
    ][i % 5]


def scene(ep, number, dest):
    W, H = 720, 1280
    bg, accent = palette(number + int(ep['id'][-3:]))
    img = Image.new('RGB', (W, H), bg)
    d = ImageDraw.Draw(img, 'RGBA')
    rng = random.Random(ep['id'] + str(number))
    for _ in range(22):
        x, y = rng.randrange(-150, 800), rng.randrange(-150, 1400)
        r = rng.randrange(15, 145)
        d.ellipse((x-r, y-r, x+r, y+r), outline=(*accent, rng.randrange(22, 90)), width=rng.randrange(2, 8))
    d.rounded_rectangle((52, 72, 668, 152), 24, fill=(255, 255, 255, 18), outline=(*accent, 200), width=3)
    d.text((77, 91), 'D A T A V I R A L', font=font(33, True), fill=(255, 255, 255))
    d.text((55, 187), ep['category'].upper(), font=font(19, True), fill=accent)
    # Zona segura central: sin párrafos de narración ni frases truncadas.
    titulares = microfrases(ep)
    texto_centrado_seguro(d, titulares[number], centro_y=600, ancho=550, max_lineas=2)
    d.line((58, 1128, 662, 1128), fill=accent, width=5)
    d.text((92, 1154), 'DATO WOW  ·  20 SEGUNDOS', font=font(23, True), fill='white')
    img.save(dest, quality=92)


def ambient(path: Path, seconds=20):
    rate = 16000
    with wave.open(str(path), 'wb') as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(rate)
        import array
        buff = array.array('h')
        for i in range(rate*seconds):
            t = i/rate
            f = min(1., t/.8, (seconds-t)/1.3)
            v = (math.sin(2*math.pi*110*t)*.17 + math.sin(2*math.pi*164.81*t)*.07 +
                 math.sin(2*math.pi*220*t)*.05)
            buff.append(int(32767*max(0,f)*v))
        w.writeframes(buff.tobytes())


async def narrate(script: str, path: Path):
    import edge_tts
    communicate = edge_tts.Communicate(script, voice=os.getenv('DV_VOICE', 'es-ES-AlvaroNeural'), rate='+12%')
    await communicate.save(str(path))
    if not path.exists() or path.stat().st_size < 500:
        raise RuntimeError('No se generó una narración válida')


def render(ep, out: Path, require_voice=False):
    out.mkdir(parents=True, exist_ok=True)
    if not ep.get('script'):
        raise ValueError(f"{ep['id']}: propuesta sin guion; no se puede producir")
    # Las fuentes son metadatos opcionales; no bloquean video ni publicacion.
    if not ep.get('source'):
        print(f"AVISO: {ep['id']} sin fuentes propuestas; contenido no verificado independientemente.", flush=True)
    folder = out / ep['id']
    folder.mkdir(parents=True, exist_ok=True)
    frames = []
    for i in range(5):
        path = folder / f'escena_{i}.jpg'
        scene(ep, i, path)
        frames.append(path)
    cover = out / f"{ep['id']}.jpg"
    cover.write_bytes(frames[0].read_bytes())
    ambient_path = folder / 'ambient.wav'
    ambient(ambient_path)
    narration = folder / 'voz.mp3'
    try:
        asyncio.run(narrate(ep['script'], narration))
    except Exception as exc:
        if require_voice:
            raise RuntimeError(f'Narración obligatoria falló: {exc}') from exc
        print(f'AVISO: preview sin voz por: {exc}', file=sys.stderr)
    args = ['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y']
    for frame in frames:
        args += ['-loop', '1', '-framerate', '12', '-t', '4', '-i', str(frame)]
    args += ['-i', str(ambient_path)]
    voice_available = narration.exists() and narration.stat().st_size > 500
    if voice_available:
        args += ['-i', str(narration)]
    video_filters = ''.join(f'[{i}:v]fps=12,scale=720:1280,setsar=1[v{i}];' for i in range(5))
    video_filters += ''.join(f'[v{i}]' for i in range(5)) + 'concat=n=5:v=1:a=0[v];'
    if voice_available:
        video_filters += '[5:a]volume=0.28[amb];[6:a]volume=1.4[voice];[amb][voice]amix=inputs=2:duration=first:dropout_transition=0[a]'
    else:
        video_filters += '[5:a]volume=0.5[a]'
    movie = out / f"{ep['id']}.mp4"
    args += ['-filter_complex', video_filters, '-map', '[v]', '-map', '[a]',
             '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-preset', 'veryfast',
             '-crf', '24', '-r', '30', '-c:a', 'aac', '-b:a', '128k',
             '-t', '20', '-movflags', '+faststart', str(movie)]
    subprocess.run(args, check=True, timeout=240)
    print(f'Video: {movie} ({movie.stat().st_size:,} bytes)')
    print(f'Portada: {cover}')
    return movie, cover


class Github:
    def __init__(self):
        self.repo = os.environ['GITHUB_REPOSITORY']
        self.token = os.environ['GH_TOKEN']
        self.base = f'https://api.github.com/repos/{self.repo}'
        self.branch = os.getenv('GITHUB_REF_NAME', 'main')
        self.s = requests.Session()
        self.s.headers.update({'Authorization': f'Bearer {self.token}',
                               'Accept': 'application/vnd.github+json',
                               'X-GitHub-Api-Version': '2022-11-28'})

    def request(self, method, route, **kwargs):
        r = self.s.request(method, self.base + route, timeout=40, **kwargs)
        if r.status_code >= 400:
            raise RuntimeError(f'GitHub API HTTP {r.status_code}: {r.text[:600]}')
        return r.json()

    def read(self, path):
        route = '/contents/' + urllib.parse.quote(path, safe='/')
        r = self.s.get(self.base + route, params={'ref': self.branch}, timeout=40)
        if r.status_code == 404:
            return None, None
        if r.status_code >= 400:
            raise RuntimeError(f'Lectura GitHub falló HTTP {r.status_code}')
        data = r.json()
        return base64.b64decode(data['content']), data['sha']

    def write(self, path, content: bytes, previous_sha=None):
        payload = {'message': f'DataViral: {path}', 'branch': self.branch,
                   'content': base64.b64encode(content).decode()}
        if previous_sha:
            payload['sha'] = previous_sha
        route = '/contents/' + urllib.parse.quote(path, safe='/')
        return self.request('PUT', route, json=payload)

    def assert_public(self):
        if self.request('GET', '').get('private') is not False:
            raise RuntimeError('Para Instagram, el repositorio que aloja el MP4 debe ser público')


def ig_api(method, path, *, token, **kwargs):
    url = f'https://graph.instagram.com/{GRAPH_VERSION}/{path}'
    data = dict(kwargs.pop('data', {}) or {})
    data['access_token'] = token
    if method == 'GET':
        r = requests.get(url, params=data, timeout=50)
    else:
        r = requests.post(url, data=data, timeout=60)
    try:
        obj = r.json()
    except ValueError:
        raise RuntimeError(f'Instagram HTTP {r.status_code} respuesta no JSON')
    if not r.ok or obj.get('error'):
        raise RuntimeError(f'Instagram HTTP {r.status_code}: {obj.get("error", obj)}')
    return obj


def publish_container(user_id, token, video_url, caption):
    """Publica una sola vez el MP4 como Reel visible también en el feed.

    La API expone el mismo video en la pestaña Reels y la cuadrícula/feed,
    sin crear una segunda publicación ni enviar ninguna imagen.
    """
    fields = {'caption': caption, 'media_type': 'REELS',
              'video_url': video_url, 'share_to_feed': 'true'}
    container = ig_api('POST', f'{user_id}/media', token=token, data=fields)['id']
    for _ in range(30):
        time.sleep(10)
        status = ig_api('GET', container, token=token, data={'fields': 'status_code,status'})
        if status.get('status_code') == 'FINISHED':
            break
        if status.get('status_code') in ('ERROR', 'EXPIRED'):
            raise RuntimeError(f'Contenedor Instagram {container}: {status}')
    else:
        raise RuntimeError(f'Timeout contenedor IG {container}; NO reintentar sin reconciliar')
    return ig_api('POST', f'{user_id}/media_publish', token=token,
                  data={'creation_id': container})['id']



def upload_video_to_public_github(gh, movie: Path, episode_id: str):
    """Sube un MP4 con nombre inmutable, sin modificar el estado histórico.

    Evita el conflicto 409 si un nombre de carpeta ya existe como archivo.
    Solo cambia la carpeta de medios; el estado sigue en dataviral/state.json.
    """
    movie_bytes = movie.read_bytes()
    digest = hashlib.sha256(movie_bytes).hexdigest()[:16]
    filename = f'{episode_id}-{digest}.mp4'
    # Nombres independientes del antiguo dataviral/media. Si un antecesor
    # de cualquiera es un archivo, probamos el siguiente directorio.
    roots = ('datoviral_assets/media', 'datoviral_video_assets/media',
             'datoviral_public_videos/media')
    for root in roots:
        remote = f'{root}/{filename}'
        try:
            old, _ = gh.read(remote)
        except (KeyError, TypeError) as exc:
            # GitHub Contents responde distinto si la ruta ya es un directorio
            # u otro objeto; no convertir errores ambiguos en sobrescrituras.
            raise RuntimeError(f'No se pudo inspeccionar ruta GitHub {remote}: {exc}') from exc
        if old is not None:
            if old != movie_bytes:
                raise RuntimeError(f'Colisión: existe otro archivo en {remote}')
            commit = gh.request('GET', f'/commits/{gh.branch}')['sha']
            print(f'Video ya almacenado en GitHub: {remote}', flush=True)
            return remote, commit
        try:
            result = gh.write(remote, movie_bytes)
        except RuntimeError as exc:
            message = str(exc)
            if 'HTTP 409' in message and ('subdirectory' in message or 'file exists' in message):
                print(f'Aviso: conflicto de ruta de medios {remote}; probando alternativa.', flush=True)
                continue
            raise
        print(f'Video almacenado en GitHub: {remote}', flush=True)
        return remote, result['commit']['sha']
    raise RuntimeError('GitHub: todos los directorios alternativos de video chocan con archivos. '
                       'Revisar manualmente la estructura del repositorio; no se publicó en Instagram.')


def publish(ep, movie, cover, approval):
    if approval != ep['id']:
        raise ValueError('Se exige aprobación explícita del mismo ID de episodio')
    if not ep.get('script'):
        raise ValueError('Publicación bloqueada: falta el guion narrado')
    if not ep.get('source'):
        print('AVISO: publicación sin enlaces de referencia; la IA no ha verificado los hechos.', flush=True)
    token = credential('INSTAGRAM_TOKEN', TEST_INSTAGRAM_TOKEN)
    user_id = credential('INSTAGRAM_USER_ID', TEST_INSTAGRAM_USER_ID)
    if not user_id.isdigit():
        raise ValueError('INSTAGRAM_USER_ID debe ser numérico')
    # La cuenta autorizada se define exclusivamente con variables de entorno.
    # Nunca escribir un usuario fijo en este archivo: la configuración vive en
    # GitHub Actions -> Settings -> Secrets and variables -> Actions -> Variables.
    expected = os.environ.get('IG_EXPECTED_USERNAME', '').strip().lstrip('@').lower()
    if not expected:
        raise RuntimeError('Falta IG_EXPECTED_USERNAME: define la variable de GitHub para publicar')
    me = ig_api('GET', 'me', token=token, data={'fields': 'id,username'})
    actual_id = str(me.get('id', '')).strip()
    actual_username = str(me.get('username', '')).strip().lstrip('@').lower()
    if actual_id != user_id:
        raise RuntimeError('INSTAGRAM_USER_ID no coincide con la cuenta autorizada por INSTAGRAM_TOKEN')
    if actual_username != expected:
        raise RuntimeError(
            f'Cuenta Instagram diferente: esperado=@{expected}, recibido=@{actual_username}'
        )
    print(f'Cuenta Instagram verificada: @{actual_username}', flush=True)
    gh = Github()
    gh.assert_public()
    path = 'dataviral/state.json'
    raw, sha = gh.read(path)
    state = json.loads(raw) if raw is not None else {'schema':1,'episodes':{}}
    row = state['episodes'].get(ep['id'], {})
    if any(row.get(key) in ('enviando','incierto','publicado') for key in ('reel', 'foto', 'feed_video')):
        raise RuntimeError('Hay publicación previa o incierta: bloqueo anti-duplicados')
    def save():
        nonlocal sha
        result = gh.write(path, json.dumps(state,ensure_ascii=False,indent=2).encode(), sha)
        sha = result['content']['sha']
    # Subida de archivos a un repositorio público: URL estable de commit. El tamaño
    # máximo de GitHub Contents API es 100 MB; no es un CDN de producción.
    remote, commit = upload_video_to_public_github(gh, movie, ep['id'])
    video_url = f'https://raw.githubusercontent.com/{gh.repo}/{commit}/{remote}'
    response = requests.get(video_url, timeout=60)
    if not response.ok or len(response.content) != movie.stat().st_size:
        raise RuntimeError(f'MP4 no accesible públicamente: HTTP {response.status_code}')
    caption = f'{ep["title"]}\n\n{ep["lesson"]}'
    if ep.get('source'):
        caption += f'\n\nReferencias sugeridas (no verificadas): {ep["source"]}'
    caption += '\n\n#DatoWow #AprendeAlgoNuevo'
    state['episodes'][ep['id']] = row
    row['reel'] = 'enviando'
    row['updated_at'] = now()
    save()
    try:
        published = publish_container(user_id, token, video_url, caption)
    except BaseException:
        row['reel'] = 'incierto'
        row['updated_at'] = now()
        try:
            save()
        except Exception as ex:
            print(f'ALERTA: sin persistencia de estado incierto: {ex}', file=sys.stderr)
        raise
    row['reel'] = 'publicado'
    row['share_to_feed'] = True
    row['reel_id'] = published
    row['updated_at'] = now()
    save()
    print(f'Video publicado como Reel Y visible en el feed: {published}')


def main():
    ap = argparse.ArgumentParser(description='DataViral: 500 ideas, IA OpenRouter Free y video Instagram')
    ap.add_argument('--list', action='store_true')
    ap.add_argument('--episode', default='', help='ID concreto; vacío = siguiente disponible')
    ap.add_argument('--out', default='output')
    ap.add_argument('--publish', action='store_true', help='Publicar Reel visible en feed')
    ap.add_argument('--approved-id', default='', help='ID revisado manualmente (modo seguro)')
    ap.add_argument('--auto-publish', action='store_true', help='Publicación autónoma (sin revisión humana)')
    args=ap.parse_args()
    episodes=catalog()
    if len(episodes)!=500 or len({e['id'] for e in episodes})!=500:
        raise RuntimeError('Catálogo de 500 propuestas dañado')
    if args.list:
        for ep in episodes:
            print(f"{ep['id']}: {ep['title']}")
        return 0
    gh=Github() if args.publish and not args.episode else None
    ep=select_episode(episodes,gh,args.episode or None)
    if ep is None:
        ap.error('ID de episodio desconocido')
    if args.publish and not args.auto_publish and args.approved_id!=ep['id']:
        ap.error('Sin --auto-publish, debe confirmar --approved-id con el ID')
    generated=create_ai_episode(ep)
    out=Path(args.out)
    out.mkdir(exist_ok=True,parents=True)
    (out/f"{ep['id']}-guion.json").write_text(
        json.dumps(generated,ensure_ascii=False,indent=2),encoding='utf-8')
    print(f"Guion OpenRouter creado: {ep['id']}; referencias propuestas: {generated['source'] or 'ninguna'}")
    if args.publish and not generated.get('source'):
        print('AVISO: el guion no tiene fuentes; se permite publicar, pero no existe verificación independiente.', flush=True)
    movie,cover=render(generated,out,require_voice=args.publish)
    if args.publish:
        # Los enlaces son opcionales y nunca equivalen a verificación independiente.
        # --auto-publish implica riesgo de errores factuales de la IA.
        publish(generated,movie,cover,generated['id'])
    else:
        print('VISTA PREVIA: no se publicó el video')
    return 0


if __name__=='__main__':
    sys.exit(main())
