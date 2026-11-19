from audit_utils import *
for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
 rel=f'sources/{tree}/fr/149.tex'
 def r(a,b,line,statement='',kind='reading',why='',count=1):
  replace(rel,a,b,layer,'149-182',line,statement,'400-dpi scan, enlarged page bands and tight formula/word crops. '+why,kind,count=count)
 r('\\operatorname{Ext}_{\\Osh_X}^{n}(X;\\Osh_X,\\Omega_X^{n}),\n\\]\ni.e.', '\\operatorname{Ext}_{\\Osh_X}^{n}(X;\\Osh_X,\\Omega_X^{n}),\\quad\\text{i.e.}\n\\]', 'first display','5.1','structure','The abbreviation i.e. stands at the right of the first displayed pairing.')
 for tag,old,new in [('5.1',r'\longrightarrow H^{n}(X,\Omega_X^{n}).',r'\longrightarrow H^{n}(X,\Omega_X^{n})'),('5.2',r"\longrightarrow\bigl(H^{p}(X,F)\bigr)'.",r"\longrightarrow\bigl(H^{p}(X,F)\bigr)'"),('5.3',r"=H^{n-p}\bigl(X,\Omega_X^{n}\otimes\Osh_X(E')\bigr).",r"=H^{n-p}\bigl(X,\Omega_X^{n}\otimes\Osh_X(E')\bigr)"),('second 5.3',r'H^{0}(X,\Osh_X)\longrightarrow H^{0}(X,k_x),',r'H^{0}(X,\Osh_X)\longrightarrow H^{0}(X,k_x)'),('5.5',r'=H^{n}(X,\Omega_X^{n}).',r'=H^{n}(X,\Omega_X^{n})')]:
  r(old,new,'formula '+tag,tag,why='No terminal punctuation is printed at this formula.')
 r("L'homomorphisme (5.2) est un isomorphisme.",r"\uline{L'homomorphisme} (5.2) \uline{est un isomorphisme}.",'Theorem 3','5-thm3',why='Prose is underlined; the formula reference is not.')
 txt,_,_=page_text(rel,182);start=txt.index(r'\result{COROLLAIRE}{} ')+len(r'\result{COROLLAIRE}{} ');stop=txt.index(r'\begin{equation}',start);old=txt[start:stop]
 r(old,underline_prose(old),'Corollary statement','5-cor',why='The statement prose is underlined, excluding the variables.')
 r(r"\noindent\textbf{(D) L'homomorphisme suivant}",r"\noindent(D) \uline{L'homomorphisme suivant}",'statement D','5-D',why='D is an ordinary label; the following words are underlined.')
 r("\\longrightarrow\\bigl(H^{p}(X,F)\\bigr)'\\otimes L,\n  \\qquad L=H^{n}(X,\\Omega_X^{n}),", "\\longrightarrow\\bigl(H^{p}(X,F)\\bigr)'\\otimes L\n  \\qquad (L=H^{n}(X,\\Omega_X^{n})),",'formula 5.2 bis','5.2-bis',why='The definition of L is parenthesized, with the comma after the closing parenthesis.')
 r("déduit de l'accouplement (5.1) est un isomorphisme.",r"\uline{déduit de l'accouplement (5.1) est un isomorphisme}.",'statement D conclusion','5-D',why='The underline extends through the formula reference.')
 txt,_,_=page_text(rel,182)
 r('k_x',r'\underline{k}_x','skyscraper sheaf symbols','5.3-bis;5.4;5.5',why='Every k identifying the point sheaf is underlined.',count=txt.count('k_x'))
 # Inspect each displayed formula separately: the print omits two Omega underlines.
 txt,_,_=page_text(rel,182)
 for m in list(re.finditer(r'\\begin\{equation\}\\tag\{([^}]+)\}(.*?)\\end\{equation\}|\\\[(.*?)\\\]',txt,re.S)):
  old=m.group(0);tag=m.group(1) or 'first display';new=old.replace(r'\Omega',r'\underline{\Omega}')
  if tree=='fr_printed' and tag=='5.3': new=old
  if tree=='fr_printed' and tag=='5.5': new=new.replace(r'\underline{\Omega}',r'\Omega',1)
  if new!=old:
   kind='misprint of the original' if tree=='fr' and tag in ('5.3','5.5') else 'reading'
   why='The canonical differential sheaf has an underlined Omega.'
   if tag in ('5.3','5.5') and tree=='fr': why+=' The first Omega in this formula lacks the underline in print; its sheaf role and the adjacent occurrences identify the missing notation.'
   r(old,new,'formula '+tag,tag,kind,why)
 if tree=='fr_printed':
  r(r'\tag{5.3 bis}',r'\tag{5.3}','second formula numbered 5.3','5.3-bis',why='The original repeats the earlier number 5.3. Corrected French retains the existing disambiguation 5.3 bis, used by the following proof.')
 upright_page(rel,layer,'149-182')
event('149-5-thm3','carried as background without fault found','Read the duality assertion and functorial pairing; the proof begins here and continues. The scope of F is to be checked in the ensuing reduction rather than silently supplemented.','149, p. 182, Theorem 3 and (5.1)–(5.2)')
event('149-5-cor','targeted proof check','For locally free O(E), the first corollary to Proposition 1 identifies Ext with cohomology of Hom(O(E),Omega), which is Omega tensor O(E prime). This verifies the dual-bundle order and exponent n-p. The omitted underline on Omega in (5.3) is a notation slip.','149, p. 182, Corollary and (5.3)')
event('149-5-D','carried as background without fault found','Read D and the start of the reduction of Theorem 2 to D. The repeated printed label 5.3 denotes the evaluation map, distinct from the vector-bundle formula. The proof continues on p. 183.','149, p. 182, D and (5.2 bis)–(5.5)')
record_page('149',182,r'''Compared sources/fr_printed/fr/149.tex entry lines 686–752 and sources/fr/fr/149.tex entry lines 689–755 against scan leaf 15, rendered at 400 dpi; inspected the full page, all three enlarged bands and tight crops of the two ununderlined Omegas, the crowded O argument in (5.4), and “fonctoriel en F”. Read all pairings, statement D and the proof beginning with the point sheaf.

Both layers restore the placement of i.e., formula punctuation, exact statement underlining, parentheses around the definition of L, underlined k and the upright typed mathematical letters. The printed layer retains the repeated label (5.3) and the two omitted Omega underlines. Corrected French retains (5.3 bis) to distinguish the evaluation map, and restores the missing sheaf notation. The crowded handwritten O in the right-hand argument of (5.4) was compared with the other O forms on the page and retained as O, rather than treated as an unsupported new lowercase-a reading. The existing words “fonctoriel en F” were confirmed. No coherence hypothesis was inserted while the proof is still pending.''')
from update_record_counts import update
update()
