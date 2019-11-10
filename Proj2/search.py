class Search:

	def __init__(self, LB, UB):
		self.UB = UB
		self.LB = LB
		self.best_model = None
		self.best_model_cost = self.UB +1

	def is_done(self, outcome, model, model_cost) -> bool:
		pass

	def get_next_n(self, previous_n, previous_outcome) -> int:
		pass

	def get_first_n(self) -> int:
		pass

	def get_best_model(self):
		return self.best_model, self.best_model_cost

	def is_sat(self) -> bool:
		return self.best_model is not None

	def __str__(self):
		return f"{self.__class__.__name__}: UB = {self.UB}; LB = {self.LB}"
