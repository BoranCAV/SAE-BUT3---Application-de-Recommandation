# Frontend — pages statiques HTML/JS + Bootstrap + Chart.js

Aucune installation : les pages appellent l'API du backend (`http://localhost:8000/api`, voir `js/api.js`) en `fetch`.

1. lancer le backend (voir `../backend/README.md`)
2. servir ce dossier :
```bash
python -m http.server 5500
```
3. ouvrir http://localhost:5500

| fichier | rôle |
|---|---|
| `index.html` | accueil |
| `catalogue.html` | catalogue (en construction) |
| `reco.html` | comparaison des 2 approches (en construction) |
| `js/api.js` | appel de l'API, échappement HTML, affichage des erreurs |
| `js/nav.js` | barre de navigation commune (équivalent du `include 'nav.html'`) |
