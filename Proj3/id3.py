from math import log2
from queue import Queue

def print_model(N, model):
	ret = ''
	for i in range(1, N+1):
		is_leaf = model[f'v_{i}']
		if is_leaf == 'false':
			ret += f'l {i} {model[f"l_{i}"]}\n'
			ret += f'r {i} {model[f"r_{i}"]}\n'
			ret += f'a {model[f"a_{i}"]} {i}\n'
		else:
			lbl = '1' if model[f"c_{i}"]=='true' else '0'
			ret += f'c {i} {lbl}\n'
	return ret
def entropy(inputs):
	''' Shannon's entropy using log base 2 '''
	# count how may inputs have class 0 and how may have class 1
	if is_pure(inputs): return 0
	count0 = sum(map(lambda i : i[-1] == 0, inputs))
	count1 = sum(map(lambda i : i[-1] == 1, inputs))
	assert count1 + count0 == len(inputs) # paranoia

	ratio0 = (count0) / len(inputs)
	ratio1 = (count1) / len(inputs)

	return -(ratio0 * log2(ratio0) + ratio1 * log2(ratio1))

def split(inputs):
	''' Splits input in the best attribute '''
	assert not is_pure(inputs)
	init_entropy = entropy(inputs)

	highest_gain = -1
	best_split = []
	for i in range(len(inputs[0])-1):
		# measure gain of split on i:
		i0 = [x for x in inputs if x[i] == 0]
		i1 = [x for x in inputs if x[i] == 1]
		assert len(i0) + len(i1) == len(inputs) # paranoia

		if len(i0) == 0 or len(i1) == 0: continue # feat i has always the same value

		h_i0 = entropy(i0)
		h_i1 = entropy(i1)

		ratio_i0 = len(i0)/len(inputs)
		ratio_i1 = len(i1)/len(inputs)

		gain_i = init_entropy - ratio_i0 * h_i0 - ratio_i1 * h_i1

		if gain_i > highest_gain:
			highest_gain = gain_i
			best_split = (i, i0, i1)

	if(highest_gain < 0): return -1, None, None # All feats are the same and class is different - unsat

	return best_split


def is_pure(inputs):
	return all(i[-1] == 0 for i in inputs) or all(i[-1] == 1 for i in inputs)

def id3(samples):
	node_counter = 0
	Q = Queue()
	Q.put((0,samples))

	model = dict()

	while not Q.empty():
		node_counter += 1
		node_id = node_counter
		parent_id, current_samples = Q.get()

		if node_id % 2 == 0:  # is even
			model[f'l_{parent_id}'] = str(node_id)
		else:                 # is odd
			model[f'r_{parent_id}'] = str(node_id)

		if is_pure(current_samples):
			model[f'v_{node_id}'] = 'true'
			c = current_samples[0][-1] # class value of all inputs
			model[f'c_{node_id}'] = 'true' if c == 1 else 'false'
			continue
		
		model[f'v_{node_id}'] = 'false'

		feat, feat0, feat1 = split(current_samples)

		if feat == -1: # unsat
			return -1, None

		model[f'a_{node_id}'] = str(feat+1)

		Q.put((node_counter, feat0))
		Q.put((node_counter, feat1))

	return node_counter, print_model(node_counter, model)