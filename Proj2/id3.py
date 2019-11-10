from math import log2

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
	init_entropy = entropy(inputs)

	highest_gain_feat = -1
	highest_gain = -1
	best_split = []
	for i in range(len(inputs[0])-1):
		# measure gain of split on i:
		i0 = [x for x in inputs if x[i] == 0]
		i1 = [x for x in inputs if x[i] == 1]
		assert len(i0) + len(i1) == len(inputs) # paranoia

		if len(i0) == 0 or len(i1) == 0: continue

		h_i0 = entropy(i0)
		h_i1 = entropy(i1)

		ratio_i0 = len(i0)/len(inputs)
		ratio_i1 = len(i1)/len(inputs)

		gain_i = init_entropy - ratio_i0 * h_i0 - ratio_i1 * h_i1

		if gain_i > highest_gain:
			highest_gain = gain_i
			highest_gain_feat = i
			best_split = [i0, i1]
	if(highest_gain < 0): return -1

	return best_split


def is_pure(inputs):
	return all(i[-1] == 0 for i in inputs) or all(i[-1] == 1 for i in inputs)


def id3(samples):
	if is_pure(samples):
		return 1 # node is leaf
	else:
		splitted = split(samples)
		# if there is no possible split because the inputs are inconsistent, -1 is returned.
		if splitted == -1: return -1

		id3_0 = id3(splitted[0])
		# if a -1 was returned, it must be propagated up the recursion
		if id3_0 == -1: return -1
		id3_1 = id3(splitted[1])
		if id3_1 == -1: return -1

		return 1 + id3_0 + id3_1