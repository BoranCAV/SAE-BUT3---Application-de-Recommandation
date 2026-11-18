import os
import json
import re
import time
import html
import requests
from prepa_db import DATA_PATH, setup_database

ANILIST_URL = "https://graphql.anilist.co"
NB_PAGES_ANILIST = 6  # 50 animés par page

TMDB_URL = "https://api.themoviedb.org/3"
TMDB_IMG = "https://image.tmdb.org/t/p/w500"
NB_PAGES_TMDB = 20  # 20 résultats par page
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

# genres en anglais (anilist, et certains genres de séries tmdb) -> noms français de tmdb
# pour que animés, films et séries partagent les mêmes genres
GENRES_FR = {
	"War": "Guerre",
	"Politics": "Politique",
	"Kids": "Enfants",
	"Reality": "Télé-réalité",
	"Soap": "Feuilleton",
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
					genres += [GENRES_FR.get(g, g) for g in genre_names[gid].split(" & ")]
			contents.append((c.get("title") or c.get("name"), ctype, year, c["overview"] or None, round(c["vote_average"], 1), cover, genres))

	print(f"[+] {len(contents)} {ctype}s récupérés")
	return contents


def save_json(contents):
	"""enregistre les contenus dans data/contenus.json (sans doublons), versionné avec le code"""
	data = []
	deja_vus = set()
	for title, ctype, year, synopsis, score, cover, genres in contents:
		if (title, ctype) in deja_vus:
			continue
		deja_vus.add((title, ctype))
		data.append({"title": title, "type": ctype, "year": year, "synopsis": synopsis, "score": score, "cover": cover, "genres": sorted(set(genres))})

	os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
	with open(DATA_PATH, "w", encoding="utf-8") as f:
		json.dump(data, f, ensure_ascii=False, indent=1)
	print(f"[+] {len(data)} contenus enregistrés dans {DATA_PATH}")


def import_data():
	# sans clé on perdrait les films et séries du json, on s'arrête avant
	api_key = os.environ.get("TMDB_API_KEY")
	if not api_key:
		print("[!] pas de variable TMDB_API_KEY, import annulé (data/contenus.json inchangé)")
		return

	animes = fetch_animes()
	films = fetch_tmdb("movie", "film", api_key)
	series = fetch_tmdb("tv", "serie", api_key)

	if not animes or not films or not series:
		print("[!] une source n'a rien renvoyé, data/contenus.json inchangé")
		return
	save_json(animes + films + series)
	setup_database()


if __name__ == '__main__':
	import_data()
