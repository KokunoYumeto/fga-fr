from audit_utils import *
from collections import Counter
import csv,re
for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
    rel=f'sources/{tree}/fr/232.tex'
    def r(a,b,line,why,kind='reading',count=1):
        replace(rel,a,b,layer,'232-144',line,'1, (1.4)-(1.5)',
                'Scan leaf 3 at 400 dpi and all three enlarged bands: '+why,kind=kind,count=count)
    for old,new in [('« de nature locale »',r'\fquote{de nature locale}'),
                    ('« familles algébriques »',r'\fquote{familles algébriques}'),
                    ('« Brauer--Severi »',r'\fquote{Brauer-Severi}'),
                    ('« compatible avec la\ndescente fidèlement plate »',r'\fquote{compatible avec la descente fidèlement plate}'),
                    ('« compatible avec la descente fidèlement plate »',r'\fquote{compatible avec la descente fidèlement plate}'),
                    ('« préfaisceau »',r'\fquote{\uline{préfaisceau}}')]:
        r(old,new,'quoted expressions','The ordinary double quotes, short name hyphen, and the underline on préfaisceau are as printed.')
    r('un « faisceau » pour',r'un \fquote{\uline{faisceau}} pour','first sheaf occurrence','The first word faisceau is straight underlined within ordinary quotes.')
    r('un « faisceau »',r'un \fquote{faisceau}','second sheaf occurrence','The second word faisceau has ordinary quotes and no underline.')
    r(r'\emph{préschéma de Picard}',r'\uline{préschéma de Picard}','representing-scheme name','The words are straight underlined.')
    r('$S$ ; donc,','$S$, donc,','representing-scheme sentence','A comma follows S.')
    r(r"\operatorname{Pic}'",r"\mathop{\text{\uwave{Pic}}}\nolimits'",'seven primed Picard signs','The primed functor signs have wavy underlines; the two representing-scheme exceptions and the group exception are restored separately below.',count=8)
    r(r"noté $\mathop{\text{\uwave{Pic}}}\nolimits'_{X/S}$",r"noté $\underline{\operatorname{Pic}}_{X/S}$",'representing scheme in prose','The representing scheme is straight underlined and unprimed.')
    r(r"\operatorname{Hom}_S(S',\mathop{\text{\uwave{Pic}}}\nolimits'_{X/S})",r"\operatorname{Hom}_S(S',\underline{\operatorname{Pic}}_{X/S})",'(1.4), Hom target','The representing scheme is straight underlined and unprimed here too.')
    r(r"=\mathop{\text{\uwave{Pic}}}\nolimits'(X\times_S S'/S').",r"=\operatorname{Pic}'(X\times_S S'/S').",'(1.4), group value','The final relative group is plain Pic prime, without a functor underline.')
    r('localisé ; de\nfaçon précise,','localisé, de\nfaçon précise','failure of descent paragraph','The print has a comma after localisé and no comma after précise.')
    r(r'\mathfrak M',r'(\mathfrak M)','six morphism-class signs','The Gothic class letter is enclosed in parentheses at every occurrence.',count=6)
    r(r'\emph{fidèlement plats et quasi-compacts} ;',r'\uline{fidèlement plats et quasi-compacts},','covering class definition','The defining words are straight underlined and followed by a comma.')
    r(r'(\mathrm{Sch})/S',r'(\text{\uwave{Sch}})/S','two category signs','Sch has a wavy underline inside its parentheses.',count=2)
    r('et, pour tout','et pour tout','covering morphism sentence','There is no comma after et.')
    r(r'\longrightarrow',r'\to','four arrows','The arrows in the text and the first arrow of (1.5) are short.',count=4)
    old="T\\longleftarrow T'\\mathrel{\\substack{\\xleftarrow{\\,\\mathrm{pr}_1\\,}\\\\[-0.35ex]\n\\xleftarrow[\\,\\mathrm{pr}_2\\,]{}}}T'\\times_TT'."
    s,_,_=page_text(rel,144)
    old=old[:-1] if old not in s else old
    new=r"T\leftarrow T'\mathrel{\overset{\mathrm{pr}_1,\ \mathrm{pr}_2}{\substack{\longleftarrow\\[-0.35ex]\longleftarrow}}}T'\times_TT'."
    r(old,new,'projection diagram','The first arrow is short; both projection names occur together above the pair of long left arrows; a full stop closes the display.')
    r(r"le morphisme $u:T'\to T$ appartienne à $(\mathfrak M)$",r"le morphisme $u:T'\to T\in(\mathfrak M)$",'last line','The print puts the membership sign directly after the morphism, without the added words appartienne à.')
    if tree=='fr':
        r(r"$\operatorname{Pic}(X\times_S S'/S')$",r"$\operatorname{Pic}(X\times_S S')$",'absolute groups in the second paragraph','The sentence explicitly concerns absolute Picard groups, defined in (1.1) on the total space. The extra relative /S prime belongs to the restricted relative group and is removed here to restore the stated absolute input.','misprint of the original')
    upright_page(rel,layer,'232-144')
