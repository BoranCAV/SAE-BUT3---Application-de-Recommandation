# Recommandation comparée : animés, films et séries

Application web **découplée** de recommandation comparée (SAÉ BUT3 5.Real.01, IUT Villetaneuse).
Deux approches de recommandation sont comparées côte à côte : filtrage par contenu et embeddings, avec un dashboard (temps de réponse, complexité, consommation…).

## Structure

| dossier | rôle |
|---|---|
| `backend/` | API Flask JSON : blueprints, services, DAO, ORM SQLAlchemy ([README](backend/README.md)) |
| `frontend/` | pages HTML/JS + Bootstrap qui appellent l'API en `fetch` ([README](frontend/README.md)) |
| `docs/` | feuille de route et documents du projet |

## Lancer le projet

```bash
# terminal 1 : l'API (http://localhost:8000/api)
cd backend
python -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
.venv\Scripts\python prepa_db.py
.venv\Scripts\python main.py

# terminal 2 : le front (http://localhost:5500)
cd frontend
python -m http.server 5500
```

## Équipe « Les Lions Conquérants »

CAV Boran · CHOUAT Oussama · LARIBI Younes · LE MESTE Enzo · TABELLOUT Amir Khaled
