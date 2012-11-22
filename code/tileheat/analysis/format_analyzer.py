class FormatAnalyzer(object):
	"""docstring for FormatAnalyzer"""
	def __init__(self):
		super(FormatAnalyzer, self).__init__()
		# {'image/dummy': {'seen':1, 'pixel_sum':1}}
		self.formats = {}
		self.text1='TITLE'
		self.text2='total count'
		self.unit='unit'
		self.mapper = lambda event: 1
		self.reducer = lambda format: round( self.formats[format]['metric'] / self.formats[format]['observations'], 2 )

	def process(self, event):
		"""docstring for add"""
		format = event.format
		if format not in self.formats:
			self.formats[format] = {'observations':0.0, 'metric':0.0}
		record = self.formats[format]
		record['observations'] += 1.0
		metric = float(self.mapper(event))
		record['metric'] += metric

	def print_report(self):
		print self.text1		
		for f in self.formats:
			print "\t", f, self.text2, self.reducer(f), self.unit

class AveragePixels(FormatAnalyzer):
	"""docstring for DummyAnalyzer"""
	def __init__(self):
		super(AveragePixels, self).__init__()
		# {'image/dummy': {'seen':1, 'pixel_sum':1}}
		self.formats = {}
		self.text1='PIXELS'
		self.text2='average pixels'
		self.mapper = lambda event: event.width*event.height
		self.unit = 'pixels'

class AverageSize(FormatAnalyzer):
	"""docstring for DummyAnalyzer"""
	def __init__(self):
		super(AverageSize, self).__init__()
		# {'image/dummy': {'seen':1, 'pixel_sum':1}}
		self.formats = {}
		self.text1='SIZE'
		self.text2='average size'
		self.mapper = lambda event: event.answer_size
		self.unit = 'bytes'

class AverageProc(FormatAnalyzer):
	"""docstring for DummyAnalyzer"""
	def __init__(self):
		super(AverageProc, self).__init__()
		# {'image/dummy': {'seen':1, 'pixel_sum':1}}
		self.formats = {}
		self.text1='PROC'
		self.text2='average proc'
		self.mapper = lambda event: event.proc_ms
		self.unit = 'ms'

class AverageProcPerTile(FormatAnalyzer):
	"""docstring for DummyAnalyzer"""
	def __init__(self):
		super(AverageProcPerTile, self).__init__()
		# {'image/dummy': {'seen':1, 'pixel_sum':1}}
		self.formats = {}
		self.text1='PROC PER TILE'
		self.text2='average ms per 256x256 tile'
		self.mapper = lambda event: event.proc_ms / ( (event.width * event.height) / (256.0 * 256.0) )
		self.unit = 'ms'