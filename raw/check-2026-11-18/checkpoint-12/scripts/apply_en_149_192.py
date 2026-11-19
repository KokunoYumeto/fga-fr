from audit_utils import *
from translation_edits import *
from update_record_counts import update
rel='sources/en/en/149.tex';page='149-192'
def ch(old,new,where,why,kind='terminology',count=1):
    replace(rel,old,new,'English',page,where,'Remarks / bibliography',
      'French 149-192 and personally inspected full 400-dpi page and enlarged top, middle and bottom bands: '+why,kind=kind,count=count)
ch('\\[\n  T_{0}^{1*}(B)=H^{*}(X,B),\n  \\qquad\n  T_{1}^{0*}(A)=\\operatorname{Ext}_{\\Osh_X}^{*}(X;A,\\Osh_X).\n\\]',
   '$T_{0}^{1*}(B)=H^{*}(X,B)$, $T_{1}^{0*}(A)=\\operatorname{Ext}_{\\Osh_X}^{*}(X;A,\\Osh_X)$',
   'Remark 2 final line','Restore two inline identities separated by a comma, with no final period.',kind='structure')
align_math(rel,'en','149',192,[(i,i) for i in range(35)],(35,35))
ch('\\subsection*{REMARKS}','\\subsection*{\\normalfont REMARKS.}',
   'heading','Restore normal heading face and final period.',kind='structure')
for i in [1,2,3]:
    ch('\\noindent '+str(i)+'.','\\noindent '+str(i)+'\\textsuperscript{o}',
       'Remark '+str(i)+' label','Restore the printed ordinal label.',kind='structure')
ch('with finite\nresolutions','with \\uline{finite}\nresolutions','Remark 1','Restore the emphasis on finite.')
ch('are coherent sheaves','are \\uline{coherent} sheaves','Remark 1','Restore the emphasis on coherent.')
ch('of any given total degree','of a given total degree','Remark 1','Translate de degré total donné without adding the universal any.',kind='translation')
ch('It is readily checked that in the formulas (8.1), one of the\n$\\symup{\\underline{L}(B_i)}$ may be replaced by $\\symup{B_i}$. In view of Proposition 3, this shows that',
   'One readily checks that in the formulas (8.1), one may replace \\uline{one} of the\n$\\symup{\\underline{L}(B_i)}$ by $\\symup{B_i}$. In view of Proposition 3, this therefore shows that one has',
   'Remark 2','Restore impersonal on and the emphasis limiting replacement to one argument; retain the corrected reference (8.1).')
ch('in both positive and\nnegative degrees','in both positive \\uline{and}\nnegative degrees',
   'Remark 3','Restore emphasis on et only.')
ch('(and, unless I am mistaken, if $\\symup{r>0}$, even between',
   '(and, barring error, if $\\symup{r>0}$, even between',
   'Remark 3 qualification','Preserve the tentative sauf erreur without introducing a personal I.')
ch('respectively between','resp. between','Remark 3','Restore the source abbreviation resp.')
ch('\\section*{BIBLIOGRAPHY}','\\section*{\\centering\\normalfont BIBLIOGRAPHY}',
   'bibliography heading','Restore centered normal heading face.',kind='structure')
for old,new,n in [('Cartier','CARTIER',1),('Grothendieck (Alexandre)','GROTHENDIECK (Alexandre)',1),('Serre (Jean-Pierre)','SERRE (Jean-Pierre)',2)]:
    ch(old,new,'bibliography authors','Restore printed author capitalization.',count=n)
ch('. --- ','. - ','bibliography separators','Restore the printed single separator hyphen.',kind='structure',count=5)
ch('t. 1, 1957, no. 3.','t. 1, 1957, n\\textsuperscript{o} 3.','bibliography [1]','Restore the printed bibliographic abbreviation and superscript.')
ch('\\emph{Tohoku Math. J.}, vol. 9, 1957, pp. 119--183.',
   'Tohoku math. J., t. 9, 1957, p. 119-183.',
   'bibliography [2]','Restore the exact printed journal capitalization, normal face, abbreviations and range hyphen.')
ch('\\emph{Annals of Math.}, vol. 61, 1955, pp. 197--278.',
   'Annals of Math., t. 61, 1955, p. 197-278.',
   'bibliography [3]','Restore the printed normal face, bibliographic abbreviations and range hyphen.')
ch('\\emph{Proc. Intern. Symp. on Alg. Number Theory}\n[1955, Tokyo and Nikko]. - Tokyo, Science Council of Japan, 1956,\npp. 175--189.',
   'Proc. Intern. Symp. on alg. number Theory\n[1955. Tokyo et Nikko] - Tokyo, Science Council of Japan, 1956 ;\np. 175-189.',
   'bibliography [4]','Restore the exact quoted bibliographic title, normal face, punctuation, event wording and range hyphen.')
record_translation_page('en','149',192,rel,
    'Read all three remarks and the four bibliography entries. Approved 35 mathematical correspondences after splitting the two inline identities. Preserved corrected reference (8.1), the distinction between the sheaf and global bounds, and the tentative sauf erreur qualification. Restored finite/coherent/one/and emphasis, ordinal labels, source bibliography typography and impersonal register. No further source assertion was silently strengthened.',(1250,1309))
event('en-149-remark1','carried as background without fault found',
    'Read the warning about unbounded resolutions on a singular space and infinitely many terms in a fixed total degree. The text does not claim that every singular example actually has noncoherent cohomology; no universal counterexample assertion is added.',
    '149, p. 192, Remark 1')
event('en-149-remark2','used and rechecked in this run',
    'For the bounded locally free resolutions on the nonsingular space, all the other covariant resolutions form a bounded flat complex; replacing one L(B_i) by B_i preserves the required total quasi-isomorphism. Proposition 3 identifies the r=s=1 groups with Ext, and the two inline specializations have the displayed argument positions.',
    '149, p. 192, Remark 2 and (8.8)')
event('en-149-remark3','targeted proof check',
    'Resolutions have length at most n. Leaving one covariant argument unresolved gives the sheaf-degree interval [-(s-1)n,rn] for s>0, or [0,rn] for s=0. Cohomological dimension n gives the stated global upper bound (r+1)n. For r>0, Theorem 6 applied to the swapped argument counts gives dual complementary degree n-d and the lower bound -(r-1)n, hence the sharper upper bound rn. The printed tentative qualification remains in the translation even though this deduction checks it under the standing hypotheses.',
    '149, p. 192, Remark 3')
update()
