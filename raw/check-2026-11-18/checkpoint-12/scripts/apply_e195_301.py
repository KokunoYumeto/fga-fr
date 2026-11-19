from audit_utils import *
from collections import Counter
import csv
dq=chr(96)*2
for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
    rel=f'sources/{tree}/fr/e195.tex'
    def r(a,b,line,why,kind='reading',count=1):
        replace(rel,a,b,layer,'e195-301',line,'Errata to TDTE II',
                'Scan leaf 3 at 400 dpi, full page and three enlarged bands: '+why,kind=kind,count=count)
    for s in [r'Page 15, n\textsuperscript{o} 3','Page 16, proposition 3.1',r'Pages 18 et 19, remarques, 2\textsuperscript{o}','Page 19, paragraphe 5','Page 20, lignes 12 et 13']:
        t=s.replace('paragraphe',r'\S')
        r(r'\textbf{'+s+'.}',r'\uline{'+t+'}.','five entry headings','Ordinary text with straight underline; the fourth heading prints the section sign.','typesetting')
    r(' --- ',' - ','entry separators','The dashes are short.',count=5)
    r('TDTE V',r'\uwave{TDTE} V','first reference','TDTE has a wavy underline.')
    r('Mumford (cf. SHMT)',r'MUMFORD (Cf. \uwave{SHMT})','moduli attribution','The surname is uppercase, Cf. begins with a capital C, and SHMT has a wavy underline.')
    r('non-diviseur de zéro','non diviseur de 0','regular section','There is no joining hyphen and the numeral 0 is printed.')
    old=r'''Au lieu de
\[
  G_x=G\bigl(\operatorname{Spec}(\widehat{\mathcal O}_{\mathfrak X,x})\bigr),
\]
lire'''
    new='Au lieu de '+dq+r'$\text{\uwave{G}}_x=G(\operatorname{Spec}(\widehat{\text{\uwave{O}}}_{\mathfrak X,x}))$'+"'', lire :"
    r(old,new,'first quoted equality','The equality is inline in ordinary quotes, followed by a comma and lire colon. The sheaf G and structure O have wavy underlines.','structure')
    r(r'G_x=G\bigl(\operatorname{Spec}(\mathcal O_{\mathfrak X,x})\bigr)',r'\text{\uwave{G}}_x=G(\operatorname{Spec}(\text{\uwave{O}}_{\mathfrak X,x}))','corrected display left side','Only the sheaf G and O have wavy underlines; G as a functor is ordinary.')
    r(r'G\bigl(\operatorname{Spec}(\widehat{\mathcal O}_{\mathfrak X,x})\bigr)',r'G(\operatorname{Spec}(\widehat{\text{\uwave{O}}}_{\mathfrak X,x}))','corrected display right side','The O has a wavy underline and a hat, and the functor G is ordinary.')
    r(r'\mathcal O',r'\text{\uwave{O}}','two final quoted rings','The two O letters are upright with a wavy underline.',count=2)
    r(' », lire\n',' », lire :\n','final correction instruction','The printed lire is followed by a colon.')
    r('« ',dq,'four quotations','Ordinary double quotes are printed.',count=4)
    r(' »',"''",'four quotations','Ordinary double quotes are printed.',count=4)
    upright_page(rel,layer,'e195-301')
event('e195-p15','carried as background without fault found','Read the reference from the preliminary Picard discussion to TDTE V (exposé 232), without merging later definitions into the exposé.','Erratum 195, p. 301, Page 15, no. 3')
event('e195-p16','carried as background without fault found','Read the qualification propre et séparable in the base-change discussion of Proposition 3.1. The supplied original print already contains properness and separable fibres in the corresponding parenthesis; the erratum is retained literally as an authorial instruction. The proper flat geometrically reduced base-change theorem supplying the equivalence is background.','Erratum 195, p. 301, Page 16, Proposition 3.1; exposé 195, p. 384')
event('e195-abelian-lifting','carried as background without fault found','Read the announced unobstructed lifting of unpolarized abelian schemes over artinian local quotients, the variance-of-obstruction proof indication, and the Mumford moduli report. The page gives no full proof; the obstruction-variance theorem and actual moduli construction remain background. No polarized unobstructedness is inferred from the unpolarized assertion.','Erratum 195, p. 301, Pages 18 et 19, remarques, 2o')
event('e195-regular-thickenings','targeted proof check','Checked necessity of regularity on every thickening, rather than only on the formal scheme: take A=k[[t]], ideal of definition (t), and section t. It is a non-zero-divisor in A but vanishes on X_0, and its formal nonvanishing open is empty. The finite free cover B=A[e]/(e squared) then has the nonidentity automorphism e maps to (1+t)e reducing to the identity on X_0, while the unramified condition over the empty open is vacuous. This refutes the original injectivity claim under the weaker hypothesis. The stated strengthened regularity excludes this example. Full sufficiency is background, based on uniqueness over the dense regular opens at all levels.','Erratum 195, p. 301, Page 19, section 5; exposé 195, p. 387')
event('e195-stalk-completion','carried as background without fault found','Read the replacement of the completed-stalk equality by the local-ring equality and inclusion into the completion, together with the hat on the marked residue algebra. Finite presentation supplies passage from germs to the local ring; injectivity after completion uses faithfully flat descent and uniqueness of marked isomorphisms under the strengthened regular-section hypotheses. Those descent and uniqueness inputs are not reproved here. The hat on the marked algebra matches the completed tensor base in the target passage.','Erratum 195, p. 301, Page 20, lines 12 and 13; exposé 195, p. 388')
with (ROOT/'CORRECTIONS.tsv').open(newline='') as f:
    c=Counter((x['layer'],x['kind']) for x in csv.DictReader(f,delimiter='\t') if x['printed_page']=='e195-301')
record_page('e195',301,'Compared sources/fr_printed/fr/e195.tex and sources/fr/fr/e195.tex, entry lines 31-63, against scan leaf 3 at 400 dpi, full page and three enlarged bands. Read all five entries, including every quoted formula, hat, subscript and reference. Restored straight headings, the section sign, short separators, wavy abbreviations/G/O, ordinary quotation marks, the inline first equality, both lire colons, uppercase MUMFORD and Cf., and the unhyphenated non diviseur de 0. The later displayed inclusion remains displayed. Both French layers agree. Checked necessity of the all-thickenings regularity condition with an explicit finite free cover and automorphism. The abelian lifting, base-change and completion/descent assertions retain their stated background dependencies. Errata remain separate.\n\nOperation counts: '+'; '.join(f'{a}, {b}: {n}' for (a,b),n in sorted(c.items()))+'. Final row verdicts remain pending.')
from update_record_counts import update
update()
