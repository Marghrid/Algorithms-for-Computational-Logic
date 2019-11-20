%run solver
solve satisfy;


output [ "l \(i) \(l[i])\n" | i in NODES where not fix(v[i])];
output [ "r \(i) \(r[i])\n" | i in NODES where not fix(v[i])];
%output [ "v \(i) \(if v[i] then 1 else 0 endif)\n" | i in NODES ] ;

% watch out for the 'fix' application
%output [ "true xs:" ] ++ [ " \(i)" | i in NODES where fix(x[i]) ] ++ ["\n"];
