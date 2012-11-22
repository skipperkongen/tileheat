import csv
import sys, traceback
from time import strptime
from event import Bbox, WmsQuery, WmtsQuery, QueryEvent

class CsvFileSource(object):
	"""docstring for CsvSource"""
	def __init__(self, path, datetime_format='%y/%m/%d %H:%M:%S', event_type='WMS'):
		super(CsvFileSource, self).__init__()
		self.reader = csv.DictReader(open(path, 'rb'))
		self.datetime_format = datetime_format
		self.event_type = event_type
		self.errors = 0
		
	def events(self):
		"""docstring for next"""
		for row in self.reader:
			
			try:
				if self.event_type == 'WMS':
					timestamp = strptime( row['TIMEOFDAY'].strip(), self.datetime_format )
					bbox = Bbox.from_string( row['BBOX'].strip().lower() )
					srs = row['SRS'].strip().lower()
					format = row['FORMAT'].strip().lower()
					proc_ms = int( row['PROC_MS'].strip().lower() )
					answer_size = int( row['SIZE_BYTES'].strip().lower() )
					width = int( row['WIDTH'].strip().lower() )
					height = int( row['HEIGHT'].strip().lower() )
					worker = row['WORKER'].strip().lower()
					userid = row['USERID'].strip().lower()
					query = WmsQuery(srs, bbox, width, height, format)
				elif self.event_type == 'WMTS':
					timestamp = strptime( row['TIMEOFDAY'].strip(), self.datetime_format )
					proc_ms = int( row['PROC_MS'].strip().lower() )
					answer_size = int( row['SIZE_BYTES'].strip().lower() )
					worker = row['WORKER'].strip().lower()
					userid = row['USERID'].strip().lower()
					width = 256
					height = 256
					format = row['FORMAT'].strip().lower()
					query = WmtsQuery(width, height, format)
				
				#print bbox_query.x_res, row
				yield QueryEvent(query, timestamp, worker, proc_ms, answer_size, userid)
			except:
				#print row
				#print sys.exc_info()[0], sys.exc_info()[1], traceback.format_exc()
				self.errors += 1



