#!/usr/bin/env python3
# File:  proj3
# Author:  mikolas
# Created on:  Thu Nov 14 16:44:14 WET 2019
# Copyright (C) 2019, Mikolas Janota
import sys,subprocess

unsat_msg = '__UNSAT__'
solver = ['minizinc', '--unsat-msg', unsat_msg,  '-']

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

# run minizinc on a fixed node_count
def run(feature_count, node_count, samples):
    global solver
    dbg=False # set to True if you want to see what goes into minizinc
    sol_in = ''
    sol_in += 'int: n = {};\n'.format(node_count)
    sol_in += 'int: k = {};\n'.format(feature_count)
    # add main.mzn to the input
    with open('main.mzn') as mf:
        sol_in += '\n' + mf.read()
    # add more constraints to sol_in if needed
    # TODO
    # add prn.mzn to the input
    with open('prn.mzn') as mf:
        sol_in += '\n' + mf.read()
    if dbg:
        sys.stderr.write(sol_in)
    # run solver
    print('# run minizinc')
    p = subprocess.Popen(solver, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (po, pe) = p.communicate(input=bytes(sol_in, encoding ='utf-8'))
    print('# minizinc done')
    po = str(po, encoding ='utf-8')
    pe = str(pe, encoding ='utf-8')
    if p.returncode != 0:
        sys.stderr.write('something went wrong with the call to {} (exit code {})'.format(solver, p.returncode))
        sys.stderr.write('\n>>' + '\n>>'.join(po.splitlines()))
        sys.stderr.write('\nerr>>' + '\nerr>>'.join(pe.splitlines()))
        exit(1)
    # return None if unsat
    return None if unsat_msg in po else po

if __name__ == "__main__":
    print('# reading from standard input')
    nms, samples = parse_samples(sys.stdin)
    print('# reading done')
    feature_count = nms[0]
    tree = run(feature_count, 3, samples)
    print(tree)
