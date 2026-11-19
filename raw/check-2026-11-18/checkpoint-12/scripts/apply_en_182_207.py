from audit_utils import *
from translation_edits import *
from update_record_counts import update
rel='sources/en/en/182.tex';page='182-207'
def ch(old,new,where,why,kind='terminology',full=False,count=1):
    replace(rel,old,new,'English',page,where,'remarks after Theorem 9 and section 7',
      'French 182-207 and personally inspected full 400-dpi scan and enlarged top, middle and bottom bands: '+why,kind=kind,full=full,count=count)
for opening in ['J.-P. Serre constructed a nonsingular projective','The speaker is by then less optimistic about the']:
    text,_,_=page_text(rel,207);start=text.index(r'\emph{1962 supplement.} --- '+opening)
    end=text.index('\n\n',start)+2
    ch(text[start:end],'','inserted 1962 supplement','This paragraph is absent from the printed exposé. Remove the merged later material here; its separate erratum section is retained and will be checked in sequence.',kind='translation')
ch('able to construct genuine moduli schemes in certain cases',
   'able to construct from this moduli schemes properly so called in certain cases',
   'opening of section 7','Restore à partir de là and put the adjective after moduli schemes so that the printed page boundary can be represented without splitting an English phrase.',kind='translation')
whole=read(rel);start=whole.index('properly so called in certain cases');end=whole.index('\\src{208}',start)+len('\\src{208}')
old=whole[start:end];new='\\src{208}\n'+old[:-len('\\src{208}')]
ch(old,new,'page break in section 7 introduction','The printed page ends after schémas de modules. Move the existing marker after moduli schemes.',kind='structure',full=True)
align_math(rel,'en','182',207,[(i,i) for i in range(30)],(30,30))
ch('is complete.','is \\uline{complete}.','Remark 2','Restore emphasis on the completeness hypothesis.')
ch('theorem,”','theorem”,','Remark 2','Restore the comma outside the quotation.',kind='structure')
ch('Kodaira--Spencer','Kodaira-Spencer','Remark 3','Restore the printed hyphen between the names.',kind='structure',count=2)
ch('assumed local.)','assumed local).','Remark 3 local qualification','Restore the period outside the parenthesis.',kind='structure')
ch(r'\fsection{7}{Application to the theory of moduli}',
   r'\fsection{\normalfont7}{\normalfont\uline{Application to the \fquote{Theory of moduli}}.}',
   'section 7 heading','Restore the normal roman underlined heading, quotation, initial capital and final period.',kind='structure')
ch('we work over a field\n$\\symup{k}$, i.e. in equal characteristic',
   'we work over a \\uline{field}\n$\\symup{k}$, i.e. we work in \\uline{equal characteristic}',
   'section 7 introduction','Restore emphasis on field and equal characteristic and the repeated authors’ nous travaillons.')
record_translation_page('en','182',207,rel,
    'Read the end of Remark 1, Remarks 2 and 3, and the opening of section 7. Removed the two inserted 1962 supplements, which do not occur in the exposé scan and belong in their separate erratum section. Restored the page-208 boundary after moduli schemes and the missing à partir de là phrase. Approved all 30 remaining formula correspondences, including Gothic projective space and G and the source residue-field letter. Restored emphasis, quotation punctuation and the section heading. The conjectural language and historical questions remain conjectural.',(680,741))
event('en-182-Theorem9-Remark1','carried as background without fault found',
    'Read the historical question about lifting to mixed characteristic and the proposed first-obstruction test. This is a question in the exposé, not an existence theorem. The later Serre–Mumford supplement is kept in the separate erratum; no proof of its examples is claimed here.',
    '182, pp. 206–207, Remark 1 after Theorem 9')
event('en-182-Theorem9-Remark2','carried as background without fault found',
    'Read the completeness restriction on Theorem 3 and the request for a fourth fundamental theorem passing from completion to a local ring. The text explicitly leaves its definitive statement open; no proof or silently modernized statement is supplied.',
    '182, p. 207, Remark 2 after Theorem 9')
event('en-182-Theorem9-Remark3','carried as background without fault found',
    'Read the conjectured finite unramified comparison, the asserted projective-space case and geometric-fiber rigidity, and the questions on variations of projective space and abelian varieties in the ongoing deformation context. Their proofs are not given in this paragraph and were not independently reconstructed in this translation reading. The source’s distinction between assertions and conjectures is preserved.',
    '182, p. 207, Remark 3 after Theorem 9')
update()
