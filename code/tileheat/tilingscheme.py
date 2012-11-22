import sys
from pyproj import Proj, transform
from tileheat import Bbox
from math import floor, ceil
from tileheat.util import roundceil

class TilingScheme(object):
	"""Grid aligned to min_x and max_y"""
	def __init__(self, srs=None, bbox=None, tilesize=None, resolutions=None):
		super(TilingScheme, self).__init__()
		self.srs = srs.strip().lower()
		self.proj = Proj(init=self.srs)
		self.bbox = bbox
		self.tilesize = tilesize
		self.width = bbox.max_x - bbox.min_x
		self.height = bbox.max_y - bbox.min_y
		self.resolutions = resolutions
	
	def __str__(self):
		"""docstring for __str__"""
		return vars(self).__str__()
	
	def dim_x(self, resolution):
		"""docstring for _dim_x"""
		# hmmm, this if decreases performance. should we care?
		if resolution not in self.resolutions:
			raise ValueError("Resolution %d not in tiling scheme" % resolution)
		return int(roundceil(self.width / (float(resolution) * self.tilesize[0])))

	def dim_y(self, resolution):
		"""docstring for _dim_y"""
		# hmmm, this if decreases performance. should we care?
		if resolution not in self.resolutions:
			raise ValueError("Resolution %d not in tiling scheme" % resolution)
		return int(roundceil(self.height / (float(resolution) * self.tilesize[1])))

	def cellsize_x(self, resolution):
		# hmmm, this if decreases performance. should we care?
		if resolution not in self.resolutions:
			raise ValueError("Resolution %d not in tiling scheme" % resolution)
		return float(resolution) * self.tilesize[0]
		
	def cellsize_y(self, resolution):
		# hmmm, this if decreases performance. should we care?
		if resolution not in self.resolutions:
			raise ValueError("Resolution %d not in tiling scheme" % resolution)
		return float(resolution) * self.tilesize[1]
	
	def nearest_resolution(self, resolution):
		if resolution in self.resolutions:
			return resolution
		closest = sys.float_info.max
		best = None
		for r in self.resolutions:
			dist = abs(r-resolution)
			if dist < closest:
				closest = dist
				best = r
		return best

	def indices(self, srs, bbox, resolution):
		"""buggiest method ever!"""
		srs = srs.strip().lower()

		if srs != self.srs:
			# do reprojection
			proj = Proj(init=srs)
			(min_x, min_y) = transform(proj, self.proj, bbox.min_x, bbox.min_y)
			(max_x, max_y) = transform(proj, self.proj, bbox.max_x, bbox.max_y)
			bbox = Bbox(min_x, min_y, max_x, max_y)

		# completely outside boundary?
		outside_x = bbox.min_x >= self.bbox.max_x or bbox.max_x <= self.bbox.min_x
		outside_y = bbox.min_y >= self.bbox.max_y or bbox.max_y <= self.bbox.min_y
		if outside_x or outside_y:
			return None

		# truncate bbox
		min_x = max(bbox.min_x, self.bbox.min_x)
		max_x = min(bbox.max_x, self.bbox.max_x)
		min_y = max(bbox.min_y, self.bbox.min_y)
		max_y = min(bbox.max_y, self.bbox.max_y)

		cellsize_x = float(self.cellsize_x(resolution))
		cellsize_y = float(self.cellsize_y(resolution))

		# Note: upside-down rows compared to coordinates
		
		row_from = floor( (self.bbox.max_y - max_y) / cellsize_y )
		row_to   = floor( (self.bbox.max_y - min_y) / cellsize_y + 1.0 )
		col_from = floor( (min_x - self.bbox.min_x) / cellsize_x )
		col_to   = floor( (max_x - self.bbox.min_x) / cellsize_x + 1.0 )

		return (int(row_from), int(row_to), int(col_from), int(col_to))
	
	@staticmethod
	def by_name(name):
		scheme_dict = None
		if name is 'kms':
			scheme_dict = {
				'srs':'epsg:25832',
				'min_x': 161139.2,
				'min_y': 6080500.0,
				'max_x': 1000000.0,
				'max_y': 6499930.4,
				'tilesize': (256,256),
				#'resolutions': [25.6, 51.2, 102.4, 204.8, 409.6, 819.2, 1638.4]
				#'resolutions': [3.2, 102.4]
				'resolutions': [0.8, 1.6, 3.2, 6.4, 12.80, 25.6, 51.2, 102.4, 204.8, 409.6, 819.2, 1638.4]
				#'resolutions': [0.4, 0.8, 1.6, 3.2, 6.4, 12.80, 25.6, 51.2, 102.4, 204.8, 409.6, 819.2, 1638.4]
				#'resolutions': [0.05, 0.1, 0.2, 0.4, 0.8, 1.6, 3.2, 6.4, 12.80, 25.6, 51.2, 102.4, 204.8, 409.6, 819.2, 1638.4]
			}
		if scheme_dict is None:
			raise Exception('Unknown tiling scheme identifier: ', name)
		
		return TilingScheme(srs=scheme_dict['srs'], bbox=Bbox.from_dict(scheme_dict), tilesize=scheme_dict['tilesize'], resolutions=scheme_dict['resolutions'])
