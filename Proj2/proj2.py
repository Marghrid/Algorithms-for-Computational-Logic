#!/usr/bin/env python3
# File:  stub.py
# Author:  mikolas
# Created on:  Sat Oct 12 10:30:54 WEST 2019
# Copyright (C) 2019, Mikolas Janota
import sys,subprocess 
from enc import Enc
import argparse
import re
import searches
from id3 import id3


solver_dir = './solvers/'
# solver_dir = ''
solvers = ['z3 -in', 'cvc4 --lang smt --produce-models']
solver = solver_dir + solvers[0]

def get_model(solver_output):
	vals = dict()
	for i, ln in enumerate(solver_output):
		ln = ln.rstrip()
		if not ln: continue

		var_match = re.search(r'\(define-fun (\w+) \(\) (\w+)', ln)
		if not var_match or not i+1 < len(solver_output)-1: continue
		var = var_match.groups()[0]
		
		val_match = re.search(r'(\w+)', solver_output[i+1])
		if not val_match: continue
		val = val_match.groups()[0]

		vals[var] = val
	return vals

def parse(f):
	header = None
	samples = []
	for l in f:
		s = l.rstrip().split()
		if not s: continue
		if header:
			samples.append([int(l) for l in s])
		else:
			header = [int(l) for l in s]
	return (header, samples)

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
	header, samples = parse(sys.stdin)

	print("# getting upper bound from ID3")
	id3_sol = id3(samples)
	if (id3_sol == -1):
		print(f"UNSAT")
		exit(0)

	upper_bound = max(3, id3_sol) # because our solvver won't work with N < 3.
	search = searches.Binary(3, upper_bound)
	print(f'# using search {search}')
	num_nodes = search.get_first_n()
	while True:
		print(f"# encoding for {num_nodes} nodes")
		e = Enc(header[0], num_nodes)
		e.enc(samples)

		smt = e.mk_smt_lib(False)

		if print_smt:
		 	print("# encoded constraints")
		 	print(smt)
		 	print("# END encoded constraints")

		print("# sending to solver '" + str(solver) + "'")
		if time:
			solver = 'time -f "%E" ' + solver
		p = subprocess.Popen(solver, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		(po, pe) = p.communicate(input=bytes(smt, encoding ='utf-8'))
		
		print("# decoding result from solver")
		rc = p.returncode
		solver_output = str(po, encoding ='utf-8').splitlines()
		solver_error = str(pe, encoding ='utf-8').split()
		
		if debug_solver:
			print('\n'.join(solver_output), file=sys.stderr)
			print(smt, file=sys.stderr)
			print(solver_output)

		if solver_output[0] not in ['unsat', 'sat']:
			print("ERROR: something went wrong with the solver")
			print(solver_output)
			exit(1)

		if search.is_done(solver_output[0], get_model(solver_output), num_nodes):
			break
		else:
			num_nodes = search.get_next_n(num_nodes, solver_output[0])


	if search.is_sat():
		model, cost = search.get_best_model()
		assert cost == header[1] , f"{cost} != {header[1]}" # we got the same cost that was on the file
		if print_model:
			e.print_model(model)
		if print_tree:
			e.print_tree(model)
		e.print_solution(model)

		print("SAT; Optimal number of nodes: " + str(cost))

