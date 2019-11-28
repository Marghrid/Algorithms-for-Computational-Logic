#!/usr/bin/env python3
import sys,subprocess
import searches
from id3 import id3

unsat_msg = '__UNSAT__'
solver = ['minizinc/bin/minizinc', '--unsat-msg', unsat_msg, '--solver', 'Chuffed', '-']

searches = [searches.Binary, searches.UNSAT_SAT, searches.SAT_UNSAT]
encodings = [('pretty', 'main_pretty.mzn'), ('fast', 'main_fast.mzn'), ('pretty_oc', 'main_pretty_overconstrained.mzn')]
solver_time = 0
time_per_call = {}
num_solver_calls = 0

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
def run(feature_count, node_count, samples, encoding):
	dbg=False # set to True if you want to see what goes into minizinc
	sol_in = ''
	sol_in += 'int: N = {};\n'.format(node_count)
	sol_in += 'int: K = {};\n'.format(feature_count)
	# add main2.mzn to the input
	with open(encoding[1]) as mf:
		sol_in += '\n' + mf.read()
	# add more constraints to sol_in if needed
	for j in range(2, node_count+1):
		for q in samples:
			if q[-1] == 1: # class is 1
				class_lit = f'not c[{j}]'
			else: # q[-1] == 0, class is 0
				class_lit = f'    c[{j}]'
			c12 = f'constraint (v[{j}] /\\ {class_lit}) -> ( false '
			for f_e, sigma in enumerate(q[:-1]):
				f = f_e+1 # because our r starts in 1 and enumerator starts in 0

				c12 += f'\\/ {f} in d{sigma}[{j}] '

			c12 += ');'
			sol_in += c12 + '\n'

	# add print.mzn to the input
	with open('print.mzn') as mf:
		sol_in += '\n' + mf.read()
	if dbg:
		sys.stderr.write(sol_in)
	# run solver
	# print(f'# run minizinc for N = {node_count}')
	p = subprocess.Popen(solver, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	(po, pe) = p.communicate(input=bytes(sol_in, encoding ='utf-8'))
	#print('# minizinc done')
	po = str(po, encoding ='utf-8')
	pe = str(pe, encoding ='utf-8').split()
	global solver_time, num_solver_calls, time_per_call
	solver_time += float(pe[-1])
	time_per_call[node_count] = pe[-1]
	num_solver_calls += 1
	if p.returncode != 0:
		sys.stderr.write('something went wrong with the call to {} (exit code {})'.format(solver, p.returncode))
		sys.stderr.write('\n>>' + '\n>>'.join(po.splitlines()))
		sys.stderr.write('\nerr>>' + '\nerr>>'.join(pe.splitlines()))
		exit(1)
	# return None if unsat
	return None if unsat_msg in po else po

if __name__ == "__main__":
	#print('# reading from standard input')
	nms, samples = parse_samples(sys.stdin)
	#print('# reading done')
	feature_count = nms[0]
	print_time = True


	if print_time:
		solver = ['/usr/bin/time', '-f' ,'%e'] + solver
	solver_time = 0
	num_solver_calls = 0

	#print("# getting upper bound from ID3")
	id3_cost, id3_model = id3(samples)

	if id3_cost == -1:
		print(f"UNSAT")
		exit(0)

	#print('# id3', id3_cost)
	times_dict = {}
	for search_class in searches:
		for encoding in encodings:
			solver_time = 0
			time_per_call = {}
			num_solver_calls = 0

			if id3_cost <= 3:
				search = search_class(3, 3)
			else:
				search = search_class(3, id3_cost, id3_model)

			#print(f'# using search {search}')
			num_nodes = search.get_first_n()

			while True:
				tree = run(feature_count, num_nodes, samples, encoding)
				solver_outcome = 'sat' if tree else 'unsat'
				if search.is_done(solver_outcome, tree, num_nodes):
					break
				else:
					num_nodes = search.get_next_n(num_nodes, solver_outcome)

			if search.is_sat():
				opt_model, opt_num_nodes = search.get_best_model()
				#print(opt_model)

				#print("# SAT; Optimal number of nodes: " + str(opt_num_nodes))

			if print_time:
				times_dict[(str(search), encoding[0])] = solver_time
				#print("# total solver wall clock time:\t", solver_time)
				#print("# number of solver calls:\t", num_solver_calls)
				#print("# time per solver call:\t", time_per_call)
	for t in sorted(times_dict, key=times_dict.get):
		print('{0: <9}'.format(t[0]), '{0: <12}'.format(t[1]), times_dict[t])	
