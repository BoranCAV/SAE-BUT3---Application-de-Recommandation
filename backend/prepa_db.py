import os
import json
from sqlalchemy.orm import sessionmaker
from app.models import Base, Genre, Content, get_engine

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, 'data', 'contenus.json')

# petit jeu d'essai, utilisé par test_reco.py
JEU_ESSAI = [
	{"title": "Fullmetal Alchemist: Brotherhood", "type": "anime", "year": 2009, "synopsis": "Deux frères alchimistes cherchent la pierre philosophale pour retrouver leurs corps.", "score": 9.1, "cover": None, "genres": ["Action", "Aventure", "Fantasy"]},
	{"title": "Attack on Titan", "type": "anime", "year": 2013, "synopsis": "L'humanité survit derrière des murs face à des titans dévoreurs d'hommes.", "score": 8.5, "cover": None, "genres": ["Action", "Drame", "Fantasy"]},
	{"title": "Your Name", "type": "anime", "year": 2016, "synopsis": "Deux adolescents échangent mystérieusement leurs corps à travers le Japon.", "score": 8.8, "cover": None, "genres": ["Romance", "Drame", "Surnaturel"]},
	{"title": "Inception", "type": "film", "year": 2010, "synopsis": "Un voleur s'infiltre dans les rêves pour y implanter une idée.", "score": 8.4, "cover": None, "genres": ["Action", "Science-Fiction"]},
	{"title": "Interstellar", "type": "film", "year": 2014, "synopsis": "Des astronautes traversent un trou de ver pour sauver l'humanité.", "score": 8.4, "cover": None, "genres": ["Aventure", "Drame", "Science-Fiction"]},
	{"title": "Breaking Bad", "type": "serie", "year": 2008, "synopsis": "Un professeur de chimie atteint d'un cancer se lance dans la fabrication de drogue.", "score": 8.9, "cover": None, "genres": ["Drame", "Crime"]},
	{"title": "Stranger Things", "type": "serie", "year": 2016, "synopsis": "Des enfants affrontent des forces surnaturelles dans une petite ville américaine.", "score": 8.6, "cover": None, "genres": ["Drame", "Science-Fiction", "Surnaturel"]},
]


def setup_database(db_path=None, contents=None):
	"""vide la base puis la remplit avec les contenus (par défaut ceux de data/contenus.json)"""
	if db_path is None:
		db_path = os.path.join(BASE_DIR, 'app', 'reco.db')
	if contents is None:
		with open(DATA_PATH, encoding='utf-8') as f:
			contents = json.load(f)

	engine = get_engine(f"sqlite:///{db_path}")
	Base.metadata.drop_all(engine)
	Base.metadata.create_all(engine)

	session = sessionmaker(bind=engine)()
	try:
		genres_map = {}
		for c in contents:
			content = Content(title=c["title"], type=c["type"], year=c["year"], synopsis=c["synopsis"], score=c["score"], cover=c["cover"])
			for g_name in c["genres"]:
				if g_name not in genres_map:
					genres_map[g_name] = Genre(name=g_name)
				content.genres.append(genres_map[g_name])
			session.add(content)
		session.commit()
		print(f"[+] base initialisée : {len(contents)} contenus, {len(genres_map)} genres")
	except Exception:
		session.rollback()
		raise
	finally:
		session.close()
	engine.dispose()


if __name__ == '__main__':
	setup_database()
