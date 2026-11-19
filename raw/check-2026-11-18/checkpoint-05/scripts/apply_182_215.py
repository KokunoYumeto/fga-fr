from audit_utils import *
for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
 rel=f'sources/{tree}/fr/182.tex'
 def r(a,b,line,statement='',kind='reading',why='',count=1,full=False):
  replace(rel,a,b,layer,'182-215',line,statement,'400-dpi full scan and all three enlarged bands; extra tight crop of the final structure-sheaf parenthesis. '+why,kind,count=count,full=full)
 if r'\uline{un schéma algébrique connexe' not in page_text(rel,215)[0]:
  r('\\src{216}\n','','page boundary','8-rem1','structure','Page 215 ends with the pi_0 sequence, before comme en Topologie algébrique.',full=True)
  r('comme en Topologie algébrique.','\\src{216}\ncomme en Topologie algébrique.','last line','8-rem1','structure','Move the marker to the actual continuation.',full=True)
  old=r''', et que $X$ ou $Y$ est propre sur
$k$.\footnote{Condition ajoutée dans l'erratum de 1962.}'''
  r(old,' et complet.','Corollary 5 hypothesis','8-thm11-cor5','structure','The printed hypothesis says X-reduced is separable over k (with the perfect-field aside) et complet. The supplied X-or-Y proper replacement and its editorial note merge a later erratum; restore the original in both layers, as required.')
  r('schéma algébrique connexe et propre sur un corps','schéma algébrique connexe sur un corps','Corollary 6 opening','8-thm11-cor6','structure','The print has no properness hypothesis. Remove the merged later qualification from both layers; the unrestricted assertion and its failure are discussed in the audit, while the author erratum remains separate.')
  txt,_,_=page_text(rel,215)
  r(r'\Osh','O','structure sheaves','',why='Plain upright O, including the final parenthesis; the tight crop shows a smudged ordinary closing parenthesis, not a brace.',count=txt.count(r'\Osh'))
  r(r'\textit{a'+ '\n'+ 'posteriori}',r'\uline{a posteriori}','first line','8-thm11-cor3',why='Underlined roman phrase.')
  r(r'\textit{a priori}',r'\uline{a priori}','first line','8-thm11-cor3',why='Underlined roman phrase.')
  r('Serre--Lang','SERRE-LANG','two attributions','8-thm11-cor5',why='Uppercase names and a short hyphen.',count=2)
  r('  }.\n\\]','  }\n\\]','boxed Corollary 4 sequence','8-thm11-cor4',why='No period follows the box in print.')
  r(r'\result{REMARQUES}{}',r'\result[.]{REMARQUES}{}','Remarks heading','8-rem','structure','The heading ends with a period and no dash.')
  r(r'''continuer par
\[
  \pi_0(\overline F)\longrightarrow\pi_0(X)
  \longrightarrow\pi_0(Y)\longrightarrow e.
\]''',r'''continuer par
$\pi_0(\overline F)\longrightarrow\pi_0(X)
  \longrightarrow\pi_0(Y)\longrightarrow e$''','last line','8-rem1','structure','The pi_0 sequence is inline and has no terminal period here.')
  if tree=='fr_printed':
   r('(déduit des morphismes fonctoriels','(déduits des morphismes fonctoriels','explanation after Corollary 5 display','8-thm11-cor5',why='Printed plural déduits. Corrected French retains singular déduit agreeing with the single morphisme naturel.')
  # Restore statement emphasis, retaining the ununderlined asides and injectif.
  for n in [4,5,6]:
   txt,_,_=page_text(rel,215);marker='\\result{COROLLAIRE}{'+str(n)+'} ';a=txt.index(marker)+len(marker);b=txt.find('\n\n',a);old=txt[a:b]
   parts=re.split(r'(\\\[.*?\\\]|\(ce qui\s+est automatiquement.*?\)|\(resp\. .*?\)|\(unique à un isomorphisme près\))',old,flags=re.S)
   new=''.join(x if i%2 else underline_prose(x) for i,x in enumerate(parts))
   r(old,new,'Corollary '+str(n)+' statement prose','8-thm11-cor'+str(n),why='Restore the printed underlining; explanatory asides and formulas remain plain.')
 bad=r"""(\uline{ce qui
est automatiquement vrai si} $k$ \uline{est parfait) et complet. Choisissons un point
géométrique}"""
 if bad in page_text(rel,215)[0]:
  r(bad,r"""(ce qui
est automatiquement vrai si $k$ est parfait) \uline{et complet. Choisissons un point
géométrique}""",'Corollary 5 perfect-field aside','8-thm11-cor5',why='Amend the first formatting operation: the perfect-field parenthesis is ununderlined, while et complet resumes the emphasis.')
 r(r'\uline{Ce morphisme est injectif, et même bijectif si}',r'\uline{Ce morphisme est} injectif, \uline{et même bijectif si}','Corollary 5 after display','8-thm11-cor5',why='Injectif alone is left plain in the printed conclusion.')
 upright_page(rel,layer,'182-215')
