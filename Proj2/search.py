class Search:

	def __init__(self, n_feats, smp):
		self.UB = 2 ** (n_feats+1) +1 # ID3(smp)
		self.LB = 3
		self.best_model = None
		self.best_model_cost = self.UB

	def is_done(self, outcome, model, model_cost) -> bool:
		pass

	def get_next_n(self, previous_n) -> int:
		pass

	def get_first_n(self) -> int:
		pass

	def get_best_model(self):
		return self.best_model, self.best_model_cost

	def is_sat(self) -> bool:
		ret = self.best_model is not None
		return ret
