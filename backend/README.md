# Backend — API Flask de recommandation comparée

API JSON uniquement (blueprints + services + DAO + ORM). Le front est servi à part et l'appelle en `fetch`.

créez un environnement virtuel
```bash
python -m venv .venv
# Windows : .venv\Scripts\activate    |    Linux/Mac : source .venv/bin/activate
```

dépendances
```bash
python -m pip install -r requirements.txt
```

(ré)initialiser la base de données à partir de `data/contenus.json` (926 contenus, aucune clé ni réseau nécessaire)
```bash
python prepa_db.py
```

## mettre à jour les données (optionnel)

les données sont figées dans `data/contenus.json`, versionné avec le code : tout le monde a le même catalogue et les mesures de temps sont comparables.
`import_data.py` refait l'import (~300 animés AniList + ~300 films et ~300 séries TMDB), réécrit le json puis la base.

une clé TMDB est nécessaire : créer un compte gratuit sur themoviedb.org, puis Paramètres > API
```bash
set TMDB_API_KEY=ta_cle          # Windows (cmd)  |  PowerShell : $env:TMDB_API_KEY="ta_cle"  |  Linux/Mac : export TMDB_API_KEY=ta_cle
python import_data.py
```
sans clé, l'import est annulé et le json reste inchangé. Ne jamais mettre la clé dans le code.

sources : [AniList](https://anilist.co) pour les animés, et TMDB pour les films et séries.
This product uses the TMDB API but is not endorsed or certified by TMDB.

## lancer l'API

```bash
python main.py
```
Puis http://localhost:8000/api

## routes

| méthode | route | rôle |
|---|---|---|
| GET | `/api/` | infos + liste des routes |
| GET | `/api/catalogue/?type=anime&genre=Drame&limit=50` | catalogue filtrable |
| GET | `/api/catalogue/<id>` | un contenu |
| GET | `/api/catalogue/genres` | tous les genres |
| GET | `/api/reco/<id>?method=contenu\|embeddings&n=10` | recommandations + temps (ms) |
