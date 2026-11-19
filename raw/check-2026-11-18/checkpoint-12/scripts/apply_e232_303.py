from audit_utils import *
from collections import Counter
import csv
dq=chr(96)*2
for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
    rel=f'sources/{tree}/fr/e232.tex'
    def r(a,b,line,why,kind='reading',count=1):
        replace(rel,a,b,layer,'e232-303',line,'Errata to TDTE V',
                'Scan leaf 2 at 400 dpi, full page and three enlarged bands: '+why,kind=kind,count=count)
    r(r"\noindent\textbf{7. TDTE V : Les schémas de Picard. Théorèmes d'existence.}",r"\noindent 7. \uwave{TDTE} V : \uwave{Les schémas de Picard. Théorèmes d'existence}.",'title','Ordinary type with separate wavy underlines under TDTE and the title words.','typesetting')
    headings=['Page 7, remarque 3.3','Page 13, remarque 5.2','Page 14, ligne 7','Page 17, remarque 6.6','Page 18, remarque 6.7',r'Page 18, remarque 6.8, 4\textsuperscript{e} ligne']
    for s in headings:
        r(r'\textbf{'+s+'.}',r'\uline{'+s.replace(r'4\textsuperscript{e}','4e')+'}.','six entry headings','Ordinary straight-underlined type; the ordinal 4e is on the baseline.','typesetting')
    r(' --- ',' - ','six separators','Short dashes are printed.',count=6)
    r('« ',dq,'four quoted readings','Ordinary double quotation marks are printed.',count=4)
    r(' »',"''",'four quoted readings','Ordinary double quotation marks are printed.',count=4)
    r('(cf. dernier','(Cf. dernier','Remark 6.7 reference','The scan prints an uppercase C.')
    upright_page(rel,layer,'e232-303')
event('e232-3.3','carried as background without fault found','Read the announcement that Mumford answered the question in Remark 3.3 affirmatively. The reference is to the following exposé and its comments; no construction or proof is supplied in this entry. The earlier Picard representability hypotheses and the Mumford argument remain background dependencies.','Erratum 232, p. 303, Page 7, Remark 3.3; exposé 232, p. 149')
event('e232-5.2','carried as background without fault found','Read the withdrawal of the existence conjecture and the announcement of a weaker theorem by Mumford. The complete-base qualification in the next entry requires algebraically closed residue field. The real conic degeneration described at the beginning of exposé 236 explains the stated obstruction, conditional on its Picard-space computation and ineffective scheme descent; those construction inputs have not been independently proved in this run. The authorial errata remain unmerged.','Erratum 232, p. 303, Page 13, Remark 5.2 and Page 14, line 7; exposé 232, pp. 155-156; exposé 236, p. 221')
event('e232-6.6','carried as background without fault found','Read the reference to Murre for the affirmative answer to the general representability question. This is a historical report without proof here; the representation theorem and its hypotheses are background.','Erratum 232, p. 303, Page 17, Remark 6.6; exposé 232, p. 159')
event('e232-6.7','carried as background without fault found','Read the affirmative answer to the question in Remark 6.7 and its reference to the final paragraph of the comments on the following exposé. The promised argument is deferred to that paragraph; this short entry itself supplies no proof.','Erratum 232, p. 303, Page 18, Remark 6.7; exposé 232, p. 160')
event('e232-6.8','targeted proof check','Read the authorial replacement of regular by simple over k, without merging it into the exposé. Checked why the hypotheses differ over an imperfect field: for k=F_p(t) and K=k(u), u^p=t, Spec K is regular, but Omega_(K/k) is nonzero, so Spec K is not smooth over k. This verifies the distinction motivating the restriction, not a counterexample to the complete formal-Lefschetz assertion, whose proof remains background.','Erratum 232, p. 303, Page 18, Remark 6.8, line 4; exposé 232, p. 160')
with (ROOT/'CORRECTIONS.tsv').open(newline='') as f:
    c=Counter((x['layer'],x['kind']) for x in csv.DictReader(f,delimiter='\t') if x['printed_page']=='e232-303')
record_page('e232',303,'Compared sources/fr_printed/fr/e232.tex and sources/fr/fr/e232.tex, entry lines 4-35, with scan leaf 2 at 400 dpi, full page and three enlarged bands. Read all six entries, their cross-references and the quoted replacement simple sur k. Restored the ordinary title with wavy underlines, six straight-underlined headings, baseline 4e, short dashes, ordinary double quotation marks, uppercase Cf. and upright k. Both French layers agree. Distinguished the announced existence results from proofs; checked regular versus smooth over an imperfect field without claiming a counterexample to the entire formal-Lefschetz statement. Errata remain separate.\n\nOperation counts: '+'; '.join(f'{a}, {b}: {n}' for (a,b),n in sorted(c.items()))+'. Final row verdicts remain pending.')
from update_record_counts import update
update()
