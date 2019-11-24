%run solver
solve satisfy;

% left and right child defined only for internal nodes
output [ "l \(i) \(l[i])\n" | i in NODES where not fix(v[i])];
output [ "r \(i) \(r[i])\n" | i in NODES where not fix(v[i])];

% a defined for internal nodes 
output [ "a \(a[i]) \(i)\n" | i in NODES where not fix(v[i])];
% c defined for leaves
output [ "c \(i) \(if c[i] then 1 else 0 endif)\n" | i in NODES where fix(v[i])] ;

output [ "\(p)\n"];
output [ "\(r)\n"];
output [ "\(l)\n"];

% watch out for the 'fix' application
%output [ "true xs:" ] ++ [ " \(i)" | i in NODES where fix(x[i]) ] ++ ["\n"];
