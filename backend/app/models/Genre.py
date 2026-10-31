from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.models.base import Base, BaseModelMixin
from app.models.associations import content_genres


class Genre(Base, BaseModelMixin):
	"""
	genre (Action, Romance, Shōnen...)
	N-N avec Content via la table d'association 'content_genres'
	"""
	__tablename__ = 'genres'

	id = Column(Integer, primary_key=True, autoincrement=True)
	name = Column(String(100), unique=True, nullable=False, index=True)

	contents = relationship(
		'Content',
		secondary=content_genres,
		back_populates='genres'
	)

	def __init__(self, name=None):
		self.name = name
