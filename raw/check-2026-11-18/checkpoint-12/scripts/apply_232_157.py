from audit_utils import *
from collections import Counter
import csv
for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
    rel=f'sources/{tree}/fr/232.tex'
    def r(a,b,line,why,kind='reading',count=1):
        replace(rel,a,b,layer,'232-157',line,'5.4, 6.1',
                'Scan leaf 16 at 400 dpi and three enlarged bands: '+why,kind=kind,count=count)
    r(r'\result{REMARQUES}',r'\result{\uline{Remarques}}','5.4 heading','The heading is mixed case and straight underlined.')
    r('« principe de compatibilité »',"``principe de compatibilité''",'opening phrase','Ordinary double quotation marks are printed.')
    r('i.e.','i. e.','two abbreviations','The initials are spaced.',count=2)
    r('discrète complet à corps','discrète \\uline{complet} à corps','special complete base','Only complet is underlined.')
    r('« compactifications »',"``compactifications''",'moduli compactifications','Ordinary double quotation marks are printed.')
    r('Baily--Satake','Baily-Satake','compound surname','The connecting mark is a short hyphen.')
    r('travaux de Igusa.)','travaux de IGUSA).','last sentence of 5.4','The second Igusa is uppercase, unlike the first, and the period follows the closing parenthesis.')
    r(r"\fsection{6}{Théorèmes d'existence relatifs}",r"\fsection{6}{\normalfont\uwave{Théorèmes d'existence relatifs}.}",'section 6 heading','The upright heading has a wavy underline and final period.')
    r(r'\longrightarrow',r'\to','three morphisms','All three arrows are short.',count=3)
    r("S'$ soit plat et à fibres", "S'$ soit \\uline{plat} et à fibres",'hypothesis on Stein factor','Only the first occurrence of plat after the Stein factor is underlined.')
    r('C 2) on a','C 2 on a','reference before the canonical isomorphism','There is no closing parenthesis after C 2 in the print.')
    if tree=='fr':
        r('C 2 on a','C 2) on a','reference before the canonical isomorphism','Supply the closing parenthesis matching the opening parenthesis before avec les notations.','misprint of the original')
    r(r'\operatorname{Pic}',r'\underline{\operatorname{Pic}}','nine Picard names','Restore the scheme underline initially; the three functor occurrences are distinguished in the following two rows.',count=9)
    r('foncteurs\n\\[\n\\underline{\\operatorname{Pic}}_{X/S}\\xrightarrow{\\sim}\n\\Pi_{S\'/S}\\underline{\\operatorname{Pic}}_{X/S\'},', 'foncteurs\n\\[\n\\text{\\uwave{Pic}}_{X/S}\\xrightarrow{\\sim}\n\\Pi_{S\'/S}\\text{\\uwave{Pic}}_{X/S\'},','second displayed isomorphism','Both Pic symbols here denote functors and have wavy underlines.')
    r("3.1, qui implique que $\\underline{\\operatorname{Pic}}_{X/S'}$", "3.1, qui implique que $\\text{\\uwave{Pic}}_{X/S'}$",'representable functor','This Pic name has a wavy underline.')
    r(r'\xrightarrow{\sim}',r'\overset{\sim}{\to}','two isomorphisms','The tilde is over a short arrow.',count=2)
    r(r'\Pi_{',r'\prod\limits_{','three restriction-of-scalars signs','The large product signs have their subscripts directly below them, including the final inline expression.',count=3)
    upright_page(rel,layer,'232-157')
event('232-5.4','carried as background without fault found','The remark interprets a historical compatibility principle through representability and points to the hypotheses of 3.1. Its comparison of the then-known results and compactifications is retained as historical background; no modern existence assertion is substituted. The algebraically closed residue-field qualification is genuinely printed on this page, in contrast with its editorial insertion on p. 156.','232, p. 157, remarque 5.4')
event('232-6.1','targeted proof check','Checked the types and direction of the scheme and functor isomorphisms, with restriction of scalars from S-prime to S. The intermediate morphism is projective because X is projective over S and S-prime is separated over S; the assumed flat integral geometric fibres put it under 3.1. A line bundle on a finite scheme over a local base becomes trivial after shrinking about any base point: trivialize over the semilocal finite fibre, lift generators, and use the finite image of the failure locus. Thus the relative Picard sheaf of the finite Stein base is zero. The remaining sheaf-identification/descent step and the restriction-of-scalars existence theorem are retained as background inputs, rather than claimed independently proved here. The open-and-closed quasi-projective pieces from section 3 give an affine neighborhood for any finite fibre subset, the condition used by the printed existence argument.','232, p. 157, proposition 6.1 and proof')
with (ROOT/'CORRECTIONS.tsv').open(newline='') as f:
    c=Counter((x['layer'],x['kind']) for x in csv.DictReader(f,delimiter='\t') if x['printed_page']=='232-157')
record_page('232',157,'Compared both French layers, entry lines 698-743, with scan leaf 16 at 400 dpi and three enlarged bands. Read all of 5.4, section 6 introduction and 6.1 with both displayed isomorphisms and the complete proof paragraph.\n\nRestored headings, quotation marks, exact case of the two Igusa names, emphasis, punctuation, short arrows, product limits and the distinction between six straight-underlined schemes and three wavy-underlined functors. Restored the missing closing parenthesis as a printed omission; supplied it only in corrected French. Checked the hypotheses and types in 6.1 and one local triviality step, while leaving the general descent and restriction-of-scalars theorems as identified background.\n\nOperation counts: '+'; '.join(f'{a}, {b}: {n}' for (a,b),n in sorted(c.items()))+'. Final row verdicts remain pending.')
from update_record_counts import update
update()
