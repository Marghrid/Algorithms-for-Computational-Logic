% Root is not a leaf
:- v(1).

not_v_sum(1, 1). 
not_v_sum(I, SUM+1) :- node(I), not_v_sum(I-1, SUM), not v(I).
not_v_sum(I, SUM) :- node(I), not_v_sum(I-1, SUM), v(I).
l(I, 2*SUM) :- not_v_sum(I, SUM), not v(I).
r(I,J) :- l(I, J-1).

1 {p(I, J): node(J)} 1 :- node(I), I!=1.
p(J+1, I) :- l(I,J).
p(J, I)   :- l(I,J).

% Root discriminates no features
:- d0(R, 1).
:- d1(R, 1).

% If my parent discriminates, I discriminate
d0(R, J) :- d0(R,I), p(J,I).
d1(R, J) :- d1(R,I), p(J,I).

% If my parent is assigned a feature, I discriminate it
d0(R, J) :- r(I,J), a(R,I).
d1(R, J) :- l(I,J), a(R,I).

% I discriminate only if either my parent discriminates
%  or my parent was assigned that feature.
1 {d0(R,I); a(R,I): r(I,J)} 1 :- d0(R, J), p(J,I).
1 {d1(R,I); a(R,I): l(I,J)} 1 :- d1(R, J), p(J,I).

% Each node is assigned only 1 feature
1 {a(R,I) : feature(R) } 1 :- node(I), not v(I).

% Each leaf is assigned only one class
1 {c(I,1); c(I, 0)} 1 :- v(I).

%#heuristic node.    [20, level]
%#heuristic feature. [20, level]
%#heuristic v. [10, level]
%#heuristic l. [9, level]
%#heuristic p. [8, level]
%#heuristic r. [8, level]
%#heuristic a. [6, level]
%#heuristic d0. [5, level]
%#heuristic d1. [5, level]

#show v/1.
#show l/2.
#show r/2.
#show p/2.
#show d0/2.
#show d1/2.
#show a/2.
#show c/2.
