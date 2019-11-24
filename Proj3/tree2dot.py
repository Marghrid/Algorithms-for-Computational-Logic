#!/usr/bin/env python3
# File:  tree2dot.py
# Author:  mikolas
# Created on:  Thu Oct 10 18:18:15 WEST 2019
# Copyright (C) 2019, Mikolas Janota
import sys

def print_dot(ls):
    ns = dict()
    a = dict()
    tl = set()
    fl = set()
    unsat = False
    for l in ls:
        l = l.rstrip()
        if not l: continue
        if l == 'UNSAT':
            print('UNSAT')
            return
        spl = l.split()
        if spl[0] == 'l' or spl[0] == 'r':
            vs = [ int(s) for s in spl[1:] ]
            assert(len(vs)==2)
            if vs[0] not in ns:
                ns[vs[0]] = [ (spl[0], vs[1]) ]
            else:
                ns[vs[0]].append((spl[0], vs[1]))
        if spl[0] == 'c':
            vs = [ int(s) for s in spl[1:] ]
            assert(len(vs)==2)
            if vs[1] == 0:
                fl.add(vs[0])
            elif vs[1] == 1:
                tl.add(vs[0])
            else:
                assert(False)
        if spl[0] == 'a':
            vs = [ int(s) for s in spl[1:] ]
            assert(len(vs)==2)
            assert(vs[1] not in a)
            a[vs[1]] = vs[0]
            

    print('digraph "T" {')
    for v in tl:
        print(' {} [shape=box, label="{}:T"];'.format(v,v))
    for v in fl:
        print(' {} [shape=box, label="{}:F"];'.format(v,v))

    for v in a:
        print(' {} [label="{}:f{}"];'.format(v,v,a[v]))

    for v in ns:
        for (lb, nv) in ns[v]: 
            print(' {} -> {} [label="{}", color="{}"];'.format(v, nv, '0' if lb=='l' else '1', "red" if lb=='l' else "blue"))
    print('}')

if __name__ == "__main__":
    print_dot(sys.stdin)
