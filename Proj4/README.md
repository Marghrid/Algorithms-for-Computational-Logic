# Project 4: Encoding Decision Trees with ASP

## Run:

`$ python3 proj4.py < <sample_file>`

Example:

`$ python3 proj4.py < t6_sat/t_1_6_7.smp`

## Encoding:

This goal of this project is to build a tool that constructs a binary decision tree that correctly classifies a set of inputs by encoding the problem into CSP. The encoding used is loosely based on the SAT encoding described in the paper [Learning Optimal Decision Trees with SAT](https://www.ijcai.org/proceedings/2018/189) by Narodytska et al. in IJCAI'18. We replaced some of the boolean variables with integer variables. We also included the additional inference constraints described in section 3.3 of this article.

### Variables:
To encode the problem of finding a fitting decision tree with N nodes fo fit inputs with K features the following variables were used:

- v(i) = True iff node i is a leaf node, i = 1,...,N

- c(i, t) = True iff class of leaf node i is t, i = 1,...,N, t in {0,1}

- d0(r, j) = True iff feature r is discriminated for value 0 by node j, or by one of its ancestors, j = 1,...,N,

- d1(r, j) = True iff feature r is discriminated for value 1 by node j, or by one of its ancestors, j = 1,...,N,

- r(i,j) iff node i has node j as the right child, i = 1,...,N, j in odd( [ i + 2; min(2i + 1, N) ] )

- l(i,j) iff node i has node j as the left child, i = 1,...,N, j in even( [ i + 1; min(2i, N - 1) ] )

- p(j,i) iff the parent of node j is node i, j = 2,...,N, i = 1,...,N

- a(r,i) iff feature r is assigned to node i, r = 1,...,K, i = 1,...,N

- not_v_sum(i,s) iff up to (and including) node i, there are s non-leaf nodes, s = ceil(i/2)+1,...,i, i = 1,...,N


## Solver:

The encoding was then fed to [clingo solver](https://potassco.org/clingo/), which was run with the following command line options:

`clingo -n1 --configuration=handy --heuristic=Berkmin'`

## Search:
In order to find the minimum number of nodes required to build a decision tree consistent with all the inputs, i.e. the optimal solution, we experimented with the following search techniques:

 - UNSAT-SAT search
 
 - SAT-UNSAT search
 
 - Binary search
 
For all search tecnhiques, the lower bound was set to 3 nodes and the upper bound was set to the number of nodes in the solution returned by applying the ID3 algorithm to the set of inputs. ID3 always produces a valid decision tree but it might not be optimal, therefore we know that the optimal number of nodes is certainly lower or equal to that of a tree returned by ID3. When ID3 returns a solution of cost N, and the SMT call for N-2 is UNSAT, we conclude the ID3 solution is optimal and return it.

Our experiments showed all 3 seacrhes to be almost equaly fast. We applied SAT-UNSAT search.

-----
## Authors:

83422, [Amândio Faustino](https://github.com/Nandinski)

80832, [Margarida Ferreira](https://github.com/Marghrid)
