from audit_utils import *
for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
    rel=f'sources/{tree}/fr/236.tex'
    for old,new,loc in [
        (r'\uline{existe (par exemple} $\symup{f}$ \uline{un morphisme'+'\n'+r'projectif). Alors}',
         r'\uline{existe} (par exemple $\symup{f}$ un morphisme projectif). \uline{Alors}',
         '2.1(i), parenthetical example'),
        (r'\uline{\noindent(ii) Soit}',r'\noindent(ii) \uline{Soit}',
         '2.1(ii), item number')
    ]:
        replace(rel,old,new,layer,'236-231',loc,'2.1',
                'Repairs this run\'s overly broad prose-emphasis conversion: the personally viewed 400-dpi scan and enlarged bands leave the projective parenthesis and the item number (ii) un-underlined.',
                kind='typesetting')
with (ROOT/'CHECK_RECORD.md').open('a') as f:
    f.write('\nFollow-up to 236-231, '+utc()+': source readback found two emphasis spans broader than the image. Repaired the projective parenthesis and item number (ii) in both layers, with four typesetting rows. These are corrections of this run, not of the print. No new mathematical reading.\n')
from update_record_counts import update
update()
