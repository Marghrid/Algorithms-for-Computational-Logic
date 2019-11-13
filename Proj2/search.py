class Search:
	''' Abstract superclass for all search methods. Follows the Strategy design pattern. '''
	def __init__(self, LB, UB):
		self.UB = UB
		self.LB = LB
		self.best_model = None
		self.best_model_cost = self.UB +1

	def is_done(self, outcome, model, model_cost) -> bool:
		'''
		Returns True iff no more iterations are needed for the search to
		output the optimal solution. Defined in subclasses.
		'''
		pass

	def get_next_n(self, previous_n, previous_outcome) -> int:
		''' Returns the next n to be tested. Defined in subclasses. '''
		pass

	def get_first_n(self) -> int:
		''' Returns the first n to be tested. Defined in subclasses. '''
		pass

	def get_best_model(self):
		'''
		Returns the best model found, along with its cost. If called after
		is_done() returns True, this is the optimum model. Defined in subclasses.
		'''
		return self.best_model, self.best_model_cost

	def is_sat(self) -> bool:
		'''
		Returns True iff a SAT model was found. If called after is_done()
		returns True, is_sat() = False means there is no SAT model.
		Defined in subclasses.
		'''
		return self.best_model is not None

	def __str__(self):
		return f"{self.__class__.__name__}: UB = {self.UB}; LB = {self.LB}"
