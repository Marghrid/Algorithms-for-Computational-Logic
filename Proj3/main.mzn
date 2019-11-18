% fixed sets
set of int: NODES=1..n;
set of int: FEATURES=1..k;

% example declarations of arrays if variables
array[NODES] of var bool: x;
array[NODES] of var bool: y;
array[NODES] of var FEATURES: s;

% example constraints
constraint forall(i in NODES)(x[i] \/ y[i]);
constraint forall(i in NODES)(not x[i] \/ not y[i]);
constraint forall(i in NODES)(x[i] \/ s[i] > i);
constraint forall(i in NODES)(not x[i] \/ s[i] < i);

