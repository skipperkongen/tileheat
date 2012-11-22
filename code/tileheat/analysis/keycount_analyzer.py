from tileheat.util import KeyCounter

class KeycountAnalyzer(object):
	"""docstring for GeneralStatistics"""
	def __init__(self, key=lambda e: 'foo'):
		super(KeycountAnalyzer, self).__init__()
		self.key = key
		self.counter = KeyCounter()
	
	def process(self, event):
		"""docstring for process"""
		self.counter.count(self.key(event))
		