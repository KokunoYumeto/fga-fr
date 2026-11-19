"""Exact integer-matrix witness for 190, p. 302(ii), with p_ij=(p_i,p_j).
For phi(i,j)=g_j g_i^{-1}, take g_1=I, g_2=A, g_3=B.
This tests the printed product order, not a general descent theorem.
"""
def mul(a,b):
 return tuple(tuple(sum(a[i][k]*b[k][j] for k in range(2)) for j in range(2)) for i in range(2))
A=((1,1),(0,1)); Ai=((1,-1),(0,1))
B=((1,0),(1,1)); Bi=((1,0),(-1,1))
I=((1,0),(0,1))
assert mul(A,Ai)==I and mul(B,Bi)==I
p31=Bi; p32=mul(A,Bi); p21=Ai
printed=mul(p32,p21); corrected=mul(p21,p32)
assert printed!=p31 and corrected==p31
print('p31 =',p31)
print('printed p32*p21 =',printed)
print('corrected p21*p32 =',corrected)
