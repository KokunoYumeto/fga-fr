from audit_utils import *
from collections import Counter
import csv
for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
    rel=f'sources/{tree}/fr/232.tex'
    def r(a,b,line,why,kind='reading',count=1):
        replace(rel,a,b,layer,'232-158',line,'6.1-6.3',
                'Scan leaf 17 at 400 dpi and three enlarged bands: '+why,kind=kind,count=count)
    notes=list(footnotes(page_text(rel,158)[0])); assert len(notes)==1
    r('\\footnote{'+notes[0][2]+'}','','6.3 parenthesis','No editorial footnote appears in the printed page; its justification is kept in the audit record.','structure')
    r('un schéma somme de schémas','un schéma \\uline{somme} de schémas','first line','Only somme is underlined.')
    r('satisfaisant aux conditions','satisfaisant les conditions','second line','The scan reads les conditions without aux.')
    r(r'\operatorname{Pic}',r'\underline{\operatorname{Pic}}','fourteen Picard names','Restore scheme underlines, then distinguish the three functor names below.',count=14)
    r('foncteurs\n\\[\n\\underline{\\operatorname{Pic}}_{X/S}\\longrightarrow\n\\underline{\\operatorname{Pic}}_{X_1/S}\\times\\underline{\\operatorname{Pic}}_{X_2/S}', 'foncteurs\n\\[\n\\text{\\uwave{Pic}}_{X/S}\\longrightarrow\n\\text{\\uwave{Pic}}_{X_1/S}\\times\\text{\\uwave{Pic}}_{X_2/S}','6.3 first morphism','These three Pic symbols have wavy functor underlines, whereas the final displayed morphism has straight scheme underlines.')
    r(r'\prod_i',r'\prod\limits_i','disjoint-sum formula','The product index is underneath the product sign.')
    r(r'\xrightarrow{\sim}',r'\overset{\sim}{\to}','disjoint-sum formula','The tilde is over a short arrow.')
    r('i.e.','i. e.','two abbreviations','The initials are spaced.',count=2)
    r(r'\mathcal I',r'\mathfrak J','six ideal letters','All six handwritten ideal signs are Gothic J, not script I.',count=6)
    r('est plat sur $S$).','est plat sur $X$).','6.3 explanatory parenthesis','The scan prints X as the base of flatness in this parenthesis.')
    if tree=='fr':
        r('est plat sur $X$).','est plat sur $S$).','6.3 explanatory parenthesis','The parenthesis explains the immediately preceding S-flatness of O_X/(J_1+J_2), which is the structure sheaf of Z. Replace X by S only in corrected French.','misprint of the original')
    r('les homomorphismes\n\\[\nk(s)\\longrightarrow H^0(X_{i,s},\\mathcal O_{X_{i,s}}),\\qquad i=1,2,\n\\]\nsoient', 'les Hom $k(s)\\longrightarrow H^0(X_{i_s},\\mathcal O_{X_{i_s}})$,\n$i=1,2$, soient','6.3 fibre-cohomology maps','Hom is the printed prose abbreviation; the map and indices are inline, and s sits below i in both nested fibre subscripts.','structure')
    r(r'\longrightarrow',r'\to','five morphisms','All arrows are short.',count=5)
    upright_page(rel,layer,'232-158')
event('232-6.1-disjoint-sum','independent re-proof','An invertible sheaf on a finite disjoint union is precisely a tuple of invertible sheaves on the components; the equivalence is compatible with pullback. Sheafifying the relative Picard groups removes the base-line-bundle ambiguity on each component, so the Picard sheaf is the finite product, and Yoneda gives the displayed product of representing schemes. Finiteness is supplied locally by the projective finite-type setting of 6.1.','232, p. 158, first paragraph and display')
event('232-6.2','targeted proof check','For a geometric fibre that is locally integral and noetherian, its irreducible components are disjoint and open, so its connected components are integral. The proper flat geometrically reduced Stein-factor theorem gives a finite etale S-prime over S and a flat map with these connected geometric fibres. Thus the hypotheses of 6.1 are met. The Stein-factor theorem and descent of the section-3 structure under finite etale restriction of scalars are identified background inputs.','232, p. 158, corollaire 6.2 and following paragraph')
event('232-6.3-flatness-base','targeted proof check','The quotient O_X/(J_1+J_2) defines the scheme-theoretic intersection Z. Its explicitly assumed flatness over S is therefore exactly Z-flatness over S. Flatness of Z over X would instead impose a different closed-immersion condition and is not equivalent: the intersection point of two transverse projective lines is flat over the ground field but not flat over their union. Retain printed X only in the as-printed layer and use S in corrected French.','232, p. 158, proposition 6.3, explanatory parenthesis')
event('232-6.3-preliminary-reductions','targeted proof check','The exact sequence 0 to O_X to O_X1 plus O_X2 to O_Z to 0, together with the stated flatness, makes X flat over S and preserves the union/intersection diagram under base change. The proof opening tacitly separates the case Z empty: since Z is proper, flat and finitely presented, its image is open and closed. On its complement the union is disjoint and the preceding product formula applies; on its image, Z to S is an fpqc cover and its own base change supplies the asserted section. This routine omitted case is explained in the record without rewriting the proof. The rigidification reference is to 2.5 as printed. The main gluing argument continues on p. 159.','232, p. 158, proposition 6.3 and last paragraph')
with (ROOT/'CORRECTIONS.tsv').open(newline='') as f:
    c=Counter((x['layer'],x['kind']) for x in csv.DictReader(f,delimiter='\t') if x['printed_page']=='232-158')
record_page('232',158,'Compared both French layers, entry lines 744-799, with scan leaf 17 at 400 dpi and three enlarged overlapping bands. Read the disjoint-sum example, all of 6.2, all of the 6.3 statement and the proof opening through Module inversible.\n\nRestored somme emphasis, exact les conditions, eleven straight and three wavy Picard names, product index, short arrows, six Gothic J ideals, the inline abbreviated Hom sentence and nested fibre subscripts. Removed the unprinted explanatory footnote. The printed flatness base X in the parenthesis is preserved diplomatically and corrected to S by the preceding quotient condition. Checked disjoint unions, the reduction in 6.2 and the preliminary flatness/section reductions in 6.3, explicitly treating empty Z in the record. The remaining gluing proof is pending its next page.\n\nOperation counts: '+'; '.join(f'{a}, {b}: {n}' for (a,b),n in sorted(c.items()))+'. Final row verdicts remain pending.')
from update_record_counts import update
update()
