from audit_utils import *
for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
 rel=f'sources/{tree}/fr/149.tex'
 def r(a,b,line,statement='',kind='reading',why='',count=1):
  replace(rel,a,b,layer,'149-181',line,statement,'400-dpi image, three enlarged bands and tight heading/final-line/Kunneth crops. '+why,kind,count=count)
 old="""tels que
\\[
  Z\\times(a)=(X\\times(a)).U,
  \\qquad
  Z'\\times(b)=(X\\times(b)).U.
\\]
Alors on a"""
 new="""tels que
$Z\\times(a)=(X\\times(a)).U$, $Z'\\times(b)=(X\\times(b)).U$.
Alors on a"""
 r(old,new,'Corollary 1, lines 4–6','4-cor1','structure','The two fiber-cycle identities run in the statement; only its conclusion is displayed.')
 if tree=='fr_printed':
  r(r"$Z'\times(b)=(X\times(b)).U$",r'$Z\times(b)=(X\times(b)).u$','Corollary 1, line 5','4-cor1',why='The second identity has Z without a prime and a lowercase u. Corrected French keeps the separately introduced Z prime and the cycle U.')
 # Both printed statements use underlined prose, without underlining variables.
 txt,_,_=page_text(rel,181);start=txt.index(r'\result{COROLLAIRE}{1} ')+len(r'\result{COROLLAIRE}{1} ');stop=txt.index(r'\[',start);old=txt[start:stop]
 r(old,underline_prose(old),'Corollary 1 prose','4-cor1',why='Restore statement emphasis over prose only.')
 r(r'\emph{classe fondamentale}',r'\uline{classe fondamentale}','point-class definition','4',why='The defined term is underlined.')
 r('généralité.)','généralité).','Remark','4-rem',why='The period follows the parenthesis.')
 r('plus bas.)','plus bas).','after Theorem 2','5-thm2',why='The period follows the parenthesis.')
 r(r'\fsection{5}{Le théorème de dualité}',r'\fsection{\normalfont5}{\normalfont\uline{Le théorème de dualité}.}','section heading','5',why='The heading is underlined with a final period.')
 txt,_,_=page_text(rel,181);start=txt.index(r'\result{THÉORÈME}{2} ')+len(r'\result{THÉORÈME}{2} ');stop=txt.index('\n\n',start);old=txt[start:stop]
 r(old,underline_prose(old),'Theorem 2','5-thm2',why='Restore prose underlining in the theorem statement.')
 r('$k$',r'$\underline{k}$','penultimate line','5',why='The base-field k is visibly underlined.')
 if tree=='fr_printed':
  r('ne semble pas résulter','ne semble par résulter','Remark, penultimate line','4-rem',why='The print reads par; corrected French retains pas, which completes the negation.')
  r(r'\uline{Le théorème de dualité}',r'\uline{La théorème de dualité}','section heading','5',why='The tight crop clearly reads La, not Le. Corrected French retains masculine agreement with théorème.')
  r(r'identifier $H^{n}(X,\Omega_X^{n})$ au corps',r'identifier $H^{n}(X,\Omega_X^{n})$. au corps','penultimate line','5',why='A stray full stop separates identifier its object from au corps; corrected French omits it.')
  r('Considérons maintenant les','Considérons maintenant. les','penultimate line','5',why='A second stray full stop is attached after maintenant; corrected French omits it.')
 txt,_,_=page_text(rel,181);r(r'\Omega',r'\underline{\Omega}','differential sheaf symbols','4;5',why='The Greek sheaf symbols are underlined.',count=txt.count(r'\Omega'))
 upright_page(rel,layer,'149-181')
event('149-4-cor1','targeted proof check','In the two fiber identities, the cycle over b is the separately introduced Z prime, and both fibers intersect the same U. The printed unprimed Z and lowercase u in the second identity are therefore slips, already corrected in supplied French. The Kunneth argument was read without an independent re-proof.','149, p. 181, Corollary 1, line 5')
event('149-4-rem','carried as background without fault found','Read the explicitly prospective extension to singular cycles, proper intersections and algebraic equivalence. The wording is preserved as historical text; later developments are deferred to the notes.','149, p. 181, Remark')
event('149-5-thm2','carried as background without fault found','Read the one-dimensionality and nonvanishing claim for the fundamental point class. Its proof is explicitly deferred by the author.','149, p. 181, Theorem 2')
record_page('149',181,r'''Compared sources/fr_printed/fr/149.tex entry lines 635–689 and sources/fr/fr/149.tex entry lines 638–692 against scan leaf 14, rendered at 400 dpi, all three enlarged bands and tight crops. Read Corollary 1 and its Künneth proof, the definition of the fundamental point class, the Remark, section 5 and Theorem 2.

Both layers restore the inline placement of the two fiber identities, exact statement and definition underlining, Greek sheaf notation, underlined k, heading formatting and punctuation outside parentheses. The printed layer restores Z (without prime) and lowercase u in the second identity, par in the negation, La in the heading and two stray full stops in the final paragraph. The corrected layer retains the corresponding existing repairs. The crowded comma/last Omega in the Künneth formula was enlarged and retained, not interpreted as a different mathematical symbol. Theorem 2 is recorded as read, with its deferred proof still to be encountered.''')
from update_record_counts import update
update()
