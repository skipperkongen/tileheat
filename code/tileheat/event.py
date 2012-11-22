from time import strptime
from pyproj import Proj, Geod
from math import sqrt

class Bbox(object):
	"""docstring for Bbox"""
	def __init__(self, min_x, min_y, max_x, max_y):
		super(Bbox, self).__init__()
		self.min_x = min_x
		self.min_y = min_y
		self.max_x = max_x
		self.max_y = max_y

	def __str__(self):
		"""docstring for __str__"""
		return '(%d, %d, %d, %d)' % (self.min_x, self.min_y, self.max_x, self.max_y)
	
	@staticmethod
	def from_string(bbox_string):
		coordinates = map(lambda x : float(x.strip()), bbox_string.split(","))
		min_x = coordinates[0]
		min_y = coordinates[1]
		max_x = coordinates[2]
		max_y = coordinates[3]
		return Bbox(min_x, min_y, max_x, max_y)
	
	@staticmethod
	def from_dict(bbox_dict):
		return Bbox(bbox_dict['min_x'], bbox_dict['min_y'], bbox_dict['max_x'], bbox_dict['max_y'])
	
	def __str__(self):
		"""docstring for __str__"""
		return "%d,%d,%d,%d" % (self.min_x, self.min_y, self.max_x, self.max_y)

class WmsQuery(object):
	"""docstring for Query"""
	def __init__(self, srs, bbox, width=None, height=None, format=None, resource_id=None):
		super(WmsQuery, self).__init__()
		self.query_type = 'WMS'
		self.srs = srs
		self.bbox = bbox
		self.width = width
		self.height = height
		self.format = format
		self.resource_id = resource_id
		if width is not None and height is not None:
			# calculate resolution... this should slow things down, yay... :-(
			p = Proj(init=srs.lower())
			if not p.is_latlong():
				min_lon, min_lat = p(bbox.min_x,bbox.min_y, inverse=True)
				max_lon, max_lat = p(bbox.max_x,bbox.max_y, inverse=True)
			else:
				min_lon, min_lat = bbox.min_x, bbox.min_y
				max_lon, max_lat = bbox.max_x, bbox.max_y
			g = Geod(ellps='clrk66') # Use Clarke 1966 ellipsoid. 
			_,_,diagonal = g.inv(min_lon, min_lat, max_lon, max_lat)
			# distance calculated geodesic
			dist_x = sqrt(diagonal**2 / (1 + float(height)/float(width)) )
			dist_y = dist_x * (float(height)/float(width))
			self.x_res = dist_x / float(width)
			self.y_res = dist_y / float(height)
		else:
			self.x_res = None
			self.y_res = None

class WmtsQuery(object):
	"""docstring for Query"""
	def __init__(self, width, height, format):
		super(WmtsQuery, self).__init__()
		self.query_type = 'WMTS'
		self.width = width
		self.height = height
		self.format = format
		
	def __str__(self):
		"""docstring for __str__"""
		return vars(self).__str__()

class QueryEvent(object):
	"""docstring for QueryEvent"""
	def __init__(self, query, timestamp, worker, proc_ms, answer_size, userid):
		super(QueryEvent, self).__init__()
		self.query = query
		self.timestamp = timestamp
		self.worker = worker
		self.proc_ms = proc_ms
		self.answer_size = answer_size
		self.userid = userid
		
	def __str__(self):
		"""docstring for __str__"""
		return vars(self).__str__()
