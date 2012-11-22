from tileheat.heatmap import MultiscaleHeatmap
from tileheat.analysis import *
from tileheat import *
from tileheat.predict import dissipate

class HoltWinter(object):
	"""docstring for HoltWinterHeat"""
	def __init__(self, tiling_scheme, alpha, beta):
		super(HoltWinter, self).__init__()
		self.tiling_scheme = tiling_scheme
		self.alpha = alpha
		self.beta = beta
		self.b = None
		self.x = None # only needed to calc b_0
		self.s = None
		self.last_prediction = None
	
	def train(self, log_source):
		"""docstring for train"""
		# build heatmap (X_t) for events in log_source
		if self.s is None:
			# initialize s and x                                             
			self.x = self._create_heatmap( log_source )
			self.s = self.x
			# notice, b still not initialized
		else:			
			# observe
			x_now = self._create_heatmap( log_source )
			x_now = self.hook( x_now )
			# smooth, level by level
			for res in self.tiling_scheme.resolutions:
				
				# get x_t and s_{t-1}
				x_z_now = x_now.levels[res].matrix
				s_z = self.s.levels[res].matrix

				# for i=1, initialize trend
				if self.x is not None:
					x_z = self.x.levels[res].matrix
					# initialize self.b
					self.b = MultiscaleHeatmap( self.tiling_scheme )
					self.b.levels[res].matrix = x_z_now - x_z
					# Don't need self.x any more, delete
					self.x = None
				b_z = self.b.levels[res].matrix
				s_z_now = self.alpha * x_z_now + (1 - self.alpha) * (s_z + b_z)
				b_z_now = self.beta * (s_z_now - s_z) + (1 - self.beta) * b_z
				# done with level, assign values back
				self.s.levels[res].matrix = s_z_now
				self.b.levels[res].matrix = b_z_now
	
	def hook(self, input): 
		"""identity function"""
		return input
	
	def predict(self, m):
		pred = MultiscaleHeatmap( self.tiling_scheme )
		for res in self.tiling_scheme.resolutions:
			pred.levels[res].matrix = self.s.levels[res].matrix + self.b.levels[res].matrix * m
		return pred
	
	def get_name(self):
		return 'HW-A%dB%d' % (self.alpha * 100, self.beta * 100)		
	
	def get_reindex(self, m):
		pred = self.predict( m )
		pred_flat = pred.flatten()
		return np.argsort(pred_flat)[::-1]
			
	def _create_heatmap(self, log_source):
		"""docstring for _create_heatmap"""
		player = LogPlayer( log_source )
		heatmap = HeatmapAnalyzer( self.tiling_scheme )
		player.add_analyzer( heatmap )
		player.forward()
		return heatmap

class HoltWinterDissipate(HoltWinter):
	"""docstring for HoltWinterDissipate"""
	def __init__(self, tiling_scheme, alpha, beta, dist, loss):
		super(HoltWinterDissipate, self).__init__(tiling_scheme, alpha, beta)
		self.dist = dist
		self.loss = loss

	def get_name(self):
		return 'HWD-A%dB%dD%dL%d' % (self.alpha * 100, self.beta * 100, self.dist, self.loss * 100)

	def hook(self, input):
		return dissipate.dissipate(input, self.dist, self.loss)
