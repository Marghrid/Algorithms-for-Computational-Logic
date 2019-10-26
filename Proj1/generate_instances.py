import threading
import random
import os

# min number of features.
min_n_feats = 6
# max number of features.
max_n_feats = 16
# max number of features.
int_n_feats = 2
# max number of active threads at a time
num_threads = 16

# directory to save inputs (no header):
inputs_dir = './my_instances_no_header/'

# directory to save complete samples:
samples_dir = './my_instances/'

def main():
	# if inputs_dir does not exist, create it
	if not os.path.exists(inputs_dir):
		os.makedirs(inputs_dir)

	# if samples_dir does not exist, create it
	if not os.path.exists(samples_dir):
		os.makedirs(samples_dir)

	# First, create inputs with no header
	generate_inputs(min_n_feats, max_n_feats, int_n_feats)

	# Then, for each input find optmal n_nodes and write to file
	find_optimals()

def generate_inputs(min_n_feats, max_n_feats, int_n_feats):
	''' Creates instances with no header (just inputs) in parallel '''
	print('generating inputs..')
	threads = []
	n_done = 0
	for n_feats in range(min_n_feats, max_n_feats+1, int_n_feats):
		for n_ins in range(n_feats//2, n_feats*4, int_n_feats):
			th = threading.Thread(target=generate_inputs_par,\
								  args=(inputs_dir, n_ins, n_feats))
			th.start()
			threads.append(th)

			n_done = check_threads(threads, n_done)
   
	join_threads(threads, n_done)

def generate_inputs_par(inputs_dir, n_inputs, n_feats):
	''' Creates one instance with no header - a set of inputs '''
	assert(n_inputs < n_feats**2)
	
	# a set is used so no two inputs are the same
	input_features = set()  # without class
	inputs = set()          # with class

	while len(input_features) < n_inputs:
		in_str = ''
		for f in range(n_feats):
			in_str += f'{random.getrandbits(1)} ' # generate features. 0.5 prob to be 0. 
		input_features.add(in_str)                # add only if input is different from all others

	# add class
	while len(input_features) > 0:
		inputs.add( input_features.pop() + f'{random.getrandbits(1)}')

	# write to file
	filepath = inputs_dir + get_filename(n_feats, n_inputs, 0)
	with open(filepath, 'w+') as inputs_file:
		for i in inputs:
			inputs_file.write(i + '\n')

def get_filename(n_feats, n_ins, n_nodes):
	''' Given sample parameters, return apropriate filename'''
	return f'inst_{n_feats:03d}_{n_ins:03d}_{n_nodes:03d}.smp'

def odd(n):
	''' Given an integer n, return the closest odd number '''
	assert(n >= 0)
	if (n%2) == 0: return n+1
	else: return n

def find_optimals():
	'''
	For all inputs (no-header samples) in a directory in parallel,
	find the optimal (minimum) number of nodes required to build
	a tree consistent with all inputs.
	'''
	print('finding optimal number of nodes..')

	# find files with no header
	filenames = get_inputs()
	random.shuffle(filenames)

	threads = []
	n_done = 0
	for filename in filenames:
		th = threading.Thread(target=find_optimal_par, args=[filename])
		th.start()
		threads.append(th)

		n_done = check_threads(threads, n_done)
			
	join_threads(threads, n_done)


def find_optimal_par(filename):
	'''
	Finds optimal (minimum) number of nodes required to construct
	a decision tree consistent with all inputs in file
	'''
	with open(filename, 'r') as f:
		inputs = f.read();

	n_feats, n_inputs = get_sample_info(inputs)

	print(f'solving instance with {n_feats} features and {n_inputs} inputs.')

	opt_n_nodes = -1
	for n_nodes in range(3, n_inputs*4, 2): # unsat - sat search
		n_nodes = odd(n_nodes)	    		# n_nodes must always be odd
		header = f'{n_feats} {n_nodes} \n'
		sample = header + inputs

		command = 'echo \'' + sample + '\' | python3 proj1.py'
		stream = os.popen(command)
		output = stream.read()

		if(output.find('UNSAT') == -1):
			# The result was SAT! Current n_nodes is the optimal n_nodes
			opt_n_nodes = n_nodes
			break

	if opt_n_nodes > 0: # do not generate unsat instances
		filepath = samples_dir + get_filename(n_feats, n_inputs, opt_n_nodes)
		with open(filepath, 'w+') as f:
			f.write(sample)

def get_inputs():
	''' get all filepaths from files in a directory '''
	filenames = []
	# r=root, d=directories, f = files
	for r, d, f in os.walk(inputs_dir):
		for file in f:
			filenames.append(os.path.join(r, file))
	return filenames

def get_sample_info(inputs):
	''' Get sample parameters from a inputs file (no header) '''
	inputs = inputs.split('\n')     # list of inputs
	first_input = inputs[0].split() # one input - list of numbers
	n_feats = len(first_input)-1    # input is a list of each feature value and input class
	n_inputs = len(inputs)-1        # inputs has a empty list at the end (I know this is ugly)
	return n_feats, n_inputs

def check_threads(threads, n_done):
	'''
	Check current state of active threads, and keep
	number of active threads below num_threads
	'''
	if threading.active_count() >= num_threads / 2:
		print(f'{num_threads//2} threads or more are running. Trying to join some..')
		for th in threads:
			if not th.is_alive():
				th.join()
				n_done += 1
				print(f'Joined. {n_done} threads done')
				threads.remove(th)
	
	if threading.active_count() >= num_threads:
		print(f'{num_threads} threads or more are running. Trying to join one..')
		th = random.choice(threads)
		th.join(10 * 60) # 10 minutes
		n_done += 1
		print(f'Joined. {n_done} threads done')
		threads.remove(th)
	return n_done

def join_threads(threads, n_done):
	''' join all threads in list threads '''
	print('All threads are running. Waiting for them..')
	for th in threads:
		th.join(10 * 60) # 10 minutes
		n_done += 1
		print(f'Joined. {n_done} threads done')

if __name__ == "__main__":
	main()
