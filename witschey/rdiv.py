from __future__ import division
import sys
import random
import math

from log import NumberLog
import texttable
from basic_stats import xtile, median
from witschey import base

# flake8: noqa

def a12(lst1,lst2):
    "how often is x in lst1 more than y in lst2?"
    def loop(t,t1,t2): 
        while t1.j < t1.n and t2.j < t2.n:
            h1 = t1.l[t1.j]
            h2 = t2.l[t2.j]
            h3 = t2.l[t2.j+1] if t2.j+1 < t2.n else None 
            if h1>  h2:
                t1.j  += 1; t1.gt += t2.n - t2.j
            elif h1 == h2:
                if h3 and h1 > h3 :
                    t1.gt += t2.n - t2.j  - 1
                t1.j  += 1; t1.eq += 1; t2.eq += 1
            else:
                t2,t1  = t1,t2
        return t.gt*1.0, t.eq*1.0
    #--------------------------
    lst1 = sorted(lst1, reverse=True)
    lst2 = sorted(lst2, reverse=True)
    n1   = len(lst1)
    n2   = len(lst2)
    t1   = base.memo(l=lst1,j=0,eq=0,gt=0,n=n1)
    t2   = base.memo(l=lst2,j=0,eq=0,gt=0,n=n2)
    gt,eq= loop(t1, t1, t2)
    return gt/(n1*n2) + eq/2/(n1*n2)


"""## Non-Parametric Hypothesis Testing

The following _bootstrap_ method was introduced in
1979 by Bradley Efron at Stanford University. It
was inspired by earlier work on the
jackknife.
Improved estimates of the variance were [developed later][efron01].  

[efron01]: http://goo.gl/14n8Wf "Bradley Efron and R.J. Tibshirani. An Introduction to the Bootstrap (Chapman & Hall/CRC Monographs on Statistics & Applied Probability), 1993"


To check if two populations _(y0,z0)_
are different, many times sample with replacement
from both to generate _(y1,z1), (y2,z2), (y3,z3)_.. etc.

Then, for all those samples,
 check if some *testStatistic* in the original pair
hold for all the other pairs. If it does more than (say) 99%
of the time, then we are 99% confident in that the
populations are the same.

In such a _bootstrap_ hypothesis test, the *some property*
is the difference between the two populations, muted by the
joint standard deviation of the populations.

"""
def testStatistic(y,z): 
    """Checks if two means are different, tempered
     by the sample size of 'y' and 'z'"""
    s1 = y.standard_deviation()
    s2 = z.standard_deviation()
    delta = z.mean() - y.mean()
    if s1+s2:
      delta =  delta/((s1/len(y) + s2/len(z))**0.5)
    return delta
"""

The rest is just details:

+ Efron advises
  to make the mean of the populations the same (see
  the _yhat,zhat_ stuff shown below).
+ The class _total_ is a just a quick and dirty accumulation class.
+ For more details see [the Efron text][efron01].  

"""
def bootstrap(y0,z0,conf=0.01,b=1000):
    """The bootstrap hypothesis test from
       p220 to 223 of Efron's book 'An
      introduction to the boostrap."""
    y, z   = NumberLog(y0), NumberLog(z0)
    x      = NumberLog(inits=(y, z))
    tobs   = testStatistic(y,z)
    yhat   = [y1 - y.mean() + x.mean() for y1 in y.contents()]
    zhat   = [z1 - z.mean() + x.mean() for z1 in z.contents()]
    bigger = 0
    for i in range(b):
        samp_with_replacement_yhat = (random.choice(yhat) for _ in yhat)
        samp_with_replacement_zhat = (random.choice(zhat) for _ in zhat)
        different_means = testStatistic(
            NumberLog(samp_with_replacement_yhat, max_size=None),
            NumberLog(samp_with_replacement_zhat, max_size=None))
        if different_means > tobs:
            bigger += 1
    return bigger / b < conf

def different(l1,l2):
  #return bootstrap(l1,l2) and a12(l2,l1)
  return a12(l2,l1) and bootstrap(l1,l2)

"""

## Saner Hypothesis Testing

The following code, which you should use verbatim does the following:


+ All treatments are clustered into _ranks_. In practice, dozens
  of treatments end up generating just a handful of ranks.
+ The numbers of calls to the hypothesis tests are minimized:
    + Treatments are sorted by their median value.
    + Treatments are divided into two groups such that the
      expected value of the mean values _after_ the split is minimized;
    + Hypothesis tests are called to test if the two groups are truly difference.
          + All hypothesis tests are non-parametric and include (1) effect size tests
            and (2) tests for statistically significant numbers;
          + Slow bootstraps are executed  if the faster _A12_ tests are passed;

In practice, this means that the hypothesis tests (with confidence of say, 95%)
are called on only a logarithmic number of times. So...

+ With this method, 16 treatments can be studied using less than _&sum;<sub>1,2,4,8,16</sub>log<sub>2</sub>i =15_ hypothesis tests  and confidence _0.99<sup>15</sup>=0.86_.
+ But if did this with the 120 all-pairs comparisons of the 16 treatments, we would have total confidence _0.99<sup>120</sup>=0.30.

For examples on using this code, see _rdivDemo_ (below).

"""
def scottknott(data,cohen=0.3,max_rank_size=3,epsilon=0.01):
    """Recursively split data, maximizing delta of
    the expected value of the mean before and 
    after the splits. 
    Reject splits with under 3 items"""
    all  = reduce(lambda x,y:x+y,data)
    return rdiv(data,all,minMu,max_rank_size,epsilon)

