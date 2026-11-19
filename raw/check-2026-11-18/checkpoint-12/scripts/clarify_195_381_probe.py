from audit_utils import *
old='A representable scheme functor is injective on an injection of test algebras: Spec of the larger algebra is schematically dominant over Spec of the smaller, so two maps agreeing after it agree. Apply this to square-zero A-algebras A plus M to A plus N induced by an injection M to N.'
new='Use square-zero A-algebras A plus M to A plus N induced by an injection M to N. Their spectra have the same underlying topological space Spec(A), and the map of structure sheaves is injective on every distinguished open. Two maps from Spec(A plus M) to any scheme agreeing after Spec(A plus N) have the same underlying map and can be compared in the same affine target neighborhoods, where injectivity of the ring maps proves equality. This argument is specific to the square-zero probes; injectivity for arbitrary injections of test algebras is not asserted.'
p=ROOT/'CHECK_EVENTS.tsv'
with p.open(newline='') as f:
 rows=list(csv.reader(f,delimiter='\t'))
n=0
for row in rows:
 if row and row[0]=='195-C2-flatness-and-finite-case':
  if old not in row[4]: raise ValueError('Expected prior proof wording')
  row[4]=row[4].replace(old,new);n+=1
if n!=1: raise ValueError(n)
with p.open('w',newline='') as f: csv.writer(f,delimiter='\t').writerows(rows)
p=ROOT/'scripts/apply_195_381.py'
s=p.read_text()
if s.count(old)!=1: raise ValueError('Expected one source wording')
p.write_text(s.replace(old,new))
event('195-C2-square-zero-probe-clarification','targeted proof check','Refined the affine flatness proof to use only injective square-zero algebra probes with the same topological spectrum. This avoids the false general claim that arbitrary injective algebra maps are epimorphic as morphisms of schemes: distinct maps into a nonseparated scheme may agree at the generic point. The actual square-zero proof is valid and is now stated in full in the earlier event.','195, p. 381, flatness-necessity check')
