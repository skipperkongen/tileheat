from datetime import datetime

class StreamStats(object):
	"""docstring for GeneralStatistics"""
	def __init__(self):
		super(StreamStats, self).__init__()
		self.min_datetime = datetime.max
		self.max_datetime = datetime.min
	
	def process(self, event):
		"""docstring for process"""
		self.min_datetime = min (self.min_datetime, event.timestamp)
		self.max_datetime = max (self.max_datetime, event.timestamp)
		