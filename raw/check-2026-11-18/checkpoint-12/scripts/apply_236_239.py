from audit_utils import *
from collections import Counter
import csv
dq=chr(96)*2
for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
    rel=f'sources/{tree}/fr/236.tex'
    def r(a,b,line,why,kind='reading',count=1):
        replace(rel,a,b,layer,'236-239',line,'3.4, 3.5',
                'Scan leaf 20 at 400 dpi, full page, three enlarged bands and first-fibre detail: '+why,kind=kind,count=count)
    r('Shimura','SHIMURA','condition a attribution','The name is in capitals.')
    for phrase in ['variété de Picard','compatible avec spécialisations','schéma formel des Modules']:
        r('« '+phrase+' »',dq+phrase+"''",'quotation marks','The print uses ordinary double quotation marks.')
    r('(cf. (1.7)) et, par suite,','(cf. (1.7)) et par suite,',
      'smooth identity component','There is no comma before par suite.')
    r("soit simple sur $k(s)$ (ou, ce qui revient au\nmême,\n\\[\n\\dim\\operatorname{Pic}_{X_s/k(s)}=\\dim H^1(X_s,\\mathcal O_{X_s})).\n\\]",
      "soit simple sur $k(s)$, (ou ce qui revient au\nmême, $\\dim\\operatorname{Pic}_{X_s/k(s)}=\\dim H^1(X_s,\\mathcal O_{X_s})$).",
      '3.5 tangent-dimension criterion','The equality is inline. There is a comma before the parenthesis and no comma after ou. The first fibre has subscript s, not s prime, as the tight crop confirms.','structure')
    r(r'$\operatorname{Pic}_{X/S}$ soit simple sur $S$ aux points de',
      r'$\operatorname{Pic}_{X/S}$ soit simple sur $S$ en les points de',
      '3.5 conclusion','The printed phrase is en les points, not aux points.')
    r('qui prolonge\n\\[\nP_n=\\operatorname{Pic}_{X_n/A_n}^\\circ,\n\\]\net',
      'qui prolonge $P_n=\\operatorname{Pic}_{X_n/A_n}^\\circ$, et',
      'inductive abelian scheme','The formula defining P_n is inline.','structure')
    r('(N.B. ---','(N. B. -','nota bene','The letters are spaced and the following dash is short.')
    r("II) pour un schéma abélien sur un corps algébriquement clos est simple",
      "II.) pour un schéma abélien sur un corps algébriquement clos, est simple",
      'formal moduli reference','A period follows II inside the parenthesis, and a comma follows clos.')
    r(r'\operatorname{Pic}',r'\underline{\operatorname{Pic}}',
      'seventeen Picard names','All seventeen names have straight underlines.',count=17)
    s,_,_=page_text(rel,239)
    start=s.index('Sous les conditions de (3.3)')
    end=s.index(r'$\underline{\operatorname{Pic}}_{X|U/U}^{\circ\circ}$ existe.',start)+len(r'$\underline{\operatorname{Pic}}_{X|U/U}^{\circ\circ}$ existe.')
    old=s[start:end]
    r(old,underline_prose(old),'3.5 statement emphasis','All prose in the theorem is straight-underlined, including the equivalence parenthesis; mathematical letters are not part of that prose underline.')
    old="tout schéma abélien défini sur un quotient d'anneau local artinien peut se\nprolonger"
    r(old,r'\uline{'+old+'}','key lifting result','These words have a straight underline, ending before the explanatory parenthesis.')
    if tree=='fr':
        r(r'\underline{\operatorname{Pic}}_{X_n/S}^{\circ\circ}',
          r'\underline{\operatorname{Pic}}_{X_n/S_n}^{\circ\circ}',
          '3.4 condition c','The infinitesimal restriction X_n is over the corresponding infinitesimal base S_n=Spec(V/m^(n+1)), not over the whole trait S; this is the Artin-base test in 3.3(ii). For a constant elliptic family, interpreting the printed relative functor over S would give trivial generic fibre and positive-dimensional special identity fibre, so it cannot have an abelian S-subscheme with those fibres, although condition b holds for the original family.','misprint of the original')
    upright_page(rel,layer,'236-239')
event('236-3.4-c','targeted proof check',
      'Condition c is the infinitesimal-base test of 3.3(ii), so its relative base must be S_n=Spec(V/m^(n+1)), with X_n the corresponding restriction. If it were the whole S as printed, a constant elliptic X/S would give an empty X_n on the generic fibre and hence trivial generic Picard functor, while its special Picard identity component has dimension one. Such fibres cannot be the fibres of an abelian S-scheme, whose relative dimension is locally constant. Thus c as printed cannot be equivalent to b. Corrected French adds the missing n to the base.',
      '236, p. 239, continuation of 3.4, condition c')
event('236-3.4-equivalences','carried as background without fault found',
      'Read the equivalence of the specialization isomorphism, the existence of the canonical abelian subscheme, and the corrected Artin-base condition. The finite p-primary kernel previously claimed implies trivial kernel when the residue characteristic exponent is 1, so the characteristic-zero consequence is consistent. The full isogeny and extension arguments remain background. The smooth-identity-component observation uses 1.7 and the standing properness of Pic^0.',
      '236, p. 239, continuation of 3.4 and paragraph before 3.5')
event('236-3.5','carried as background without fault found',
      'Read the smooth geometric fibre hypothesis, its tangent-dimension equivalent from 2.10(iii), and the claimed smoothness near the identity components over an open U. Read the induction over Artin quotients and the simultaneous lifting of the abelian scheme P_n and its universal line bundle. The assumed local section is intended to rigidify the Poincare family. The final key lifting statement and its proof continue on p. 240; no proof verdict is claimed at this stage.',
      '236, p. 239, theorem 3.5 and first part of proof')
with (ROOT/'CORRECTIONS.tsv').open(newline='') as f:
    c=Counter((x['layer'],x['kind']) for x in csv.DictReader(f,delimiter='\t') if x['printed_page']=='236-239')
record_page('236',239,'Compared sources/fr_printed/fr/236.tex and sources/fr/fr/236.tex, entry lines 830-888, with scan leaf 20 at 400 dpi, full page, three enlarged bands and a tight enlarged first-fibre crop. Read the equivalences ending 3.4, theorem 3.5 and its induction through the unfinished formal-moduli sentence.\n\nRestored capitals, ordinary quotes, punctuation, two inline formulas, the phrase en les points, seventeen straight Picard names, theorem emphasis and the underlined lifting claim. The first-fibre detail shows s without a prime; no prime was introduced. Corrected French alone supplies the missing n on the infinitesimal base in condition c, checked against 3.3(ii) and a constant elliptic-family test. The proof of 3.5 remains unfinished on this page and its deformation inputs are recorded as background.\n\nOperation counts: '+'; '.join(f'{a}, {b}: {n}' for (a,b),n in sorted(c.items()))+'. Final row verdicts remain pending.')
from update_record_counts import update
update()
