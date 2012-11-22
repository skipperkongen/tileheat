from tileheat.analysis import MultiscaleHeatmap, Level
import numpy as np
import unittest

class TestHeatmap(unittest.TestCase):

	def test_incrementrange(self):
		
		level = Level(3, 10)
		level.increment_range(1,2,3,5)
		m = np.zeros((3,10))
		m[1:2, 3:5] += 1
		# test increment range
		self.assertTrue(np.array_equal(level.matrix, m))

	def test_hits(self):

		level = Level(3, 10)
		# test cell_hits equal sum of cell values
		hits = 0
		for i in range(1, 4):
			for j in range(1, 11):
				level.increment_range(0,i,0,j)
				hits += (0-i)*(0-j)
		self.assertEqual(np.sum(level.matrix), hits)
		
if __name__ == '__main__':
	unittest.main()