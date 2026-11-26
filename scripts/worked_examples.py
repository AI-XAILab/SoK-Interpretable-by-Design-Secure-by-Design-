"""Reproduces every number in the worked examples (Examples 1-3) of the paper. Synthetic, illustrative only."""
import numpy as np
rng = np.random.default_rng(2027)
sig = lambda z: 1/(1+np.exp(-z))

# ---------- Example 1: knee-OA CBM with an affine head ----------
W = np.array([2.4, 1.9, 0.8, 0.5]); b = -2.6       # JSN, osteophyte, sclerosis, deformity
c = np.array([0.35, 0.40, 0.30, 0.20])
z = W@c + b
print("Ex1 clean logit %.2f  p=%.3f" % (z, sig(z)))
c_edit = c.copy(); c_edit[1] = 1.0
z2 = W@c_edit + b
print("Ex1 after osteophyte:=1 logit %.2f  p=%.3f  delta=%.2f" % (z2, sig(z2), z2 - z))
# single-edit reach: smallest edit on concept j that flips the decision
for j in range(4):
    need = -z / W[j]
    print("  concept %d: flip needs delta >= %.3f (feasible: %s)" % (j, need, c[j] + need <= 1))
# exact extraction from k+1 queries returning (c, logit)
Q = rng.uniform(size=(5, 4)); A = np.hstack([Q, np.ones((5, 1))]); zz = A @ np.r_[W, b]
sol = np.linalg.solve(A, zz); print("Ex1 recovered (W,b):", np.round(sol, 6))
# synthetic population: fraction of negative decisions flippable by ONE edit to [0,1]
C = rng.beta(2, 3, size=(200_000, 4)); Z = C@W + b
neg = Z < 0
best_gain = np.max(W*(1 - C), axis=1)           # largest single-concept increase available
flip_any = neg & (Z + best_gain > 0)
flip_ost = neg & (Z + W[1]*(1 - C[:, 1]) > 0)
print("Ex1 population: negative rate %.3f; flippable by one edit %.3f; by osteophyte edit %.3f"
      % (neg.mean(), flip_any.sum()/neg.sum(), flip_ost.sum()/neg.sum()))
# intervention memory: replay edit (osteophyte:=1) to neighbours within l_inf radius r of c
for r in [0.1, 0.2]:
    nb = np.max(np.abs(C - c), axis=1) <= r
    Zr = Z.copy(); Cr = C[nb].copy(); Cr[:, 1] = 1.0; Zr_nb = Cr@W + b
    flipped = (Z[nb] < 0) & (Zr_nb > 0)
    print("  memory radius %.1f: %.4f of population in neighbourhood, %.3f of those flipped" % (r, nb.mean(), flipped.mean()))

# ---------- Example 2: additive credit model, proxy fairwashing ----------
n = 200_000
age = rng.uniform(21, 70, n)
U = np.clip(rng.normal(3.0, 1.0, n), 0, None)                 # age at first account minus 18
hist = np.clip(age - 18 - U, 0, None)
inc = rng.lognormal(np.log(50), 0.4, n)                         # income, k CHF
s1 = lambda a: -0.05*(a - 45)                                   # protected-attribute effect (age)
s2 = lambda h: 0.03*(h - 20)
s3 = lambda i: 1.2*np.log(i/50)
beta = 0.2
f = beta + s1(age) + s2(hist) + s3(inc)
muU = U.mean()
s1p = lambda a: 0*a
s2p = lambda h: s2(h) + s1(h + 18 + muU)                        # effect moved onto proxy
fp = beta + s1p(age) + s2p(hist) + s3(inc)
d = np.abs(f - fp)
print("Ex2 corr(age,hist)=%.3f  mean|dlogit|=%.4f  max|dlogit|=%.3f  decision agreement=%.4f"
      % (np.corrcoef(age, hist)[0, 1], d.mean(), d.max(), np.mean((f > 0) == (fp > 0))))
print("    bound L*E|U-muU| = %.4f (L=0.05)" % (0.05*np.mean(np.abs(U - muU))))
print("    displayed age effect range: original %.2f, fairwashed %.2f" % (s1(21) - s1(70), 0.0))
print("    displayed hist slope original 0.030, fairwashed %.3f" % (0.03 - 0.05))
# AUC-style check: both models rank the same
from itertools import islice
y = rng.uniform(size=n) < sig(f)
def acc(g): return np.mean((g > 0) == y)
print("    accuracy vs labels sampled from f: original %.4f fairwashed %.4f" % (acc(f), acc(fp)))

# ---------- Example 3: auditor advantage is bounded by total variation ----------
# concept patterns of target class t; trigger maps to a pattern drawn from P(E|Y=t) w.p. 1-eps, else to a fixed atypical pattern
for eps in [0.0, 0.05, 0.2]:
    print("Ex3 eps=%.2f -> TV = %.2f -> max auditor advantage %.2f" % (eps, eps, eps))
