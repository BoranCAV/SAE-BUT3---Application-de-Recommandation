import os
from sqlalchemy.orm import sessionmaker
from app.models import Base, Genre, Content, get_engine

# petit jeu d'essai en attendant l'import Jikan / TMDB
CONTENTS_DATA = [
	("Fullmetal Alchemist: Brotherhood", "anime", 2009, "Deux frères alchimistes cherchent la pierre philosophale pour retrouver leurs corps.", 9.1, ["Action", "Aventure", "Fantasy"]),
	("Attack on Titan", "anime", 2013, "L'humanité survit derrière des murs face à des titans dévoreurs d'hommes.", 8.5, ["Action", "Drame", "Fantasy"]),
	("Your Name", "anime", 2016, "Deux adolescents échangent mystérieusement leurs corps à travers le Japon.", 8.8, ["Romance", "Drame", "Surnaturel"]),
	("Inception", "film", 2010, "Un voleur s'infiltre dans les rêves pour y implanter une idée.", 8.4, ["Action", "Science-Fiction"]),
	("Interstellar", "film", 2014, "Des astronautes traversent un trou de ver pour sauver l'humanité.", 8.4, ["Aventure", "Drame", "Science-Fiction"]),
	("Breaking Bad", "serie", 2008, "Un professeur de chimie atteint d'un cancer se lance dans la fabrication de drogue.", 8.9, ["Drame", "Crime"]),
	("Stranger Things", "serie", 2016, "Des enfants affrontent des forces surnaturelles dans une petite ville américaine.", 8.6, ["Drame", "Science-Fiction", "Surnaturel"]),
]


def setup_database(db_path=None):
	if db_path is None:
		base_dir = os.path.dirname(os.path.abspath(__file__))
		db_path = os.path.join(base_dir, 'app', 'reco.db')

	engine = get_engine(f"sqlite:///{db_path}")
	Base.metadata.drop_all(engine)
	Base.metadata.create_all(engine)

	session = sessionmaker(bind=engine)()
	try:
		genres_map = {}
		for title, ctype, year, synopsis, score, genre_names in CONTENTS_DATA:
			content = Content(title=title, type=ctype, year=year, synopsis=synopsis, score=score)
			for g_name in genre_names:
				if g_name not in genres_map:
					genres_map[g_name] = Genre(name=g_name)
				content.genres.append(genres_map[g_name])
			session.add(content)
		session.commit()
		print("[+] base de données initialisée")
	finally:
		session.close()


if __name__ == '__main__':
	setup_database()
