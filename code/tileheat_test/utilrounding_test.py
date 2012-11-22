from tileheat.util import roundceil, roundfloor
import unittest

class TestUtilRounding(unittest.TestCase):

    def test_roundceil_round(self):
		
		# hitting the rounding case
        self.assertEqual(roundceil(1.00000001), 1)
        self.assertEqual(roundceil(1.001, epsilon=0.1), 1)
		
    def test_roundceil_ceil(self):

		# hitting the ceiling case
        self.assertEqual(roundceil(1.1), 2)
        self.assertEqual(roundceil(1.01, epsilon=0.001), 2)

if __name__ == '__main__':
    unittest.main()