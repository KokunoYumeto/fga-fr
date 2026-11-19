"""Apply the reader-requested English preamble dependency repair once.

Prepared from the frozen en149_complete_193 compiler failure. This script changes
one package declaration and records it through the existing correction helper.
It must be run by the root reader at the chosen mutation boundary.
"""
from audit_utils import replace


PREIMAGE = '\\usepackage{microtype}\n\\usepackage{graphicx}\n'
POSTIMAGE = '\\usepackage{microtype}\n\\usepackage[normalem]{ulem}\n\\usepackage{graphicx}\n'


if __name__ == '__main__':
    replace(
        'sources/en/tex/base.tex',
        PREIMAGE,
        POSTIMAGE,
        'English',
        '149-170',
        'preamble source lines 9-10; package insertion after microtype',
        'English build dependency: ulem',
        'Frozen build en149_complete_193, pass 1: undefined control sequence '
        '\\uline at sources/en/en/149.tex line 67, anchored to printed 149-170. '
        'The captured English preamble does not load ulem. The successful French '
        'preamble loads ulem with normalem, and the package is already present '
        'in the pinned runtime. This declaration supplies the underline commands '
        'while retaining the existing emph behavior. Rebuild verification pending.',
        kind='typesetting',
        confidence='low',
        count=1,
        full=True,
    )
