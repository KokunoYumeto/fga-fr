from audit_utils import *
from translation_edits import *
from update_record_counts import update
rel='sources/en/en/182.tex';page='182-208'
def ch(old,new,where,why,kind='terminology',full=False,count=1):
    replace(rel,old,new,'English',page,where,'formal moduli scheme definition',
      'French 182-208 and personally inspected full 400-dpi scan and enlarged top, middle and bottom bands: '+why,kind=kind,full=full,count=count)
text,_,_=page_text(rel,208);start=text.index(r'\emph{1962 supplement.} --- Mumford constructed')
end=text.index('\n\n',start)+2
ch(text[start:end],'','inserted 1962 supplement','The printed page passes directly from the speaker’s intended construction to Reprenons. Remove the merged later supplement here; it belongs in the separate erratum section.',kind='translation')
align_math(rel,'en','182',208,[(i,i) for i in range(55)],(55,55))
ch('Return to the situation','Let us return to the situation','start of formal moduli setup','Restore the authors’ Reprenons register.')
ch('Suppose that one can find','\\uline{Suppose} that one can find','representability hypothesis','Restore the source emphasis on Supposons.')
ch(r'\emph{formal moduli scheme} for',r'\uline{formal moduli scheme for}',
   'definition','Restore underlined emphasis including for, as in schéma formel des modules pour.')
ch('(It need not exist.)','(Let us note that it need not exist).','qualification after the definition','Restore Notons and the period outside the parenthesis.')
ch(r'\textit{a priori}',r'\uline{a priori}','nilpotents and final observation','Restore underlined source emphasis.',count=2)
ch('regular rings','\\uline{regular} rings','final observation','Restore emphasis on regular alone.')
ch('Kodaira--Spencer','Kodaira-Spencer','final observation','Restore the printed hyphen.',kind='structure')
record_translation_page('en','182',208,rel,
    'Read the opening continuation, the covariant deformation functor, the conditional representability isomorphism (*), the formal moduli scheme and its universal formal family, and the discussion of nilpotents. Removed the inserted 1962 supplement. Approved all 55 formula correspondences, restoring the plain O_n quotient notation and Gothic Y-prime throughout the geometric base-change formulation. Restored the definition’s emphasis, the two a priori underlines, regular, and the authors’ Reprenons/Notons register. Existence of the representing ring remains an explicit hypothesis.',(722,772))
event('en-182-formal-moduli-star','targeted proof check',
    'Checked covariance and the conditional uniqueness of the representing complete local ring. Base change preserves flatness and the chosen closed fiber and composes associatively, giving F(A) to F(B). Under the assumed natural bijection (*), evaluation on the Artinian quotients of two proposed representing rings gives mutually inverse compatible maps of those quotients; completeness gives the canonical isomorphism. Naturality identifies finite-level pullback of the universal class with the specified element of F(A). This does not establish existence of a representing ring.',
    '182, p. 208, equation (*) and the formal moduli scheme definition')
event('en-182-formal-moduli-family','carried as background without fault found',
    'Read the construction from compatible finite-level classes, the asserted extension of (*) to complete Noetherian local test algebras, and the possibility of nonreduced moduli rings. The passage’s assertions about formal families and passage from isomorphism classes to the inverse limit have not been independently proved in this page check; the text’s nonexistence caveat is retained.',
    '182, p. 208, paragraphs after equation (*)')
update()
