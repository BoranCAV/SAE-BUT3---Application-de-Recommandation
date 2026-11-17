# Frontend — pages statiques HTML/JS + Bootstrap

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
| `catalogue.html` + `js/catalogue.js` | catalogue en cartes, filtres par type et genre, recherche par titre |
| `reco.html` + `js/reco.js` | choix d'un contenu, résultats des 2 méthodes en parallèle, dashboard des temps |
| `js/api.js` | appel de l'API, échappement HTML, affichage des erreurs, libellés des types |
| `js/nav.js` | barre de navigation commune (équivalent du `include 'nav.html'`) |
