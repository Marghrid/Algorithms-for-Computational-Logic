#!/usr/bin/env python3
# File:  stub.py
# Author:  mikolas
# Created on:  Sat Oct 12 10:30:54 WEST 2019
# Copyright (C) 2019, Mikolas Janota
import sys,subprocess 

solver = './lingeling'

def neg(l): return l[1:] if l[0] == '-' else '-'+l
def var(l): return l[1:] if l[0] == '-' else l
def sign(l): return l[0] == '-'

class Enc:
    def __init__(self, input_count,  node_count):
         self.node_count = node_count
         self.input_count = input_count
         self.constraints = []
         self.fresh = 0

    # 1 iff node i is a leaf node, i = 1,...,N
    def v(self,i):
        assert(i >= 1 and i <= self.node_count)
        return f'v_{i}'

    def l(self, i, j):
        assert(i >= 1 and i <= self.node_count)
        assert(j%2 == 0)
        assert(j >= i+1 and j <= min(2*i, self.node_count-1))
        return f'l_{i}_{j}'

    def r(self, i, j):
        assert(i >= 1 and i <= self.node_count)
        assert(j%2 == 0)
        assert(j >= i+2 and j <= min(2*i+1, self.node_count))
        return f'r_{i}_{j}'
    
    def p(self, i, j): return f'p_{i}_{j}'
        assert(i >= 1 and i <= self.node_count-1)
        assert(j >= 2 and i <= self.node_count)

    def LR(self,i):
        if (i+1)%2 == 0:
            first = i+1
        else:
            first = i+2

        return range(first, min(2*i, self.node_count-1), 2)

    def RR(self,i):
        if (i+2)%2 == 1:
            first = i+2
        else:
            first = i+3

        return range(first, min(2*i+1, self.node_count), 2)

    def add_constraint(self, constraint):
        '''add constraints, which is a list of literals'''
        self.constraints.append(constraint)

    def mk_fresh(self, nm):
        '''make fresh variable'''
        self.fresh = self.fresh + 1
        return '_' + nm + '__' + str(self.fresh)

    def mk_and(self, l1, l2):
        '''encode and between l1 and l2 by introducing a fresh variable'''
        r = self.mk_fresh(l1+'_and_'+l2)
        self.constraints.append([neg(l1), neg(l2), r])
        self.constraints.append([l1, neg(r)])
        self.constraints.append([l2, neg(r)])
        return r

    def add_iff(self, l1, l2):
        '''add iff constraint between l1 and l2'''
        self.constraints.append([neg(l1), l2])
        self.constraints.append([l1, neg(l2)])

    def add_impl(self, l1, l2):
        '''add implication constraint between l1 and l2'''
        self.constraints.append([neg(l1), l2])


    def print_model(self,model):
        '''prints SAT model, eventually should print the decision tree'''
        print('# === model')
        for str_var in sorted(self.var_map.keys()):
            v = self.var_map[str_var]
            val = '?'
            if v in model and model[v]: val='T'
            if v in model and not model[v]: val='F'
            print('# {}={} ({})'.format(str_var,val,v))
        print('# === end of model')
        print('# === tree (TODO)')
        print('# === end of tree')


    def mk_cnf(self,print_comments):
        '''encode constraints as CNF in DIMACS'''
        maxid = 0
        self.var_map = dict()
        cs = 0
        rv = ''
        for c in self.constraints:
            if not isinstance(c, list): continue
            cs = cs + 1
            for l in c:
                if var(l) not in self.var_map:
                    maxid = maxid + 1
                    self.var_map[var(l)] = maxid

        rv += 'p cnf {} {}'.format(len(self.var_map), cs) + '\n'
        for c in self.constraints:
            if isinstance(c, list):
                if print_comments:
                    rv += 'c ' + str(c) + '\n'
                rv += ' '.join(map(str,[ -(self.var_map[var(l)]) if sign(l) else self.var_map[l] for l in c])) + ' 0\n'
            else:
                if print_comments:
                    rv += 'c ' + str(c) + '\n'

        return rv

    def enc(self, samples):
        '''encode the problem'''

        # root node is not a leaf
        self.add_constraint([neg(self.v(1))])

        # if i is a leaf then i has no children
        for i in range(2, self.node_count+1): #TODO: check
            for j in self.LR(i):
        self.add_impl(self.v(i), neg(self.l(i, j)))



        # -x1 | -x2
        # self.add_constraint([neg(self.x(1)), neg(self.x(2))])
        # x1 | x2
        # self.add_constraint([self.x(1), self.x(2)])
        # x1 <=> x2
        # self.add_iff(self.x(3), self.x(4))
        # y1 | (y2 & y3)
        # self.add_constraint([self.y(1), self.mk_and(self.y(2),self.y(3))])
        # -y1
        # self.add_constraint([neg(self.y(1))])

        
def get_model(lns):
    vals=dict()
    found=False
    for l in lns:
        l=l.rstrip()
        if not l: continue
        if not l.startswith('v ') and not l.startswith('V '): continue
        found=True
        vs = l.split()[1:]
        for v in vs:
            if v == '0': break
            vals[int(var(v))] = not sign(v)
    return vals if found else None

def parse(f):
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



if __name__ == "__main__":
    debug_solver = False 

    print("# reading from stdin")
    nms, samples = parse(sys.stdin)
    print("# encoding")
    e = Enc(nms[0], nms[1])
    e.enc(samples)
    print("# encoded constraints")
    print("# " + "\n# ".join(map(str, e.constraints)))
    print("# END encoded constraints")
    print("# sending to solver '" + solver + "'")
    cnf = e.mk_cnf(False)
    p = subprocess.Popen(solver, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (po, pe) = p.communicate(input=bytes(cnf, encoding ='utf-8'))
    if debug_solver:
        print('\n'.join(lns), file=sys.stderr)
        print(cnf, file=sys.stderr)
    print("# decoding result from solver")
    rc = p.returncode
    lns = str(po, encoding ='utf-8').splitlines()
    if rc == 10:
        e.print_model(get_model(lns))
    elif rc == 20:
        print("UNSAT")
    else:
        print("ERROR: something went wrong with the solver")
