from search import Search

class UNSAT_SAT(Search):
	''' UNSAT-SAT search '''
	def is_done(self, outcome, model, model_cost) -> bool:
		if outcome=='sat':
			if model_cost < self.best_model_cost:
				self.best_model = model
				self.best_model_cost = model_cost
		return outcome=='sat' or self.get_next_n(model_cost) > self.UB

	def get_next_n(self, previous_n, previous_outcome='sat') -> int:
		assert (previous_n+2) % 2 == 1, f"{previous_n+2} is not odd"
		return previous_n+2

	def get_first_n(self) -> int:
		return self.LB

class SAT_UNSAT(Search):
	''' SAT-UNSAT search '''
	def is_done(self, outcome, model, model_cost) -> bool:
		if outcome=='sat':
			if model_cost < self.best_model_cost:
				self.best_model = model
				self.best_model_cost = model_cost
		return outcome=='unsat' or self.get_next_n(model_cost) < self.LB

	def get_next_n(self, previous_n, previous_outcome='') -> int:
		assert (previous_n+2) % 2 == 1, f"{previous_n+2} is not odd"
		return previous_n-2

	def get_first_n(self) -> int:
		return self.UB

def odd(n):
	''' Given an integer n, return the closest odd number '''
	assert(n >= 0)
	if (n%2) == 0: return n-1
	else: return n


class Binary(Search):
	''' Binary search '''
	def is_done(self, outcome, model, model_cost) -> bool:
		if outcome=='sat':
			if model_cost < self.best_model_cost:
				self.best_model = model
				self.best_model_cost = model_cost
			return self.LB == model_cost
		else: # previous_outcome == 'unsat':
			return self.LB == self.UB

	def get_next_n(self, previous_n, previous_outcome) -> int:
		assert (previous_n+2) % 2 == 1, f"{previous_n+2} is not odd"
		assert previous_outcome in ['sat', 'unsat']
		if previous_outcome == 'sat':
			self.UB = previous_n
		else: # previous_outcome == 'unsat':
			self.LB = previous_n + 2
		return odd((self.UB + self.LB) // 2)

	def get_first_n(self) -> int:
		return odd((self.UB + self.LB) // 2)

class Progressive(Search):
	''' Progressive search '''
	def __init__(self, LB, UB, UB_model=None):
		super().__init__(LB, UB, UB_model)
		self.state = 'progressive'

	def is_done(self, outcome, model, model_cost) -> bool:
		if self.state == 'progressive':
			if model_cost == self.UB and self.best_model:
				if outcome == 'sat' and model_cost < self.best_model_cost:
					self.best_model = model
					self.best_model_cost = model_cost
				return True 
			return False
		if outcome=='sat':
			if model_cost < self.best_model_cost:
				self.best_model = model
				self.best_model_cost = model_cost
			return self.LB == model_cost
		else: # previous_outcome == 'unsat':
			return self.LB == self.UB

	def get_next_n(self, previous_n, previous_outcome) -> int:
		assert (previous_n+2) % 2 == 1, f"{previous_n+2} is not odd"
		assert previous_outcome in ['sat', 'unsat']
		if self.state == 'progressive':
			if previous_outcome == 'unsat':
				self.LB = previous_n + 2
				return min((previous_n-1) * 2 + 1, self.UB)
			else: # previous_outcome == 'sat'
				self.state = 'binary'
				self.UB = previous_n
				return odd((self.UB + self.LB) // 2)
		else: # self.state == 'binary'
			if previous_outcome == 'sat':
				self.UB = previous_n
			else: # previous_outcome == 'unsat':
				self.LB = previous_n + 2
			return odd((self.UB + self.LB) // 2)

	def get_first_n(self) -> int:
		return self.LB # which is 3
