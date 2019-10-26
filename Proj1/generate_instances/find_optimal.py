import os
import subprocess
from random import shuffle

def odd(n):
	assert(n >= 0)
	if (n%2) == 0: return n+1
	else: return n

no_head_samples_dir = '../my_instances_no_header/'
opt_samples_dir = '../my_instances/'

# if opt_samples_dir does not exist, create it
if not os.path.exists(opt_samples_dir):
    os.makedirs(opt_samples_dir)


filenames = []
# r=root, d=directories, f = files
for r, d, f in os.walk(no_head_samples_dir):
	for file in f:
		filenames.append(os.path.join(r, file))

# shuffle(filenames)

processes = []

for filename in filenames:
	with open(filename, 'r') as f:
		contents = f.read();
	
	inputs = contents.split('\n')    # list of inputs
	first_input = inputs[0].split()  # list of numbers
	n_feats = len(first_input)-1
	# if n_feats > 15: continue

	n_inputs = len(inputs)
	# if n_inputs > 40: continue
	print("=== Instance: ===")
	print(contents)

	os.chdir('..') # ugly hack! cd's to parent directory, so proj1 is run from there.

	for n_nodes in range(3, n_inputs*4, 2):
		n_nodes = odd(n_nodes)
		header = f'{n_feats} {n_nodes} \n'
		sample = header + contents

		print(header[:-1]) # do not print las \n
		command = 'echo \'' + sample + '\' | python3 proj1.py'
		p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)

		output = str(p.stdout.read())
		opt_n_nodes = -1
		if(output.find('UNSAT') == -1):
			# The result was SAT! Current n_nodes is the optimal n_nodes
			opt_n_nodes = n_nodes
			print("optimum n_nodes: ", opt_n_nodes)
			break

	os.chdir('generate_instances')
	assert(opt_n_nodes > 0)
	with open(opt_samples_dir + f'inst_{n_feats}_{n_inputs}_{opt_n_nodes}.smp', 'w+') as f:
		f.write(sample)
		
		#for p in processes: p.wait()
	

#for p in processes: p.wait()



