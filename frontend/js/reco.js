// page reco : compare les deux méthodes pour un contenu et garde leurs temps de réponse

const METHODES = ["contenu", "embeddings"];
const temps = { contenu: [], embeddings: [] };
let tousLesContenus = [];
let dernierIdCompare = null;
let debounceTimer = null;

function normaliser(str) {
	return (str || "")
		.toLowerCase()
		.normalize("NFD")
		.replace(/[\u0300-\u036f]/g, "");
}

function trouverMeilleurContenu(saisie) {
	if (!saisie) return null;
	const q = normaliser(saisie);

	// 1. Correspondance exacte sur le titre
	let match = tousLesContenus.find(c => normaliser(c.title) === q);
	if (match) return match;

	// 2. Le titre commence par la recherche
	match = tousLesContenus.find(c => normaliser(c.title).startsWith(q));
	if (match) return match;

	// 3. Le titre contient la recherche
	match = tousLesContenus.find(c => normaliser(c.title).includes(q));
	if (match) return match;

	return null;
}

function autoRechercherEtComparer(depuisToucheEntree = false) {
	const saisie = document.getElementById("recherche").value.trim();
	if (!saisie) return;

	const anime = trouverMeilleurContenu(saisie);
	if (anime) {
		const select = document.getElementById("contenu");
		select.value = anime.id;
		if (dernierIdCompare !== String(anime.id)) {
			comparer(anime.id);
		}
	} else if (depuisToucheEntree) {
		showError(new Error(`Aucun animé trouvé pour "${saisie}".`));
	}
}

async function chargerContenus() {
	const select = document.getElementById("contenu");
	try {
		tousLesContenus = await api("/catalogue/?limit=1000");
		select.innerHTML = tousLesContenus.map(c =>
			`<option value="${c.id}">${esc(c.title)} (${TYPE_LABELS[c.type] || c.type})</option>`
		).join("");

		const id = new URLSearchParams(location.search).get("id");
		if (id) {
			select.value = id;
			if (select.selectedIndex < 0) select.selectedIndex = 0;
			comparer(id);
		}
	} catch (e) {
		showError(e);
	}
}

async function comparer(id) {
	dernierIdCompare = String(id);
	document.getElementById("erreur").innerHTML = "";
	try {
		const contenu = await api("/catalogue/" + id);
		afficherFiche(contenu);

		const recos = await Promise.all([
			api("/reco/" + id + "?method=contenu&n=10"),
			api("/reco/" + id + "?method=embeddings&n=10"),
		]);
		recos.forEach(reco => {
			temps[reco.method].push(reco.time_ms);
			afficherMethode(reco);
		});
		afficherTemps();
	} catch (e) {
		showError(e);
	}
}

function afficherFiche(c) {
	document.getElementById("fiche").innerHTML = `
	<div class="card border-0 shadow-sm">
		<div class="card-body">
			<h2 class="h5 mb-1">${esc(c.title)} <span class="badge text-bg-${TYPE_COLORS[c.type]}">${TYPE_LABELS[c.type]}</span></h2>
			<p class="text-secondary mb-2">${c.year ?? "année inconnue"} · ${esc(c.genres.join(", "))}</p>
			<p class="mb-0">${esc(c.synopsis)}</p>
		</div>
	</div>`;
}

function afficherMethode(reco) {
	document.getElementById("temps-" + reco.method).textContent = reco.time_ms + " ms";

	const zone = document.getElementById("resultats-" + reco.method);
	if (reco.results.length === 0) {
		zone.innerHTML = `<div class="alert alert-info mb-0">Pas encore de résultats pour cette méthode</div>`;
		return;
	}
	zone.innerHTML = `<ol class="list-group list-group-numbered list-group-flush">` + reco.results.map(c => {
		const explication = c.shared_genres && c.shared_genres.length > 0 
			? `<div class="small text-success mt-1"><em>Justification :</em> Genres en commun (${c.shared_genres.join(', ')})</div>` 
			: '';
			
		return `
		<li class="list-group-item">
			${esc(c.title)} <span class="badge text-bg-${TYPE_COLORS[c.type]}">${TYPE_LABELS[c.type]}</span>
			<div class="small text-secondary">${c.year ?? "année inconnue"} · ${esc(c.genres.join(", "))}</div>
			${explication}
		</li>`;
	}).join("") + `</ol>`;
}

function afficherTemps() {
	document.getElementById("dashboard").innerHTML = METHODES.map(m => {
		const t = temps[m];
		const moyenne = t.reduce((a, b) => a + b, 0) / t.length;
		return `
		<tr>
			<td>${m}</td>
			<td>${t[t.length - 1]}</td>
			<td>${Math.min(...t)}</td>
			<td>${Math.max(...t)}</td>
			<td>${moyenne.toFixed(3)}</td>
			<td>${t.length}</td>
		</tr>`;
	}).join("");
}

// Recherche automatique pendant la saisie (avec délai de 350ms pour laisser taper)
document.getElementById("recherche").addEventListener("input", () => {
	clearTimeout(debounceTimer);
	const saisie = document.getElementById("recherche").value.trim();
	if (saisie.length >= 2) {
		debounceTimer = setTimeout(() => {
			autoRechercherEtComparer(false);
		}, 350);
	}
});

// Touche Entrée dans la barre de recherche : comparaison instantanée
document.getElementById("recherche").addEventListener("keydown", (e) => {
	if (e.key === "Enter") {
		e.preventDefault();
		clearTimeout(debounceTimer);
		autoRechercherEtComparer(true);
	}
});

// Changement manuel dans la liste déroulante : comparaison automatique
document.getElementById("contenu").addEventListener("change", () => {
	const id = document.getElementById("contenu").value;
	if (id) {
		comparer(id);
	}
});

// Clic sur le bouton Comparer
document.getElementById("comparer").addEventListener("click", () => {
	const id = document.getElementById("contenu").value;
	if (id) {
		comparer(id);
	}
});

chargerContenus();
