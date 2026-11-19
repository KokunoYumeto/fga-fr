from audit_utils import *
for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
 rel=f'sources/{tree}/fr/182.tex'
 def r(a,b,line,statement='',kind='reading',why='',count=1):
  replace(rel,a,b,layer,'182-220',line,statement,'400-dpi full scan and all three enlarged bands. '+why,kind,count=count)
 r('des trois points}, du moins',r'\uline{des trois points}}, du moins','first line','8-three-points',why='The quoted continuation des trois points is underlined.')
 r(r'\result{REMARQUES}{}',r'\result[]{REMARQUES}{}','remarks heading','8-final-remarks',why='REMARQUES has no following punctuation.')
 r('« tame »',r'\fquote{tame}','Remark 1','8-final-rem1',why='Ordinary double quotation marks.')
 r('« abstraite »',r'\fquote{abstraite}','Remark 2','8-final-rem2',why='Ordinary double quotation marks.')
 r('théorème de Lefschetz sur',r'\uline{théorème de Lefschetz} sur','end of Remark 2','8-final-rem2',why='Only théorème de Lefschetz is underlined.')
 r(r'\textbf{BIBLIOGRAPHIE}','BIBLIOGRAPHIE','bibliography heading','bibliography',why='The centered heading is plain roman.')
 for a,b in [('Dieudonné (J.) et Grothendieck (A.)','DIEUDONNÉ (J.) et GROTHENDIECK (A.)'),('Grothendieck (Alexander)','GROTHENDIECK (Alexander)'),('Serre (Jean-Pierre)','SERRE (Jean-Pierre)')]:
  txt,_,_=page_text(rel,220);r(a,b,'bibliography author names','bibliography',why='Surnames are printed in capitals.',count=txt.count(a))
 r('. --- ','. - ','bibliography separators','bibliography',why='Each author/title separator is a single short hyphen.',count=4)
 txt,_,_=page_text(rel,220)
 for m in list(re.finditer(r'\\emph\{([^{}]*)\}',txt,re.S)):
  r(m.group(0),m.group(1),'bibliography titles','bibliography',why='The titles are upright, not italicized.')
 r('Éléments de','Eléments de','bibliography [1]','bibliography-1',why='The initial capital E is unaccented, while the lower-case é is retained.')
 r('Études Scientifiques','Etudes Scientifiques','bibliography [1]','bibliography-1',why='The capital E of Etudes is unaccented.')
 r('varieties. International','varieties, International','bibliography [2]','bibliography-2',why='A comma separates the article title from International Congress.')
 for a,b in [('197--278','197-278'),('1955--1956','1955-1956'),('1--42','1-42')]:r(a,b,'bibliography numeric ranges','bibliography',why='The printed ranges use a single short hyphen.')
 for n in range(1,5):r(r'\item[{['+str(n)+r']}]',r'\item[{\normalfont['+str(n)+r']}]','bibliography item '+str(n),'bibliography-'+str(n),why='The bracketed bibliography numbers are plain roman.')
 r('\\par\\smallskip\n\\begingroup\\footnotesize\n\\endgroup',r'\begin{center}'+ '\n'+r'  \rule{.16\linewidth}{.3pt}'+ '\n'+r'\end{center}','end of exposé','bibliography',kind='structure',why='Restore the centered closing horizontal rule; replace the empty editorial footnote wrapper.')
 upright_page(rel,layer,'182-220')
event('182-8-three-points','carried as background without fault found','Read the genus-zero, three-puncture consequence and the suggested reverse deduction from the three-points problem. The first follows conditionally from the preceding prime-to-characteristic realization corollary. The reverse deduction is phrased as an expectation and is not proved here; no Belyi-type theorem or unrestricted positive-characteristic reduction is inferred from it.','182, pp. 219–220, three-points remark')
event('182-8-final-rem1','carried as background without fault found','Read the prospective proposal to recover the specialization kernel using generalized Galois covers with possibly infinitesimal group schemes, and the observation that wild ramification is harder. This is a research direction, not an established assertion certified in this run. It is retained literally for later contextual notes.','182, p. 220, Remark 1')
event('182-8-final-rem2','carried as background without fault found','Read the proposed algebraic Lefschetz deduction from nilpotent invariance and a formal-neighborhood theorem attributed to Grauert, alternatively from the then-unproved local-base statement following Theorem 11. A proof needs an existence/full-faithfulness theorem for covers over the formal hyperplane neighborhood and algebraization or extension from that neighborhood, with the appropriate dimension hypotheses for surjectivity versus isomorphism. The cited formal-neighborhood result is not supplied here and is not independently proved in this run.','182, p. 220, Remark 2')
record_page('182',220,r'''Compared sources/fr_printed/fr/182.tex and sources/fr/fr/182.tex entry lines 1312–1352 with scan leaf 29 at 400 dpi and all three enlarged bands, including the bibliography and closing rule. Read the end of the three-points remark, both final remarks, all four bibliography entries and the end of the exposé.

Restored the underlined quotation continuation and Lefschetz theorem name, the unpunctuated REMARQUES heading, ordinary quotation marks, plain bibliography heading and titles, capital surnames, unaccented initial capitals in Eléments and Etudes, the comma in reference [2], single short hyphens, plain bracketed bibliography numbers and the centered closing rule. No new correction of the original was made on this page. The speculative generalized-cover and reverse three-points remarks remain explicitly prospective; the formal Lefschetz claim is carried with its missing proof inputs named. All 28 printed pages of exposé 182 have now been read in both French layers, with the later author errata kept separate.''')
from update_record_counts import update
update()