event('182-8-thm11-cor4','targeted proof check','Let H be the image of pi_1(F-bar) in G=pi_1(X), and N the kernel of G -> pi_1(Y). Corollary 3 says a transitive finite G-set with an H-fixed point comes from the quotient G/N; hence N acts trivially on it. For each open subgroup U containing H, apply this to G/U: N is contained in U. Since H is compact and therefore closed, the intersection of all such U is H, so N is contained in H. The reverse inclusion follows from the composite fiber-to-base map being constant. Surjectivity is Lemma 4. This proves middle exactness without assuming H normal in advance.','182, p. 215, Corollary 4')
event('182-8-thm11-cor5','carried as background without fault found','Restored the printed hypothesis that X-reduced is separable and complete; the supplied X-or-Y proper replacement is a later modification and cannot be merged into this exposé. Read the product homomorphism and injectivity/bijectivity claims. Their proof uses the proper homotopy sequence, invariance under nilpotent thickenings, geometric connectedness and descent over the ground field; not independently reconstructed in full here. The printed déduits is a grammatical mismatch with morphisme naturel; singular retained in corrected French.','182, p. 215, Corollary 5')
event('182-8-thm11-cor6','refuted, with the refined statement\'s id','Refined statement id: 182-8-thm11-cor6-proper. In characteristic p, take algebraically closed k, K an algebraic closure of k(t), X=A^1_k. The finite étale Artin–Schreier torsor z^p-z=t x over K[x] does not descend to k[x]: after reducing polynomials modulo h^p-h, the coefficient of the degree-one term is t, whereas a class from k[x] has degree-one coefficient in k. Even changing the F_p generator only multiplies by an element of F_p^*, which does not put t in k. Thus the unrestricted printed scalar-extension assertion fails. Restored it in both text layers because the later qualification must stay in its erratum; no silent merge.','182, p. 215, Corollary 6')
event('182-8-thm11-cor6-proper','carried as background without fault found','The proper-case invariance of finite étale covers under algebraically closed field extension is the intended refinement suggested by the supplied edit; it requires proper covering descent and the product theorem. This check has not yet read the author erratum, so its exact wording and any characteristic-zero extension remain to be checked there.','182, p. 215, audit refinement of Corollary 6')
event('182-8-rem1','targeted proof check','For proper separable f, Proposition 4 gives a finite étale Stein factor Y-prime. The geometric fiber components form the finite pi_1(Y)-set given by Y-prime; their orbit containing the chosen component has stabilizer the image of pi_1(X). Its orbits correspond to connected components of X over the selected base component. This supplies the pointed-set continuation through pi_0, conditional on the preceding homotopy sequence; it is not a sequence of groups in degree zero.','182, pp. 215–216, Remark 1, initial assertion')
record_page('182',215,r'''Compared sources/fr_printed/fr/182.tex and sources/fr/fr/182.tex entry lines 1061–1117 with scan leaf 24, 400 dpi, all three enlarged bands, and a tight crop of the final O_X parenthesis. Read Corollaries 4–6 and the start of Remark 1. Marker 216 now precedes comme en Topologie algébrique.

Restored Corollary 5's printed et complet hypothesis in both layers, removing the supplied later X-or-Y proper replacement and its footnote. Removed the merged properness qualification from Corollary 6 in both layers. The original unrestricted Corollary 6 is explicitly refuted in the check events by an Artin–Schreier example; its refined statement remains outside the exposé until the separate erratum is read. Restored plain O, uppercase SERRE-LANG, underlined Latin phrases and statement prose, the period-only Remarks heading, the unpunctuated box and inline pi_0 continuation. Printed French has déduits in the Corollary 5 explanation; corrected French retains déduit agreeing with morphisme. Proved the Corollary 4 group criterion from Corollary 3 and checked the pointed-set continuation; Corollary 5 and the proper refinement are explicitly background.''')
p='CHECK_RECORD.md';t=read(p).replace('## Open reading questions','- 182-215, Corollaries 5–6: restored the original hypotheses in both layers and removed merged later qualifications; recorded an Artin–Schreier counterexample to unrestricted Corollary 6 without silently changing the exposé.\n\n## Open reading questions');write(p,t)
from update_record_counts import update
update()
