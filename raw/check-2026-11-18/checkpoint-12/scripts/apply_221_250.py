from audit_utils import *
from collections import Counter
import csv

for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
    rel=f'sources/{tree}/fr/221.tex'
    def r(a,b,line,why,kind='reading',count=1):
        replace(rel,a,b,layer,'221-250',line,'section 1',
                'Scan leaf 3 at 400 dpi and all enlarged bands: '+why,kind=kind,count=count)
    r(r'\emph{équivalents}',r'\uline{équivalents}','line 1','The term is straight-underlined, not italic.')
    r(r'$k$-homomorphismes',r'$K$-homomorphismes','line 2','The printed letter is uppercase K.')
    r(r"$\mathcal F'_{K''}$",r"$\mathcal F_{K'}$",'line 3','The second sheaf has no prime on F and only one prime on K in the print.')
    r('Notons que si $X$','Notons que si $X_0$','line 5','The printed X bears the small zero subscript.')
    s,_,_=page_text(rel,250)
    for a,b,body in list(footnotes(s)):
        r(s[a:b],'','line 6 / footnote','There is no note marker or footnote on the printed page. The editorial explanation belongs in the audit record.','structure')
    r('une extension de type fini de $k$','une extension \\uline{de type fini} de $k$','line 7','The three-word phrase de type fini is straight-underlined.')
    r('aux extensions algébriquement closes','aux extensions \\uline{algébriquement closes}','lines 8-9','The two words algébriquement closes are straight-underlined.')
    r(r'$k$-automorphisme',r'$K$-automorphisme','lines 11-12','The printed prefix uses uppercase K.')
    r(r'\mathcal F\otimes_\Omega(\Omega,\sigma)',r'\mathcal F\otimes_K(\Omega,\sigma)','line 12','The printed tensor subscript is K, not Omega.')
    r('sur un même $X_K$, la classe','sur un \\uline{même} $X_K$, la classe','paragraph 2, line 3','Only this occurrence of même is underlined.')
    r(r'\operatorname{Tor}_i',r'\mathop{\text{\uwave{Tor}}}\nolimits_i','paragraph 2, line 5','Tor has a wavy underline; its lower index is i.')
    r('$U$',r'$\mathcal U$','paragraphs 2-3, isolated operation symbols','The operation letter is handwritten script U, unlike typed ordinary E, X and n.',count=3)
    r('$U(',r'$\mathcal U(','paragraph 2, two operation values','The two function symbols have the same handwritten script U.',count=2)
    r(r'\ldots',r'\cdots','paragraph 2, four lists','The three-dot groups are raised to midline in the four indexed lists.',count=4)
    r('ensembles $E_1','ensemble $E_1','paragraph 2, penultimate sentence','The print has singular ensemble after n.')
    r(r'\emph{limités}',r'\uline{limités}','paragraph 3','The defining occurrence is straight-underlined.')
    r('$S$ noethérien.','$S$ \\uline{noethérien}.','paragraph 4, line 1','The adjective noethérien is underlined.')
    r("$E\\otimes E'$, etc., faisant","$E\\otimes E'$ etc. faisant",'last two lines','Neither comma around etc. appears in the print.')
    if tree=='fr':
        r(r'$K$-homomorphismes',r'$k$-homomorphismes','line 2',
          'The common base field is k; K and K-prime are arbitrary extensions of k, so K-prime need not have a K-algebra structure. Restore the justified supplied lowercase k.',
          'misprint of the original')
        r(r"$\mathcal F_{K'}$",r"$\mathcal F'_{K''}$",'line 3',
          'The two sheaves being compared are F and F-prime after extension to the common field K-double-prime. Restore both the sheaf prime and the second prime on the field.',
          'misprint of the original')
        r('Notons que si $X_0$','Notons que si $X$','line 5',
          'Only X has been introduced as the k-prescheme. The zero subscript is undefined here; the supplied X reading is justified.',
          'misprint of the original')
        r(r'$K$-automorphisme',r'$k$-automorphisme','lines 11-12',
          'The fixed field extension is Omega over k; K is a variable field of definition, not a fixed base of this automorphism criterion.',
          'misprint of the original')
        r(r'\mathcal F\otimes_K(\Omega,\sigma)',r'\mathcal F\otimes_\Omega(\Omega,\sigma)','line 12',
          'F is a sheaf on X_Omega and the twist is the base change along the automorphism sigma of Omega. The tensor product therefore uses Omega as its base, not K.',
          'misprint of the original')
        r('ensemble $E_1','ensembles $E_1','paragraph 2, penultimate sentence',
          'The general n-term list requires the plural ensembles; the printed singular breaks agreement.',
          'misprint of the original')
    upright_page(rel,layer,'221-250')

event('221-1-equivalence','carried as background without fault found',
      'Read the common-extension definition. Confirmed the supplied repairs k-homomorphisms and F-prime over K-double-prime: these are required for the two sheaves to be compared on the stated common base. No independent proof of equivalence is claimed.',
      '221, p. 250, lines 1-4')
event('221-1-field-of-definition','carried as background without fault found',
      'Read the finite-type field-of-definition claim; the undefined X-zero is corrected to the previously introduced X. Proof of finite-presentation descent is not supplied by this reading.',
      '221, p. 250, lines 5-10')
event('221-1-universal-field-criterion','carried as background without fault found',
      'Read the algebraically closed universal-field criterion. Its automorphism must fix k and its twist is taken over Omega; these two existing repairs are retained with explicit evidence. No independent proof of the criterion is claimed.',
      '221, p. 250, lines 10-15')
with (ROOT/'CORRECTIONS.tsv').open(newline='') as f:
    counts=Counter((x['layer'],x['kind']) for x in csv.DictReader(f,delimiter='\t') if x['printed_page']=='221-250')
record_page('221',250,
    'Compared both French 221.tex files, entry lines 46-94, with scan leaf 3 at 400 dpi, full page and enlarged top, middle and bottom bands. Read all four paragraphs, the small indices, primes, alphabets, operator underline, four ellipses and punctuation. There is no printed footnote.\n\n'
    'Restored all printed readings in the printed layer, including uppercase K in the two field-homomorphism phrases, the defective second sheaf F_K-prime, X-zero, the tensor subscript K and singular ensemble. The corrected layer retains the justified supplied corrections of those five mathematical places and the grammatical plural. Its earlier explanatory footnote is removed from the exposition and its rationale kept in this record and ledger. Script U, wavy-underlined Tor, straight prose emphasis and upright typed letters are restored in both layers.\n\n'
    'Operation counts: '+ '; '.join(f'{a}, {b}: {n}' for (a,b),n in sorted(counts.items()))+
    '. Printed readings were first restored in both layers before justified emendations were reapplied, so totals include those auditable intermediate operations. Final second reading pending.')
record=read('CHECK_RECORD.md')
needle='| Source quotations |'
pos=record.index(needle)
record=record[:pos]+'| General sheaf operations in exposé 221 | '+chr(96)+r'\mathcal U'+chr(96)+'; '+chr(96)+r'\mathop{\text{\uwave{Tor}}}\nolimits_i'+chr(96)+' | Handwritten script U and wavy-underlined roman Tor on 221-250, distinct from ordinary typed set letters E |\n'+record[pos:]
write('CHECK_RECORD.md',record)
from update_record_counts import update
update()
