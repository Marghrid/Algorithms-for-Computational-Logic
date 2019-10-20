#!/usr/bin/env python3
# File:  stub.py
# Author:  mikolas
# Created on:  Sat Oct 12 10:30:54 WEST 2019
# Copyright (C) 2019, Mikolas Janota
import sys,subprocess 
from itertools import combinations

solver_dir = './solvers/'
solvers = ['cadical', 'cryptominisat5_simple', 'MapleCBTCoreFirst', 'optsat', 'smallsat', 'lingeling', 'mergesat']
solver_w_options = [['./solvers/cryptominisat5_simple', '--sls=walksat'], ['./solvers/cryptominisat5_simple', '--sls=yalsat']]
solver = solver_dir + solvers[0]

def neg(l): return l[1:] if l[0] == '-' else '-'+l
def var(l): return l[1:] if l[0] == '-' else l
def sign(l): return l[0] == '-'

class Enc:
	def __init__(self, feat_count,  node_count):
		 self.node_count = node_count
		 self.feat_count = feat_count
		 self.constraints = []
		 self.fresh = 0

	def LR(self,i):
		if (i+1)%2 == 0:
			first = i+1
		else:
			first = i+2

		return range(first, min(2*i, self.node_count-1)+1, 2)

	def RR(self,i):
		if (i+2)%2 == 1:
			first = i+2
		else:
			first = i+3

		return range(first, min(2*i+1, self.node_count)+1, 2)		 

	# 1 iff node i is a leaf node, i = 1,...,N
	def v(self, i):
		assert(i >= 1 and i <= self.node_count)
		return f'v_{i}'

	def l(self, i, j):
		assert(i >= 1 and i <= self.node_count)
		assert(j%2 == 0)
		assert(j >= i+1 and j <= min(2*i, self.node_count-1))
		return f'l_{i}_{j}'

	def r(self, i, j):
		assert(i >= 1 and i <= self.node_count)
		assert(j%2 == 1)
		assert j >= i+2 and j <= min(2*i+1, self.node_count), f'j is {j}, i is {i} and min(2*i+1, self.node_count) is {min(2*i+1, self.node_count)}'
		return f'r_{i}_{j}'
	
	def p(self, j, i): 
		assert(i >= 1 and i <= self.node_count-1)
		assert(j >= 2 and j <= self.node_count)
		return f'p_{j}_{i}'

	def a(self, r, j):
		assert(r >= 1 and r <= self.feat_count)
		assert(j >= 1 and j <= self.node_count)
		return f'a_{r}_{j}'

	def u(self, r, j):
		assert(r >= 1 and r <= self.feat_count)
		assert(j >= 1 and j <= self.node_count)
		return f'u_{r}_{j}'

	def d0(self, r, j):
		assert(r >= 1 and r <= self.feat_count)
		assert(j >= 1 and j <= self.node_count)
		return f'd0_{r}_{j}'

	def d1(self, r, j):
		assert(r >= 1 and r <= self.feat_count)
		assert(j >= 1 and j <= self.node_count)
		return f'd1_{r}_{j}'

	def c(self, j):
		assert(j >= 1 and j <= self.node_count)
		return f'c_{j}'


	def add_constraint(self, constraint):
		'''add constraints, which is a list of literals'''
		assert(constraint is not None)
		assert(isinstance(constraint, list))
		self.constraints.append(constraint)

	def mk_fresh(self, nm):
		'''make fresh variable'''
		self.fresh = self.fresh + 1
		return '_' + nm + '__' + str(self.fresh)

	def mk_and(self, l1, l2):
		'''encode and between l1 and l2 by introducing a fresh variable'''
		r = self.mk_fresh(l1+'_and_'+l2)
		self.constraints.append([neg(l1), neg(l2), r])
		self.constraints.append([l1, neg(r)])
		self.constraints.append([l2, neg(r)])
		return r

	def add_iff(self, l1, l2):
		'''add iff constraint between l1 and l2'''
		self.constraints.append([neg(l1), l2])
		self.constraints.append([l1, neg(l2)])

	def add_impl(self, l1, l2):
		'''add implication constraint between l1 and l2'''
		self.constraints.append([neg(l1), l2])

	def add_sum_eq0(self, sum_lits, or_lits = []):
		"""
		encodes clauses or_lits V (SUM(sum_lits) = 0).
		or_lits is optional 
		"""
		for lit in sum_lits:
			self.add_constraint(or_lits + [neg(lit)])


	def add_sum_eq1(self, sum_lits, or_lits = []):
		"""
		encodes clauses or_lits V (SUM(sum_lits) = 1).
		or_lits is optional 
		"""
		self.add_sum_le1(sum_lits, or_lits)
		self.add_sum_ge1(sum_lits, or_lits)

	def add_sum_le1(self, sum_lits, or_lits = []):
		"""
		encodes clauses or_lits V (SUM(sum_lits) <= 1).
		or_lits is optional 
		"""
		if len(sum_lits) == 0:
			return
		if len(sum_lits) == 1:
			self.add_constraint(sum_lits + or_lits)
			return
		
		lit_pairs = list(combinations(sum_lits, 2))
		for lit_pair in lit_pairs:
			self.add_constraint([neg(lit_pair[0]), neg(lit_pair[1])] + or_lits)


	def add_sum_ge1(self, sum_lits, or_lits = []):
		"""
		encodes clauses or_lits V (SUM(sum_lits) <= 1).
		or_lits is optional 
		"""
		# creates a clause with all the lits in the sum, plus the optional lits for OR
		self.add_constraint(sum_lits + or_lits)


	def add_lit_iff_clause(self, lit, clause):
		''' Encode clause of type lit <--> clause '''
		# ->
		self.add_constraint(clause + [neg(lit)])
		# <-
		for lit2 in clause:
			self.add_constraint([neg(lit2), lit])

	def print_model(self,model):
		'''prints SAT model, eventually should print the decision tree'''
		print('# === model')
		for str_var in sorted(self.var_map.keys()):
			v = self.var_map[str_var]
			val = '?'
			if v in model and model[v]: val='T'
			if v in model and not model[v]: val='F'
			print('# {}={} ({})'.format(str_var,val,v))
		print('# === end of model')

		print('# === tree')
		print('digraph T {')

		node_labels = {}
		is_node_leaf = {}
		for str_var in sorted(self.var_map.keys()):
			if str_var[0] == 'v':  # p vars
				dimacs_idx = self.var_map[str_var]
				if dimacs_idx in model: # if var is true
					i = str_var[2] # feature
					is_node_leaf[i] = model[dimacs_idx]


		for str_var in sorted(self.var_map.keys()):
			if str_var[0] == 'a': # a vars
				dimacs_idx = self.var_map[str_var]
				if dimacs_idx in model and model[dimacs_idx]: # if var is true
					r = str_var[2] # feature
					j = str_var[4] # node
					if not is_node_leaf[j]:
						node_labels[j] = f'{j} : f{r}'
			elif str_var[0] == 'c': # c vars
				dimacs_idx = self.var_map[str_var]
				if dimacs_idx in model: # if var is true
					j = str_var[2] # feature
					if is_node_leaf[j]:
						node_labels[j] = f'{j} : {"T" if model[dimacs_idx] else "F"}'


		
		for str_var in sorted(self.var_map.keys()):
			if str_var[0] == 'p':         # p vars
				v = self.var_map[str_var] # v is index of var in DIMACS
				if v in model and model[v]:
					j = str_var[2] # get parent name from var name
					i = str_var[4] # get child name from var name

					print(f'  "{node_labels[i]}" -> "{node_labels[j]}"  [label="T or F?"]')
		print('}')
		print('# === end of tree')


	def mk_cnf(self,print_comments):
		'''encode constraints as CNF in DIMACS'''
		maxid = 0
		self.var_map = dict()
		cs = 0
		rv = ''
		for c in self.constraints:
			if not isinstance(c, list): continue
			cs = cs + 1
			for l in c:
				if var(l) not in self.var_map:
					maxid = maxid + 1
					self.var_map[var(l)] = maxid

		rv += 'p cnf {} {}'.format(len(self.var_map), cs) + '\n'
		for c in self.constraints:
			if isinstance(c, list):
				if print_comments:
					rv += 'c ' + str(c) + '\n'
				rv += ' '.join(map(str,[ -(self.var_map[var(l)]) if sign(l) else self.var_map[l] for l in c])) + ' 0\n'
			else:
				if print_comments:
					rv += 'c ' + str(c) + '\n'

		return rv

	def enc(self, samples):
		'''encode the problem'''

		## Encoding Topology
		# root node is not a leaf (1)
		self.add_constraint([neg(self.v(1))]) #TODO: this is a redundant constraint. Try to remove it?

		# if i is a leaf then i has no children (2)
		for i in range(1, self.node_count+1): #TODO: check
			for j in self.LR(i):
				self.add_impl(self.v(i), neg(self.l(i, j)))

		# the left child and the right child of node i are numbered consecutively (3)
		for i in range(1, self.node_count+1):
			for j in self.LR(i):
				self.add_iff(self.l(i, j), self.r(i, j+1))

		# non-leaf node must have a child (4)
		for i in range(1, self.node_count+1):
			# This is how it is in the paper:
			#self.add_sum_eq1([self.l(i,j) for j in self.LR(i)], [self.v(i)])
			# This is equivalent
			self.add_sum_ge1([self.l(i,j) for j in self.LR(i)], [self.v(i)])

		# if node i is a parent then it has a child (5)
		for i in range(1, self.node_count+1):
			for j in self.LR(i):
				self.add_iff(self.p(j, i), self.l(i, j))
			for j in self.RR(i):
				self.add_iff(self.p(j, i), self.r(i, j))

		# all nodes but node 1 have a parent (6)
		for j in range(2, self.node_count+1):
			self.add_sum_eq1([self.p(j, i) for i in range(j//2, j)])


		## Encoding Semantics
		#  To discriminate a feature for value 0 at node j (7)
		for r in range(1, self.feat_count+1):
			self.add_constraint([neg(self.d0(r, 1))])
			for j in range(2, self.node_count + 1):
				big_OR = []
				for i in range(j//2, j):
					aux1 = self.mk_and(self.p(j, i), self.d0(r, i))
					if j in self.RR(i):
						aux2 = self.mk_and(self.a(r, i), self.r(i, j))
						big_OR.extend([aux1, aux2])
					else:
						big_OR.append(aux1)
				self.add_lit_iff_clause(self.d0(r, j), big_OR)

		# To discriminate a feature for value 1 at node j (8)
		for r in range(1, self.feat_count+1):
			self.add_constraint([neg(self.d1(r, 1))])
			for j in range(2, self.node_count + 1):
				big_OR = []
				for i in range(j//2, j):
					aux1 = self.mk_and(self.p(j, i), self.d1(r, i))

					print(j, 'in', self.LR(i))
					if j in self.LR(i):
						print(True)
						print(self.l(i, j))
						aux2 = self.mk_and(self.a(r, i), self.l(i, j))
						print(aux2)

						big_OR.extend([aux1, aux2])
					else:
						big_OR.append(aux1)
				self.add_lit_iff_clause(self.d1(r, j), big_OR)

		# Using a feature r at node j (9)
		for r in range(1, self.feat_count):
			for j in range(2, self.node_count+1):
				for i in range(j//2, j): # big AND
					#self.add_constraint([self.u(r, i)])
					#self.add_impl(self.p(j, i), neg(self.a(r, j)))
					self.add_constraint([neg(self.u(r, i)), neg(self.p(j, i)), neg(self.a(r, j))])
				
				big_OR = []
				for i in range(j//2, j): # big OR
					aux = self.mk_and(self.u(r, i), self.p(j, i))
					big_OR.append(aux)
				big_OR.append(self.u(r, j))

				self.add_lit_iff_clause(self.u(r, j), big_OR)

		# For a non-leaf node j, exactly one feature is used (10)
		#  and For a leaf node j, no feature is used (11)
		for j in range(1, self.node_count+1):
			sum_lits = []
			for r in range(1, self.feat_count+1):
				sum_lits.append(self.a(r, j))

			self.add_sum_eq1(sum_lits, [self.v(j)])       # (10)
			self.add_sum_eq0(sum_lits, [neg(self.v(j))])  # (11)

		
		# Any positive example must be discriminated if the leaf node is
		#  associated with the negative class (12)
		#  and any negative example must be discriminated if the leaf node
		#  is associated with the positive class (13)
		# samples is a list of samples, sample[:-1] are features
		#  and sample[-1] is the class (for sample in samples)
		for j in range(2, self.node_count+1):
			for q in samples:
				sum_lits = []
				for r_e, sigma in enumerate(q[:-1]):
					r = r_e+1 # because our r starts in 1 and enumerator starts in 0
					if sigma==1: # feature is 1
						sum_lits.append(self.d1(r, j))
					else: # sigma == 0, feature is 0
						sum_lits.append(self.d0(r, j))
				if q[-1] == 1: # class is 1
					class_lit = self.c(j)
				else: # q[-1] == 0, class is 0
					class_lit = neg(self.c(j))

				self.add_sum_ge1(sum_lits, [neg(self.v(j)), class_lit])



def get_model(lns):
	vals=dict()
	found=False
	for l in lns:
		l=l.rstrip()
		if not l: continue
		if not l.startswith('v ') and not l.startswith('V '): continue
		found=True
		vs = l.split()[1:]
		for v in vs:
			if v == '0': break
			vals[int(var(v))] = not sign(v)
	return vals if found else None

def parse(f):
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



if __name__ == "__main__":
	debug_solver = False 

	print("# reading from stdin")
	nms, samples = parse(sys.stdin)
	print("# encoding")
	e = Enc(nms[0], nms[1])
	e.enc(samples)
	print("# encoded constraints")
	print("# " + "\n# ".join(map(str, e.constraints)))
	print("# END encoded constraints")
	print("# sending to solver '" + str(solver) + "'")
	cnf = e.mk_cnf(False)
	p = subprocess.Popen(solver, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	(po, pe) = p.communicate(input=bytes(cnf, encoding ='utf-8'))
	if debug_solver:
		print('\n'.join(lns), file=sys.stderr)
		print(cnf, file=sys.stderr)
	print("# decoding result from solver")
	rc = p.returncode
	lns = str(po, encoding ='utf-8').splitlines()
	if rc == 10:
		e.print_model(get_model(lns))
	elif rc == 20:
		print("UNSAT")
	else:
		print("ERROR: something went wrong with the solver")
