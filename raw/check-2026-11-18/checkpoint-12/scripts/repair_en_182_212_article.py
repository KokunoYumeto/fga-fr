from audit_utils import *
from update_record_counts import update
replace('sources/en/en/182.tex',r'\uline{is} a separable scheme',r'\uline{is a} separable scheme',
    'English','182-212','Proposition 4 parenthesis','Proposition 4',
    'French 182-212, bottom enlarged crop personally inspected: the phrase est un is underlined; only schéma séparable is unaccented. Correct the article emphasis boundary introduced in this run.',
    kind='terminology')
update()
