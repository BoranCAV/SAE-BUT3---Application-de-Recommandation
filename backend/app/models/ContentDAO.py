import os
from sqlalchemy.orm import sessionmaker, selectinload

from app.models.ContentDAOInterface import ContentDAOInterface
from app.models.Content import Content
from app.models.Genre import Genre
from app.models.base import get_engine


class ContentSqliteORM(ContentDAOInterface):
	"""
	DAO des contenus par orm
	les genres sont préchargés (selectinload) pour pouvoir sérialiser après la fermeture de session
	"""

	def __init__(self, db_path=None, db_uri=None):
		if db_uri is not None:
			self.db_uri = db_uri
		elif db_path is not None:
			self.db_uri = f"sqlite:///{db_path}"
		else:
			base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
			self.db_uri = f"sqlite:///{os.path.join(base_dir, 'reco.db')}"

		self.engine = get_engine(self.db_uri)
		self.SessionFactory = sessionmaker(bind=self.engine, expire_on_commit=False)

	def connect(self):
		"""retourne une nouvelle session orm"""
		return self.SessionFactory()

	def _query_with_relations(self, session):
		"""requête de base avec les genres préchargés (N-N donc selectinload)"""
		return session.query(Content).options(selectinload(Content.genres))

	def findAll(self, limit=None):
		session = self.connect()
		try:
			query = self._query_with_relations(session).order_by(Content.title)
			if limit is not None:
				query = query.limit(limit)
			return query.all()
		finally:
			session.close()

	def findById(self, id):
		"""retourne [contenu] ou [] si non trouvé"""
		session = self.connect()
		try:
			content = self._query_with_relations(session).filter(Content.id == id).first()
			return [content] if content else []
		finally:
			session.close()

	def findByType(self, ctype):
		session = self.connect()
		try:
			return (
				self._query_with_relations(session)
				.filter(Content.type == ctype)
				.order_by(Content.title)
				.all()
			)
		finally:
			session.close()

	def findByGenre(self, genre_name):
		session = self.connect()
		try:
			return (
				self._query_with_relations(session)
				.join(Content.genres)
				.filter(Genre.name.ilike(genre_name))
				.order_by(Content.title)
				.all()
			)
		finally:
			session.close()

	def findAllGenres(self):
		session = self.connect()
		try:
			return session.query(Genre).order_by(Genre.name).all()
		finally:
			session.close()
