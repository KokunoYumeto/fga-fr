from audit_utils import *
from collections import Counter
import csv
dq=chr(96)*2
for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
    rel=f'sources/{tree}/fr/e221.tex'
    def r(a,b,line,why,kind='reading',count=1):
        replace(rel,a,b,layer,'e221-302',line,'Errata to TDTE IV',
                'Scan leaf 2 at 400 dpi, full page, three enlarged bands and a projective-space glyph crop: '+why,kind=kind,count=count)
    r(r'\noindent\textbf{6. TDTE IV : Les schémas de Hilbert.}',r'\noindent 6. \uwave{TDTE} IV : \uwave{Les schémas de Hilbert}.','title','Ordinary type, with separate wavy underlines under TDTE and the title words.','typesetting')
    headings=[r'Page 6, théorème 2.1, 3\textsuperscript{e} ligne','Page 15, ligne 13','Ligne 15','Ligne 18, formule (*)','Ligne 5 à partir du bas','Page 18, remarque 3.9','Page 23, ligne 5 à partir du bas','Pages 23 et 24, remarque 5.5']
    for s in headings:
        t=s.replace(r'3\textsuperscript{e}','3e')
        if s.startswith('Ligne'):
            new=r'- \quad \uline{'+t[0].lower()+t[1:]+'}.'
        else: new=r'\uline{'+t+'}.'
        r(r'\textbf{'+s+'.}',new,'eight entry headings','The heading is ordinary straight-underlined type; 3e is on the baseline, and the three continuation headings start with a ditto dash and lowercase ligne.','typesetting')
    r(' --- ',' - ','entry and footnote separators','Short dashes are printed.',count=9)
    r('« ',dq,'fourteen quoted readings','Ordinary double quotation marks are printed.',count=14)
    r(' »',"''",'fourteen quoted readings','Ordinary double quotation marks are printed.',count=14)
    r(r'\geq',r'\geqslant','two inequalities','The equality stroke is oblique, parallel to the lower stroke of the greater-than sign.',count=2)
    r(r'\leq',r'\leqslant','one inequality','The equality stroke is oblique.')
    r(r'\operatorname{Hilb}',r'\underline{\operatorname{Hilb}}','two Hilbert schemes','Hilb has a straight underline.',count=2)
    r(r'\operatorname{Hilb}}^{P}_{r}\neq\varnothing',r'\operatorname{Hilb}}^{P}_{r}=\varnothing','emptiness condition','The scan has an equality sign, not a crossed equality sign; it says the scheme is empty.')
    r(r'\mathbf P^3_{\mathbf C}',r'\mathfrak P^3_{\text{\uwave{C}}}','projective space','The projective-space P is handwritten Gothic; the complex field C has a wavy underline.')
    r(r'\mathbf C',r'\text{\uwave{C}}','two other complex-field letters','Ordinary upright C with wavy underline, not bold.',count=2)
    r('À propos','A propos','last entry opening','The initial uppercase A has no accent.')
    r('(cf.\nSéminaire','(Cf.\nSéminaire','Cartan reference','Cf. begins with an uppercase C.')
    r('(Thesis, Harvard, 1962)','(Thesis. Harvard. 1962)','footnote punctuation','The two separators are periods.')
    r(r'\footnote{HARTSHORNE',r'\footnote[4]{HARTSHORNE','footnote number','The note is numbered 4.','typesetting')
    r(r'\src{302}',r'''\src{302}
\begingroup
\makeatletter
\renewcommand\@makefnmark{\hbox{\normalfont(\textsuperscript{\@thefnmark})}}
\makeatother''','footnote marker','Both call and note label use a raised 4 within baseline parentheses; the format is local to the item.','typesetting')
    r('est non réduite en tous ses points.','est non réduite en tous ses points.\n'+r'\endgroup','end of item','Close the local note-label formatting group.','typesetting')
    upright_page(rel,layer,'e221-302')
event('e221-2.1','used and rechecked in this run','Read the restored necessary-and-sufficient formulation of boundedness. The sufficiency is the s=0 case of Theorem 2.2, with the degree-bound direction already corrected in that theorem: F_(0)=F and finitely many Hilbert polynomials bound all coefficients. This deduction is conditional on the boundedness theorem, whose full proof remains background. The original one-direction wording stays unmerged.','Erratum 221, p. 302, Page 6, Theorem 2.1; exposé 221, p. 254')
event('e221-polynomial-order','targeted proof check','Checked the repaired dichotomy for Lemma 3.5: on each flat connected stratum the rank is Q(n) for large n. If P<Q in eventual polynomial order, Q(n)>P(n) eventually and U_N becomes empty. Otherwise P(n)>=Q(n) eventually, so all sufficiently large degree inequalities impose no new conditions, and only finitely many earlier degrees remain. This proves stationarity on each of finitely many strata. The strict-to-nonstrict signs and r-to-Z instructions are read as separate literal errata; target text is not silently replaced.','Erratum 221, p. 302, Page 15 entries; exposé 221, p. 263, Lemmas 3.5-3.6')
event('e221-hartshorne','carried as background without fault found','Read the connectedness theorem report and the classification of pairs (r,P) for which Hilb_r^P is empty. The supplied transcription reversed the displayed emptiness sign; the print clearly has equality with the empty set, and both French layers now follow it. The actual connectedness proof and Hilbert-polynomial classification are external background.','Erratum 221, p. 302, Page 18, Remark 3.9 and footnote 4')
event('e221-component-grammar','used and rechecked in this run','Read the authorial insertion of d before une composante in the tangent-map discussion. The corrected wording gives the required complement of the preceding definition of the parameter space; the original exposition remains as printed because errata are not merged.','Erratum 221, p. 302, Page 23, line 5 from bottom; exposé 221, p. 271')
event('e221-mumford-nonreduced','carried as background without fault found','Read the announced nonreduced Hilbert component for smooth space curves of degree 14 and genus 24, and the blow-up construction of a smooth projective threefold with nonreduced local deformation space. The curve construction, generic nonreducedness and comparison of deformations under blow-up are not proved here; they remain background dependencies. The analytic/formal equivalence additionally uses the comparison between the completed local deformation algebra and the analytic germ.','Erratum 221, p. 302, Pages 23 et 24, Remark 5.5')
with (ROOT/'CORRECTIONS.tsv').open(newline='') as f:
    c=Counter((x['layer'],x['kind']) for x in csv.DictReader(f,delimiter='\t') if x['printed_page']=='e221-302')
record_page('e221',302,'Compared sources/fr_printed/fr/e221.tex and sources/fr/fr/e221.tex, entry lines 5-47, with scan leaf 2 at 400 dpi, full page, three enlarged bands and a tight projective-space glyph crop. Read all eight entries and footnote 4. Restored title/heading underlines, baseline 3e, continuation ditto dashes and lowercase ligne, ordinary quotation marks, oblique nonstrict inequalities, straight-underlined Hilb, the printed equality with the empty set, handwritten Gothic projective P, wavy complex C, unaccented A, capital Cf., short dashes and thesis punctuation. Footnote 4 uses raised digits in baseline parentheses via a local group. Both French layers agree. Rechecked the boundedness deduction and the eventual-polynomial-order stationarity argument; the Hartshorne and Mumford reports retain their background dependencies.\n\nOperation counts: '+'; '.join(f'{a}, {b}: {n}' for (a,b),n in sorted(c.items()))+'. Final row verdicts remain pending.')
from update_record_counts import update
update()
