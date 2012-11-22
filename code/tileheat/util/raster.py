import gdal
import osr
import numpy as np

class RasterUtil(object):
	"""docstring for RasterFile"""
	def __init__(self, arg):
		super(RasterFile, self).__init__()
		self.arg = arg
	
	@staticmethod
	def write_geotiff(matrix, tiling_scheme, resolution, normalize=False, path=None):
		"""docstring for to_geotiff"""
		if resolution not in tiling_scheme.resolutions:
			raise Error("Resolution not in heatmap: %d" % resolution)
		if path is None:
			path = '%s.tiff' % resolution
		matrix = MatrixUtil.normalize( matrix ) if normalize else matrix			
		driver = gdal.GetDriverByName( "GTiff" )
		dst_ds = driver.Create( path, int(tiling_scheme.dim_x(resolution)), int(tiling_scheme.dim_y(resolution)), 1, gdal.GDT_Byte )
		# TODO: important if using with e.g. QGis
		# dst_ds.SetGeoTransform( [ self.bbox.min_x, self.tilesize[0], 0, self.bbox.max_y, self.tilesize[1], 0 ] )

		srs = osr.SpatialReference()
		srs.ImportFromEPSG( int(tiling_scheme.srs.split(":")[1]) )
		dst_ds.SetProjection( srs.ExportToWkt() )

		dst_ds.GetRasterBand(1).WriteArray( matrix )

	@staticmethod
	def write_geotiff_heatmap(heatmap, normalize=False, path_prefix=None):
		"""docstring for to_geotiff"""

		for level in heatmap.levels.values():
			RasterUtil.write_geotiff( level.matrix, heatmap.tiling_scheme, level.resolution, normalize, path='%s_%.2f.tiff' % (path_prefix, level.resolution) )

class MatrixUtil(object):
	"""docstring for MatrixUtil"""
	def __init__(self, arg):
		super(MatrixUtil, self).__init__()
		self.arg = arg

	@staticmethod
	def normalize(matrix, norm_max=255):
		"""docstring for normalize"""
		max_cell = np.max( matrix )
		return (matrix / max_cell) * norm_max
		
	@staticmethod
	def one_sum(matrix):
		"""docstring for normalize"""
		sum_cells = np.sum(matrix)
		return matrix / sum_cells

	@staticmethod
	def to_sorted_list(matrix, reverse=True):
		"""docstring for sorted_cells"""		
		return sorted(matrix.flatten(), reverse=reverse)
	
	@staticmethod
	def accumulate_inorder(matrix, onesum=False):
		"""docstring for accumulated"""
		if onesum:
			matrix = MatrixUtil.one_sum( matrix )
		sorted_list = MatrixUtil.to_sorted_list( matrix )
		accum_val = 0
		accum = [0]
		for x in sorted_list:
			accum_val  += x
			accum.append(accum_val)
		return accum

