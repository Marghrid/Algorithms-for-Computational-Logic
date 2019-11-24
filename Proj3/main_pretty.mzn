
set of int: NODES=1..N;
set of int: FEATURES=1..K;

array[NODES] of var bool: v; % v[i] is true iff i is a leaf
array[NODES] of var bool: c; % c[i]
array[NODES] of var 0..N: l; % l[i] = j iff node i has node j as the left child, j in LR(i), i = 1,...,N
array[NODES] of var 0..N: r; % r[i] = j iff node i has node j as the left child, j in LR(i), i = 1,...,N
array[NODES] of var 0..N-2: p; % p[i] 

array[NODES] of var 0..K: a;
% d0[i] is a set of all the features that have been discriminated against 0 in node i
array[NODES] of var set of 1..K: d0; 
% d1[i] is a set of all the features that have been discriminated against 1 in node i
array[NODES] of var set of 1..K: d1;

array[NODES] of var 1..N: not_v_sum;

constraint (not v[1]);
constraint (not_v_sum[1] = 1);
constraint forall(i in 2..N)(not_v_sum[i] == not_v_sum[i-1] + (if v[i] then 0 else 1 endif));

constraint forall(i in NODES)(v[i] <-> (l[i] == 0));
constraint forall(i in NODES)(not v[i] -> ((l[i] == 2*not_v_sum[i]) /\ (p[l[i]] == i)));

constraint forall(i in NODES)(v[i] <-> (r[i] == 0));
constraint forall(i in NODES)(not v[i] -> ((r[i] == 2*not_v_sum[i]+1) /\ (p[r[i]] == i)));

constraint forall(f in FEATURES) (
  not (f in d0[1]) /\ not (f in d1[1])
);
constraint forall(j in 2..N)(
  d0[j] == (d0[p[j]] union if j == r[p[j]] then {a[p[j]]} else {} endif)
);
constraint forall(j in 2..N)(
  d1[j] == (d1[p[j]] union if j == l[p[j]] then {a[p[j]]} else {} endif)
);
 
% For a non-leaf node j, one feature is used (10)
constraint forall(j in NODES)((not v[j]) -> (a[j] > 0));

% For a leaf node j, no feature is used (11)
constraint forall(j in NODES)(v[j] -> (a[j] == 0));

