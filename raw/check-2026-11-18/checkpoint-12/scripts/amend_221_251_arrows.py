from audit_utils import *
for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
    rel=f'sources/{tree}/fr/221.tex'
    s,_,_=page_text(rel,251)
    n=s.count(r'\longrightarrow')
    replace(rel,r'\longrightarrow',r'\to',layer,'221-251','base-change and product-parameter arrows','section 1',
            'The enlarged middle and bottom scan bands inspected with page 251 show short single arrows, as do the adjacent page 252 arrows. Use the short glyph without altering any source, target or direction.',count=n)
with (ROOT/'CHECK_RECORD.md').open('a') as f:
    f.write('\nFocused typography follow-up to 221-251, '+utc()+': its five short arrows per layer are now represented by the short arrow command, using the already inspected middle and bottom crops. A later close crop of the flat-family sentence confirmed the final e in définie; no edit was needed there. The ledger helper now writes one row for each repeated occurrence, with an occurrence and source-line locator, instead of one aggregate row. Earlier aggregate rows still require the mandated per-place final review.\n')
with (ROOT/'progress.log').open('a') as f:
    f.write('221-251 short-arrow follow-up and per-occurrence ledger refinement '+utc()+'\n')
from update_record_counts import update
update()
