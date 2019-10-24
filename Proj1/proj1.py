#!/usr/bin/env python3
# File:  stub.py
# Author:  mikolas
# Created on:  Sat Oct 12 10:30:54 WEST 2019
# Copyright (C) 2019, Mikolas Janota
import sys,subprocess 
from enc import Enc, var, sign
import argparse

solver_dir = './solvers/'
solvers = ['cadical', 'cryptominisat5_simple', 'MapleCBTCoreFirst', 'optsat', 'smallsat', 'lingeling', 'mergesat']
solver_w_options = [['./solvers/cryptominisat5_simple', '--sls=walksat'], ['./solvers/cryptominisat5_simple', '--sls=yalsat']]
solver = solver_dir + solvers[0]

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

	argparser = argparse.ArgumentParser()
	argparser.add_argument('-t', '--print_tree', action='store_true', help='print decision tree')
	argparser.add_argument('-m', '--print_model', action='store_true', help='print model')
	argparser.add_argument('-c', '--print_constraints', action='store_true', help='print all encoded constraints')
	argparser.add_argument('-v', '--verbose', action='store_true', help='print everything')
	cmd_args = argparser.parse_args()

	print_tree = cmd_args.print_tree
	print_constraints = cmd_args.print_constraints
	print_model = cmd_args.print_model
	if cmd_args.verbose:
		print_tree = True
		print_constraints = True
		print_model = True


	print("# reading from stdin")
	nms, samples = parse(sys.stdin)

	print("# encoding")
	e = Enc(nms[0], nms[1])
	e.enc(samples)

	if print_constraints:
		print("# encoded constraints")
		print("# " + "\n# ".join(map(str, e.constraints)))
		print("# END encoded constraints")

	print("# sending to solver '" + str(solver) + "'")
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
		print("SAT")
		e.print_solution(get_model(lns))
		if print_model:
			e.print_model(get_model(lns))
		if print_tree:
			e.print_tree(get_model(lns))

	
	elif rc == 20:
		print("UNSAT")
	else:
		print("ERROR: something went wrong with the solver")
