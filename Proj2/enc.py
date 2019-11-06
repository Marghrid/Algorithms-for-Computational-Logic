class Enc:
	def __init__(self, feat_count,  node_count):
		 self.node_count = node_count
		 self.feat_count = feat_count
		 self.constraints = []
		 self.fresh = 0
		 self.s_fresh = 0

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

	# Bool. True iff node i is a leaf node, i = 1,...,N
	def v(self, i):
		assert(i >= 1 and i <= self.node_count)
		return f'v_{i}'

	# Int. l_i = j iff node i has node j as the left child, j in LR(i), i = 1,...,N
	#      l_i = 0 iff i is a leaf -> does not have any children
	def l(self, i):
		assert(i >= 1 and i <= self.node_count)
		return f'l_{i}'

	# Int. r_i = j iff node i has node j as the right child, j in RR(i), i = 1,...,N.
	#      r_i = 0 iff i is a leaf -> does not have any children
	def r(self, i):
		assert(i >= 1 and i <= self.node_count)
		return f'r_{i}'
	
	# Int. p_j = i iff the parent of node j is node i, j = 2,...,N, i = 1,...,N −1
	def p(self, j): 
		assert(j >= 1 and j <= self.node_count)
		return f'p_{j}'

	# # 1 iff feature r is assigned to node j, r = 1,...,K, j = 1,...,N
	# def a(self, r, j):
	# 	assert(r >= 1 and r <= self.feat_count)
	# 	assert(j >= 1 and j <= self.node_count)
	# 	return f'a_{r}_{j}'

	# # 1 iff feature r is being discriminated against by node j, r = 1,...,K, j = 1,...,N,
	# def u(self, r, j):
	# 	assert(r >= 1 and r <= self.feat_count)
	# 	assert(j >= 1 and j <= self.node_count)
	# 	return f'u_{r}_{j}'

	# # 1 iff feature r is discriminated for value 0 by node j,
	# #  or by one of its ancestors, r = 1,...,K, j = 1,...,N,
	# def d0(self, r, j):
	# 	assert(r >= 1 and r <= self.feat_count)
	# 	assert(j >= 1 and j <= self.node_count)
	# 	return f'd0_{r}_{j}'

	# # 1 iff feature r is discriminated for value 1 by node j,
	# #  or by one of its ancestors, r = 1,...,K, j = 1,...,N,
	# def d1(self, r, j):
	# 	assert(r >= 1 and r <= self.feat_count)
	# 	assert(j >= 1 and j <= self.node_count)
	# 	return f'd1_{r}_{j}'

	# # 1 iff class of leaf node j is 1, j = 1,...,N.
	# def c(self, j):
	# 	assert(j >= 1 and j <= self.node_count)
	# 	return f'c_{j}'

	def add_assert(self, atom):
		'''add asserts, which are atoms??'''
		assert(atom is not None)
		assert(isinstance(atom, str))
		self.constraints.append(f'(assert {atom})')

	def add_decl_bool(self, name):
		assert(name is not None)
		self.constraints.append(f'(declare-const {name} Bool)')

	def add_decl_int(self, name):
		assert(name is not None)
		self.constraints.append(f'(declare-const {name} Int)')

	# Integer comparison operations
	def mk_le(self, left, right):
		assert(left is not None)
		assert(right is not None)
		return f'(<= {left} {right})'

	def mk_ge(self, left, right):
		assert(left is not None)
		assert(right is not None)
		return f'(>= {left} {right})'

	def mk_eq(self, left, right):
		assert(left is not None)
		assert(right is not None)
		return f'(= {left} {right})'

	# Integer arithmetic operations
	def mk_mod(self, left, right):
		assert(left is not None)
		assert(right is not None)
		return f'(mod {left} {right})'

	def mk_sum(self, left, right):
		assert(left is not None)
		assert(right is not None)
		return f'(+ {left} {right})'


	# Boolean operations
	def mk_not(self, arg):
		assert(arg is not None)
		return f'(not {arg})'

	def mk_impl(self, left, right):
		assert(left is not None)
		assert(right is not None)
		return f'(=> {left} {right})'

	def mk_iff(self, left, right):
		assert(left is not None)
		assert(right is not None)
		return f'(= {left} {right})'

	def print_solution(self, model):
		'''
		prints solution output, according to the format:
		- 'l i j' representing that j is a left (0) child of i
		- 'r i j' representing that j is a right (1) child of i
		- 'c i v' leaf i responds with the class v
		- 'a r i' the feature r is assigned to internal node i
		'''

		# I need to know v(i) so the values of vars are printed only for relevant nodes:
		#  l, r, and a are only for internal nodes i s.t. v(i) = False
		#  c is only for leaf nodes i s.t. v(i) = True

		for str_var in sorted(self.var_map.keys()):
			if str_var[0] in ['l', 'r']: # l and r are treated the same
				dimacs_idx = self.var_map[str_var] # get dimacs idx
				if dimacs_idx in model and model[dimacs_idx]: # if var is true
					var_name, i, j = str_var.split("_")
					v_dimax_idx = self.var_map[self.v(int(i))]
					if v_dimax_idx in model and not model[v_dimax_idx]: # i is an internal node
						print(f'{var_name} {i} {j}')

			elif str_var[0] == 'a': # a vars
				dimacs_idx = self.var_map[str_var] # get dimacs idx
				if dimacs_idx in model and model[dimacs_idx]: # if var is true
					_, r, i = str_var.split("_")
					v_dimax_idx = self.var_map[self.v(int(i))]
					if v_dimax_idx in model and not model[v_dimax_idx]: # i is an internal node
						print(f'a {r} {i}')

			elif str_var[0] == 'c': # c vars have only one arg
				dimacs_idx = self.var_map[str_var] # get dimacs idx
				if dimacs_idx in model: # if var is true
					_, j = str_var.split("_")
					v_dimax_idx = self.var_map[self.v(int(j))]
					if v_dimax_idx in model and model[v_dimax_idx]: # j is a leaf node
						print(f'c {j} {"1" if model[dimacs_idx] else "0"}')

	def print_model(self,model):
		'''prints SAT model'''
		print('# === model')
		for var in sorted(model):
			print(f'# {var} = {model[var]}')
		print('# === end of model')

	def print_tree(self, model):
		''' prints the decision tree '''
		print('# === tree')
		print('digraph T {')
		print('edge [penwidth=2]')
		is_node_leaf = {}

		# fill is_node_leaf
		for str_var in sorted(self.var_map.keys()):
			if str_var[0] == 'v':  # v vars
				dimacs_idx = self.var_map[str_var]
				if dimacs_idx in model: # if var is true
					_, i = str_var.split("_")
					is_node_leaf[i] = model[dimacs_idx]

		for str_var in sorted(self.var_map.keys()):
			if str_var[0] == 'a': # a vars
				dimacs_idx = self.var_map[str_var]
				if dimacs_idx in model and model[dimacs_idx]: # if var is true
					_, r, j = str_var.split("_")
					if not is_node_leaf[j]:
						print(f'{j} [label="{j} : f{r}"]')
			elif str_var[0] == 'c': # c vars
				dimacs_idx = self.var_map[str_var]
				if dimacs_idx in model:
					_, j = str_var.split("_")
					if is_node_leaf[j]:
						label = f'{j} : {"1" if model[dimacs_idx] else "0"}'
						print(f'{j} [label="{label}", style=filled, color="#DFDFDF"]')

		for str_var in sorted(self.var_map.keys()):
			if str_var[0] in ['r', 'l']:
				dimacs_idx = self.var_map[str_var]
				if dimacs_idx in model and model[dimacs_idx]:
					var_name, i, j = str_var.split("_")
					if var_name == 'r':
						print(f'{i} -> {j}  [label="1", color="blue"]')
					else:
						print(f'{i} -> {j}  [label="0", color="red"]')

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

	def enc(self, samples):
		'''encode the problem'''

		# Declare variables:
		for i in range(1, self.node_count+1):
			self.add_decl_bool(self.v(i))
			self.add_decl_int(self.l(i))
			self.add_decl_int(self.r(i))
			self.add_decl_int(self.p(i))

		# Declare variable domains:
		for i in range(1, self.node_count+1):
			self.add_assert(self.mk_le(self.l(i), self.node_count)) # l_i <= N
			self.add_assert(self.mk_le(self.r(i), self.node_count)) # r_i <= N
			self.add_assert(self.mk_le(self.p(i), self.node_count)) # p_i <= N

			self.add_assert(self.mk_ge(self.l(i), 0))               # l_i <= 0
			self.add_assert(self.mk_ge(self.r(i), 0))               # r_i <= 0
			self.add_assert(self.mk_ge(self.p(i), 0))               # p_i <= 0

			# from here onwards: can I remove?
			## l(i) in LR(i)
			self.add_assert(self.mk_eq(self.mk_mod(self.l(i), 2), 0))            # l_i%2 == 0
			self.add_assert(self.mk_impl(self.mk_not(self.v(i)), self.mk_ge(self.l(i), i+1))) # not v(i) -> l_i >= i+1
			self.add_assert(self.mk_le(self.l(i), min(2*i, self.node_count-1)))  # l_i <= min(2*i, N-1))
