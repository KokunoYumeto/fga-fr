"""Construct the provisional printed layer from the supplied release records.
Every reversal still needs an in-order decision against its scan image.
"""
from audit_utils import read,replace,footnotes
PREFIX='Construction from the supplied release disposition FGA-CANON-ERR-'
def revert(ex,page,num,needle,changes):
    rel=f'sources/fr_printed/fr/{ex}.tex'; s=read(rel)
    fs=[(a,b,t) for a,b,t in footnotes(s) if needle in t]
    if len(fs)>1: raise ValueError((num,len(fs),needle))
    if fs:
        a,b,_=fs[0]
        replace(rel,s[a:b],'','French as printed',f'{ex}-{page}','pending scan line',f'FGA-CANON-ERR-{num:04}',PREFIX+f'{num:04}: remove its editorial footnote from the printed layer. Scan comparison pending; not a confirmed reading.',kind='structure')
    for old,new in changes:
        replace(rel,old,new,'French as printed',f'{ex}-{page}','pending scan line',f'FGA-CANON-ERR-{num:04}',PREFIX+f'{num:04}: restore the recorded printed preimage. Scan comparison pending; not a confirmed reading.')
revert(212,109,1,'puissance fibrée',[(r'$n$-ième de $(R,p_1)$ sur $X$',r'$(n+1)$-ième de $(R,p_1)$ sur $X$'),(r'K_0=X,\qquad',r'K_0=R,\qquad')])
revert(221,251,2,'déterminant « des »',[('transforment encore des ensembles limités','transforment encore ensembles limités')])
revert(221,251,3,'coupe au morceaux',[('coupe en morceaux','coupe au morceaux')])
revert(221,252,4,"inverse les deux termes extrêmes",[(r"0\longrightarrow\mathcal G'_{T_1}\longrightarrow\mathcal G''"+"\n"+r"\longrightarrow\mathcal G_{T_1}\longrightarrow0",r"0\longrightarrow\mathcal G_{T_1}\longrightarrow\mathcal G''"+"\n"+r"\longrightarrow\mathcal G'_{T_1}\longrightarrow0")])
revert(221,253,5,'singulier « classe »',[('famille limitée de classes de faisceaux','famille limitée de classe de faisceaux')])
revert(221,259,6,"l'article « les »",[('transforme les Modules','transforme Modules')])
revert(221,262,7,'localisation homogène',[(r'modules localisés de $N_*$',r'modules localisés de $N$')])
revert(221,263,8,"l'ouvert qui vient d'être défini",[(r"remplacer $S$ par l'ouvert $U_\infty$",r"remplacer $S$ par l'ouvert $U$")])
revert(221,264,9,"qui n'est défini qu'à la phrase suivante",[(r'sous-schémas fermés de $S$, donc',r'sous-schémas fermés de $Z$, donc')])
revert(221,266,10,'féminin « telle »',[("(tel qu'il s'introduit","(telle qu'il s'introduit")])
revert(221,267,11,'le point quantifié',[(r"$\mathcal G_{s'}$ ($s'\in S'$)",r"$\mathcal G_s$ ($s'\in S'$)")])
revert(221,267,12,'corps résiduel',[(r"« sur $k(s')$ »",r'« sur $k(s)$ »')])
revert(221,267,13,'correction intermédiaire',[(r"des $S'$-intersections complètes",r'des $k$-intersections complètes')])
revert(221,267,14,"incompatible avec l'identité affichée",[(r'le cas de $\operatorname{Hom}_S(X,Y)$',r'le cas de $\operatorname{Hom}_S(X,X)$')])
revert(221,267,15,'les graphes considérés',[(r"l'ensemble des sous-préschémas $\Gamma$ de $Z'$",r"l'ensemble des sous-préschémas $\Gamma$ de $Z$")])
revert(221,267,16,'Dans les six occurrences',[(r"([3], IV) sur $S'$,",r'([3], IV) sur $S$,'),(r"normal sur $S'$ (i.e.",r'normal sur $S$ (i.e.'),(r"locales dans $X'$ relativement",r'locales dans $X$ relativement'),(r"relativement à $S'$ (i.e.",r'relativement à $S$ (i.e.'),(r"dans les $X'_{s'}$",r"dans les $X_{s'}$")])
revert(221,268,17,'pluriel « Soient »',[(r'Soit $\mathcal L$ (resp. $\mathcal M$)',r'Soient $\mathcal L$ (resp. $\mathcal M$)')])
