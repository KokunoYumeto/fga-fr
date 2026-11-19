from audit_utils import *
for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
    replace(f'sources/{tree}/fr/232.tex',r'\toP(',r'\to P(',layer,'232-149','3.3, projective immersion','3.3','Repairs this run\'s merged TeX token: the previously read scan has an arrow followed by P; the frozen compiler diagnostic identifies undefined control sequence toP. A separating space preserves the verified printed formula.',kind='typesetting')
with (ROOT/'CHECK_RECORD.md').open('a') as f:
    f.write('\n#### Build follow-up to 232-149\n\nRecorded '+utc()+'. Both French layers: separated the control word to from the following P in the projective immersion of 3.3. The failed frozen build is documented in build_reports/read_through_236_222. No mathematical reading changed; two typesetting rows record the repair.\n')
