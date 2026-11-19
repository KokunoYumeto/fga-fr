from audit_utils import *
from translation_edits import *
from update_record_counts import update
rel='sources/en/en/182.tex';page='182-198'
def ch(old,new,where,why,kind='terminology',full=False,count=1):
    replace(rel,old,new,'English',page,where,'Theorems 3 and 4',
      'French 182-198 and personally inspected full 400-dpi scan and enlarged top, middle and bottom bands: '+why,kind=kind,full=full,count=count)
whole=read(rel)
start=whole.index('    \\[\n      H^2(\\mathfrak X_0,\\Osh_{\\mathfrak X_0})=0.')
end=whole.index('\\src{199}',start)+len('\\src{199}')
old=whole[start:end]
new='\\src{199}\n'+old[:-len('\\src{199}')]
ch(old,new,'printed page break within Theorem 4(ii)','Page 198 ends after one has; page 199 begins with the H^2 vanishing formula. Relocate the existing marker without changing the intervening text.',kind='structure',full=True)
align_math(rel,'en','182',198,[(i,i) for i in range(42)],(42,42))
ch(r'\emph{subcategory}',r'\uline{subcategory}','subcategory statements','Restore printed underlining.',count=2)
ch('topology.]','topology].','Theorem 3 bracketed recall','Restore punctuation outside the square bracket.',kind='structure')
text,_,_=page_text(rel,198)
body=text.split(r'\result{THEOREM}{3} ',1)[1].split(' (determined',1)[0]
ch(body,underline_prose(body),'Theorem 3 statement','Restore all printed statement emphasis before the unaccented parenthesis.')
text,_,_=page_text(rel,198)
body=text.split(r'\result{COROLLARY}{1} ',1)[1].split('\n\n',1)[0]
ch(body,underline_prose(body),'Theorem 3 Corollary 1','Restore statement underlining.')
ch('respectively\nof','resp.\nof','Corollary 1 explanation','Apply the prescribed abbreviation resp.')
text,_,_=page_text(rel,198)
body=text.split(r'\result{COROLLARY}{2} ',1)[1].split('\n\n',1)[0]
pre,rest=body.split(' (a Noetherian',1);parent,post=rest.split('). ',1)
newbody=underline_prose(pre)+' (a Noetherian'+parent+'). '+underline_prose(post)
ch(body,newbody,'Theorem 3 Corollary 2','Restore statement emphasis, keeping the Noetherian complete-ring parenthesis unaccented.')
ch('algebraic schemes proper over $\\symup{A}$ appear as a\n\\uline{subcategory}',
   '\\uline{algebraic schemes proper over} $\\symup{A}$ \\uline{appear as a\nsubcategory}',
   'explanation after Corollary 2','Restore the full printed emphasis, not only subcategory.')
ch('that\nthere are formal schemes proper over $\\symup{\\overline Y}$ that are not\n“algebraizable,”',
   '\\uline{that\nthere are formal schemes proper over} $\\symup{\\overline Y}$ \\uline{that are not\n“algebraizable”},',
   'nonalgebraizable formal schemes','Restore the source emphasis and punctuation outside the quotation.')
ch('“theory of moduli.”','\\uline{“theory of moduli”}.','moduli remark','Restore source underlining and quotation punctuation.')
text,_,_=page_text(rel,198)
body=text.split(r'\result{THEOREM}{4} ',1)[1].split(' (equipped',1)[0]
ch(body,underline_prose(body),'Theorem 4 opening','Restore statement emphasis before the unaccented parenthesis.')
ch(r'\textit{i.}',r'\textnormal{i.}','Theorem 4(i) marker','Restore roman item label.',kind='structure')
ch(r'\textit{ii.}',r'\textnormal{ii.}','Theorem 4(ii) marker','Restore roman item label.',kind='structure')
text,_,_=page_text(rel,198)
body=text.split(r'\item[\textnormal{i.}] ',1)[1].split('\n  \\item',1)[0]
newbody=underline_prose(body).replace('\\uline{are flat}', '\\uline{are} flat')
# The source excludes the word plats from the underline; the English has it at the end of the first prose span.
newbody=newbody.replace('are flat}', 'are} flat')
# Alignment made the associated-graded identity inline, so restore its external period.
newbody=newbody.rstrip()+'.'
ch(body,newbody,'Theorem 4(i)','Restore prose emphasis with flat excluded, inline formula structure and final period.')
text,_,_=page_text(rel,198)
body=text.split(r'\item[\textnormal{ii.}] ',1)[1]
ch(body,underline_prose(body),'Theorem 4(ii) opening','Restore emphasis through the page-end words one has.')
record_translation_page('en','182',198,rel,
    'Read the algebraization theorem for coherent sheaves, both corollaries, the warning about nonalgebraizable proper formal schemes, and the opening hypotheses of Theorem 4. Moved the misplaced page-199 marker to the actual break within (ii), then approved all 42 mathematical correspondences. Restored the Gothic r(A), plain arrow g to g-bar, inline associated-graded relation, and statement emphasis. The corrected completed structure sheaf in the Corollary 1 explanation was already present in English.',(237,312))
for sid,description in [
 ('Theorem3','Coherent-sheaf algebraization over a Noetherian complete adic base and uniqueness from full faithfulness.'),
 ('Theorem3-Cor1','Closed subschemes correspond to coherent ideal subsheaves; the formal side uses the completed structure sheaf.'),
 ('Theorem3-Cor2','The graph construction gives the proper-scheme morphism correspondence; properness and completeness hypotheses are retained.'),
 ('Theorem4-hypotheses','Read flatness and the associated-graded reformulation; the H^2 condition and conclusion continue on the next page.')]:
    event('en-182-'+sid,'carried as background without fault found',description+' No independent proof is claimed by this translation reading.','182, p. 198, section 3')
update()
