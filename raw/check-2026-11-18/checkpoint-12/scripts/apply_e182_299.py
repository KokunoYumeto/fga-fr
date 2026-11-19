from audit_utils import *
from collections import Counter
import csv
dq=chr(96)*2
for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
    rel=f'sources/{tree}/fr/e182.tex'
    def r(a,b,line,why,kind='reading',count=1):
        replace(rel,a,b,layer,'e182-299',line,'Errata, pages 12-23; later developments',
                'Scan leaf 3 at 400 dpi, full page and three enlarged bands: '+why,kind=kind,count=count)
    for title in ['Page 12, et page 14, remarque 1','Page 15, remarques 2 et 3','Page 16, ligne 3','Page 23, ligne 12, 1\\textsuperscript{re} ligne du corollaire\n5']:
        r(r'\textbf{'+title+'.}',r'\uline{'+title+'}.','four entry headings',
          'The entry heading is ordinary upright type with a straight underline.','typesetting')
    r(' --- ',' - ','entry and bibliographic separators','The dashes are short.',count=5)
    for old,new,n in [('Serre','SERRE',2),('Mumford','MUMFORD',2),('Hironaka','HIRONAKA',1),('Koizumi','KOIZUMI',1),('Igusa','IGUSA',1),('Ogg','OGG',1),('Šafarevič','ŠAFAREVIČ',1),('Artin','ARTIN',1)]:
        r(old,new,'attributions','The surname is printed in uppercase.',count=n)
    r('une surface projective',r'une \uline{surface} projective','surface example','Only surface has a straight underline.')
    r('nulle.\\footnote{','nulle \\footnote[2]{','note call','The printed note number is 2, before the period.')
    r('108--109.} MUMFORD','108-109.}. MUMFORD','footnote ending','The range dash is short and the main-text period follows the note call.')
    r('\\emph{Proc. Nat.\nAcad. Sc. U.S.A.}','Proc. Nat.\nAcad. Sc. U. S. A.','footnote journal',
      'The journal abbreviation is upright, with separated U., S. and A.','typesetting')
    r('(cf. SHMI)','(Cf. \\uwave{SHMT})','moduli reference','The last letter is T, not I; Cf. has a capital C and SHMT a wavy underline.')
    r('« ',dq,'three quotations','The print uses ordinary double quotation marks.',count=3)
    r(' »',"''",'three quotations','The print uses ordinary double quotation marks.',count=3)
    r(r'\mathbf Z',r'\text{\uwave{Z}}','integer base','The letter Z has a wavy underline, not bold weight.')
    r(r'1\textsuperscript{re}','1re','corollary locator','The letters re are on the baseline.')
    r('§§','§','two section ranges','The print has a single section sign.',count=2)
    r('EGA III',r'\uwave{EGA} III','EGA reference','The abbreviation is wavy-underlined.')
    r('SGA ',r'\uwave{SGA} ','three SGA references','Only the abbreviation is wavy-underlined.',count=3)
    r('(cf. théorème 14)','(Cf. théorème 14)','theorem reference','The capital C is printed.')
    r('caractéristique quelconque ;','caractéristique quelconque,','first application','The item ends with a comma.')
    r('quelconque ;','quelconque,','second application','The item ends with a comma.')
    if tree=='fr':
        r("d'un schéma propre sur un anneau","d'un schéma propre et plat sur un anneau",
          'non-liftability assertion','Without flatness the assertion is false: every proper k-scheme X is itself proper over a mixed-characteristic DVR R with residue k, by composition with the closed immersion Spec k into Spec R, and its reduction is X. For instance take R=W(k) for perfect k. Its generic fibre is empty and multiplication by p kills its structure sheaf. A lifting must be required flat; this qualification removes that counterexample. The existence of the non-liftable Serre example is retained as a cited background result.','misprint of the original')
    upright_page(rel,layer,'e182-299')
    r('\\src{299}\n','\\src{299}\n\\begingroup\n\\makeatletter\n\\renewcommand\\@makefnmark{\\hbox{\\normalfont(\\textsuperscript{\\@thefnmark})}}\n\\makeatother\n',
      'note-call formatting','The note marker has baseline parentheses around a raised numeral; the override is page-local.','typesetting')
    r("des variétés algébriques.\n","des variétés algébriques.\n\\endgroup\n",
      'end of note-call formatting','Close the local note-formatting group without changing text.','typesetting')
