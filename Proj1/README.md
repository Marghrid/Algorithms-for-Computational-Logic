# Project 1: Encoding Decision Trees with SAT

## Run:

`$ python3 proj1.py < <sample_file>`

Example:

`$ python3 proj1.py < t6_sat/t_1_6_7.smp`

## About

This goal of this project is to build a tool that constructs a binary decision tree that correctly classifies a set of inputs by encoding the problem into SAT. The encoding used is the one described in the paper [Learning Optimal Decision Trees with SAT](https://www.ijcai.org/proceedings/2018/189) by Narodytska et al. in IJCAI'18. Several variations of this encoding (that did not compromise the correctness of the resulting tree) were tested:

1. Try pairwise encoding instead of sequential encoding for cardinality constraints
2. In constraints 4 and 10, remove the implication in the "<=1" part of the constraint
3. Remove all "u" variables and respective constraints

We concluded that pairwise encoding was faster than the sequential counter encoding for the vast majority of our instances. Even though sequential counter encoding yielded much better results when we added the alteration described in 2., pairwise encoding still outperformed it. We believe this is the case because pairwise encoding allows the solver to simplify clauses using subsumption in a preprocessing step, while sequential counter, with the addition of auxiliary variables, reduces the solver's ability to apply these improvements.
The removal of "u" variables and respective constraints did not prove benefitial either: Even though in some instances it produced a significant speedup (up to 2x), in others it doubled the running time. 

In the final solution, we did applied only the first of the described alterations: we used pairwise encoding to encode all cardinality constraints.

## Check correctness:

### For 1 sample:

`python proj1.py < t6_sat/t_10_6_7.smp |  python3 chk.py  t6_sat/t_10_6_7.smp`

### For all samples:
`./chk_all.sh "./proj1.py" t6_sat`

`./chk_all.sh "./proj1.py" t6_unsat`

`./chk_all.sh "./proj1.py" my_instances`

`./chk_all.sh "./proj1.py" my_instances_unsat`

Note the last two commands may take a long time to finish

## Solvers:

On the folder `solvers` there are Linux 64 bits executables for some solvers, most of which participated in the [SAT Race 2019](http://sat-race-2019.ciirc.cvut.cz/index.php) - [view results](http://sat-race-2019.ciirc.cvut.cz/index.php?cat=results).

 - MapleLCMDiscChronoBT-DL-v3 - [get](http://sat-race-2019.ciirc.cvut.cz/solvers/MapleLCMDiscChronoBT-DL-v3.zip)
 
 - [CaDiCal](https://github.com/arminbiere/cadical) - [get](http://sat-race-2019.ciirc.cvut.cz/solvers/CaDiCaL.zip)

 - MapleCBTCoreFirst - [get](http://sat-race-2019.ciirc.cvut.cz/solvers/MapleLCMdistCBTcoreFirst.zip)
 
 - optsat - [get](http://sat-race-2019.ciirc.cvut.cz/solvers/optsat.zip)
 
 - [cryptominisat](https://github.com/msoos/cryptominisat) - [get](http://sat-race-2019.ciirc.cvut.cz/solvers/cmsatv56-walksat.zip)
 
 - [MergeSAT](https://github.com/conp-solutions/mergesat) - [get](http://sat-race-2019.ciirc.cvut.cz/solvers/MergeSAT.zip)
 
 - smallsat - [get](http://sat-race-2019.ciirc.cvut.cz/solvers/smallsat.zip)
 
 - [lingeling](https://github.com/arminbiere/lingeling) - [get](http://fmv.jku.at/lingeling/lingeling-bcj-78ebb86-180517.tar.gz)
 
 - [Glucose4](https://www.labri.fr/perso/lsimon/glucose/) - [get](http://sat-race-2019.ciirc.cvut.cz/solvers/glucose-4.2.1.zip)
 
 In the end, CaDiCal performed best in most instances.
 
 ## Generate instances:
 
 Set desired samples' parameters on file `generate_instances.py`:
 - `min_n_feats`: minimum number of features for inputs.
 - `max_n_feats`: maximum number of features for inputs.
 - `int_n_feats`: interval between number of features generated in consecutive iterations.
 - `num_threads`: maximum number of threads running at a time.
 - `inputs_dir`: Path to directory where inputs (no header) should be stored.
 - `samples_dir`: Path to directory where samples (complete instances) should be stored.
 
After these parameters are set, run the script with
 
`python3 generate_instances.py`
 
The script will first generate inputs without header according to the parameters specified, and store these in files in the directory specified in `inputs_dir`.
 
Then, for each set of inputs, the script will call the solver (`proj1.py`) repeatedly to find the optimal (minimum) number of nodes required to generate a decision tree that is consistent with all inputs.
 
Finally, the sample will be stored in a file in the directory specified in `samples_dir`.
