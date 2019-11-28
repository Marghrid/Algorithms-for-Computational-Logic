#!/usr/bin/env python3
# File:  chk.py
# Author:  mikolas
# Created on:  Fri Oct 11 14:18:32 WEST 2019
# Copyright (C) 2019, Mikolas Janota
import sys
def err(msg):
    print("ERROR:", msg)
    exit(1)

def parse_samples(f):
    nms = None
    samples = []
    for l in f:
        s = l.rstrip().split()
        if not s: continue
        if nms:
            samples.append([int(l) for l in s])
        else:
            nms = [int(l) for l in s]
    return (nms, samples)

def chk(nfts, nns, ls, samples):
    all_ns = set()
    lns = dict() #  left children
    rns = dict() #  right children
    a = dict() #  assigned features
    tl = set() #  leaf true
    fl = set() #  leaf  false
    for l in ls:
        l = l.rstrip()
        if not l: continue
        if l == 'UNSAT':
            print('OK (UNSAT)')
            return
        spl = l.split()
        if spl[0] == 'l' or spl[0] == 'r':
            vs = [ int(s) for s in spl[1:] ]
            assert(len(vs)==2)
            all_ns.add(vs[0])
            all_ns.add(vs[1])
            if spl[0] == 'l':
                if vs[0] in lns: err("{}  already has left child".format(vs[0]))
                lns[vs[0]] = vs[1]
            else:
                if vs[0] in rns: err("{}  already has right child".format(vs[0]))
                rns[vs[0]] = vs[1]
        if spl[0] == 'c':
            vs = [ int(s) for s in spl[1:] ]
            assert(len(vs)==2)
            all_ns.add(vs[0])
            if vs[1] == 0:
                fl.add(vs[0])
            elif vs[1] == 1:
                tl.add(vs[0])
            else:
                assert(False)
        if spl[0] == 'a':
            vs = [ int(s) for s in spl[1:] ]
            assert(len(vs)==2)
            if vs[1] in a: err("{}  already has assigned feature".format(vs[1]))
            a[vs[1]] = vs[0]
            all_ns.add(vs[1])
    if len(all_ns) != nns:
        err("wrong number of nodes")

    def check_structure(nd, visited):
        if nd in visited: err("there is a cycle on node {}".format(nd))
        visited.add(nd)
        hl = nd in lns
        hr = nd in rns
        if hl != hr: err("{} can only have zero or two children".format(nd))
        if not hl:
            if nd in a: err("{} is a leaf and therefore it  cannot have have a feature assigned".format(nd))
            if nd not in fl and nd not in tl: err("{} is a leaf and therefore it has to have a class  assigned".format(nd))
            return
        if nd not in a: err("{} is internal and therefore it has to have a  feature assigned".format(nd))
        if nd in fl or nd in tl: err("{} is internal and therefore it  cannot have have a  class assigned".format(nd))
        check_structure(lns[nd], visited)
        check_structure(rns[nd], visited)

    check_structure(1, set())

    def get_val(nd, sample):
        if nd in fl: return 0
        if nd in tl: return 1
        ftr = a[nd]
        nxt = lns[nd] if sample[ftr - 1] == 0 else rns[nd]
        return get_val(nxt, sample)

    for sample  in samples:
        if sample[-1] != get_val(1, sample):
            err('FAIL on sample {} '.format(sample))
            return False
        else:
            print('OK on {} '.format(sample))
    return True

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print('USAGE: {} <sample-file>'.format(sys.argv[0]))
        exit(1)

    with open(sys.argv[1]) as sf:
        nms, samples = parse_samples(sf)

    if chk(nms[0], nms[1], sys.stdin, samples):
        print('OK')
