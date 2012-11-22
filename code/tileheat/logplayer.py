from datetime import datetime
from datetime import timedelta
import sys, traceback

class LogPlayer(object):
	
	"""docstring for Analyzer"""
	def __init__(self, datasource):
		super(LogPlayer, self).__init__()
		self.generator = datasource.events()
		self.analyzers = []
		# just for info
		self.events_analyzed = 0
		self.events_seen = 0
		self.event = None
		self.errors_last_run = 0
		self.samples_last_run = 0
	
	def add_analyzer(self, analyzer):
		"""docstring for add_analyzer"""
		self.analyzers.append(analyzer)	
	
	def forward(self, count=None, time_delta=None, from_time=None, to_time=None):
		self.errors_last_run = 0
		self.samples_last_run = 0
		try:
			if self.event is None:
				self.event = self.generator.next()
			
			# configure predicates
			halt = self._halt_predicate( count, time_delta, to_time )
			record = self._record_predicate( from_time )
						
			while True:
				if halt( self.events_analyzed, self.event ):
					raise StopIteration
				if record( self.event ):
					for analyzer in self.analyzers:
						#
						try:
							analyzer.process( self.event )
							self.samples_last_run += 1
						except:
							#print sys.exc_info()[0], sys.exc_info()[1], traceback.format_exc()  
							self.errors_last_run += 1
					self.events_analyzed += 1
				# get next event
				self.events_seen += 1
				self.event = self.generator.next()
							
		except StopIteration:
			pass
	
	def _halt_predicate(self, count, time_delta, to_time):
		"""docstring for _get_halt"""
		if count is not None:
			target = self.events_analyzed + count
			return lambda events_analyzed, event: events_analyzed >= target
		if time_delta is not None:
			target = self.event.timestamp + time_delta
			return lambda events_analyzed, event: event.timestamp >= target
		if to_time is not None:
			target = to_time
			return lambda events_analyzed, event: event.timestamp >= target
		# default predicate: continue to end
		return lambda events_analyzed, event: False
	
	def _record_predicate(self, from_time):
		"""docstring for _get_record"""
		if from_time is not None:
			return lambda event: event.timestamp >= from_time
		else:
			return lambda event: True