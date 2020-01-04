# Algorithms-for-Computational-Logic
Programming assignments and projects of Algorithms for Computational Logic

## Projects:
This goal of the projects was to build a tool that constructs a binary decision tree that correctly classifies a given set of inputs.
Each project solves this problem by encoding it into a different logic formalisms:

- [__Project 1__](Proj1/README.md): SAT
- [__Project 2__](Proj2/README.md): SMT
- [__Project 3__](Proj3/README.md): CSP
- [__Project 4__](Proj4/README.md): ASP

## Lab4:
Download and extract the pseudo-boolean solver from [wbo](http://sat.inesc-id.pt/~vmm/wbo.gz).

Run the script and save output to opb file:

```console
$ python3 mincover.py graph.txt > example.opb
```

Run the solver with the generated `opb` file:

```console
$ ./wbo example.opb
```

---------------
[Margarida Ferreira](https://github.com/Marghrid)

[Amândio Faustino](https://github.com/Nandinski)

