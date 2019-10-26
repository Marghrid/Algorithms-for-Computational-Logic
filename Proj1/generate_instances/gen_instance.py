#!/usr/bin/env/python3

import argparse
from random import getrandbits

def main():
	parser = argparse.ArgumentParser(description='.')
	parser.add_argument('num_inputs', type=int, metavar='num-inputs', help='number of inputs')
	parser.add_argument('num_feats', type=int, metavar='num-features', help='number of features for each input')
	parser.add_argument('num_nodes', type=int, metavar='num-nodes', help='number of nodes in the decision tree')
	parser.add_argument('--no_header', action='store_true', help='generate only inputs, no header')
	args = parser.parse_args()

	generate_instance(args.num_inputs, args.num_feats, args.num_nodes, args.no_header)


def generate_instance(n_inputs, n_feats, n_nodes, no_header):
	assert(n_inputs < n_feats**2)
	
	if not no_header:
		print(f'{n_feats} {n_nodes}')

	# a set is used so no two inputs are the same
	input_features = set()  # without class
	inputs = set()          # with class

	while len(input_features) < n_inputs:
		in_str = ''
		for f in range(n_feats):
			in_str += f'{getrandbits(1)} ' # generate features. 0.5 prob to be 0. 
		input_features.add(in_str)   # add only if input is different from all others

	while len(input_features) > 0:
		inputs.add( input_features.pop() + f'{getrandbits(1)}') # class

	for s in inputs:
		print(s)


if __name__ == "__main__":
	main()

