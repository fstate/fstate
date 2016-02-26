import json

multiplets_db = json.loads(open('../data/multiplets.json').read())
particles_db  = json.loads(open('../data/particles.json').read())

multiplets = set(multiplets_db.keys())
particles = set(particles_db.keys())

names = particles.union(multiplets)

class Decay(object):
	"""
	Decay class used for:
	* Parsing of decay string with proper exceptions
	* Proper CC
	"""
	def __init__(self, decay=None):
		if decay:
			self.br = tuple(decay['branching'])
			self.parse_decstring(decay['decay'])

	def parse_decstring(self, decstring):
		tokens = [x for x in decstring.split(' ') if x != '']
		self.father = tokens.pop(0)
		
		if not self.father in names:
			raise Exception('Father %s is invalid' % self.father)

		if tokens.pop(0) != '-->':
			raise Exception('More than one token before -->')

		self.products = tokens

		for p in self.products:
			if not p in names:
				raise Exception('Product %s is invalid' % p)