def rdiv(data,  # a list of class Nums
         all,   # all the data combined into one num
         div,   # function: find the best split
         max_rank_size,   
         epsilon): # small enough to split two parts
    """Looks for ways to split sorted data, 
    Recurses into each split. Assigns a 'rank' number
    to all the leaf splits found in this way. 
    """
    def recurse(parts,all,rank=0):
        "Split, then recurse on each part."
        cut,left,right = maybeIgnore(div(parts,all,max_rank_size,epsilon),parts)
        if cut: 
            # if cut, rank "right" higher than "left"
            rank = recurse(parts[:cut],left,rank) + 1
            rank = recurse(parts[cut:],right,rank)
        else: 
            # if no cut, then all get same rank
            for part in parts: 
                part.rank = rank
        return rank
    recurse(sorted(data),all)
    return data

def maybeIgnore((cut,left,right),parts):
    if cut:
        pre = NumberLog(inits=(f for p in parts[:cut] for f in p.contents()), max_size=None)
        post = NumberLog(inits=(f for p in parts[cut:] for f in p.contents()), max_size=None)
        if not different(pre.contents(), post.contents()):
            cut = left = right = None
    return cut,left,right

def minMu(parts,all,max_rank_size,epsilon):
    """Find a cut in the parts that maximizes
    the expected value of the difference in
    the mean before and after the cut.
    Reject splits that are insignificantly
    different or that generate very small subsets.
    """
    cut,left,right = None,None,None
    before, mu     =  0, all.mean()
    for i,l,r in leftRight(parts,epsilon):
        if len(l) > max_rank_size and len(r) > max_rank_size:
            n   = len(all) * 1.0
            now = len(l)/n*(mu- l.mean())**2 + len(r)/n*(mu- r.mean())**2  
            if now > before:
                before,cut,left,right = now,i,l,r
    return cut,left,right

def leftRight(parts,epsilon=0.01):
    """Iterator. For all items in 'parts',
    return everything to the left and everything
    from here to the end. For reasons of
    efficiency, take a first pass over the data
    to pre-compute and cache right-hand-sides
    """
    rights = {}
    n = j = len(parts) - 1
    while j > 0:
        rights[j] = NumberLog(parts[j])
        if j < n:
            rights[j] += rights[j+1]
        j -=1
    left = NumberLog(parts[0])
    for i,one in enumerate(parts):
        if i> 0: 
            if parts[i].median() - parts[i-1].median() > epsilon:
                yield i,left,rights[i]
            left += one
"""

## Putting it All Together

Driver for the demos:

"""
def rdiv_report(data):
    rows = []
    def z(x):
        return int(100 * (x - lo) / (hi - lo + 0.00001))
    data = map(lambda lst:NumberLog(label=lst[0], inits=lst[1:], max_size=None),
               data)
    ranks=[]
    for x in scottknott(data):
        ranks += [(x.rank,x.median(),x)]
    all=[]
    for _,__,x in sorted(ranks): all += x.contents()
    all = sorted(all)
    lo, hi = all[0], all[-1]
    last = None
    rows.append(['rank', 'name', 'med', 'iqr', '',
                '10%', '30%', '50%', '70%', '90%'])
    for _,__,x in sorted(ranks):
        q1 = x.value_at_proportion(.25)
        q2 = x.value_at_proportion(.50)
        q3 = x.value_at_proportion(.75)
        xtile_out = xtile(x.contents(), lo=lo, hi=hi, width=30, as_list=True)
        row_xtile = [xtile_out[0]] + map(lambda x: x + ',', xtile_out[1:-1]) +\
                    [xtile_out[-1]]
        rows.append([x.rank+1] +
          map(lambda y: str(y) + ',', [x.label, q2]) + [q3 - q1] + row_xtile)
        last = x.rank
    table = texttable.Texttable(200)
    table.set_precision(2)
    table.set_cols_dtype(['t', 't', 'f', 'f', 't', 't', 't', 't', 't', 't'])
    table.set_cols_align(['r', 'l', 'r', 'r', 'c', 'r', 'r', 'r', 'r', 'r'])
    table.set_deco(texttable.Texttable.HEADER)
    table.add_rows(rows)
    return table.draw()
