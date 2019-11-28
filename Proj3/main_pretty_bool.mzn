include "alldifferent_except_0.mzn";
include "count.mzn";

set of int: NODES=1..N;
set of int: FEATURES=1..K;

array[NODES] of var bool: v; % v[i] is true iff i is a leaf
array[NODES] of var bool: c; % c[i]
array[NODES] of var 0..N: l; % l[i] = j iff node i has node j as the left child, j in LR(i), i = 1,...,N
array[NODES] of var 0..N: r; % r[i] = j iff node i has node j as the left child, j in LR(i), i = 1,...,N
array[NODES] of var 0..N-2: p; % p[i] 

array[NODES] of var 0..K: a;
array[FEATURES,NODES] of var bool: d0;
array[FEATURES,NODES] of var bool: d1;

array[NODES] of var 1..(N div 2): not_v_sum;

% 1 is not a leaf
constraint (not v[1]);

% define not_v_sum
constraint (not_v_sum[1] = 1);
constraint forall(i in 2..N) (not_v_sum[i] == not_v_sum[i-1] + not v[i]);

% if node is leaf, it has no left or right child
constraint forall(i in NODES)(v[i] <-> (l[i] == 0));
constraint forall(i in NODES)(v[i] <-> (r[i] == 0));

% number left and right children
constraint forall(i in NODES)(not v[i] -> ( (l[i] == 2*not_v_sum[i]) /\ (p[l[i]] == i) ) );
constraint forall(i in NODES)(not v[i] -> ( (r[i] == 2*not_v_sum[i]+1) /\ (p[r[i]] == i) ) );

constraint forall(r in FEATURES)(not d0[r,1]);
constraint forall(r in FEATURES)(not d1[r,1]);

constraint forall(f in FEATURES)(forall(j in 2..N)(
  d0[f, j] <-> d0[f, p[j]] \/ 
  (if j = r[p[j]] then (a[p[j]] == f) else false endif)
));

constraint forall(f in FEATURES)(forall(j in 2..N)(
  d1[f, j] <-> d1[f, p[j]] \/ (if j = l[p[j]] then (a[p[j]] == f) else false endif)
));
 
% For a non-leaf node j, one feature is used (10)
constraint forall(j in NODES)( (not v[j]) -> (a[j] > 0) );

% For a leaf node j, no feature is used (11)
constraint forall(j in NODES)( v[j] -> (a[j] == 0) );

