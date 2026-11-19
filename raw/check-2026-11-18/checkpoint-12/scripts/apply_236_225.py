from audit_utils import *
from collections import Counter
import csv
for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
    rel=f'sources/{tree}/fr/236.tex'
    def r(a,b,line,why,kind='reading',count=1):
        replace(rel,a,b,layer,'236-225',line,'1.1, 1.2, 1.3',
                'Scan leaf 6 at 400 dpi, full page and three enlarged bands: '+why,kind=kind,count=count)
    r(r'H\longrightarrow G|U',r'H\to G|U','opening arrow','The arrow is short.')
    s,_,_=page_text(rel,225)
    a=s.index('Soient $X$');b=s.index('\n\nPar descente',a)
    old=s[a:b]
    r(old,underline_prose(old),'lemma 1.3 statement','The statement prose has straight underlines, with mathematical symbols outside the emphasis. The plural Soient is printed and is retained.')
    r('i.e.','i. e.','1.3 proof','The printed abbreviation is spaced.')
    s,_,_=page_text(rel,225)
    a=s.index(r'\noindent a.');b=s.index('\nPour (a)',a)
    old=s[a:b]
    new=old.replace(r'G_y^\tau',r'G^\tau').replace(r'G_{y\'}^\tau',r'G^\tau')
    new=new.replace("G_{y'}^\\tau",r'G^\tau')
    r(old,new,'openness conditions a and b','All four occurrences in these two conditions are G tau without a fibre subscript; the final occurrence at the foot of the page does have y.')
    r(r'\overline{\{y\}}',r'\overline{y}','conditions a and proof of a','The print has an overbar on y alone, without set braces.',count=2)
    r(r'$g^n(y)\in G_y^\circ$ ;',r'$g^n(y)\in G^\circ$,','proof of a, first membership','The print has G zero without a fibre subscript and follows the formula with a comma.')
    r(r"$g^n(y')\in G_{y'}^\circ$",r"$g^n(y')\in G^\circ$",'proof of a, second membership','The print again uses G zero without a fibre subscript.')
    r('classes modulo','classes mod.','proof of b','The printed word is abbreviated mod. with its period.')
    upright_page(rel,layer,'236-225')
event('236-1.2-spreading','targeted proof check','The final identification is valid: a connected open subgroup H_s of a group over a field is contained in the identity component and is also closed there, because its other cosets are open; hence it equals that component. The finite-presentation spreading of the subgroup and the persistence of connected fibres after shrinking are inputs from limit and constructibility theory, not independently established here. No change to the printed proof is needed.','236, p. 225, opening paragraph')
event('236-1.3','carried as background without fault found','Read the full statement and its proof, including the faithfully flat complete-local reduction, the exact reference [2], III, 5.5.1, and the valuative criterion for a proper subset. A complete proof requires the cited proper-component decomposition, descent and specialization/connectedness results. These are not re-proved by the present reading. Soient introduces X, g and X zero and is retained.','236, p. 225, lemma 1.3 and proof')
event('236-1.1-tau-open','targeted proof check','Checked the power argument. A torsion component class at y prime puts every power of g(y prime) in finitely many finite-type components, hence in a quasi-compact open of that fibre and in an ambient quasi-compact open U. Since U is open it contains all corresponding generizations g(y)^n. After restricting the base near y prime, the fibre U_y is quasi-compact and meets only finitely many open connected components of G_y. The component class of g(y) therefore has finite order. The constructibility argument gives a neighborhood of each point in its closure on which some power lies in G zero; together with generization stability, the Noetherian topological criterion gives openness. Constructibility of G zero and the field-case finiteness are the preceding inputs; no fibre subscripts need to be inserted in the printed conditions.','236, p. 225, proof of 1.1(ii), conditions a and b')
with (ROOT/'CORRECTIONS.tsv').open(newline='') as f:
    c=Counter((x['layer'],x['kind']) for x in csv.DictReader(f,delimiter='\t') if x['printed_page']=='236-225')
record_page('236',225,'Compared sources/fr_printed/fr/236.tex and sources/fr/fr/236.tex, entry lines 189-236, against scan leaf 6 at 400 dpi, full page and three enlarged bands. Read the conclusion of 1.2, all of 1.3, and the two-condition proof that G tau is open, including every exponent, prime, circle and fibre subscript.\n\nRestored the short opening arrow, all lemma emphasis, spaced abbreviation, six memberships without the added fibre subscripts, the closure bar on y without braces, the comma after the first power membership, printed mod., and upright mathematical letters. The final G tau at the bottom retains its printed y subscript. There is no corrected-versus-printed mathematical difference on this page. Checked the connected-open-subgroup conclusion and the finite-component power argument; the complete-local decomposition and descent input for 1.3 remain background, explicitly recorded as such.\n\nOperation counts: '+'; '.join(f'{a}, {b}: {n}' for (a,b),n in sorted(c.items()))+'. Final row verdicts remain pending.')
from update_record_counts import update
update()
