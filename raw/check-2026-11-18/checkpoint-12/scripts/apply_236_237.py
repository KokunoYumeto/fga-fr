from audit_utils import *
from collections import Counter
import csv
dq=chr(96)*2
for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
    rel=f'sources/{tree}/fr/236.tex'
    def r(a,b,line,why,kind='reading',count=1):
        replace(rel,a,b,layer,'236-237',line,'3.3',
                'Scan leaf 18 at 400 dpi, full page and three enlarged bands: '+why,kind=kind,count=count)
    for phrase in ['variété de Picard','est définie sur $k$']:
        r('« '+phrase+' »',dq+phrase+"''",'opening historical paragraph','The print uses ordinary double quotation marks.')
    r(r'$(\operatorname{Pic}_{X/k})_{\mathrm{réd}}^\circ$',
      r'$(\operatorname{Pic}_{X/\bar k})_{\mathrm{réd}}^\circ$',
      'classical Picard variety','The base k in this formula has a bar. It names the geometric Picard variety whose descent to k is being asserted.')
    r('avec\n\\[\n\\mathcal O_S\\xrightarrow{\\sim}f_*(\\mathcal O_X)\n\\]\npour',
      'avec $\\mathcal O_S\\overset{\\sim}{\\to}f_*(\\mathcal O_X)$ pour',
      'structure-sheaf hypothesis','The isomorphism is inline, with a short arrow and tilde above it.','structure')
    r('pour (3.3), (ii),', 'pour (3.3), (ii)',
      'extra hypothesis for (ii)','There is no comma after (ii).')
    r("qu'on appelle schéma\nabélien sur", "qu'on appelle \\uline{schéma\nabélien} sur",
      'definition','Only schéma abélien is underlined.')
    r('Sous les conditions précédentes :',r'\uline{Sous les conditions précédentes} :',
      'theorem opening','The opening words are underlined.')
    r(r'\mathfrak m',r'm','Artin quotients','The ideal letter m is ordinary typed m, not Gothic.')
    r("valuation discrète (complet", "valuation discrète,\n(complet",
      'trait qualification','A comma precedes the parenthesis.')
    r('i.e.','i. e.','two parenthetical definitions','Both abbreviations are spaced.',count=2)
    r('le schéma abélien dual (i. e.','le schéma abélien dual, (i. e.',
      'dual abelian scheme','A comma is printed before the parenthesis.')
    r('schémas en groupes commutatifs : si','schémas en groupes commutatifs, si',
      'proof opening','The print has a comma, not a colon.')
    r(r'\operatorname{Pic}',r'\underline{\operatorname{Pic}}',
      'ten Picard names before exception','The names are straight-underlined except the second name in (i), restored separately.',count=10)
    r(r'$\underline{\operatorname{Pic}}_{X/S}^\circ$, il est unique.',
      r'$\operatorname{Pic}_{X/S}^\circ$, il est unique.',
      'second Picard name in (i)','The enlarged crop shows no underline on this name.')
    r(r'\operatorname{Alb}^0',r'\operatorname{Alb}^\circ',
      'two degree-zero Albanese names','The superscript zero is the open-circle shape used for identity components on this page.',count=2)
    r(r'\longrightarrow',r'\to','five arrows','The five arrows are short.',count=5)
    s,_,_=page_text(rel,237)
    spans=[
        ("S'il existe un sous-schéma abélien de","compatible avec les changements de base."),
        ("Pour qu'il existe un tel sous-schéma abélien,","si on y tient)."),
        ("Supposons que $A$ existe, et soit","le schéma abélien dual"),
        ("Alors on peut construire","dans des schémas para-abéliens"),
        ("La formation de","commute au changement de base."),
    ]
    for start,end in spans:
        a=s.index(start); b=s.index(end,a)+len(end); old=s[a:b]
        r(old,underline_prose(old),'theorem emphasis','This prose span has a straight underline; displayed symbols and the explanatory parentheses in (iii) are excluded.')
    upright_page(rel,layer,'236-237')
event('236-3.3-i','targeted proof check',
      'Read the uniqueness statement and the opening rigidity argument, which continues on the next page. Conditional on uniqueness, the base-change conclusion follows because the base change of an abelian subscheme is still an abelian subscheme and its geometric fibres are the reduced identity components; identity components of the group fibres are compatible with field extension. The general rigidity assertion itself remains background pending its continuation.',
      '236, p. 237, theorem 3.3(i) and beginning of proof')
event('236-3.3-ii','carried as background without fault found',
      'Read all three existence tests: arbitrary local Artin bases, the quotients A/m^(n+1) for a local base, and discrete valuation bases when S is reduced. The additional quasi-projective-open hypothesis is explicitly restricted to (ii). No proof of these tests is claimed before the continuation; all indices, the completeness qualification and the reduced-base condition have been checked against the enlarged image.',
      '236, p. 237, hypotheses and theorem 3.3(ii)')
event('236-3.3-iii','carried as background without fault found',
      'Read the construction claimed for the dual abelian scheme Alb^0, its torsor Alb^1 and the universal map X to Alb^1, including the scope of the universal property (maps into torsors under abelian schemes) and base-change compatibility. Duality, existence of the torsor and the universal property remain background here pending the proof. The introductory geometric Picard-variety symbol is over the algebraic closure, as the scan shows.',
      '236, p. 237, theorem 3.3(iii)')
with (ROOT/'CORRECTIONS.tsv').open(newline='') as f:
    c=Counter((x['layer'],x['kind']) for x in csv.DictReader(f,delimiter='\t') if x['printed_page']=='236-237')
record_page('236',237,'Compared sources/fr_printed/fr/236.tex and sources/fr/fr/236.tex, entry lines 730-785, with scan leaf 18 at 400 dpi, full page and three enlarged bands. Read the hypotheses, all of theorem 3.3 and the first part of its rigidity proof.\n\nRestored the bar on the base field of the classical Picard variety, inline structure-sheaf isomorphism, ordinary m, short arrows, quotation marks, punctuation, nine straight Picard names and the un-underlined second name in (i). Restored the theorem’s straight prose emphasis with both explanatory parentheses in (iii) excluded; the trait qualification in (ii) is underlined as printed. The zero Albanese superscripts use the printed open-circle shape. There is no new mathematical difference between the French layers on this page. Checked the conditional base-change deduction and recorded the remaining existence, rigidity and duality statements as background before reading their continuation.\n\nOperation counts: '+'; '.join(f'{a}, {b}: {n}' for (a,b),n in sorted(c.items()))+'. Final row verdicts remain pending.')
from update_record_counts import update
update()
