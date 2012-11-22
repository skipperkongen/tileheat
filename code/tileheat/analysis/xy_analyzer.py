class XYAnalyzer(object):
	"""docstring for FormatAnalyzer"""
	def __init__(self, mapper=lambda event: (1,1), filter=lambda event: True):
		super(XYAnalyzer, self).__init__()
		self.X = []
		self.Y = []
		self.mapper = mapper
		self.filter = filter
		self.hits = 0

	def process(self, event):
		"""docstring for add"""
		#print event.format, self.filter(event)
		
		if self.filter(event):

			x,y = self.mapper(event)
			self.X.append(x)
			self.Y.append(y)
			self.hits += 1
	
	def get_xy(self):
		return (self.X, self.Y)