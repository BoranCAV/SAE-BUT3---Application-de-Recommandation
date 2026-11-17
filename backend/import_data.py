import os
import re
import time
import html
import requests
from sqlalchemy.orm import sessionmaker
from app.models import Base, Genre, Content, get_engine

ANILIST_URL = "https://graphql.anilist.co"
NB_PAGES_ANILIST = 6  # 50 animés par page

TMDB_URL = "https://api.themoviedb.org/3"
TMDB_IMG = "https://image.tmdb.org/t/p/w500"
NB_PAGES_TMDB = 15  # 20 résultats par page
GENRE_ANIMATION = 16

ANILIST_QUERY = """
query ($page: Int) {
	Page(page: $page, perPage: 50) {
		media(type: ANIME, sort: POPULARITY_DESC, isAdult: false) {
			title { romaji english }
			startDate { year }
			description
			averageScore
			coverImage { large }
			genres
		}
	}
}
"""

# genres anilist (anglais) -> mêmes noms que tmdb en français, pour comparer animés et films
GENRES_FR = {
	"Adventure": "Aventure",
	"Comedy": "Comédie",
	"Drama": "Drame",
	"Fantasy": "Fantastique",
	"Horror": "Horreur",
	"Mystery": "Mystère",
	"Sci-Fi": "Science-Fiction",
	"Music": "Musique",
	"Sports": "Sport",
	"Supernatural": "Surnaturel",
	"Psychological": "Psychologique",
	"Slice of Life": "Tranche de vie",
}


def fetch_animes():
	"""animés les plus populaires d'anilist, sous forme de tuples comme dans prepa_db"""
	print("[*] import des animés depuis AniList...")
	animes = []
	for page in range(1, NB_PAGES_ANILIST + 1):
		try:
			r = requests.post(ANILIST_URL, json={"query": ANILIST_QUERY, "variables": {"page": page}}, timeout=15)
			r.raise_for_status()
		except requests.RequestException as e:
			print(f"[!] AniList injoignable ({e}), on garde ce qu'on a")
			break

		for a in r.json()["data"]["Page"]["media"]:
			title = a["title"]["english"] or a["title"]["romaji"]
			synopsis = html.unescape(re.sub(r"<[^>]+>", "", a["description"] or "")).strip() or None
			score = a["averageScore"] / 10 if a["averageScore"] else None
			genres = [GENRES_FR.get(g, g) for g in a["genres"]]
			animes.append((title, "anime", a["startDate"]["year"], synopsis, score, a["coverImage"]["large"], genres))
		time.sleep(2)  # anilist limite à 30 requêtes par minute

	print(f"[+] {len(animes)} animés récupérés")
	return animes


def fetch_tmdb(kind, ctype, api_key):
	"""films (kind='movie') ou séries (kind='tv') les mieux notés de tmdb"""
	print(f"[*] import des {ctype}s depuis TMDB...")
	params = {"api_key": api_key, "language": "fr-FR"}
	try:
		r = requests.get(f"{TMDB_URL}/genre/{kind}/list", params=params, timeout=15)
		r.raise_for_status()
	except requests.RequestException as e:
		print(f"[!] TMDB injoignable ({e}), {ctype}s ignorés")
		return []
	genre_names = {g["id"]: g["name"] for g in r.json()["genres"]}

	contents = []
	for page in range(1, NB_PAGES_TMDB + 1):
		try:
			r = requests.get(f"{TMDB_URL}/{kind}/top_rated", params={**params, "page": page}, timeout=15)
			r.raise_for_status()
		except requests.RequestException as e:
			print(f"[!] TMDB injoignable ({e}), on garde ce qu'on a")
			break

		for c in r.json()["results"]:
			## les animés japonais viennent déjà d'anilist, on évite les doublons
			if c["original_language"] == "ja" and GENRE_ANIMATION in c["genre_ids"]:
				continue
			date = c.get("release_date") or c.get("first_air_date") or ""
			year = int(date[:4]) if date else None
			cover = TMDB_IMG + c["poster_path"] if c.get("poster_path") else None
			genres = []
			for gid in c["genre_ids"]:
				if gid in genre_names:
					# côté séries tmdb regroupe des genres : "Action & Adventure"
					genres += genre_names[gid].split(" & ")
			contents.append((c.get("title") or c.get("name"), ctype, year, c["overview"] or None, c["vote_average"], cover, genres))

	print(f"[+] {len(contents)} {ctype}s récupérés")
	return contents


def save_contents(contents, db_path=None):
	"""vide la base puis enregistre les contenus et leurs genres"""
	if db_path is None:
		base_dir = os.path.dirname(os.path.abspath(__file__))
		db_path = os.path.join(base_dir, 'app', 'reco.db')

	engine = get_engine(f"sqlite:///{db_path}")
	Base.metadata.drop_all(engine)
	Base.metadata.create_all(engine)

	session = sessionmaker(bind=engine)()
	try:
		genres_map = {}
		deja_vus = set()
		for title, ctype, year, synopsis, score, cover, genre_names in contents:
			if (title, ctype) in deja_vus:
				continue
			deja_vus.add((title, ctype))

			content = Content(title=title, type=ctype, year=year, synopsis=synopsis, score=score, cover=cover)
			for g_name in set(genre_names):
				if g_name not in genres_map:
					genres_map[g_name] = Genre(name=g_name)
				content.genres.append(genres_map[g_name])
			session.add(content)
		session.commit()
		print(f"[+] {len(deja_vus)} contenus et {len(genres_map)} genres enregistrés")
	except Exception:
		session.rollback()
		raise
	finally:
		session.close()


def import_data(db_path=None):
	contents = fetch_animes()

	api_key = os.environ.get("TMDB_API_KEY")
	if api_key:
		contents += fetch_tmdb("movie", "film", api_key)
		contents += fetch_tmdb("tv", "serie", api_key)
	else:
		print("[!] pas de variable TMDB_API_KEY, films et séries ignorés")

	if not contents:
		print("[!] rien récupéré, la base n'est pas modifiée")
		return
	save_contents(contents, db_path)


if __name__ == '__main__':
	import_data()
