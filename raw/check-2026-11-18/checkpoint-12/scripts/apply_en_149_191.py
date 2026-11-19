from audit_utils import *
from translation_edits import *
from update_record_counts import update
rel='sources/en/en/149.tex';page='149-191'
def ch(old,new,where,why,kind='terminology',count=1):
    replace(rel,old,new,'English',page,where,'Contraction / Theorem 6',
      'French 149-191 and the personally inspected full 400-dpi page and enlarged top, middle and bottom bands: '+why,kind=kind,count=count)
ch('\\footnote{The printed text has\n$H^{p}(H^{q}(X,K))$; the initial term is that of the spectral sequence (8.2),\nnamely $H^{p}(X,H^{q}(K))$.}', '',
   'last paragraph','Withdraw the unprinted note: it incorrectly identifies this other hypercohomology spectral sequence with (8.2). Termwise duality uses H^p of the complex H^q(X,K).',kind='reading')
ch('$H^{p}(X,H^{q}(K))$','$H^{p}(H^{q}(X,K))$',
   'last paragraph','Restore the meaningful printed expression and corrected French. Here H^q(X,K) is the complex of cohomology groups of the locally free terms, and the outside H^p is its cohomology.',kind='reading')
align_math(rel,'en','149',191,[(i,i) for i in range(28)],(28,28))
ch('arguments $\\symup{B_j}$:','arguments $\\symup{B_j}$;',
   'opening','Restore the printed semicolon.',kind='structure')
ch('is a locally free sheaf, it may be removed','is a locally free sheaf, then one may remove it',
   'after (8.4)','Restore alors on peut.')
ch('); there is an analogous calculation rule','); one has an analogous calculation rule',
   'after the dual definition','Restore on a.')
ch('In particular, an argument\nequal to $\\symup{\\Osh_X}$ may always be removed.',
   'In particular, one may always remove an argument\nequal to $\\symup{\\Osh_X}$.',
   'unit argument','Restore on peut toujours.')
ch('where it is immediate; one may','where it is immediate: one may',
   'after (8.5)','Restore the source colon.',kind='structure')
ch('Successively applying a tensor composition\n(8.3) and contractions (8.4) to the repeated arguments gives a pairing',
   'By successively applying a tensor composition\n(8.3) and contractions (8.4) to the repeated arguments, one obtains a pairing',
   'before (8.6)','Restore on obtient.')
ch('is a complex of locally free\ncoherent algebraic sheaves',
   'is a complex of \\uline{locally free}\ncoherent algebraic sheaves',
   'Theorem 6 proof','Restore the printed emphasis on locally free.')
ch('This is seen by using','One sees this by using','last paragraph','Restore on le voit.')
t=page_text(rel,191)[0];start=r'\result{THEOREM}{6} ';old=t.split(start,1)[1].split('\n\n',1)[0]
ch(old,underline_prose(old),'Theorem 6 assertion','Restore printed underlined assertion prose, excluding (8.6).')
record_translation_page('en','149',191,rel,
    'Read contraction (8.4), locally free argument rules, (8.5), the pairing (8.6), Theorem 6 and (8.7). Rejected the English editorial substitution of the spectral-sequence term and removed its explanatory footnote: the printed H^p(H^q(X,K)) is meaningful and appropriate here. Approved all 28 mathematical correspondences, including the first B_j versus subsequent B_i, the hatted omitted letters and the continuation dash in (8.4). Restored theorem and locally-free emphasis, source punctuation and impersonal forms.',(1185,1248))
event('en-149-spectral-sequence-editorial-note','refuted, with the refined statement\'s id',
    'The English note calls H^p(H^q(X,K)) a misprint and substitutes the different spectral sequence H^p(X,H^q(K)). This is unjustified: for the bounded locally free complex in this construction, H^q(X,K) denotes the termwise cohomology complex, whose H^p is the second spectral-sequence term. Termwise Serre duality is precisely the argument used here. Refined statement: en-149-theorem6-spectral-proof.',
    '149, p. 191, last paragraph and removed English footnote')
event('en-149-theorem6-spectral-proof','targeted proof check',
    'For a bounded complex of locally free coherent sheaves, termwise Serre duality pairs H^q(X,K^a) with H^(n-q)(X,(K^a)^dual tensor Omega^n). The dual complex reverses a, so total complementary degrees are d and n-d. Duality of the finite spectral sequences passes to their abutments and gives (8.7); inserting the bounded Hom/tensor complex of (8.1) gives (8.6). This verifies the printed spectral-sequence order. Boundedness comes from the finite resolutions under discussion; no assertion about arbitrary unbounded complexes is added.',
    '149, p. 191, Theorem 6 and (8.7)')
event('en-149-8.4-8.5','used and rechecked in this run',
    'Checked the contraction removal of exactly one contravariant and one covariant argument, and the locally free dual A_i-prime. In (8.5), tensoring by the locally free arguments leaves only one possibly non-flat covariant argument, so the bounded resolution reduces to the stated ordinary tensor sheaf and its cohomology. General tensor-calculus sign compatibilities remain background.',
    '149, p. 191, (8.4)–(8.5)')
update()
