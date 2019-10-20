#!/usr/bin/env/python3

import argparse
from random import getrandbits

def main():
	parser = argparse.ArgumentParser(description='.')
	parser.add_argument('num_inputs', type=int, metavar='num-inputs', help='number of inputs')
	parser.add_argument('num_feats', type=int, metavar='num-features', help='number of features for each input')
	parser.add_argument('num_nodes', type=int, metavar='num-nodes', help='number of nodes in the decision tree')

	args = parser.parse_args()

	generate_instance(args.num_inputs, args.num_feats, args.num_nodes)


def generate_instance(n_inputs, n_feats, n_nodes):
	assert(n_inputs < n_feats**2)
	
	print(f'{n_feats} {n_nodes}')

	inputs = set()

	while len(inputs) < n_inputs:
		in_str = ''
		for f in range(n_feats + 1):
			in_str += f'{getrandbits(1)} '

		inputs.add(in_str)

	for s in inputs:
		print(s)


if __name__ == "__main__":
	main()

