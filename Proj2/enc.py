import re
import math

class Encoder:
	def __init__(self, feat_count):
		self.feat_count = feat_count
		self.fresh = 0
		self.s_fresh = 0

	def LR(self,i):
		if (i+1)%2 == 0: first = i+1
		else: first = i+2
		return range(first, min(2*i, self.node_count-1)+1, 2)

	def RR(self,i):
		if (i+2)%2 == 1: first = i+2
		else: first = i+3
		return range(first, min(2*i+1, self.node_count)+1, 2)		 

	# Bool. True iff node i is a leaf node, i = 1,...,N
	def v(self, i):
		assert i >= 1 and i <= self.node_count, f'i was {i}, node_count = {self.node_count}'
		return f'v_{i}'

	# Int. l_i = j iff node i has node j as the left child, j in LR(i), i = 1,...,N
	#      l_i = 0 iff i is a leaf -> does not have any children
	def l(self, i):
		assert i >= 1 and i <= self.node_count
		return f'l_{i}'

	# Int. r_i = j iff node i has node j as the right child, j in RR(i), i = 1,...,N.
	#      r_i = 0 iff i is a leaf -> does not have any children
	def r(self, i):
		assert i >= 1 and i <= self.node_count
		return f'r_{i}'
	
	# Int. p_j = i iff the parent of node j is node i, j = 2,...,N, i = 1,...,N
	#      p_j = 0 for node 1, it has no parent.
	def p(self, j): 
		assert j >= 1 and j <= self.node_count
		return f'p_{j}'

	# Int. a_j = r iff feature r is assigned to node j, r = 1,...,K, j = 1,...,N
	#      a_j = 0 iff node has no feature assigned -> it is a leaf
	def a(self, j):
		assert j >= 1 and j <= self.node_count
		return f'a_{j}'

	# Bool. True iff feature r is being discriminated against by node j, r = 1,...,K, j = 1,...,N,
	def u(self, r, j):
		assert r >= 1 and r <= self.feat_count
		assert j >= 1 and j <= self.node_count
		return f'u_{r}_{j}'

	# Bool. True iff feature r is discriminated for value 0 by node j,
	#  or by one of its ancestors, r = 1,...,K, j = 1,...,N,
	def d0(self, r, j):
		assert r >= 1 and r <= self.feat_count
		assert j >= 1 and j <= self.node_count
		return f'd0_{r}_{j}'

	# Bool. True iff feature r is discriminated for value 1 by node j,
	#  or by one of its ancestors, r = 1,...,K, j = 1,...,N,
	def d1(self, r, j):
		assert r >= 1 and r <= self.feat_count
		assert j >= 1 and j <= self.node_count
		return f'd1_{r}_{j}'

	# Bool. True iff class of leaf node j is 1, j = 1,...,N.
	def c(self, j):
	 	assert j >= 1 and j <= self.node_count
	 	return f'c_{j}'

	# Int. v_sum_i = t. Meaning that up to, and including, node i, there are t leaf nodes.
	#  i = 1,...,N, t = 0,...,i//2
	def v_sum(self, i):
		assert i >= 1 and i <= self.node_count
		return f'v_sum_{i}'
	
	# Int. not_v_sum_i = t. Meaning that up to, and including, node i, there are t non-leaf nodes.
	#  i = 1,...,N, t = ceil(i//2),...,i
	def not_v_sum(self, i):
		assert i >= 1 and i <= self.node_count
		return f'not_v_sum_{i}'

	def add_assert(self, atom):
		'''add asserts, which are atoms??'''
		assert atom is not None
		assert isinstance(atom, str)
		self.constraints.append(f'(assert {atom})')


	def add_decl_bool(self, name):
		assert name is not None
		self.constraints.append(f'(declare-const {name} Bool)')

	def add_decl_int(self, name):
		assert name is not None
		self.constraints.append(f'(declare-const {name} Int)')

	def add_iff(self, b1, b2):
		'''add iff constraint between b1 and b2'''
		assert(b1 is not None)
		assert(b2 is not None)
		self.add_assert(self.mk_iff(b1, b2))

	def add_comment(self, comment):
		self.constraints.append(';⭐⭐⭐⭐⭐⭐⭐⭐⭐  ' + comment + '  ⭐⭐⭐⭐⭐⭐⭐⭐⭐;')

	# Integer comparison operations
	def mk_le(self, left, right):
		assert left is not None
		assert right is not None
		return f'(<= {left} {right})'

	def mk_ge(self, left, right):
		assert left is not None
		assert right is not None
		return f'(>= {left} {right})'

	def mk_gt(self, left, right):
		assert left is not None
		assert right is not None
		return f'(> {left} {right})'

	def mk_eq(self, left, right):
		assert left is not None
		assert right is not None
		return f'(= {left} {right})'

	# Integer arithmetic operations
	def mk_mod(self, left, right):
		assert left is not None
		assert right is not None
		return f'(mod {left} {right})'

	def mk_sum(self, left, right):
		assert left is not None
		assert right is not None
		return f'(+ {left} {right})'

	def mk_sub(self, left, right):
		assert left is not None
		assert right is not None
		return f'(- {left} {right})'

	def mk_mul(self, left, right):
		assert left is not None
		assert right is not None
		return f'(* {left} {right})'

	# Boolean operations
	def mk_not(self, arg):
		assert arg is not None
		return f'(not {arg})'

	def mk_or(self, left, right):
		assert left is not None
		assert right is not None
		return f'(or {left} {right})'

	def mk_and(self, left, right):
		assert left is not None
		assert right is not None
		return f'(and {left} {right})'

	def mk_impl(self, left, right):
		assert left is not None
		assert right is not None
		return f'(=> {left} {right})'

	def mk_iff(self, left, right):
		assert left is not None
		assert right is not None
		return f'(= {left} {right})'

	def mk_or_list(self, or_list):
		assert or_list is not None

		if len(or_list) == 0:
			return ""

		if len(or_list) == 1: # so it doesn't have two '((', '))'.
			return or_list[0]

		# [a, b, c, d] becomes
		# (or a (or b (or c d)))
		ret_str = ''
		for atom in or_list[:-1]:
			ret_str += f'(or {atom} '
		ret_str += f'{or_list[-1]}' + (len(or_list)-1)*')'

		return ret_str

	def bool_to_int(self, b):
		return f'(ite {b} 1 0)'

	def def_v_sum(self, i):
		''' Define v sum as the sum of leaf nodes up to i'''
		
		if i == 1:
			int_v_i = self.bool_to_int(self.v(i))
			return self.mk_eq(int_v_i, self.v_sum(i))

		# Compute v_sum(i) as v_sum(i) = v_sum(i-1) + v(i)
		int_v_i = self.bool_to_int(self.v(i))
		v_sum_val = self.mk_sum(self.v_sum(i-1), int_v_i)

		return self.mk_eq(v_sum_val, self.v_sum(i))
	
	def def_not_v_sum(self, i):
		''' Define not v sum as the difference between nodes up to i and v_sum(i)'''
		
		not_v_sum_val = self.mk_sub(i, self.v_sum(i))

		return self.mk_eq(not_v_sum_val, self.not_v_sum(i))


	def print_solution(self, model, node_count):
		self.node_count = node_count
		'''
		prints solution output, according to the format:
		- 'l i j' representing that j is a left (0) child of i
		- 'r i j' representing that j is a right (1) child of i
		- 'c i v' leaf i responds with the class v
		- 'a r i' the feature r is assigned to internal node i
		'''

		for i in range(1, node_count+1):
			is_leaf = model[self.v(i)]
			if is_leaf == 'false':
				print(f'l {i} {model[self.l(i)]}')
				print(f'r {i} {model[self.r(i)]}')
				print(f'a {model[self.a(i)]} {i}')
			else:
				lbl = '1' if model[self.c(i)]=='true' else '0'
				print(f'c {i} {lbl}')

	def print_model(self,model):
		'''prints SAT model'''
		print('# === model')
		for var in sorted(model):
			print(f'# {var} = {model[var]}')
		print('# === end of model')

	def print_tree(self, model, node_count):
		self.node_count = node_count

		''' prints the decision tree '''
		print('# === tree')
		print('digraph T {')
		print('edge [penwidth=2]')

		# print nodes
		for i in range(1, node_count+1):
			is_leaf = model[self.v(i)]
			if is_leaf == 'false':
				feature_split = model[self.a(i)]
				print(f'{i} [label="{i} : f{feature_split}"]')
			else:
				class_ = "1" if model[self.c(i)] == "true" else "0"
				label = f'{i} : {class_}'
				print(f'{i} [label="{label}", style=filled, color="#DFDFDF"]')

		# print edges
		for i in range(1, node_count+1):
			l_ch = int(model[self.l(i)])
			r_ch = int(model[self.r(i)])
			is_leaf = model[self.v(i)]
			if is_leaf == 'false':
				print(f'{i} -> {l_ch}  [label="1", color="blue"]')
				print(f'{i} -> {r_ch}  [label="0", color="red"]')

		print('}')
		print('# === end of tree')

	def mk_smt_lib(self,print_comments):
		'''encode constraints in SMT-LIB2'''
		return_string = ''
		for c in self.constraints:
			return_string += c + '\n'

		return_string += '(check-sat)\n'
		return_string += '(get-model)\n'

		return return_string

	def enc(self, samples, node_count):
		'''encode the problem'''
		self.node_count = node_count
		self.constraints = []
		# Declare variables:
		for i in range(1, self.node_count+1):
			self.add_decl_bool(self.v(i))
			self.add_decl_bool(self.c(i))
			self.add_decl_int(self.l(i))
			self.add_decl_int(self.r(i))
			self.add_decl_int(self.p(i))
			self.add_decl_int(self.a(i))
			self.add_decl_int(self.v_sum(i))
			self.add_decl_int(self.not_v_sum(i))

			for r in range(1, self.feat_count+1):
				self.add_decl_bool(self.u(r, i))
				self.add_decl_bool(self.d0(r, i))
				self.add_decl_bool(self.d1(r, i))

		# Declare variable domains:
		self.add_comment('Variables domain')
		for i in range(1, self.node_count+1):
			self.add_assert(self.mk_le(self.a(i), self.feat_count)) 	# a_i <= K
			self.add_assert(self.mk_ge(self.a(i), 0))               	# a_i >= 0

			# p_j = i
			self.add_assert(self.mk_ge(self.p(i), i//2))  		# p_j >= j//2
			self.add_assert(self.mk_le(self.p(i), i-1))   		# p_j <= j-1

		# Define variable:
		self.add_comment('Variables definition')
		for i in range(1, self.node_count+1):
			self.add_assert(self.def_v_sum(i))
			self.add_assert(self.def_not_v_sum(i))

		## Encoding Topology
		# root node is not a leaf (1)
		self.add_comment('root node is not a leaf (1)')
		self.add_assert(self.mk_not(self.v(1)))

		# if i is a leaf then i has no children (2)
		self.add_comment('if i is a leaf then i has no children (2)')
		for i in range(1, self.node_count+1):
			self.add_assert(self.mk_impl(self.v(i), self.mk_eq(self.r(i), 0))); # v_i -> r_i = 0
			self.add_assert(self.mk_impl(self.v(i), self.mk_eq(self.l(i), 0))); # v_i -> l_i = 0
		
		# the left child and the right child of node i are numbered consecutively or they are both zero (3)
		self.add_comment('the left child and the right child of node i are numbered consecutively or they are both zero (3)')
		for i in range(1, self.node_count+1):
			l_plus_1 = self.mk_sum(self.l(i), 1)
			r_eq_l_plus_1 = self.mk_eq(self.r(i), l_plus_1)
			l_eq_0 = self.mk_eq(self.l(i), 0)
			r_eq_0 = self.mk_eq(self.r(i), 0)
			l_eq_0_and_r_eq_0 = self.mk_and(l_eq_0, r_eq_0)
			self.add_assert(self.mk_or(l_eq_0_and_r_eq_0, r_eq_l_plus_1))       # (l_i = 0 and r_i = 0) or (r_i = l_i+1)

		# l(i) in LR(i)
		self.add_comment('l(i) in LR(i)')
		for i in range(1, self.node_count+1):
			#  l_i is even
			self.add_assert(self.mk_eq(self.mk_mod(self.l(i), 2), 0)) # l_i%2 == 0
			
			# if i is not leaf, l_i >= i+1
			i_not_leaf = self.mk_not(self.v(i))
			l_i_ge_i_plus_1 = self.mk_ge(self.l(i), i+1)
			self.add_assert(self.mk_impl(i_not_leaf, l_i_ge_i_plus_1))          # not v(i) -> l_i >= i+1

			self.add_assert(self.mk_le(self.l(i), min(2*i, self.node_count-1))) # l_i <= min(2*i, N-1))
			refined_UB = self.mk_mul(2, self.mk_sub(i, self.v_sum(i)))
			self.add_assert(self.mk_le(self.l(i), refined_UB)) 					# l_i <= 2*(i - v_sum(i))
			refined_LB = self.mk_mul(2, self.mk_sub(self.not_v_sum(i), 1))
			li_gt_ref_LB = self.mk_gt(self.l(i), refined_LB)
			self.add_assert(self.mk_impl(i_not_leaf, li_gt_ref_LB)) 			# l_i > 2*(not_v_sum(i) - 1)

		# r(i) in RR(i)
		self.add_comment('r(i) in RR(i)')
		for i in range(1, self.node_count+1):
			# if i is not leaf, r_i is odd
			r_i_is_odd = self.mk_eq(self.mk_mod(self.r(i), 2), 1)
			i_not_leaf = self.mk_not(self.v(i))
			self.add_assert(self.mk_impl(i_not_leaf, r_i_is_odd))  # (-v_i) => (r_i%2 == 1)

			# if i is not leaf, r_i >= i+2
			r_i_ge_i_plus_2 = self.mk_ge(self.r(i), i+2)
			self.add_assert(self.mk_impl(i_not_leaf, r_i_ge_i_plus_2))          # not v(i) -> r_i >= i+2

			self.add_assert(self.mk_le(self.r(i), min(2*i+1, self.node_count))) # r_i <= min(2*i+1, N))
			refined_UB = self.mk_sum(1, self.mk_mul(2, self.mk_sub(i, self.v_sum(i))))
			self.add_assert(self.mk_le(self.r(i), refined_UB)) 					# r_i <= 2*(i - v_sum(i)) + 1
			refined_LB = self.mk_sub(self.mk_mul(2, self.not_v_sum(i)), 1)
			ri_gt_ref_LB = self.mk_gt(self.r(i), refined_LB)
			self.add_assert(self.mk_impl(i_not_leaf, ri_gt_ref_LB)) 			# l_i > 2*(not_v_sum(i) - 1)
		
		# if node i is a parent then it has a child (5)
		self.add_comment('if node i is a parent then it has a child (5)')
		for i in range(1, self.node_count+1):
			for j in self.LR(i):
				p_j_eq_i = self.mk_eq(self.p(j), i)
				l_i_eq_j = self.mk_eq(self.l(i), j)
				self.add_iff(p_j_eq_i, l_i_eq_j)     # p_j = i <-> l_i = j
			for j in self.RR(i):
				p_j_eq_i = self.mk_eq(self.p(j), i)
				r_i_eq_j = self.mk_eq(self.r(i), j)
				self.add_iff(p_j_eq_i, r_i_eq_j)     # p_j = i <-> r_i = j

		## Encoding Semantics
		# To discriminate a feature for value 0 at node j (7)
		self.add_comment('discriminate feature for value 0 (7)')
		for r in range(1, self.feat_count+1):
			# Why was the line below commented
			self.add_assert(self.mk_not(self.d0(r, 1)))
			for j in range(2, self.node_count + 1):
				big_OR = []
				for i in range(j//2, j):
					left_and = self.mk_and(self.mk_eq(self.p(j), i), self.d0(r, i))
					big_OR.append(left_and)
					if j in self.RR(i):
						right_and = self.mk_and(self.mk_eq(self.a(i), r), self.mk_eq(self.r(i), j))
						big_OR.append(right_and)

				or_clause = self.mk_or_list(big_OR)
				self.add_assert(self.mk_iff(self.d0(r, j), or_clause))

		# To discriminate a feature for value 1 at node j (8)
		self.add_comment('discriminate feature for value 1 (8)')
		for r in range(1, self.feat_count+1):
			self.add_assert(self.mk_not(self.d1(r, 1)))
			for j in range(2, self.node_count + 1):
				big_OR = []
				for i in range(j//2, j):
					left_and = self.mk_and(self.mk_eq(self.p(j), i), self.d1(r, i))
					big_OR.append(left_and)
					if j in self.LR(i):
						right_and = self.mk_and(self.mk_eq(self.a(i), r), self.mk_eq(self.l(i), j))
						big_OR.append(right_and)

				or_clause = self.mk_or_list(big_OR)
				self.add_assert(self.mk_iff(self.d1(r, j), or_clause))

		# Using a feature r at node j (9)
		for r in range(1, self.feat_count+1):
			for j in range(2, self.node_count+1):
				for i in range(j//2, j): # big AND
					u_and_p = self.mk_and(self.u(r, i), self.mk_eq(self.p(j), i))
					not_a_r = self.mk_not(self.mk_eq(self.a(j), r))
					self.add_assert(self.mk_impl(u_and_p, not_a_r))
				
				big_OR = []
				for i in range(j//2, j): # big OR
					u_r_i_and_p_j_i = self.mk_and(self.u(r, i), self.mk_eq(self.p(j), i))
					big_OR.append(u_r_i_and_p_j_i)
				big_OR.append(self.mk_eq(self.a(j), r))

				or_clause = self.mk_or_list(big_OR)
				self.add_assert(self.mk_iff(self.u(r, j), or_clause))

		# For a non-leaf node j, one feature is used (10)
		self.add_comment('For a non-leaf node j, one feature is used (10)')
		for j in range(1, self.node_count+1):
			not_v_j = self.mk_not(self.v(j))
			a_j_gt_0 = self.mk_gt(self.a(j), 0)
			self.add_assert(self.mk_impl(not_v_j, a_j_gt_0)) #  not(v_j) -> a_j > 0
		
		#  For a leaf node j, no feature is used (11)
		self.add_comment('For a leaf node j, no feature is used (11)')
		for j in range(1, self.node_count+1):
			a_j_eq_0 = self.mk_eq(self.a(j), 0)
			self.add_assert(self.mk_impl(self.v(j), a_j_eq_0)) #  v_j -> a_j = 0

		# Any positive example must be discriminated if the leaf node is
		#  associated with the negative class (12)
		#  and any negative example must be discriminated if the leaf node
		#  is associated with the positive class (13)
		#  samples is a list of samples, sample[:-1] are features
		#  and sample[-1] is the class (for sample in samples)
		self.add_comment('Any positive example must be discriminated if the leaf node is associated with the negative class (12)')
		self.add_comment('Any negative example must be discriminated if the leaf node is associated with the positive class (13)')

		for j in range(2, self.node_count+1):
			for q in samples:
				big_or = []
				for r_e, sigma in enumerate(q[:-1]):
					r = r_e+1 # because our r starts in 1 and enumerator starts in 0
					if sigma==1: # feature is 1
						big_or.append(self.d1(r, j))
					else: # sigma == 0, feature is 0
						big_or.append(self.d0(r, j))
				if q[-1] == 1: # class is 1
					class_lit = self.mk_not(self.c(j))
				else: # q[-1] == 0, class is 0
					class_lit = self.c(j)

				v_j_and_class_lit = self.mk_and(self.v(j), class_lit)
				self.add_assert(self.mk_impl(v_j_and_class_lit, self.mk_or_list(big_or))) # (v_j and class_lit) -> big_or
		
