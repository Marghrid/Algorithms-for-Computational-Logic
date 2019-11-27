#!/usr/bin/env python3
# File:  gen.py
# Author:  mikolas
# Created on:  Fri Oct 11 11:07:00 WEST 2019
# Copyright (C) 2019, Mikolas Janota
import sys,random

def run(fs, ss, seed) :
    random.seed(seed)
    lhss = set()
    i = ss
    print(fs, '-1')
    while i > 0:
        lhs = ' '.join([ '1' if random.random() < 0.1 else '0' for _ in range(fs) ])
        if lhs in lhss: continue
        i = i - 1
        lhss.add(lhs)
        print(lhs, ('1' if random.random() < 0.5 else '0'))

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print('<features> <samples> <seed>')
        exit(100)

    run(*map(int,sys.argv[1:]))
    exit(0)
