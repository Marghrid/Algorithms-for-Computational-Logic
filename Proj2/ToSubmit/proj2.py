#!/usr/bin/env python3
import sys,subprocess 
from enc import Encoder
import argparse
import re
import searches
from id3 import id3
import time


solver_dir = './solvers/'
# solver_dir = ''
solvers = ['z3 -in', 'cvc4 --lang smt --produce-models']
solver = solver_dir + solvers[0]

def get_model(solver_output):
	vals = dict()
	for i, ln in enumerate(solver_output):
		ln = ln.rstrip()
		if not ln: continue

		if 'z3' in solver:
			var_match = re.search(r'\(define-fun (\w+) \(\) (\w+)', ln)
			if not var_match or not i+1 < len(solver_output)-1: continue
			var = var_match.groups()[0]
			
			val_match = re.search(r'(\w+)', solver_output[i+1])
			if not val_match: continue
			val = val_match.groups()[0]

		elif 'cvc4' in solver:
			match = re.search(r'\(define-fun (\w+) \(\) (\w+) (\w+)', ln)
			if not match or not i+1 < len(solver_output)-1: continue
			var = match.groups()[0]
			val = match.groups()[2]

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
	argparser.add_argument('-t', '--tree', action='store_true', help='print decision tree')
	argparser.add_argument('-m', '--model', action='store_true', help='print model')
	argparser.add_argument('-s', '--smt', action='store_true', help='print smt-lib encoded constraints')
	argparser.add_argument('-v', '--verbose', action='store_true', help='print everything')
	argparser.add_argument( '--time', action='store_true', help='time solver')
	cmd_args = argparser.parse_args()

	print_time = cmd_args.time
	print_tree = cmd_args.tree
	print_smt = cmd_args.smt
	print_model = cmd_args.model
	if cmd_args.verbose:
		print_tree = True
		print_smt = True
		print_model = True


	print("# reading from stdin")
	header, samples = parse(sys.stdin)

	if print_time:
		solver = '/usr/bin/time -f "%e" ' + solver
		id3_time = 0
		solver_time = 0
		num_solver_calls = 0

	print("# getting upper bound from ID3")
	if print_time: start = time.time()
	id3_cost, id3_model = id3(samples)
	if print_time: 
		end = time.time()
		id3_time = end - start

	if id3_cost == -1:
		print(f"UNSAT")
		exit(0)

	print('# id3', id3_cost, id3_model)
	# if id3_cost == 1, our solver does not deal with N<3. We want to return a
	#  solution with N=3
	# if id3_cost == 3, UB = LB, and due to our definition of Search, we must
	#  compute another solution.
	if id3_cost <= 3:
		search = searches.Binary(3, 3)
	else:
		search = searches.Binary(3, id3_cost, id3_model)

	print(f'# using search {search}')
	num_nodes = search.get_first_n()
	e = Encoder(header[0])
	while True:
		print(f"# encoding for {num_nodes} nodes")
		e.enc(samples, num_nodes)

		smt = e.mk_smt_lib(False)

		if print_smt:
		 	print("# encoded constraints")
		 	print(smt)
		 	print("# END encoded constraints")

		print("# sending to solver '" + str(solver) + "'")
		p = subprocess.Popen(solver, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		(po, pe) = p.communicate(input=bytes(smt, encoding ='utf-8'))
		
		print("# decoding result from solver")
		rc = p.returncode
		solver_output = str(po, encoding ='utf-8').splitlines()
		solver_error = str(pe, encoding ='utf-8').split()
		
		if print_time:
			solver_time += float(solver_error[-1])
			num_solver_calls += 1

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
		opt_model, opt_num_nodes = search.get_best_model()
		# if len(header) > 1: assert opt_num_nodes == header[1] , f"{opt_num_nodes} != {header[1]}" # we got the same cost that was on the file
		if print_model:
			e.print_model(opt_model)
		if print_tree:
			e.print_tree(opt_model, opt_num_nodes)
		e.print_solution(opt_model, opt_num_nodes)

		print("SAT; Optimal number of nodes: " + str(opt_num_nodes))

	if print_time:
		print("ID3 wall clock time:\t\t", id3_time)
		print("total solver wall clock time:\t", solver_time)
		print("number of solver calls:\t", num_solver_calls)

