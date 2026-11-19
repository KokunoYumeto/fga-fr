from audit_utils import *
for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
 rel=f'sources/{tree}/fr/190.tex'
 def r(a,b,line,kind='reading',why='',count=1):
  replace(rel,a,b,layer,'190-326',line,'B.6','400-dpi full scan and three enlarged bands. '+why,kind,count=count)
 r("\\[\n  S'\\longmapsto\\operatorname{Hom}_S(S',G)\n\\]","$S'\\longrightarrow\\operatorname{Hom}_S(S',G)$",'representable group functor',kind='structure',why='The formula is inline, and the printed arrow has no mapsto bar.')
 r("\\[\n  \\operatorname{Gl}(n)(S')\n  =\\operatorname{Gl}\\bigl(n,H^0(S',\\mathcal O_{S'})\\bigr)\n\\]","$\\operatorname{Gl}(n)(S')=\\operatorname{Gl}(n,H^0(S',\\mathcal O_{S'}))$",'general linear group formula',kind='structure',why='The entire identity runs inline.')
 for old,new,line in [
  ('du A, paragraphe 4.e.','du A, paragraphe 4, (e).','cross-reference'),
  ('« trivial »',r'\fquote{trivial}','trivial object'),
  ('convenable de $S$ ; (ii)','convenable de $S$, (ii)','three-part argument'),
  ('« formellement »',r'\fquote{formellement}','conclusion'),
  ('« revient\nau même »',r'\fquote{revient au même}','equivalence wording'),
  ('équivalence de catégories fibrées.)',r'\uline{équivalence de catégories fibrées}).','underlined equivalence'),
  ('Tout fibré principal homogène de groupe\n$\\operatorname{Gl}(n)_S$ est localement trivial.',r'\uline{Tout fibré principal homogène de groupe} $\operatorname{Gl}(n)_S$ \uline{est localement trivial}.','Proposition 6.1'),
  ('alors tout fibré','alors \\uline{tout} fibré','subgroup consequence'),
  ('« groupes linéaires »',r'\fquote{groupes linéaires}','linear-group terminology'),
  ('question de Serre (loc. cit.).','question de SERRE (loc. cit.).','first historical reference'),
  ('ce qui résout en particulier une autre question de Serre (loc.\ncit., p. 1--14)','ce qui résout en particulier, une autre question de SERRE (loc.\ncit. 1-14)','second historical reference'),
  ('descente à la Cartier','descente à la CARTIER','Cartier name'),
  ('plat non fini.','plat \\uline{non fini}.','final qualification')]:
  r(old,new,line,why='Restore the printed wording, capitalization, quotation marks, punctuation or selective underline.')
 r(r'\mathcal O',r'\text{\uwave{O}}','two structure sheaves',count=2,why='Ordinary O with a wavy underline.')
 upright_page(rel,layer,'190-326')
event('190-6.1','targeted proof check','For a rank-n locally free sheaf E, the frame scheme Isom(O^n,E) is obtained by gluing GL_n on local trivializations and is an affine fpqc right GL_n-torsor. Conversely descend the standard rank-n representation along a trivializing fpqc cover of a torsor, using B.1; the same transition matrices give E. Frames of the descended E recover the original torsor by descent of their local equivariant isomorphisms, and equivariant maps recover the sheaf isomorphisms. This proves the asserted equivalence of fibered groupoids and local triviality in Proposition 6.1. The preliminary automorphism identification uses left translations of a right trivial torsor, with the same multiplication order as matrices.','190, p. 326, opening paragraph and Proposition 6.1')
event('190-B6-SL-Sp','targeted proof check','An SL_n-torsor gives a rank-n bundle with a generator of its determinant. Locally choose a basis and multiply one vector by the inverse determinant unit to make its volume the given generator. For Sp, a nondegenerate alternating form locally has a unit pairing entry; choose a hyperbolic pair, split its orthogonal complement, and induct. This works also in characteristic two because alternating, rather than merely skew-symmetric, is required. Products are trivialized on intersections of the finitely many local trivializations.','190, p. 326, paragraph after Proposition 6.1')
event('190-B6-closed-subgroup','targeted proof check','For an F-torsor P with F a closed flat subgroup of GL_n, form the extended GL_n-torsor by affine effective descent. Locally it is trivial by Proposition 6.1. Its F-reduction then identifies P with the pullback of GL_n to GL_n/F along the corresponding quotient-valued section (inversion exchanges a left-coset convention if needed). A finite faithfully flat, or finite etale surjective, trivializing cover of the universal F-torsor pulls back to one of P. Thus the stated isotriviality implication follows under the printed existence and trivialization assumptions on the quotient.','190, p. 326, closed-subgroup implication')
event('190-B6-classical-isotriviality','carried as background without fault found','The claims that the classical groups mentioned satisfy the quotient hypotheses, and that isotrivial torsors for the smooth groups described are strictly isotrivial, require quotient existence and finite etale quasi-section results. Those general results have not been independently reproved here. Cartier descent itself is along a finite locally free cover in the preceding example, so its output is isotrivial by the definition on 325. The historical references and the final remark about effectivity are reserved for the notes.','190, p. 326, final two paragraphs and Remark')
record_page('190',326,r'''Compared sources/fr_printed/fr/190.tex and sources/fr/fr/190.tex entry lines 1391–1445 with scan leaf 29 at 400 dpi, full page and all three enlarged bands. Read the two opening formulas, all group subscripts, the quotient and fiber product, Proposition 6.1 and both historical references.

Restored both formulas inline, the ordinary arrow, wavy O, the exact section reference, selective underlines, double quotes, SERRE/CARTIER capitals, parenthesis punctuation, the comma in the three-part argument and the short page-range dash. No new mathematical difference between the French layers was introduced.

Checked the frame-bundle equivalence and Proposition 6.1 by explicit mutually inverse descent constructions. Checked the SL and Sp consequences by choosing volume-one and symplectic bases, and the closed-subgroup consequence by extension of structure group and pullback of the quotient torsor. The broad classical-group existence and strict-isotriviality assertions remain background inputs; their full proofs are not claimed here.''')
from update_record_counts import update
update()
