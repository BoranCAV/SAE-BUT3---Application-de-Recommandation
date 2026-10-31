from sqlalchemy import Column, Integer, String, Text, Float
from sqlalchemy.orm import relationship
from app.models.base import Base, BaseModelMixin
from app.models.associations import content_genres


class Content(Base, BaseModelMixin):
	"""
	un contenu recommandable : animé, film ou série
	relations : genres N-N
	"""
	__tablename__ = 'contents'

	TYPES = ("anime", "film", "serie")

	id = Column(Integer, primary_key=True, autoincrement=True)
	title = Column(String(255), nullable=False, index=True)
	type = Column(String(20), nullable=False, index=True)  # une valeur de TYPES
	year = Column(Integer, nullable=True, index=True)
	synopsis = Column(Text, nullable=True)  # servira aux deux approches de reco
	score = Column(Float, nullable=True)  # note source (MAL / TMDB) sur 10
	cover = Column(String(500), nullable=True)

	genres = relationship(
		'Genre',
		secondary=content_genres,
		back_populates='contents'
	)

	def __init__(self, title=None, type=None, year=None, synopsis=None, score=None, cover=None):
		self.title = title
		self.type = type
		self.year = year
		self.synopsis = synopsis
		self.score = score
		self.cover = cover

	@property
	def genres_str(self):
		"""retourne les noms de genres séparés par des virgules"""
		return ", ".join(g.name for g in self.genres)

	def to_dict(self):
		"""colonnes + la liste des genres, pour le JSON de l'API"""
		data = super().to_dict()
		data["genres"] = [g.name for g in self.genres]
		return data
