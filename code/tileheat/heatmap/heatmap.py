from tileheat.util import MatrixUtil
from math import floor
import numpy as np

class MultiscaleHeatmap(object):
	"""docstring for Heatmap"""
	def __init__(self, tiling_scheme, snap=True):
		super(MultiscaleHeatmap, self).__init__()
		self.tiling_scheme = tiling_scheme
		self.snap = snap
		self.levels = {}	
		for resolution in tiling_scheme.resolutions:
			rows = tiling_scheme.dim_y( resolution )
			cols = tiling_scheme.dim_x( resolution )
			self.levels[resolution] = Level( rows, cols, resolution )

	def squish(self):
		total_heat = self.total_heat()
		for level in self.levels.values():
			level.matrix = level.matrix / total_heat

	def get_level(self, resolution):
		if resolution not in self.levels:
			raise ValueError("Resolution not supported: %s" % resolution)
		return self.levels[resolution]
	
	def get_indices(self, srs, bbox, resolution):
		return self.tiling_scheme.indices(srs, bbox, resolution)

	def sorted_cells(self, exclude_zeros=True, hottest_first=True):
		return sorted( self.cell_generator(exclude_zeros), reverse=hottest_first, key=lambda cell: cell.value)
		
	def cell_generator(self, exclude_zeros=True):
		for resolution in sorted(self.levels, reverse=True):
			level = self.get_level(resolution)
			for i in range(level.rows):
				for j in range(level.cols):
					if not exclude_zeros or level.matrix[i,j] > 0:
						yield Cell(resolution, i, j, level.matrix[i,j])
	
	def flatten(self):
		flat = np.zeros((0,0))
		for level in self.levels.values():
			flat = np.append(flat, level.matrix.flatten())
		return flat
				
	def max_heat(self):
		return max( [np.max(level.matrix) for level in self.levels.values()] )

	def total_heat(self):
		return sum( [level.total_heat() for level in self.levels.values()] )

	def get_cell(self, resolution, row, col):
		return Cell(resolution, row, col, self.levels[resolution].matrix[row,col])

	def get_cells(self, row_from, row_to, col_from, col_to, resolution):
		return self.get_level(resolution).matrix[row_from:row_to, col_from:col_to]
	
	
	def num_cells_affected(self):
		return sum( [level.cells_affected() for level in self.levels.values()] )
	
	def num_cells(self):
		return sum( [level.num_cells() for level in self.levels.values()] )
	
	def dissipate(self, coefficient, scale=0.1):
		for level in self.levels.values():
			level.dissipate(coefficient, scale)
	
	def increment_cell(self, resolution, row, col, value=1):
		level = self.get_level( resolution )
		level.increment( row, col, value )

	def increment_cells(self, row_from, row_to, col_from, col_to, resolution, value=1):
		level = self.get_level( resolution )
		level.increment_range( row_from, row_to, col_from, col_to, value )

	def get_cells_by_bbox(self, srs, bbox, resolution):
		if self.snap:
			resolution = self.tiling_scheme.nearest_resolution( resolution )
		indices = self.get_indices(srs, bbox, resolution)
		if indices is not None:
			(row_from, row_to, col_from, col_to) = indices
			return self.get_cells(row_from, row_to, col_from, col_to, resolution)
	
	def increment_cells_by_bbox(self, srs, bbox, resolution, value):
		if self.snap:
			resolution = self.tiling_scheme.nearest_resolution( resolution )		
		indices = self.get_indices(srs, bbox, resolution)
		if indices is not None:
			(row_from, row_to, col_from, col_to) = indices
			# debug:
			#if row_to - row_from > 10 or col_to - col_from > 10:
			#	print "Big one: SRS=%s BBOX=(%f,%f,%f,%f) RES=%s" % (srs, bbox.min_x, bbox.min_y, bbox.max_x, bbox.max_y, resolution) 
			self.increment_cells( row_from, row_to, col_from, col_to, resolution, value )
	
class Level(object):
	"""docstring for Level"""
	def __init__(self, rows, cols, resolution):
		super(Level, self).__init__()
		# initialize it
		self.rows = rows
		self.cols = cols
		self.resolution = resolution
		self.matrix = np.zeros((rows, cols))
			
	def __str__(self):
		"""docstring for __str__"""
		return vars(self).__str__()
	
	def dissipate(self, coefficient, scale=0.1):		
		"""docstring for dissipate"""
		iterations = int(floor (scale * (self.rows + self.cols) / 2.0))
		tmp = np.zeros((self.matrix.shape))
		frac = coefficient / 8.0 # heat that goes to neighbours
		if 0 < coefficient < 1:
			# write down
			tmp += self.matrix * (1- coefficient)
			# scatter
			for i in range(iterations):
				for shift in [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]:
					tmp += np.roll(np.roll(self.matrix, shift[0], 0), shift[1], 1) * frac
				self.matrix = tmp
	
	def increment(self, row, col, value = 1):
		"""docstring for sample_cell"""
		self.matrix[row, col] += value

	def increment_range(self, row_from, row_to, col_from, col_to, value = 1):
		"""docstring for sample_cells"""
		if min(row_from, row_to, col_from, col_to) < 0:
			raise ValueError("Negative indices not allowed: %d, %d, %d, %d " % (row_from, row_to, col_from, col_to)) 
		self.matrix[ row_from:row_to, col_from:col_to ] += value

	def get_shape(self):
		return (self.rows, self.cols)

	def num_cells(self):
		return self.rows * self.cols

	def num_cells_affected(self):
		return np.count_nonzero(self.matrix)

	def total_heat(self):
		return np.sum(self.matrix)

class Cell(object):
	"""docstring for Cell"""
	def __init__(self, resolution, row, col, value):
		super(Cell, self).__init__()
		self.resolution = resolution
		self.row = row
		self.col = col
		self.value = value
	
	def __str__(self):
		return '(%.2f, %d, %d, %.2f)' % (self.resolution, self.row, self.col, self.value)
		"""docstring for __str__"""
		pass
			