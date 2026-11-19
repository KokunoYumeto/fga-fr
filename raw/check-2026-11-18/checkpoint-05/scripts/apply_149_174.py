from audit_utils import *
for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
    rel=f'sources/{tree}/fr/149.tex'
    def r(a,b,line,statement='',kind='reading',count=1):
        replace(rel,a,b,layer,'149-174',line,statement,'400-dpi image and enlarged bands show the replacement; all indices and punctuation inspected.',kind,count=count)
    r(r'$A$-multilinéaire alternée du système des $x_i\in J$.',r'$A$-multilinéaire alternée du système des $x_i\in J$','1','3.2(i)')
    r("positifs, et l'homologie de ce complexe","positifs, et la cohomologie de ce complexe",'9–10','3')
    r('un complexe libre augmenté',r'un complexe \uline{libre} augmenté','12','3')
    r(r'\otimes_A M',r'\otimes M','unnumbered comparison; 3.3; 3.4','3.3–3.4',count=3)
    r('\\bigr)\n\\]\net\n\\[\n\\operatorname{Tor}','\\bigr)\\quad\\text{et}\\quad\n\\operatorname{Tor}','14','3','structure')
    r('H_{*}\\bigl(K_{\\underline{x}}\\otimes M\\bigr),\n\\]','H_{*}\\bigl(K_{\\underline{x}}\\otimes M\\bigr)\n\\]','14','3')
    r(r'&\longrightarrow H^{*}\bigl(\operatorname{Hom}_{A}(K_{\underline{x}},M)\bigr),\\',r'&\longrightarrow H^{*}\bigl(\operatorname{Hom}_{A}(K_{\underline{x}},M)\bigr)\\','3.3 first line','3.3')
    r(r'&\longleftarrow H_{*}\bigl(K_{\underline{x}}\otimes M\bigr).',r'&\longleftarrow H_{*}\bigl(K_{\underline{x}}\otimes M\bigr)','3.3 second line','3.3')
    r(r'&\longrightarrow M\otimes A/J,\\',r'&\longrightarrow M\otimes A/J\\','3.4 first line','3.4')
    r(r'&\longleftarrow\operatorname{Hom}_{A}(A/J,M).',r'&\longleftarrow\operatorname{Hom}_{A}(A/J,M)','3.4 second line','3.4')
    upright_page(rel,layer,'149-174')
event('149-eq3.3–3.4','carried as background without fault found','Read the Koszul construction, augmentation and comparison maps, including both arrows in each display and the top-degree description. The omitted multilinearity verification is identified for the later notes; it has not been reconstructed here.','149, printed p. 174, section 3')
record_page('149',174,r'''Compared both French source intervals `\src{174}` to before `\src{175}` (current entry lines 268–332) against the full 400-dpi leaf 7 and enlarged top, middle and bottom bands. Read conditions i–ii, the full construction of the Koszul complex, the unnumbered paired comparison, (3.3)–(3.4), and the final omitted-verification sentence.

Both layers now retain the print's cohomologie in the first Koszul paragraph: changing this to homologie merely imposes a terminology distinction the author is not maintaining here. Restored underlining of libre, absence of a period after condition i, absent tensor subscripts A in three places, the single paired display joined by et, and absence of display-terminal punctuation. All typed letters are upright. These changes preserve the author's conventions; no original mathematical error is asserted. Every sign in the Koszul degrees and augmentation was enlarged. The proof gap concerning multilinearity remains for the notes stage. Final second reading and PDF checks pending.''')
