// fonctions communes à toutes les pages : appel de l'API et petits utilitaires d'affichage

const API_URL = "http://localhost:8000/api";

const TYPE_LABELS = { anime: "Animé", film: "Film", serie: "Série" };
const TYPE_COLORS = { anime: "danger", film: "primary", serie: "success" };

async function api(path) {
	// appelle le backend et renvoie le JSON, ou lève une erreur lisible
	let response;
	try {
		response = await fetch(API_URL + path);
	} catch (e) {
		throw new Error("API injoignable : le backend est-il lancé sur le port 8000 ?");
	}
	const data = await response.json();
	if (!response.ok) {
		throw new Error(data.error || response.statusText);
	}
	return data;
}

function esc(text) {
	// échappe le HTML : les titres/synopsis viendront d'API externes, on ne les injecte pas tels quels
	const div = document.createElement("div");
	div.textContent = text ?? "";
	return div.innerHTML;
}

function showError(error) {
	document.getElementById("erreur").innerHTML =
		`<div class="alert alert-danger">${esc(error.message)}</div>`;
}
