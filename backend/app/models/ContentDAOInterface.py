
class ContentDAOInterface:
	"""interface pour le DAO des contenus"""

	def connect(self):
		"""retourne une session de connexion ORM"""
		pass

	def findAll(self, limit=None):
		"""trouve tous les contenus"""
		pass

	def findById(self, id):
		"""trouve un contenu par son id"""
		pass

	def findByType(self, ctype):
		"""trouve les contenus d'un type (anime, film, serie)"""
		pass

	def findByGenre(self, genre_name):
		"""trouve les contenus d'un genre (relation N-N)"""
		pass

	def findAllGenres(self):
		"""trouve tous les genres"""
		pass
