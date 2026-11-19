from audit_utils import *
for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
 rel=f'sources/{tree}/fr/182.tex'
 def r(a,b,line,statement='',kind='reading',why='',count=1,full=False):
  replace(rel,a,b,layer,'182-209',line,statement,'400-dpi scan, full page and all three enlarged bands. '+why,kind,count=count,full=full)
 r('\\src{210}\n','','page boundary','8','structure','The page ends within the opening covering definition, before de X si.',full=True)
 r('ramifié de $X$ si','ramifié\n\\src{210}\nde $X$ si','last line','8-def-cover','structure','Move marker 210 to the printed boundary; the three defining conditions remain for page 210.',full=True)
 txt,_,_=page_text(rel,209)
 r(r'\Theta',r'\mathfrak G','three derivation sheaves','7-thm10',why='All three handwritten derivation symbols are Gothic G.',count=txt.count(r'\Theta'))
 r(r'\Osh','O','algebraization paragraph','7-thm10',why='The structure sheaf O is plain.')
 r(r'A\longmapsto F(A)',r'A\longrightarrow F(A)','opening functor notation','7',why='The printed arrow has no vertical mapsto bar.')
 r('Kodaira--Spencer','KODAIRA-SPENCER','parenthetical analytic comparison','7-thm10',why='The names are uppercase with a short hyphen.')
 r('Lang--Serre','LANG-SERRE','section 8 introduction','8',why='The names are uppercase with a short hyphen.')
 r('condition\nsuffisante (bien','condition\n\\uline{suffisante} (bien','opening sufficient condition','7',why='Only suffisante is underlined here.')
 if tree=='fr_printed':
  r('supposé propre sur $k$. De façon','supposé propre sur $k$,. De façon','first paragraph, second line','7',why='The scan has both a comma and a period after k. Corrected French retains the grammatical single period.')
  r(r'contre que la condition $H^0(X_0,\mathfrak G_{X_0/k})=0$',r'contre que la condition $H^0(X,\mathfrak G_{X_0/k})=0$','first paragraph, H^0 condition','7-thm10',why='The printed first argument is unindexed X. Corrected French retains X_0, the space supporting the derivation sheaf, as also written in Theorem 10 below.')
 r('H^2(X_0,\\mathfrak G_{X_0/k})=0.\n\\]','H^2(X_0,\\mathfrak G_{X_0/k})=0\n\\]','Theorem 10 display','7-thm10',why='There is no period at the end of the displayed equality.')
 txt,_,_=page_text(rel,209);marker=r'\result{THÉORÈME}{10} ';a=txt.index(marker)+len(marker);b=txt.index('\n\n',a);old=txt[a:b]
 parts=re.split(r'(\\\[.*?\\\]|\(i\.e\..*?\))',old,flags=re.S)
 new=''.join(x if i%2 else underline_prose(x) for i,x in enumerate(parts))
 r(old,new,'Theorem 10 prose','7-thm10',why='Statement prose is underlined, including simple, but the explanatory parenthesis and mathematics are not.')
 r(r'\fsection{8}{Application au groupe fondamental}',r'\fsection{\normalfont8}{\normalfont\uline{Application au groupe fondamental}.}','section 8 heading','8',why='The number and heading are roman; the title is underlined, with final period outside the underline.')
 r('appelé un revêtement non\nramifié','appelé un \\uline{revêtement non\nramifié}','covering definition, last line','8-def-cover',why='Only the defined phrase is underlined on this page.')
 upright_page(rel,layer,'182-209')
event('182-7-thm10','targeted proof check','Conditional on the preceding deformation calculations, let d=dim_k H^1(G), finite by properness, and R=k[[t_1,...,t_d]]. Choose the first-order universal class via a basis of H^1; H^2=0 lifts it successively to R/m^(n+1). For an Artin small extension with kernel I killed by the maximal ideal, lifts of a ring map form a torsor under Hom(m_R/m_R^2,I), and lifts of its deformation form a torsor under H^1(G) tensor I. The chosen first-order class identifies these torsors. H^0=0 makes augmented automorphisms trivial by induction, so forgetting a chosen reduction does not create ambiguity. Induction on Artin length therefore gives a bijection Hom(R,A)=F(A), proving the stated regular prorepresenting ring using the earlier obstruction theory. Formal-limit existence is used as background.','182, p. 209, Theorem 10')
event('182-7-h0-condition','targeted proof check','Corrected French retains X_0 in the opening H^0 condition: G_{X_0/k} is a sheaf on X_0, and Theorem 10 directly below writes that space correctly. The claim that H^0=0 is not necessary has the simple check X_0=P^1: its augmented deformation functor is constant by H^1(T)=0, hence represented by k, although H^0(T) is nonzero. General sufficiency without H^2=0 is stated as plausible in the historical text and not independently proved here.','182, p. 209, paragraph before Theorem 10')
event('182-7-algebraization','targeted proof check','The algebraization assertion applies Theorem 4 to the formal universal family and H^2(O)=0 to lift an ample bundle. For a proper smooth curve, projectivity and vanishing coherent H^2 supply the hypotheses. The wider Picard-construction programme is read as an announced application, not as a proved theorem on this page.','182, p. 209, paragraphs after Theorem 10')
record_page('182',209,r'''Compared sources/fr_printed/fr/182.tex and sources/fr/fr/182.tex entry lines 777–835 with scan leaf 18 at 400 dpi, full page and enlarged top, middle and bottom bands. Read the representability discussion, Theorem 10 and its applications, section 8's introduction, and the start of the covering definition. Moved marker 210 before de X si and reserved all three defining conditions for the following page.

Restored Gothic G, plain structure O, the ordinary arrow in A to F(A), uppercase hyphenated names, selective underlining, the unpunctuated Theorem 10 display, and the exact section heading. Printed French restores the extra comma before the first period and the missing zero subscript in the introductory H^0 space. Corrected French retains the grammatical period and X_0, justified by the sheaf's base and the correctly indexed theorem immediately below. Checked Theorem 10 by induction on Artin extensions using the previous obstruction/torsor results, explicitly separating the formal-limit background. Also checked the projective-line example showing H^0=0 is not necessary.''')
p='CHECK_RECORD.md';t=read(p).replace('## Open reading questions','- 182-209, representability discussion: retained X_0 rather than printed X as the space in the H^0 vanishing condition.\n\n## Open reading questions');write(p,t)
from update_record_counts import update
update()
