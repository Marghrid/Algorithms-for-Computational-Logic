:- v(1).
1 {l(I, J): node(J), J >= I+1, J <= 2*I, J\2 = 0} 1 :- node(I), not v(I).
r(I,J) :- l(I, J-1).

1 {p(I, J): node(J)} 1 :- node(I), I!=1.
p(J+1, I) :- l(I,J).
p(J, I) :- l(I,J).

:- d0(R, 1).
:- d1(R, 1).

d0(R, J) :- d0(R,I), p(J,I).
d1(R, J) :- d1(R,I), p(J,I).

d0(R, J) :- r(I,J), a(R,I).
d1(R, J) :- l(I,J), a(R,I).

1 {d0(R,I); a(R,I): r(I,J)} 1 :- d0(R, J), p(J,I).
1 {d1(R,I); a(R,I): l(I,J)} 1 :- d1(R, J), p(J,I).

1 {a(R,I) : feature(R) } 1 :- node(I), not v(I).
1 {c(I,1); c(I, 0)} 1 :- v(I).

#show v/1.
#show l/2.
#show r/2.
#show p/2.
#show d0/2.
#show d1/2.
#show a/2.
#show c/2.
