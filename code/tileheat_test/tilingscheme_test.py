from tileheat.analysis import TilingScheme
from tileheat import Bbox
import unittest
import pyproj as proj

class TestTilingScheme(unittest.TestCase):

	def setUp(self):
		# making 1000 x 1000 bbox. choice of resolutions should give fractional computations
		bbox = Bbox(500000,5000000, 502000, 5001000)
		self.ts = TilingScheme(srs='epsg:25832', bbox=Bbox(500000,5000000, 502000, 5001000), tilesize=(256,256), resolutions=[1,2,4,8,16,32])
		self.bbox = bbox

	def tearDown(self):
		self.ts = None

	def test_dim_x(self):
		
		# should "round up" to nearest integer
		self.assertEqual(self.ts.dim_x(1), 8)
		# should raise an exception for resolution not in ts
		self.assertRaises(ValueError, self.ts.dim_x, -1)

	def test_dim_y(self):

		# should "round up" to nearest integer
		self.assertEqual(self.ts.dim_y(1), 4)
		# should raise an exception for resolution not in ts
		self.assertRaises(ValueError, self.ts.dim_y, -1)

	def test_cellsize_x(self):
		"""docstring for test_cellsize_x"""
		self.assertEqual(self.ts.cellsize_x(2), 512)
		# should raise an exception for resolution not in ts
		self.assertRaises(ValueError, self.ts.cellsize_x, -1)
		
	def test_cellsize_y(self):
		"""docstring for test_cellsize_y"""
		self.assertEqual(self.ts.cellsize_y(2), 512)
		# should raise an exception for resolution not in ts
		self.assertRaises(ValueError, self.ts.cellsize_y, -1)

	def test_nearest_resolution(self):
		"""docstring for test_nearest_resolution"""
		self.assertEqual(self.ts.nearest_resolution(3.5), 4)

	def test_indices(self):
		"""docstring for test_indices"""
		srs = 'epsg:25832'
		bbox = self.bbox
		self.assertEqual(self.ts.indices(srs=srs, bbox=bbox, resolution=1), (0,4,0,8))
		# lower left
		bbox = Bbox(500000, 5000000, 500999, 5000487)
		self.assertEqual(self.ts.indices(srs=srs, bbox=bbox, resolution=1), (2,4,0,4))
		# single cell
		bbox = Bbox(500010, 5000900, 500020, 5000910)
		self.assertEqual(self.ts.indices(srs=srs, bbox=bbox, resolution=1), (0,1,0,1))
		# outside
		bbox = Bbox(200000, 1000000, 300000, 2000000)
		self.assertEqual(self.ts.indices(srs=srs, bbox=bbox, resolution=1), None)
		# trunc
		bbox = Bbox(200000, 1000000, 700000, 7000000)
		self.assertEqual(self.ts.indices(srs=srs, bbox=bbox, resolution=1), (0,4,0,8))
		# reproject
		srs = 'epsg:4326'		
		utm = proj.Proj(init='epsg:25832')
		geo = proj.Proj(init='epsg:4326')
		min_x, min_y = proj.transform(utm, geo, 500010, 5000900)
		max_x, max_y = proj.transform(utm, geo, 500020, 5000910)
		bbox = Bbox(min_x, min_y, max_x, max_y)
		print "Bbox: %f, %f, %f, %f, srs: %s" % (bbox.min_x, bbox.min_y, bbox.max_x, bbox.max_y, srs)
		self.assertEqual(self.ts.indices(srs=srs, bbox=bbox, resolution=1), (0,1,0,1))
		
if __name__ == '__main__':
	unittest.main()