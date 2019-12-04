#!/usr/bin/env python3
import sys,subprocess,time

solver = ['clingo']
dbg=True

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
def run(feature_count, node_count, samples):
    global solver, dbg
    sol_in = ''
    sol_in += 'node(1..{}).\n'.format(node_count)
    sol_in += 'feature(1..{}).\n'.format(feature_count)
    sol_in += f'{int((node_count+1)//2)} {{v(I): node(I)}} {int((node_count+1)//2)}.\n'

    for q in samples:
        if q[-1] == 1: # class is 1
            head = 'c(I, 0) '
        else: # q[-1] == 0, class is 0
            head = 'c(I, 1) '

        d_string = []
        for r_e, sigma in enumerate(q[:-1]):
            r = r_e+1 # because our r starts in 1 and enumerator starts in 0
            d_string += [f' d{sigma}({r}, I)']
        sol_in += head + ':- ' + ','.join(d_string) + ', v(I).\n'

    with open('main.lp') as mf:
        sol_in += '\n' + mf.read()

    options = [ '-n1' ]
    if dbg:
        sys.stderr.write(sol_in)
    sys.stdout.write('# running {} {}\n'.format(solver, options))
    t0 = time.time()
    p = subprocess.Popen(solver + options, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (po, pe) = p.communicate(input=bytes(sol_in, encoding ='utf-8'))
    po = str(po, encoding ='utf-8').splitlines()
    pe = str(pe, encoding ='utf-8').splitlines()
    sys.stdout.write('# solver ended with exit code {} ({:.2f} s)\n'.format(p.returncode, time.time() - t0))
    if p.returncode % 10 != 0:
        sys.stderr.write('something went wrong with the call to {} (exit code {})'.format(solver, p.returncode))
        sys.stderr.write('\n>>' + '\n>>'.join(po) + '\n')
        sys.stderr.write('\nerr>>' + '\nerr>>'.join(pe) + '\n')
        exit(1)
    if dbg:
        sys.stderr.write('\n>>' + '\n>>'.join(po) + '\n')
        sys.stderr.write('\nerr>>' + '\nerr>>'.join(pe) + '\n')
    return None if p.returncode == 20 else read_model(po)

if __name__ == "__main__":
    header, samples = parse_samples(sys.stdin)
    print ("# solver:", solver)
    print("K", header[0])
    for n in range(9, 11, 2):
        amandio = run(header[0], n, samples)
        if amandio: 
            print(amandio)
            break

