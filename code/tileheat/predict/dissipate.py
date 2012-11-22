from tileheat.heatmap import MultiscaleHeatmap 
import numpy as np
          
def dissipate(input_heatmap, dist, k):
	"""docstring for dissipate"""
	if (1 >= k <= 0) or dist <= 0:
		raise Exception("Invalid parameters")
	
	# init empty heatmap
	result = MultiscaleHeatmap( input_heatmap.tiling_scheme )

	# iterate levels
	for res in input_heatmap.tiling_scheme.resolutions:
		
		src = input_heatmap.levels[res].matrix
		dst = src * (1-k)
		frac = k / 8.0 # heat that goes to neighbours
   		# scatter
		for i in range( dist ):
			for shift in [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]:
				dst += np.roll(np.roll(src, shift[0], 0), shift[1], 1) * frac
			src = dst
	   	
		result.levels[res].matrix = dst
	
	return result