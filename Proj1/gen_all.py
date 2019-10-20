#!/usr/bin/env/python3

from subprocess import Popen


# number of instances per number of features
n_insts = 100

# min number of features.
min_n_feats = 5
# max number of features.
max_n_feats = 75
# max number of features.
int_n_feats = 5

# directory to save instances:
inst_dir = 'my_instances'

commands = []


n_threads = 48

def break_list(l, n):
	'''Auxiliary function: break list l into n-sized chunks'''
	new_l = []
	for i in range(0, len(l), n):
		new_l.append(l[i:i + n])
	return new_l

for n_feats in range(min_n_feats, max_n_feats, int_n_feats):
	for n_ins in range(n_feats//2, n_feats**2, int_n_feats):
		for n_nodes in range(2, int(n_ins*1.5), int_n_feats):
			#print(f'generating instance: {n_feats} features, {n_ins} inputs and {n_nodes} nodes.')

			cmd = 'python3 gen_instance.py '
			cmd += f'{n_ins} {n_feats} {n_nodes} '                # command args
			cmd += f'> {inst_dir}/inst_{n_feats}_{n_nodes}.smp '  # output file
 
			commands.append(cmd)
	
# run in parallel
for some_commands in break_list(commands, n_threads):
	print(f'\nRunning {len(some_commands)} commands, from')
	print('\t', some_commands[0])
	print('to')
	print('\t', some_commands[-1])
	processes = [Popen(cmd, shell=True) for cmd in some_commands]

	# wait for completion
	for p in processes: p.wait()
