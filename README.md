# Recommandation comparée : animés, films et séries

Application web **découplée** de recommandation comparée (SAÉ BUT3, IUT Villetaneuse).
Pour un contenu choisi, deux approches de recommandation sont comparées côte à côte, avec un dashboard des temps de réponse (min, max, moyenne).

## Structure

| dossier | rôle |
|---|---|
| `backend/` | API Flask JSON : blueprints, services, DAO, ORM SQLAlchemy ([README](backend/README.md)) |
| `frontend/` | pages HTML/JS + Bootstrap qui appellent l'API en `fetch` ([README](frontend/README.md)) |

## Lancer le projet

```bash
# terminal 1 : l'API (http://localhost:8000/api)
cd backend
python -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
.venv\Scripts\python prepa_db.py          # jeu d'essai (7 contenus)
.venv\Scripts\python import_data.py       # ou les vraies données, voir backend/README.md
.venv\Scripts\python main.py

# terminal 2 : le front (http://localhost:5500)
cd frontend
python -m http.server 5500
```

## Les deux approches

| méthode | principe | état |
|---|---|---|
| contenu | score de similarité : 60 % genres communs (Jaccard), 20 % même type, 20 % proximité de l'année. Parcours de tout le catalogue : O(N × G) + tri O(N log N) | fait |
| embeddings | similarité cosinus entre les vecteurs des synopsis | à faire |

tests de la méthode contenu :
```bash
cd backend
.venv\Scripts\python test_reco.py
```
attention, le test remet le jeu d'essai dans la base : relancer `import_data.py` après.

## Données

~900 contenus : animés depuis [AniList](https://anilist.co), films et séries depuis [TMDB](https://www.themoviedb.org).
This product uses the TMDB API but is not endorsed or certified by TMDB.

## Équipe « Les Lions Conquérants »

CAV Boran · CHOUAT Oussama · LARIBI Younes · LE MESTE Enzo · TABELLOUT Amir Khaled
