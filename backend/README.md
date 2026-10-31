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

(ré)initialiser la base de données
```bash
python prepa_db.py
```

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
