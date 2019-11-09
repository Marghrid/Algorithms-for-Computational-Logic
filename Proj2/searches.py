from search import Search

class UNSAT_SAT(Search):

	def is_done(self, outcome, model, model_cost) -> bool:
		if outcome=='sat':
			if model_cost < self.best_model_cost:
				self.best_model = model
				self.best_model_cost = model_cost
		return outcome=='sat' or model_cost >= self.UB

	def get_next_n(self, previous_n) -> int:
		assert (previous_n+2) % 2 == 1, f"{previous_n+2} is not odd"
		return previous_n+2

	def get_first_n(self) -> int:
		return self.LB