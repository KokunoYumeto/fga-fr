"""Exact matrix witnesses for 190, p. 311, nonabelian cocycles."""
from itertools import product
def mul(a,b):
 return tuple(tuple(sum(a[i][k]*b[k][j] for k in range(2)) for j in range(2)) for i in range(2))
def inv(a):
 assert a[0][0]*a[1][1]-a[0][1]*a[1][0]==1
 return ((a[1][1],-a[0][1]),(-a[1][0],a[0][0]))
I=((1,0),(0,1)); A=((1,1),(0,1)); B=((1,0),(1,1))
def coboundary(h):
 return {(i,j):mul(h[j],inv(h[i])) for i,j in product(range(len(h)),repeat=2)}
def corrected(g,n):
 return all(g[(k,i)]==mul(g[(j,i)],g[(k,j)]) for i,j,k in product(range(n),repeat=3))
def printed(g,n):
 return all(g[(k,i)]==mul(g[(k,j)],g[(j,i)]) for i,j,k in product(range(n),repeat=3))
g=coboundary([I,A,B])
assert corrected(g,3) and not printed(g,3)
a=coboundary([I,A]); b=coboundary([I,B])
assert corrected(a,2) and corrected(b,2)
ab={ij:mul(a[ij],b[ij]) for ij in a}
assert not corrected(ab,2)
print('Gauge transform of the identity obeys corrected cocycle order and fails printed order.')
print('Two cocycles on a two-point cover have a pointwise product that is not a cocycle.')
print('Product at (1,0)*(0,1):',mul(ab[(1,0)],ab[(0,1)]))
