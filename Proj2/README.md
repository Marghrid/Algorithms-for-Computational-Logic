# Project 2: Encoding Decision Trees with SMT

## Run:

`$ python3 proj1.py < <sample_file>`

Example:

`$ python3 proj1.py < t6_sat/t_1_6_7.smp`

## Encoding:

This goal of this project is to build a tool that constructs a binary decision tree that correctly classifies a set of inputs by encoding the problem into SMT. The encoding used is based on the SAT encoding described in the paper [Learning Optimal Decision Trees with SAT](https://www.ijcai.org/proceedings/2018/189) by Narodytska et al. in IJCAI'18.

### Variables:
To encode the problem of finding a fitting decision tree with N nodes fo fit inputs with K features the following variables were used:

**Boolean**:
- v(i) = True iff node i is a leaf node, i = 1,...,N

- c(i) = True iff class of leaf node i is 1, i = 1,...,N.

- u(r,j) = True iff feature r is being discriminated against by node j, r = 1,...,K, j = 1,...,N.

- d0(r,j) = True iff feature r is discriminated for value 0 by node j, or by one of its ancestors, r = 1,...,K, j = 1,...,N,

- d1(r,j) = True iff feature r is discriminated for value 1 by node j, or by one of its ancestors, r = 1,...,K, j = 1,...,N,

**Integer**:
- r(i) = j iff node i has node j as the right child, i = 1,...,N, j in odd( [ i + 2; min(2i + 1, N) ] )

  r(i) = 0 iff i is a leaf (does not have any children)
  
- l(i) = j iff node i has node j as the left child, i = 1,...,N, j in even( [ i + 1; min(2i, N - 1) ] )

  l(i) = 0 iff i is a leaf (does not have any children)
  
- p(j) = i iff the parent of node j is node i, j = 2,...,N, i = 1,...,N

  p(j) = 0 for node 1, as it has no parent.

- a(i) = r iff feature r is assigned to node j, r = 1,...,K, j = 1,...,N

  a(i) = 0 iff i is a leaf (has no feature assigned)

## Search:
In order to find the minimum number of nodes required to build a decision tree consistent with all the inputs, i.e. the optimal solution, we experimented with the following search techniques:

 - UNSAT-SAT search
 
 - SAT-UNSAT search
 
 - Binary Search
 
 - Progression/Progressive(?) search
 
For all search tecnhiques, the lower bound was set to 3 nodes and the upper bound was set to the number of nodes in the solution returned by applying the ID3 algorithm to the set of inputs. ID3 always produces a valid decision tree but it might not be optimal, therefore we know that the optimal number of nodes is certainly lower or equal to that of a tree returned by ID3.

Because our upper bound is always very close to the optimal number of nodes, we concluded UNSAT-SAT performed the worst for our scenario - it made the most calls to the solver.

## Solvers:

On the folder `solvers` there are Linux 64 bits executables for some SMT solvers:

 - [z3](https://github.com/Z3Prover/z3)
 - [CVC4](https://github.com/CVC4/CVC4)


## Check correctness:

### For 1 sample:

`python proj1.py < t6_sat/t_10_6_7.smp |  python3 chk.py  t6_sat/t_10_6_7.smp`

### For all samples:
`./chk_all.sh "./proj1.py" t6_sat`

`./chk_all.sh "./proj1.py" my_instances`

Note the last command may take a long time to finish

-----
## Authors:

[Amândio Faustino](https://github.com/Nandinski)

[Margarida Ferreira](https://github.com/Marghrid)
