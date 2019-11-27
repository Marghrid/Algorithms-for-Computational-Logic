#!/usr/bin/env python3
import sys,subprocess

unsat_msg = '__UNSAT__'
solver = ['minizinc/bin/minizinc', '--unsat-msg', unsat_msg,  '-']

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
    dbg=False # set to True if you want to see what goes into minizinc
    sol_in = ''
    sol_in += 'int: N = {};\n'.format(node_count)
    sol_in += 'int: K = {};\n'.format(feature_count)
    # add main2.mzn to the input
    with open('main_pretty.mzn') as mf:
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
    print(f'# run minizinc for N = {node_count}')
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
    for num_nodes in range(3, 25, 2):
        tree = run(feature_count, num_nodes, samples)
        if tree: break
    print(tree)
