import time
from flask import current_app
from app.models.ContentDAO import ContentSqliteORM as ContentDAO


class RecoService:
	"""
	les deux approches de recommandation comparées
	chaque appel est chronométré pour alimenter le dashboard
	"""

	METHODS = ("contenu", "embeddings")

	def __init__(self, db_path=None, db_uri=None):
		if db_uri is None and db_path is None:
			try:
				db_uri = current_app.config.get('SQLALCHEMY_DATABASE_URI')
				db_path = current_app.config.get('DATABASE_PATH')
			except RuntimeError:
				pass
		self.cdao = ContentDAO(db_path=db_path, db_uri=db_uri)

	def recommend(self, content_id, method, n=10):
		"""retourne (liste de contenus recommandés, temps en ms)"""
		start = time.perf_counter()
		if method == "contenu":
			results = self.recoContenu(content_id, n)
		else:
			results = self.recoEmbeddings(content_id, n)
		time_ms = round((time.perf_counter() - start) * 1000, 3)
		return results, time_ms

	def recoContenu(self, content_id, n):
		"""approche 1 : filtrage basé sur le contenu (genres, type, année...)"""
		return []  # à implémenter

	def recoEmbeddings(self, content_id, n):
		"""approche 2 : similarité cosinus entre embeddings des synopsis"""
		return []  # à implémenter
