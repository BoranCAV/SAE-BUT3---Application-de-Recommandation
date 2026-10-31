from sqlalchemy import Table, Column, Integer, ForeignKey
from app.models.base import Base


content_genres = Table(
	'content_genres',
	Base.metadata,
	Column('content_id', Integer, ForeignKey('contents.id', ondelete='CASCADE'), primary_key=True),
	Column('genre_id', Integer, ForeignKey('genres.id', ondelete='CASCADE'), primary_key=True)
)
