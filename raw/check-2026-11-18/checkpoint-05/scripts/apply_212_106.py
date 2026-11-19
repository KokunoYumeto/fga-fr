from audit_utils import *

for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
 rel=f'sources/{tree}/fr/212.tex'
 with (ROOT/'CORRECTIONS.tsv').open(newline='') as ledger:
  prior_operations={(row['old'],row['new']) for row in csv.DictReader(ledger,delimiter='\t') if row['file']==rel and row['printed_page']=='212-106'}
 def r(a,b,line,kind='reading',why='',count=1):
  if (a,b) in prior_operations:
   return
  replace(rel,a,b,layer,'212-106',line,'4. Category and groupoid structures','400-dpi full scan and all three enlarged bands. '+why,kind,count=count)
 for term in ['application-source','application-but','application-composition','symétrie','catégorie','groupoïde','morphisme-source','morphisme-but']:
  r(r'\emph{'+term+'}',r'\uline{'+term+'}','defined '+term,why='The scan emphasizes the term with a straight underline.')
 r(r'\longrightarrow',r'\to','composition and symmetry arrows',count=2,why='Ordinary-length printed arrows.')
 r('(nécessairement unique) rendant commutatifs','(nécessairement unique) rend commutatifs','identity-map sentence',why='The print has rend, not the supplied participle rendant. This compressed wording is retained in both layers.')
 r("s'écrivent:", "s'écrivent :",'symmetry equations introduction',why='The printed colon has a preceding space.')
 r(r'\guillemotleft variant fonctoriellement\guillemotright{}',r'\fquote{variant fonctoriellement}','functoriality quotation',why='The scan has ordinary double quotation marks.')
 r(r'$\mathcal C$:',r'$\mathcal C$ :','internal-category definition colon',why='A space precedes the colon after C.')
 s,_,_=page_text(rel,106)
 r(r'\mathcal C',r'\text{\uwave{C}}','category letters',count=s.count(r'\mathcal C'),why='The category letters have a wavy underline. Plain objects R and X retain their upright typed alphabet.')
 r('\\[\n  p_1,p_2:R\\rightrightarrows X\n\\]',r'''\[
  \symup{p_1,p_2:R\rightrightarrows X}
\]''','first and last double-arrow displays',count=2,why='Both identical printed displays have upright typed mathematical letters. This explicit repeated replacement also recovers the interrupted generic typography pass before any page record was appended.')
 upright_page(rel,layer,'212-106')

event('212-4-category-axioms','targeted proof check','With p1 source and p2 target, the displayed fibre product consists of (a,b) with target(a)=source(b), and pi(a,b)=b after a. Its source and target are p1(a), p2(b). Associativity is pi(pi(a,b),c)=pi(a,pi(b,c)); the unit laws are pi(D p1(a),a)=a and pi(a,D p2(a))=a. These imply uniqueness of each identity arrow by composing two candidates, and p1 D=p2 D=id_X as printed. The written rend is retained; the intended diagrammatic unit requirement is made explicit in this audit argument.','212, p. 106, conditions (i)–(ii) and identity paragraph')
event('212-4-inverse-axioms','targeted proof check','The four inverse conditions are p1 s=p2, p2 s=p1, pi(a,s(a))=D p1(a), and pi(s(a),a)=D p2(a), using the displayed composition order. The first two make the last two composites defined, and the last two say that s(a) is a two-sided inverse; uniqueness follows by associativity and the unit laws. The scan distinctly uses Latin D for identities and later a triangular Delta in the phrase about forming diagrams. Delta could denote the ordinary diagonal used to form (id,s) and (s,id), rather than a mistaken replacement for D. Since that reading is coherent, the two symbols are retained in both layers and no unsupported emendation is made.','212, p. 106, symmetry paragraph and two equations')
event('212-4-internal-category','targeted proof check','A functorial category on the sets X(T),R(T) gives natural source and target maps, hence arrows R to X by Yoneda. Natural identities and, for a groupoid, inverses similarly give X to R and R to R. If the composable-arrow fibre product exists, its T-points are exactly the composable pairs, so natural composition is represented by the stated morphism. The axioms hold as morphism identities because Hom(T,-) detects equality. Conversely these identities induce the prescribed set-theoretic categories for every T.','212, p. 106, final paragraph')
record_page('212',106,r'''Compared sources/fr_printed/fr/212.tex and sources/fr/fr/212.tex entry lines 316–365 with scan leaf 9 at 400 dpi, full page and all three enlarged bands. Inspected the order (R,p_2) times_X (R,p_1), every index in the identity and symmetry equations, Latin D versus the later triangular Δ, all arrows and emphasis, and the reference ([2], A, §1).

Both layers restore straight underlines, wavy category letters, ordinary arrows and quotes, the literal rend in the identity-map sentence, spacing before colons and upright mathematical letters. D and Δ are both retained as printed: the latter can denote the ordinary diagonal in forming the inverse diagrams, so replacing it by D is not forced. There is no mathematical difference between the two layers on this page.

Wrote out the omitted source/target, associativity, unit and inverse identities with the printed order of composition, checked uniqueness, and verified the internal-category formulation by Yoneda.''')
from update_record_counts import update
update()
