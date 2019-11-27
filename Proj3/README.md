# Project 3: Encoding Decision Trees with CSP

## Run:

`$ python3 proj3.py < <sample_file>`

Example:

`$ python3 proj3.py < t6_sat/t_1_6_7.smp`

## Encoding:

This goal of this project is to build a tool that constructs a binary decision tree that correctly classifies a set of inputs by encoding the problem into CSP. The encoding used is based on the SAT encoding described in the paper [Learning Optimal Decision Trees with SAT](https://www.ijcai.org/proceedings/2018/189) by Narodytska et al. in IJCAI'18. We replaced some of the boolean variables with integer or set of integer variables. We also included the additional inference constraints described in section 3.3 of this article.

### Variables:
To encode the problem of finding a fitting decision tree with N nodes fo fit inputs with K features the following variables were used:

**Boolean**:
- v(i) = True iff node i is a leaf node, i = 1,...,N

- c(i) = True iff class of leaf node i is 1, i = 1,...,N.

**Set of Integers**:
- d0(j) = the set of features that are discriminated for value 0 by node j, or by one of its ancestors, j = 1,...,N,

- d1(j) = the set of features that are discriminated for value 1 by node j, or by one of its ancestors, j = 1,...,N,

**Integer**:
- r(i) = j iff node i has node j as the right child, i = 1,...,N, j in odd( [ i + 2; min(2i + 1, N) ] )

  r(i) = 0 iff i is a leaf (does not have any children)
  
- l(i) = j iff node i has node j as the left child, i = 1,...,N, j in even( [ i + 1; min(2i, N - 1) ] )

  l(i) = 0 iff i is a leaf (does not have any children)
  
- p(j) = i iff the parent of node j is node i, j = 2,...,N, i = 1,...,N

  p(j) = 0 for node 1, as it has no parent.

- a(i) = r iff feature r is assigned to node i, r = 1,...,K, i = 1,...,N

  a(i) = 0 iff i is a leaf (has no feature assigned)

- not_v_sum(i) = t iff up to (and including) node i, there are t non-leaf nodes, t = ceil(i/2)+1,...,i, i = 1,...,N

## Search:
In order to find the minimum number of nodes required to build a decision tree consistent with all the inputs, i.e. the optimal solution, we experimented with the following search techniques:

 - UNSAT-SAT search
 
 - SAT-UNSAT search
 
 - Binary search
 
For all search tecnhiques, the lower bound was set to 3 nodes and the upper bound was set to the number of nodes in the solution returned by applying the ID3 algorithm to the set of inputs. ID3 always produces a valid decision tree but it might not be optimal, therefore we know that the optimal number of nodes is certainly lower or equal to that of a tree returned by ID3. When ID3 returns a solution of cost N, and the SMT call for N-2 is UNSAT, we conclude the ID3 solution is optimal and return it.

Our experiments showed Binary search to be the fastest in most cases, closely followed by UNSAT-SAT search.

## Minizinc:
We used [Minizinc](https://www.minizinc.org/) coupled with the following solvers:

- Chuffed

- CPLEX

- Gecode

Chuffed outperformed the others.

-----
## Authors:

83422, [Amândio Faustino](https://github.com/Nandinski)

80832, [Margarida Ferreira](https://github.com/Marghrid)

