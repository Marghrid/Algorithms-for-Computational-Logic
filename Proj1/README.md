# Project 1: Encoding Decision Trees with SAT

## Run:

`$ python3 proj1.py < <sample_file>`

Example:

`$ python3 proj1.py < t6_sat/t_1_6_7.smp`

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
