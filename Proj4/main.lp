foo(P, N) :- node(P), node(N), P < N, N \ 2 = 0, N <= 2*P.
bar(P, N) :- foo(N, P).
#show foo/2.
#show bar/2.
