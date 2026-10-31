from flask import current_app
from app.models.ContentDAO import ContentSqliteORM as ContentDAO


class ContentService:
	"""logique du catalogue"""

	def __init__(self, db_path=None, db_uri=None):
		if db_uri is None and db_path is None:
			try:
				db_uri = current_app.config.get('SQLALCHEMY_DATABASE_URI')
				db_path = current_app.config.get('DATABASE_PATH')
			except RuntimeError:
				pass
		self.cdao = ContentDAO(db_path=db_path, db_uri=db_uri)

	def getAllContents(self, limit=100):
		return self.cdao.findAll(limit=limit)

	def getContentById(self, content_id):
		"""retourne toujours une liste : [contenu] ou []"""
		return self.cdao.findById(content_id)

	def getContentsByType(self, ctype):
		return self.cdao.findByType(ctype)

	def getContentsByGenre(self, genre_name):
		return self.cdao.findByGenre(genre_name)

	def getAllGenres(self):
		return self.cdao.findAllGenres()
