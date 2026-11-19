from audit_utils import *
from collections import Counter
import csv
dq=chr(96)*2
for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
    rel=f'sources/{tree}/fr/236.tex'
    def r(a,b,line,why,kind='reading',count=1):
        replace(rel,a,b,layer,'236-234',line,'2.7, 2.8',
                'Scan leaf 15 at 400 dpi, full page, three enlarged bands and abbreviation detail: '+why,kind=kind,count=count)
    s,_,_=page_text(rel,234)
    for a,b,body in reversed(list(footnotes(s))):
        r(s[a:b],'','added corollary footnote','The print has no footnote or call.','structure')
    r(r'\result{COROLLAIRE}{2.7} Soit $f:X\longrightarrow S$',
      r'\result{COROLLAIRE}{2.7} Soit $f:X\longrightarrow Y$',
      '2.7 opening arrow','The target letter is Y in the printed arrow.')
    r('la fonction\n\\[\ns\\longmapsto\\dim\\operatorname{Pic}_{X_s/k(s)}\n\\]\nsur',
      'la fonction $s\\rightsquigarrow\\dim\\operatorname{Pic}_{X_s/k(s)}$ sur',
      'dimension function','The assignment is inline and its arrow is wavy.','structure')
    r('i.e.','i. e.','two explanatory abbreviations','Both abbreviations are spaced; the tight crop of the second shows a damaged period rather than a comma.',count=2)
    r('« spécialisée »',dq+"spécialisée''",'remark 2.8','The print uses ordinary double quotation marks.')
    r("D'ailleurs, Serre","D'ailleurs SERRE",'Serre attribution','There is no comma after ailleurs and the name is in capitals.')
    r('morphisme simple $f:',r'morphisme \uline{simple} $f:','smoothness emphasis','Only simple has a straight underline.')
    r('rendu abélien ([4], XI)','rendu abélien, ([4], XI)','second reference','A comma is printed before this parenthetical reference.')
    r(r'\operatorname{Pic}_{X_s/k(s)}^\circ',r'\operatorname{Pic}_{X_s/k(s)}',
      'definition of alpha, mu, lambda','The print has no identity-component superscript here. The dimensions already refer to the named parts.')
    r("les relations connues s'expriment","les relations connues, s'expriment",
      'before inequalities','The print includes a comma after connues.')
    r(r'\operatorname{Pic}',r'\underline{\operatorname{Pic}}',
      'five Picard scheme names','All five names have straight underlines.',count=5)
    r(r'\longrightarrow',r'\to','two structure arrows','Both arrows are short.',count=2)
    r(r'\geq',r'\geqslant','formula (*)','The lower inequality stroke is slanted.')
    r(r'\leq',r'\leqslant','formula (**)','The lower inequality stroke is slanted.')
    if tree=='fr':
        r(r'\result{COROLLAIRE}{2.7} Soit $f:X\to Y$',
          r'\result{COROLLAIRE}{2.7} Soit $f:X\to S$',
          '2.7 opening arrow','The Picard scheme and the following function both use base S, and no Y is defined. The base arrow must therefore end at S. This confirms the existing correction.','misprint of the original')
    upright_page(rel,layer,'236-234')
event('236-2.7','targeted proof check',
      'For a locally finite-type group scheme, geometric translations make every component of a fibre have the identity-component dimension. Upper semicontinuity of local fibre dimension evaluated along the unit section therefore gives the first assertion. Absence of additive parts, 2.5 and its preceding unnumbered corollary give universal openness along the identity locus; the corresponding fibre-dimension theorem gives local constancy. The two dimension theorems are background inputs. This verifies the reduction and the direction of the inequality, and confirms that the printed target Y must be S.',
      '236, p. 234, corollary 2.7 and proof')
event('236-2.8-star','targeted proof check',
      'The unprimed data belong to the special fibre s and the primed data to its generization s prime. The dimension is alpha+mu+lambda, so upper semicontinuity gives the displayed greater-than-or-equal sign in (*). If both endpoint unipotent dimensions vanish, restriction to a trait with those two fibres and the local-constancy conclusion gives alpha+mu=alpha prime+mu prime. Trait reduction and the group-structure decomposition are background inputs; the arithmetic and directions are checked.',
      '236, p. 234, remark 2.8 through equality after (*)')
event('236-2.8-double-star','carried as background without fault found',
      'Read the fundamental-group specialization references [4], X and XI and the prime-to-characteristic torsion-rank expression 2 alpha+mu. The displayed inequality is less-than-or-equal from special to generic, consistent with the injection on prime-to-characteristic H1 induced by proper specialization. The cited specialization, Kummer and Tate-rank results are background here; the qualification and continuation on p. 235 have not yet been read.',
      '236, p. 234, remark 2.8, formula (**)')
with (ROOT/'CORRECTIONS.tsv').open(newline='') as f:
    c=Counter((x['layer'],x['kind']) for x in csv.DictReader(f,delimiter='\t') if x['printed_page']=='236-234')
record_page('236',234,'Compared sources/fr_printed/fr/236.tex and sources/fr/fr/236.tex, entry lines 597-641, with scan leaf 15 at 400 dpi, full page, three enlarged bands and a tight enlarged crop of the second i. e. Read 2.7 and the beginning of 2.8 through (**).\n\nRestored the printed target Y, inline wavy assignment, five straight Picard names, omitted identity superscript, SERRE, the simple underline, punctuation and slanted inequality signs. Removed the editorial footnote. The tight abbreviation crop supports a damaged period, so no comma was introduced. Corrected French alone confirms the original edition correction of target Y to S. Checked the dimension reduction and both inequality directions, while identifying the geometric dimension and fundamental-group results as background. The final inequality continues on the next page.\n\nOperation counts: '+'; '.join(f'{a}, {b}: {n}' for (a,b),n in sorted(c.items()))+'. Final row verdicts remain pending.')
from update_record_counts import update
update()
