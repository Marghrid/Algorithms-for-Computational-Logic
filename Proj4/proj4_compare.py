#!/usr/bin/env python3
import sys,subprocess,time
import searches
from id3 import id3

solver = ['clingo']
dbg=False

searches = [searches.Binary, searches.UNSAT_SAT, searches.SAT_UNSAT]
encodings = [('basic', 'main.lp'), ('v_sum', 'main_v_sum.lp')]

solver_time = 0
time_per_call = {}
num_solver_calls = 0

def parse_samples(f):
    header = None
    samples = []
    for l in f:
        s = l.rstrip().split()
        if not s: continue
        if header:
            assert(len(s) == header[0]+1)
            samples.append([int(l) for l in s])
        else:
            header = [int(l) for l in s]
    return (header, samples)

def read_model(modlines):
    def get_atom_params(a): return a[a.find('(') + 1 : a.find(')')].split(',')
    def get_int_atom_params(a): return map(int, get_atom_params(a))

    has_answer = False
    tree = []
    for l in modlines:
        l = l.strip()
        if not l: continue
        if has_answer: # parse answer set
            els = l.split()
            for e in els:
                if e.startswith('v('):
                    tree.append('v {}'.format(*get_int_atom_params(e)))
                if e.startswith('l('):
                    tree.append('l {} {}'.format(*get_int_atom_params(e)))
                if e.startswith('r('):
                    tree.append('r {} {}'.format(*get_int_atom_params(e)))
                if e.startswith('a('):
                    tree.append('a {} {}'.format(*get_int_atom_params(e)))
                if e.startswith('c('):
                    tree.append('c {} {}'.format(*get_int_atom_params(e)))
            break
        elif l.startswith('Answer'):
            has_answer = True
    return '\n'.join(sorted(tree)) if has_answer else None

# run solver on given number of features, nodes, and samples
def run(feature_count, node_count, samples, encoding):
    global solver, dbg
    sol_in = ''
    sol_in += 'node(1..{}).\n'.format(node_count)
    sol_in += 'feature(1..{}).\n'.format(feature_count)
    sol_in += f'{int((node_count+1)//2)} {{v(I): node(I)}} {int((node_count+1)//2)}.\n'

    # You can only be a leaf with a given class if the path leading to you from the root
    # discriminates samples with a different class
    for q in samples:
        d_list = []
        for r_e, sigma in enumerate(q[:-1]):
            r = r_e+1 # because our r starts in 1 and enumerator starts in 0
            d_list.append(f'd{sigma}({r}, I)')
    
        if q[-1] == 1: # class is pos
            class_lit = 'c(I, 0)'
        else: # q[-1] == 0, class is neg
            class_lit = 'c(I, 1)'
        d_str = '; '.join(d_list)
        sol_in += f'1 {{{d_str}}} {feature_count} :- {class_lit}, v(I).\n'
    
    with open(encoding[1]) as mf:
        sol_in += '\n' + mf.read()

    options = ['-n1', '--configuration=handy', '--heuristic=Berkmin']
    if dbg:
        sys.stderr.write(sol_in)
    # sys.stdout.write(f'# running N = {node_count}: {solver} {options}\n')
    t0 = time.time()
    p = subprocess.Popen(solver + options, \
        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (po, pe) = p.communicate(input=bytes(sol_in, encoding ='utf-8'))
    po = str(po, encoding ='utf-8').splitlines()
    pe = str(pe, encoding ='utf-8').splitlines()
    # save times:
    global solver_time, num_solver_calls, time_per_call
    solver_time += float(pe[-1])
    time_per_call[node_count] = float(pe[-1])
    num_solver_calls += 1

    # sys.stdout.write('# solver ended with exit code {} ({:.2f} s)\n'.format(p.returncode, time.time() - t0))
    if p.returncode % 10 != 0:
        sys.stderr.write('something went wrong with the call to {} (exit code {})'.format(solver, p.returncode))
        sys.stderr.write('\n>> ' + '\n>> '.join(po) + '\n')
        if len(pe) > 0: sys.stderr.write('\nerr>> ' + '\nerr>> '.join(pe) + '\n')
        exit(1)
    if dbg:
        sys.stderr.write('\n>> ' + '\n>> '.join(po) + '\n')
        if len(pe) > 0: sys.stderr.write('\nerr>> ' + '\nerr>> '.join(pe) + '\n')
    return None if p.returncode == 20 else read_model(po)

if __name__ == "__main__":
    header, samples = parse_samples(sys.stdin)
    # print ("# solver:", solver)
    print_time = True

    if print_time:
        solver = ['timeout', '300', '/usr/bin/time', '-f' ,'%e'] + solver
    solver_time = 0
    num_solver_calls = 0

    # print("# getting upper bound from ID3")
    id3_cost, id3_model = id3(samples)

    if id3_cost == -1:
        # print(f"UNSAT")
        exit(0)

    # print('# id3', id3_cost)

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

            # print(f'# using search {search}')
            num_nodes = search.get_first_n()

            while True:
                oidnama = run(header[0], num_nodes, samples, encoding)
                solver_outcome = 'sat' if oidnama else 'unsat'
                if search.is_done(solver_outcome, oidnama, num_nodes):
                    break
                else:
                    num_nodes = search.get_next_n(num_nodes, solver_outcome)

            if search.is_sat():
                opt_model, opt_num_nodes = search.get_best_model()
                # print(opt_model)

                # print("# SAT; Optimal number of nodes: " + str(opt_num_nodes))

            if print_time:
                times_dict[(str(search), encoding[0])] = solver_time
                # print("# total solver wall clock time:\t", solver_time)
                # print("# number of solver calls:\t", num_solver_calls)
                # print("# time per solver call:\t", time_per_call)

    for t in sorted(times_dict, key=times_dict.get):
        print('{0: <9}'.format(t[0]), '{0: <12}'.format(t[1]), times_dict[t])   
