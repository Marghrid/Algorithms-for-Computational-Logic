#!/usr/bin/env/python3
import os
from subprocess import Popen

# min number of features.
min_n_feats = 10
# max number of features.
max_n_feats = 20
# max number of features.
int_n_feats = 5

# directory to save instances:
inst_dir = '../my_instances_no_header'

# if inst_dir does not exist, create it
if not os.path.exists(inst_dir):
    os.makedirs(inst_dir)

commands = []

n_threads = 48

def break_list(l, n):
	'''Auxiliary function: break list l into n-sized chunks'''
	new_l = []
	for i in range(0, len(l), n):
		new_l.append(l[i:i + n])
	return new_l

for n_feats in range(min_n_feats, max_n_feats+1, int_n_feats):
	for n_ins in range(n_feats//2, n_feats**2, int_n_feats):
			print(f'generating instance: {n_feats} features, {n_ins} inputs and {0} nodes.')

			cmd = 'python3 gen_instance.py '
			cmd += f'{n_ins} {n_feats} {0} --no_header '           # command args
			cmd += f'> {inst_dir}/inst_{n_feats}_{n_ins}_{0}.smp'  # output file
 
			commands.append(cmd)
	
# run in parallel
# only lauch n_threads threads at a time
for some_commands in break_list(commands, n_threads):
	print(f'\nRunning {len(some_commands)} commands, from')
	print('\t', some_commands[0])
	print('to')
	print('\t', some_commands[-1])
	processes = [Popen(cmd, shell=True) for cmd in some_commands]

	# wait for completion
	for p in processes: p.wait()
