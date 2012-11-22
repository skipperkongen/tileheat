class CacheAnalyzer(object):
	"""docstring for CacheAnalyzer"""
	def __init__(self, cache):
		super(CacheAnalyzer, self).__init__()
		self.cache = cache
		self.hits = 0
		self.misses = 0
	
	def process(self, event):
		"""docstring for process"""
		result = self.cache.test_query( event.query )
		self.misses += result.num_tiles - result.hits
		self.hits += result.hits
	
	def get_hit_ratio(self):
		return float(self.hits) / float(self.hits + self.misses)