event('e182-nonliftable-printed','refuted, with the refined statement\'s id',
      'Refined statement e182-nonliftable-flat. The printed sentence omits flatness: for any proper k-scheme X and mixed-characteristic DVR R with residue k, the composite X to Spec k to Spec R is proper and has special fibre X. It therefore contradicts the literal assertion of no proper model. Such a model is not flat and has empty generic fibre. R=W(k) supplies a base for perfect k; existence of the Witt ring is a background input, while the proper-composition counterexample is checked directly.',
      'Erratum 182, p. 299, Page 12, et page 14, remarque 1')
event('e182-nonliftable-flat','targeted proof check',
      'Added et plat in corrected French only. Over a mixed-characteristic DVR, the false countermodel has p-torsion, whereas flatness implies p acts injectively. This verifies the necessary qualification and removes the counterexample. The claimed Serre threefold and the tentative Mumford surface are not constructed or independently verified here.',
      'Erratum 182, p. 299, first paragraph')
for sid,result,loc in [
    ('e182-rem2-3','Read the author\'s reduced optimism and the assertions about Hironaka\'s projective-space result and Koizumi\'s abelian-variety result. The page provides neither proof nor precise publication locator; retain these as dated reports.','Page 15, remarques 2 et 3'),
    ('e182-th10-moduli','Read the moduli-scheme existence report and the asserted consequence of theorem 10 for Jacobi schemes of level n. Representability, the precise level convention and the smoothness inference are background dependencies; no independent construction is supplied on this page.','Page 16, ligne 3'),
    ('e182-cor5-addition','Read the instruction to add properness of X or Y to corollary 5. Preserve the instruction in the erratum and do not merge it into the exposé. The product fundamental-group theorem remains a background dependency for the notes.','Page 23, ligne 12'),
    ('e182-th14-applications','Read the publication-status paragraph, all EGA/SGA references, and the three reported uses of the corollary to theorem 14 by Igusa, Ogg/Šafarevič and Artin. These are reported applications, not proofs rechecked here.','final four paragraphs')]:
    event(sid,'carried as background without fault found',result,'Erratum 182, p. 299, '+loc)
with (ROOT/'CORRECTIONS.tsv').open(newline='') as f:
    c=Counter((x['layer'],x['kind']) for x in csv.DictReader(f,delimiter='\t') if x['printed_page']=='e182-299')
record_page('e182',299,'Compared sources/fr_printed/fr/e182.tex and sources/fr/fr/e182.tex, entry lines 18-62, with scan leaf 3 at 400 dpi, full page and three enlarged bands. Read all four errata, the later-publication paragraph, the three applications and footnote 2. Restored headings and surface emphasis, uppercase names, ordinary quotations, wavy abbreviations/Z, SHMT, baseline 1re, single section signs, commas, short dashes, upright variables and exact footnote number/placement.\n\nThe as-printed layer retains the absence of flatness in the non-liftability assertion. Corrected French adds et plat: otherwise any proper special-fibre scheme, viewed over the mixed-characteristic base through its closed point, is a counterexample. The necessity is checked; the actual non-liftable constructions and other cited results remain background. All errata remain separate from the exposé.\n\nOperation counts: '+'; '.join(f'{a}, {b}: {n}' for (a,b),n in sorted(c.items()))+'. Final row verdicts remain pending.')
from update_record_counts import update
update()
