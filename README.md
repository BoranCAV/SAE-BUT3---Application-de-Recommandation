# Recommandation comparée : animés, films et séries

Dépôt : https://github.com/BoranCAV/SAE-BUT3---Application-de-Recommandation

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
.venv\Scripts\python prepa_db.py          # crée la base depuis data/contenus.json (926 contenus)
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
le test utilise une base temporaire avec un petit jeu d'essai, la vraie base n'est pas modifiée.

## Données

926 contenus versionnés dans `backend/data/contenus.json` (import du 17/11/2026) : animés depuis [AniList](https://anilist.co), films et séries depuis [TMDB](https://www.themoviedb.org).
This product uses the TMDB API but is not endorsed or certified by TMDB.

## Licence

[MIT](LICENSE), choisie dans la liste de l'[Open Source Initiative](https://opensource.org/licenses/MIT) :
- licence courte et simple, facile à comprendre et à respecter
- permissive : tout le monde peut réutiliser, modifier et redistribuer le code, à condition de garder la mention des auteurs
- compatible avec les bibliothèques utilisées (Flask : BSD, SQLAlchemy : MIT, Requests : Apache 2.0, Bootstrap : MIT)
- adaptée à un projet pédagogique : le code peut servir à d'autres étudiants, sans obligation de publier leurs modifications comme avec une licence GPL

la licence couvre uniquement notre code : les données restent soumises aux conditions d'AniList et de TMDB.

## Équipe « Les Lions Conquérants »

CAV Boran · CHOUAT Oussama · JEREMIAS Sherwin · LARIBI Younes · LE MESTE Enzo · TABELLOUT Amir Khaled
