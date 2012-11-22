from tileheat.heatmap import MultiscaleHeatmap

class HeatmapAnalyzer(MultiscaleHeatmap):
	"""docstring for HeatmapAnalyzer"""
	def __init__(self, tiling_scheme, snap=True, valuefunc=lambda event: 1):
		super(HeatmapAnalyzer, self).__init__(tiling_scheme, snap)
		self.valuefunc = valuefunc
	
	def process(self, event):

		bbox = event.query.bbox
		srs = event.query.srs
		resolution = event.query.x_res
				
		if self.snap:			
			resolution = self.tiling_scheme.nearest_resolution( resolution )

		self.increment_cells_by_bbox( srs, bbox, resolution, value = self.valuefunc(event) )	
		