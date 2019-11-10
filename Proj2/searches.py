from search import Search

class UNSAT_SAT(Search):

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

def odd(n):
	''' Given an integer n, return the closest odd number '''
	assert(n >= 0)
	if (n%2) == 0: return n-1
	else: return n

class Binary(Search):
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