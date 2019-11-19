%run solver
solve satisfy;

% example prints
output [ "x \(i) = \(x[i])\n" | i in NODES ] ;
output [ "y \(i) = \(y[i])\n" | i in NODES ] ;
output [ "s \(i) = \(s[i])\n" | i in NODES ] ;

% watch out for the 'fix' application
output [ "true xs:" ] ++ [ " \(i)" | i in NODES where fix(x[i]) ] ++ ["\n"];