event('232-1.4','targeted proof check','Representability means a natural isomorphism Hom_S(S prime,Pic_{X/S}) with the restricted functor value; substituting (1.3) gives the last term. The print deliberately distinguishes the unprimed straight-underlined representing scheme from the primed wavy-underlined functor, so no prime is added to the scheme name.','232, p. 144, first paragraph and (1.4)')
event('232-1-Brauer-Severi-obstruction','targeted proof check','Take a smooth conic over the real numbers with no real points. Over the complex numbers it is P^1, whose degree-one line-bundle class is invariant under conjugation and therefore equalizes the two pullbacks to C tensor_R C. Every divisor on the real conic has even degree because all its closed points have degree two; hence no real line bundle pulls back to that degree-one class. On a field the restricted relative group is the absolute Picard group, so the fpqc equalizer condition fails for Spec C to Spec R. This proves a concrete instance of the printed Brauer-Severi example.','232, p. 144, second paragraph')
event('232-1.5','used and rechecked in this run','The fpqc descent theorem for morphisms identifies Hom(T,Y) with the equalizer of the two pullbacks from Hom(T prime,Y). In affine charts the ring statement is the faithfully flat equalizer A to B to B tensor_A B; descent and gluing of the charts gives the scheme statement. Thus a representable P satisfies (1.5). Flatness, surjectivity and quasi-compactness are each stable under base change and composition, as required for the stated covering class. The general descent theorem remains the cited background input.','232, p. 144, (1.5) and following paragraph')
event('232-1-associated-sheaf-introduction','carried as background without fault found','The universal associated sheaf for the stated localization is introduced; its proposed explicit construction continues on the next page and is not yet certified here. No local-triviality or finer-topology assumption is silently inserted.','232, p. 144, final paragraph')
with (ROOT/'CORRECTIONS.tsv').open(newline='') as f:
    c=Counter((x['layer'],x['kind']) for x in csv.DictReader(f,delimiter='\t') if x['printed_page']=='232-144')
record_page('232',144,'Compared both French layers, entry lines 51-102, with scan leaf 3 at 400 dpi and all three enlarged bands. Read every paragraph, both numbered displays and the unnumbered projection diagram, including the sentence continued on the next page.\n\nRestored ordinary quotation marks, short name hyphen, printed emphasis and punctuation, the wavy functor and category signs, the unprimed straight-underlined representing scheme, parentheses around the Gothic covering class, the projection-label placement and final full stop, the literal final membership formula, and upright typed letters. Corrected French removes the extraneous relative base from the explicitly absolute Picard group in the second paragraph. Checked the representability identity, supplied a real-conic equalizer obstruction, and rechecked how morphism descent gives (1.5). The associated-sheaf construction remains pending its continuation.\n\nOperation counts: '+'; '.join(f'{a}, {b}: {n}' for (a,b),n in sorted(c.items()))+'. Final row verdicts remain pending.')
from update_record_counts import update
update()
