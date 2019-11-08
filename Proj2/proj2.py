#!/usr/bin/env python3
# File:  stub.py
# Author:  mikolas
# Created on:  Sat Oct 12 10:30:54 WEST 2019
# Copyright (C) 2019, Mikolas Janota
import sys,subprocess 
from enc import Enc
import argparse
import re

solver_dir = './solvers/'
#solver_dir = ''
solvers = ['z3 -in']
solver = solver_dir + solvers[0]

def get_model(lns):
	vals = dict()
	for i, ln in enumerate(lns):
		ln = ln.rstrip()
		if not ln: continue

		var_match = re.search(r'\(define-fun (\w+) \(\) (\w+)', ln)
		if not var_match or not i+1 < len(lns)-1: continue
		
		var = var_match.groups()[0]
		
		val_match = re.search(r'(\w+)', lns[i+1])
		if not val_match: continue

		val = val_match.groups()[0]

		vals[var] = val

	return vals
	# vals=dict()
	# found=False
	# for l in lns:
	# 	
	# 	if not l.startswith('v ') and not l.startswith('V '): continue
	# 	found=True
	# 	vs = l.split()[1:]
	# 	for v in vs:
	# 		if v == '0': break
	# 		vals[int(var(v))] = not sign(v)
	# return vals if found else None

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

	argparser = argparse.ArgumentParser()
	argparser.add_argument('-t', '--print_tree', action='store_true', help='print decision tree')
	argparser.add_argument('-m', '--print_model', action='store_true', help='print model')
	argparser.add_argument('-s', '--print_smt', action='store_true', help='print smt-lib encoded constraints')
	argparser.add_argument('-v', '--verbose', action='store_true', help='print everything')
	argparser.add_argument( '--time', action='store_true', help='time solver')
	cmd_args = argparser.parse_args()

	time = cmd_args.time
	print_tree = cmd_args.print_tree
	print_smt = cmd_args.print_smt
	print_model = cmd_args.print_model
	if cmd_args.verbose:
		print_tree = True
		print_smt = True
		print_model = True


	print("# reading from stdin")
	nms, samples = parse(sys.stdin)

	print("# encoding")
	e = Enc(nms[0], nms[1])
	e.enc(samples)

	cnf = e.mk_smt_lib(False)

	if print_smt:
	 	print("# encoded constraints")
	 	print(cnf)
	 	print("# END encoded constraints")

	print("# sending to solver '" + str(solver) + "'")
	if time:
		solver = 'time -f "%E" ' + solver
	p = subprocess.Popen(solver, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	(po, pe) = p.communicate(input=bytes(cnf, encoding ='utf-8'))
	
	print("# decoding result from solver")
	rc = p.returncode
	lns = str(po, encoding ='utf-8').splitlines()
	lnse = str(pe, encoding ='utf-8').split()
	
	if debug_solver:
		print('\n'.join(lns), file=sys.stderr)
		print(cnf, file=sys.stderr)
		print(lns)

	if(lns[0] == 'sat'):
		if print_model:
			e.print_model(get_model(lns))
		if print_tree:
			e.print_tree(get_model(lns))
		print("SAT")
		# e.print_model(get_model(lns))
		e.print_solution(get_model(lns))

	elif(lns[0] == 'unsat'):
		print("UNSAT")

	else:
		print("ERROR: something went wrong with the solver")
		print(lns)

	if time:
		print('real (wall clock) time:', lnse[-1])
