import sys


class KeyCounter(object):
	"""docstring for KeyCounter"""
	def __init__(self, domain=None):
		super(KeyCounter, self).__init__()
		self.domain = domain
		self.counter = {}
	
	def count(self, key):
		self.counter[key] = self.counter.setdefault(key,0) + 1
	
	def get_max(self):
		max = 0
		max_key = None
		for key in self.counter:
			if self.counter[key] > max:
				max = self.counter[key]
				max_key = key
		return (max_key, max)

	def get_min(self):
		min = sys.maxint
		min_key = None
		for key in self.counter:
			if self.counter[key] < min:
				min = self.counter[key]
				min_key = key
		return (min_key, min)
	
	def get_average(self):
		return sum(self.counter.values()) / float(len(self.counter)) if len(self.counter) > 0 else 0

	def to_xy(self):
		x = []
		y = []
		for key in sorted(self.counter.keys()):
			x.append(key)
			y.append(self.counter[key])
		return (x,y)
	
	def flatten(self):
		return [(key, self.counter[key]) for key in self.counter]
