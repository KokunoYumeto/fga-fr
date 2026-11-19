from audit_utils import replace,page_text,read,write
import re
for folder,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
    rel=f'sources/{folder}/fr/149.tex'
    replace(rel,'\\unimathsetup{math-style=upright}\n\\makeatletter\\tagsleft@true\\makeatother\n','',layer,'149-169','before first text','','Withdraw the initial global style switch: installed unicode-math code does not guarantee local remapping after font setup. Use explicit upright alphabets instead.',kind='typesetting',full=True)
    replace(rel,'\\unimathsetup{math-style=TeX}\n\\makeatletter\\tagsleft@false\\makeatother','',layer,'149-169','end of page','','Remove the matching reset of the withdrawn style switch.',kind='typesetting')
    s,_,_=page_text(rel,169)
    distinct=list(dict.fromkeys(re.findall(r'(?<!\\)\$([^$]+)\$',s)))
    for expr in distinct:
        count=s.count('$'+expr+'$')
        replace(rel,'$'+expr+'$',r'$\symup{'+expr+'}$',layer,'149-169','inline mathematical letters','1','The 400-dpi image and enlarged crops show upright typed variables; explicit symup preserves nested script, roman operators and sheaf underlines.',kind='reading',count=count)
    replacements=[
      (r'h_A(B)=\operatorname{Hom}_{\Osh}(X;A,B)',r'\symup{h_A(B)=\operatorname{Hom}_{\Osh}(X;A,B)}'),
      (r'\hsh_A(B)=\Homsh_{\Osh}(A,B)',r'\symup{\hsh_A(B)=\Homsh_{\Osh}(A,B)}'),
      (r'\operatorname{Ext}_{\Osh}^{p}(X;A,B)'+'\n  &= (R^{p}h_A)(B)\n   = H^{p}'+r'\bigl(\operatorname{Hom}_{\Osh}(X;A,C(B))\bigr)',r'\symup{\operatorname{Ext}_{\Osh}^{p}(X;A,B)}'+'\n  &= '+r'\symup{(R^{p}h_A)(B)'+'\n   = H^{p}'+r'\bigl(\operatorname{Hom}_{\Osh}(X;A,C(B))\bigr)}'),
      (r'\Extsh_{\Osh}^{p}(A,B)'+'\n  &= (R^{p}'+r'\hsh_A)(B)'+'\n   = H^{p}'+r'\bigl(\Homsh_{\Osh}(A,C(B))\bigr)',r'\symup{\Extsh_{\Osh}^{p}(A,B)}'+'\n  &= '+r'\symup{(R^{p}\hsh_A)(B)'+'\n   = H^{p}'+r'\bigl(\Homsh_{\Osh}(A,C(B))\bigr)}')]
    for old,new in replacements:
        replace(rel,old,new,layer,'149-169','displayed formulae','(1.1)-(1.2)','The formula crops show upright typed variables; explicit symup on each alignment cell preserves script and underline distinctions.',kind='reading')
    replace(f'sources/{folder}/fr/main.tex','[11pt,twoside,openany]','[11pt,twoside,openany,leqno]',layer,'149-169','equation labels','(1.1)-(1.2)','Printed equation numbers are on the left. The standard leqno document-class option initializes all amsmath tag machinery consistently; first observed on p. 169, to be checked on subsequent pages.',kind='typesetting',full=True)
s=read('CHECK_RECORD.md')
s=s.replace('The page-specific controls set typed mathematical variables upright and put equation labels on the left; explicit script and underlined alphabets remain distinct. They explicitly restore the supplied default settings after this page because unicode-math style options use global assignments.', 'The initial global font-policy controls were withdrawn after inspection of installed unicode-math/amsmath code showed that they did not safely implement the intended behavior. Explicit `\\symup` now gives upright variables on this page while preserving script and underlined alphabets. The standard `leqno` class option initializes left equation labels. The ledger retains the attempted changes and their withdrawal; totals must therefore distinguish operations from final differences.')
write('CHECK_RECORD.md',s)
