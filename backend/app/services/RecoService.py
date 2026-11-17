import time
from flask import current_app
from app.models.ContentDAO import ContentSqliteORM as ContentDAO


class RecoService:
	"""
	les deux approches de recommandation comparées
	chaque appel est chronométré pour alimenter le dashboard
	"""

	METHODS = ("contenu", "embeddings")
	POIDS_GENRES = 0.6
	POIDS_TYPE = 0.2
	POIDS_ANNEE = 0.2

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

	def _scoreSimilarite(self, cible, genres_cible, candidat) -> float:
		genres_cand = {g.name for g in candidat.genres}
		union = genres_cible | genres_cand
		score_genres = len(genres_cible & genres_cand) / len(union) if union else 0
		score_type = 1 if candidat.type == cible.type else 0

		if cible.year is not None and candidat.year is not None:
			score_annee = max(0, 1 - abs(cible.year - candidat.year) / 20)
		else:
			score_annee = 0

		return (
			self.POIDS_GENRES * score_genres
			+ self.POIDS_TYPE * score_type
			+ self.POIDS_ANNEE * score_annee
		)

	def recoContenu(self, content_id: int, n: int = 10) -> list:
		"""filtrage par contenu : O(N × G) pour les scores (N contenus, G genres) + O(N log N) pour le tri"""
		if n <= 0:
			return []

		cible = self.cdao.findById(content_id)
		if not cible:
			return []
		cible = cible[0]

		## approche simple : on parcourt tout le catalogue. Un index inversé sur les genres éviterait ce parcours complet
		contenus = self.cdao.findAll()
		genres_cible = {g.name for g in cible.genres}
		scores = []
		for c in contenus:
			if c.id == cible.id:
				continue
			genres_cand = {g.name for g in c.genres}
			communs = list(genres_cible & genres_cand)
			
			if not communs: 
				continue 

			# On calcule le score ET on garde les genres en commun
			score = self._scoreSimilarite(cible, genres_cible, c)
			scores.append((score, c, communs))

		scores.sort(key=lambda x: x[0], reverse=True)
		
		# On attache l'explication à l'objet avant de le renvoyer
		resultats = []
		for score, c, communs in scores[:n]:
			c.similarity = round(score, 3)
			c.shared_genres = communs
			resultats.append(c)
			
		return resultats

	def recoEmbeddings(self, content_id, n):
		"""approche 2 : similarité cosinus entre embeddings des synopsis"""
		return []  # à implémenter
