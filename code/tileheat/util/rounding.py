from math import floor, ceil

def roundceil(x, epsilon=0.00001):
	"""if (abs) the fractional part is less than epsilon do round. Else do ceil"""
	return round(x) if abs(x % 1) < epsilon else ceil(x)
	
def roundfloor(x, epsilon=0.00001):
	"""if (abs) the fractional part is less than epsilon do round. Else do floor"""
	return round(x) if abs(x % 1) < epsilon else floor(x)