#
			## r(i) in RR(i)
			self.add_assert(self.mk_eq(self.mk_mod(self.r(i), 2), 1))            # r_i%2 == 1
			#self.add_assert(self.mk_impl(self.mk_not(self.v(i)), self.mk_ge(self.r(i), i+2))) # not v(i) -> r_i >= i+2
			self.add_assert(self.mk_le(self.r(i), min(2*i+1, self.node_count)))  # r_i <= min(2*i+1, N))

		## Encoding Topology
		# root node is not a leaf (1)
		self.add_assert(self.mk_not(self.v(1)))

		# if i is a leaf then i has no children (2)
		for i in range(1, self.node_count+1):
			self.add_assert(self.mk_impl(self.v(i), self.mk_eq(self.l(i), 0))); # v_i -> l_i = 0
			self.add_assert(self.mk_impl(self.v(i), self.mk_eq(self.r(i), 0))); # v_i -> r_i = 0
		
		# the left child and the right child of node i are numbered consecutively (3)
		for i in range(1, self.node_count+1):
			for j in self.LR(i):
				l_plus_1 = self.mk_sum(self.l(i), 1)
				self.add_assert(self.mk_eq(self.r(i), l_plus_1))  # r_i = l_i + 1
		
		# non-leaf node must have a child (4) is implicit in domain!! :D
		
		# if node i is a parent then it has a child (5)
		for i in range(1, self.node_count+1):
			for j in self.LR(i):
				p_j_eq_i = self.mk_eq(self.p(j), i)
				l_i_eq_j = self.mk_eq(self.l(i), j)
				self.add_assert(self.mk_iff(p_j_eq_i, l_i_eq_j)) # p_j = i <-> l_i = j
			for j in self.RR(i):
				p_j_eq_i = self.mk_eq(self.p(j), i)
				r_i_eq_j = self.mk_eq(self.r(i), j)
				self.add_assert(self.mk_iff(p_j_eq_i, r_i_eq_j)) # p_j = i <-> r_i = j

		# all nodes but node 1 have a parent (6).
		# Just need to say that 1 does not have a parent, the rest is implicit in domain.

		self.add_assert(self.mk_eq(self.p(1), 0))                # p_1 = 0
		

		# ## Encoding Semantics
		# #  To discriminate a feature for value 0 at node j (7)
		# for r in range(1, self.feat_count+1):
		# 	self.add_constraint([neg(self.d0(r, 1))])
		# 	for j in range(2, self.node_count + 1):
		# 		big_OR = []
		# 		for i in range(j//2, j):
		# 			aux1 = self.mk_and(self.p(j, i), self.d0(r, i))
		# 			if j in self.RR(i):
		# 				aux2 = self.mk_and(self.a(r, i), self.r(i, j))
		# 				big_OR.extend([aux1, aux2])
		# 			else:
		# 				big_OR.append(aux1)
		# 		self.add_lit_iff_clause(self.d0(r, j), big_OR)

		# # To discriminate a feature for value 1 at node j (8)
		# for r in range(1, self.feat_count+1):
		# 	self.add_constraint([neg(self.d1(r, 1))])
		# 	for j in range(2, self.node_count + 1):
		# 		big_OR = []
		# 		for i in range(j//2, j):
		# 			aux1 = self.mk_and(self.p(j, i), self.d1(r, i))

		# 			if j in self.LR(i):
		# 				aux2 = self.mk_and(self.a(r, i), self.l(i, j))
		# 				big_OR.extend([aux1, aux2])
		# 			else:
		# 				big_OR.append(aux1)
		# 		self.add_lit_iff_clause(self.d1(r, j), big_OR)

		# # Using a feature r at node j (9)
		# for r in range(1, self.feat_count):
		# 	for j in range(2, self.node_count+1):
		# 		for i in range(j//2, j): # big AND
		# 			#self.add_constraint([self.u(r, i)])
		# 			#self.add_impl(self.p(j, i), neg(self.a(r, j)))
		# 			self.add_constraint([neg(self.u(r, i)), neg(self.p(j, i)), neg(self.a(r, j))])
				
		# 		big_OR = []
		# 		for i in range(j//2, j): # big OR
		# 			aux = self.mk_and(self.u(r, i), self.p(j, i))
		# 			big_OR.append(aux)
		# 		big_OR.append(self.u(r, j))

		# 		self.add_lit_iff_clause(self.u(r, j), big_OR)

		# # For a non-leaf node j, exactly one feature is used (10)
		# #  and For a leaf node j, no feature is used (11)
		# for j in range(1, self.node_count+1):
		# 	sum_lits = []
		# 	for r in range(1, self.feat_count+1):
		# 		sum_lits.append(self.a(r, j))

		# 	self.add_sum_eq1(sum_lits, [self.v(j)])       # (10)
		# 	self.add_sum_eq0(sum_lits, [neg(self.v(j))])  # (11)

		
		# # Any positive example must be discriminated if the leaf node is
		# #  associated with the negative class (12)
		# #  and any negative example must be discriminated if the leaf node
		# #  is associated with the positive class (13)
		# # samples is a list of samples, sample[:-1] are features
		# #  and sample[-1] is the class (for sample in samples)
		# for j in range(2, self.node_count+1):
		# 	for q in samples:
		# 		sum_lits = []
		# 		for r_e, sigma in enumerate(q[:-1]):
		# 			r = r_e+1 # because our r starts in 1 and enumerator starts in 0
		# 			if sigma==1: # feature is 1
		# 				sum_lits.append(self.d1(r, j))
		# 			else: # sigma == 0, feature is 0
		# 				sum_lits.append(self.d0(r, j))
		# 		if q[-1] == 1: # class is 1
		# 			class_lit = self.c(j)
		# 		else: # q[-1] == 0, class is 0
		# 			class_lit = neg(self.c(j))

		# 		self.add_sum_ge1(sum_lits, [neg(self.v(j)), class_lit])
