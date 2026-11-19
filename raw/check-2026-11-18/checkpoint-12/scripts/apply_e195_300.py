from audit_utils import *
from collections import Counter
import csv
dq=chr(96)*2
for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
    rel=f'sources/{tree}/fr/e195.tex'
    def r(a,b,line,why,kind='reading',count=1):
        replace(rel,a,b,layer,'e195-300',line,'Errata to TDTE II',
                'Scan leaf 2 at 400 dpi, full page, three enlarged bands and a tight cotangent crop: '+why,kind=kind,count=count)
    r("\\noindent\\textbf{4. TDTE II : Le théorème d'existence en théorie formelle des\nmodules.}","\\noindent 4. \\uwave{TDTE} II : \\uwave{Le théorème d'existence en théorie formelle des\nmodules}.",'title','Ordinary type and separate wavy underlines under TDTE and the title words; the numbering, II, colon and final period remain outside.','typesetting')
    for s in ['Page 8','Page 14, remarque']:
        r(r'\textbf{'+s+'.}',r'\uline{'+s+'}.','entry headings','The heading words have a straight underline.','typesetting')
    r(' --- ',' - ','entry separators','Short dashes are printed.',count=2)
    r(r'\mathfrak m_\xi/\mathfrak m_\xi^2',r'\mathfrak m_\xi/m_\xi^2','cotangent quotient','The numerator m is Gothic and the denominator m is ordinary upright handwritten; the two letterforms are visibly different.')
    r(r'\mathfrak n','n','base ideal and its quotient','All three n letters are ordinary upright, including the isolated n.',count=3)
    r('$O$',r'$\text{\uwave{O}}$','simplicity clause','The O has a wavy underline.')
    r('SGA III',r'\uwave{SGA} III','reference','SGA has a wavy underline.')
    r('« ',dq,'Hilbert quotation','Ordinary double quotation marks are printed.')
    r(' »',"''",'Hilbert quotation','Ordinary double quotation marks are printed.')
    r('(cf. TDTE IV)',r'(Cf. \uwave{TDTE} IV)','Hilbert reference','Cf. begins with a capital C and TDTE has a wavy underline.')
    r('Nagata et Hironaka','NAGATA et HIRONAKA','counterexample attributions','The surnames are uppercase.')
    r('dimension zéro','dimension 0','dimension','The numeral 0 is printed, not the word zéro.')
    upright_page(rel,layer,'e195-300')
event('e195-relative-cotangent','targeted proof check',
      'Checked the need to quotient out the base cotangent image when the residue extension is separable: for O=Lambda=k[[t]] with residue k, the relative tangent functor is zero whereas m/m squared has dimension one, and the image of n/n squared is the whole space. The quotient is m/(m squared+nO), with the image understood after extension to the residue field. This corrects the absolute dimension assertion. The scan of the original proposition already prints n_xi O_xi in the displayed denominator; the erratum therefore also has to be read against the surrounding absolute formula and dimension sentence. No erratum is merged into the exposé.',
      'Erratum 195, p. 300, Page 8; exposé 195, p. 376, Proposition 5, 1')
event('e195-relative-cotangent-inseparable','refuted, with refined statement e195-relative-cotangent-separable',
      'The quotient prescription does not by itself give the general relative tangent space for inseparable residue extensions. Rechecked the earlier counterexample Lambda=F_p(s), O=K=Lambda(u), u^p=s: m=n=0 but the Lambda-derivation d(u)=1 gives a nonzero tangent vector. Thus the conormal-quotient formula needs the separable-residue setting, or replacement by the relative differentials formulation. The author separately flags inseparability for simplicity; the historical erratum wording is preserved, and this limitation is recorded for the notes.',
      'Erratum 195, p. 300, Page 8, quotient and separability clauses')
event('e195-simplicity','carried as background without fault found',
      'Read the explicit separability restriction on the earlier simplicity definition and the reference to SGA III, 1.1 for the general case. A full replacement definition and formal smoothness theorem are external background, not proved by the wording of this erratum.',
      'Erratum 195, p. 300, Page 8, final two sentences')
event('e195-p14','carried as background without fault found',
      'Read the projective Hilbert-scheme solution and the Nagata/Hironaka nonrepresentability reports for zero-dimensional subschemes of smooth proper threefolds. The existence and properties of those examples require their construction; the failure of the symmetric square is the indicated obstruction, not a construction supplied on this page.',
      'Erratum 195, p. 300, Page 14, remarque')
with (ROOT/'CORRECTIONS.tsv').open(newline='') as f:
    c=Counter((x['layer'],x['kind']) for x in csv.DictReader(f,delimiter='\t') if x['printed_page']=='e195-300')
record_page('e195',300,'Compared sources/fr_printed/fr/e195.tex and sources/fr/fr/e195.tex, entry lines 5-30, against scan leaf 2 rendered at 400 dpi, full page, three enlarged bands and a tight cotangent crop. Read the title, source line and both entries. Restored separate wavy title/abbreviation underlines, straight entry headings, short dashes, mixed Gothic/ordinary m in the quotient, ordinary n, wavy O, capital Cf., ordinary quotes, uppercase surnames and numeral 0. Both French layers agree. Checked the relative cotangent correction in the separable setting and its failure for inseparable residue extensions; the precise limitations and the distinction between the original displayed quotient and its following absolute dimension sentence are recorded. The Hilbert/symmetric-square existence reports remain background.\n\nOperation counts: '+'; '.join(f'{a}, {b}: {n}' for (a,b),n in sorted(c.items()))+'. Final row verdicts remain pending.')
from update_record_counts import update
update()
