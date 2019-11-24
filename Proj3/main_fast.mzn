%int: N = 5;
%int: K = 2;

% fixed sets
set of int: NODES=1..N;
set of int: FEATURES=1..K;

array[NODES] of set of int: LR = [ {k | k in (i+1)..(min(2*i, N-1)) where k mod 2 == 0} | i in NODES ];
array[NODES] of set of int: RR = [ {k | k in (i+2)..(min(2*i+1, N)) where k mod 2 == 1} | i in NODES ];

% example declarations of arrays if variables
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

% l[i] in LR[i]
constraint forall(i in NODES)(v[i] <-> (l[i] == 0)); %TODO
constraint forall(i in NODES)(not v[i] -> (l[i] in LR[i]));

% r[i] in RR[i]
constraint forall(i in NODES)(v[i] <-> (r[i] == 0));
constraint forall(i in NODES)(not v[i] -> (r[i] in RR[i]));


constraint forall(i in NODES)(p[i] <= i-1);
constraint forall(i in NODES)(p[i] >= i div 2);

% the left child and the right child of node i are numbered consecutively or they are both zero (3)
constraint forall(i in NODES)((l[i] == 0 /\ r[i] == 0)\/(r[i] == l[i]+1)); % (l_i = 0 and r_i = 0) or (r_i = l_i+1)

% if node i is a parent then it has a child (5)
constraint forall(i in 2..N) (
  forall(j in LR[i]) (
    p[j] = i <-> l[i] = j
  )
);
constraint forall(i in NODES) (  
  forall(j in RR[i]) (
    p[j] = i <-> r[i] = j
  )
);

% SEMANTICS
% (7) and (8)

% The root node does not discriminate any feature
constraint forall(f in FEATURES) (
  not (f in d0[1]) /\ not (f in d1[1])
);
/*
constraint forall(f in FEATURES) (
  forall(j in 2..N)(
    (f in d0[j]) <-> exists(i in (j div 2)..(j-1))(
                           (f in d0[p[j]] \/ ((a[i] == f) /\ (r[i] == j))) 
    )
  )
);
*/

constraint forall(j in 2..N)(
  d0[j] == (d0[p[j]] union if j in RR[p[j]] then {a[p[j]]} else {} endif)
 );
 /*
constraint forall(f in FEATURES) (
  forall(j in 2..N)(
    (f in d1[j]) <-> exists(i in (j div 2)..(j-1))(
                           (f in d1[p[j]] \/ ((a[i] == f) /\ (l[i] == j))) 
    )
  )
);
*/

constraint forall(j in 2..N)(
  d1[j] == (d1[p[j]] union if j in LR[p[j]] then {a[p[j]]} else {} endif)
 );
 
% For a non-leaf node j, one feature is used (10)
constraint forall(j in NODES)((not v[j]) -> (a[j] > 0));

% For a leaf node j, no feature is used (11)
constraint forall(j in NODES)(v[j] -> (a[j] == 0));

