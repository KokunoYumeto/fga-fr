"""An exact polynomial certificate for the example checked at 190-306.

Over k=Q let B=k[t]/(t^8), A=span(1,t^4,t^5,t^6),
and E=span(1,t^4,t^5,t^6,t^7). All are subrings.
The additional equalizer element t^7 follows from the identity below.
The argument about degrees <4 and the geometric consequences are in
CHECK_EVENTS.tsv; this script certifies the displayed polynomial identity.
"""
from collections import defaultdict

def add(*polynomials):
    out = defaultdict(int)
    for p in polynomials:
        for m, c in p.items():
            out[m] += c
    return {m: c for m, c in out.items() if c}

def mul(p, q):
    out = defaultdict(int)
    for (a, b), c in p.items():
        for (d, e), f in q.items():
            out[(a+d, b+e)] += c*f
    return {m: c for m, c in out.items() if c}

def delta(n):
    return {(n, 0): 1, (0, n): -1}

right = add(mul({(1, 0): 1, (0, 1): 1}, delta(6)),
            mul({(1, 1): -1}, delta(5)))
assert right == delta(7)
print('Verified: x^7-y^7=(x+y)(x^6-y^6)-xy(x^5-y^5).')
print('Thus t^7 lies in Eq(B => B tensor_A B), although t^7 is not in A.')
