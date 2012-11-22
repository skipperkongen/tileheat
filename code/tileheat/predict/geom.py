import numpy as np
from tileheat import *
from tileheat.heatmap import MultiscaleHeatmap

class Geom(object):
	"""docstring for Geom, if no tilesize is given, use the size of this image: http://b.tile.openstreetmap.org/10/545/321.png"""
	def __init__(self, seeding_plan):
		super(Geom, self).__init__()
		self.seeding_plan = seeding_plan
		heatmap = MultiscaleHeatmap(seeding_plan.tiling_scheme)
 		# build cache
		for seed in seeding_plan.seeds:
			for resolution in seed.resolutions:
				heatmap.increment_cells_by_bbox(seed.srs, seed.bbox, resolution, 1)
		# make cells equal, i.e. zero or tilesize_bytes
		for level in heatmap.levels.values():
			matrix = level.matrix
			level.matrix = (matrix > 0).astype(int)
		self.heatmap = heatmap
	
	def get_name(self):
		return "GEOM"
	
	def predict(self, m):
		return self.heatmap
	
	def get_reindex(self, m):
		pred_flat = self.predict( m ).flatten()
		return np.argsort(pred_flat)[::-1] 

class TopDownGeom(Geom):
	"""docstring for Geom, if no tilesize is given, use the size of this image: http://b.tile.openstreetmap.org/10/545/321.png"""
	def __init__(self, seeding_plan):
		super(TopDownGeom, self).__init__(seeding_plan)

	def get_name(self):
		return "GEOM-TD"

	def predict(self, m):
		return self.heatmap

	def get_reindex(self, m):
		pred_flat = self.predict( m ).flatten()
		size = len(pred_flat)
		reindex = np.zeros((1,size), dtype=int).flatten()
		front = 0
		rear = size -1
		for i in range( len(pred_flat) ):
			if pred_flat[i] == 1:
				reindex[front] = i
				front += 1
			else:
				reindex[rear] = i
				rear -= 1
		return reindex


class SeedingPlan(object):
	"""docstring for SeedingPlan"""
	def __init__(self, tiling_scheme, seeds):
		super(SeedingPlan, self).__init__()
		self.tiling_scheme = tiling_scheme
		self.seeds = seeds

	@staticmethod
	def by_name(name):
		seeds = []
		if name.lower() == 'kms':
			tiling_scheme = TilingScheme.by_name( 'kms' )
			resolutions = sorted(tiling_scheme.resolutions, reverse=True)
			srs = 'epsg:25832'
			# territorial omraader
			seeds.append( Seed(srs, Bbox(120000, 5600000, 1000000,6500000), resolutions[0:6]))
			# anholt
			seeds.append( Seed(srs, Bbox(653000, 6285000, 664000, 6292000), resolutions[6:12]))
			# bornholm
			seeds.append( Seed(srs, Bbox(860000, 6100000, 900000, 6150000), resolutions[6:12]))
			# nv
			seeds.append( Seed(srs, Bbox(435000, 6240000, 636000, 6410000), resolutions[6:12]))		
			# nv1
			seeds.append( Seed(srs, Bbox(550000, 6320000, 636000, 6410000), resolutions[6:12]))		
			# nv2
			seeds.append( Seed(srs, Bbox(435000, 6320000, 550000, 6410000), resolutions[6:12]))		
			# nv3
			seeds.append( Seed(srs, Bbox(435000, 6240000, 550000, 6320000), resolutions[6:12]))		
			# nv14
			seeds.append( Seed(srs, Bbox(550000, 6240000, 636000, 6410000), resolutions[6:12]))
			# nv4
			seeds.append( Seed(srs, Bbox(550000, 6240000, 636000, 6320000), resolutions[6:12]))		
			# nv23
			seeds.append( Seed(srs, Bbox(435000, 6240000, 550000, 6410000), resolutions[6:12]))		
			# sv
			seeds.append( Seed(srs, Bbox(435000, 6040000, 636000, 6240000), resolutions[6:12]))		
			# sv1
			seeds.append( Seed(srs, Bbox(435000, 6040000, 550000, 6240000), resolutions[6:12]))		
			# sv2
			seeds.append( Seed(srs, Bbox(550000, 6040000, 636000, 6240000), resolutions[6:12]))		

			# se
			seeds.append( Seed(srs, Bbox(636000, 6040000, 742000, 6240000), resolutions[6:12]))

			return SeedingPlan( tiling_scheme, seeds )

class Seed(object):
	"""docstring for Seeding"""
	def __init__(self, srs, bbox, resolutions):
		super(Seed, self).__init__()
		self.srs = srs
		self.bbox = bbox
		self.resolutions = resolutions
