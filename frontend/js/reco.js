// page reco : compare les deux méthodes pour un contenu et garde leurs temps de réponse

async function chargerContenus() {
	const select = document.getElementById("contenu");
	try {
		const contenus = await api("/catalogue/?limit=1000");
		select.innerHTML = contenus.map(c =>
			`<option value="${c.id}">${esc(c.title)} (${TYPE_LABELS[c.type]})</option>`).join("");

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
	document.getElementById("erreur").innerHTML = "";
	try {
		const contenu = await api("/catalogue/" + id);
		afficherFiche(contenu);

		const recos = await Promise.all([
			api("/reco/" + id + "?method=contenu&n=10"),
			api("/reco/" + id + "?method=embeddings&n=10"),
		]);
		recos.forEach(reco => afficherMethode(reco));
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
	zone.innerHTML = `<ol class="list-group list-group-numbered list-group-flush">` + reco.results.map(c => `
		<li class="list-group-item">
			${esc(c.title)} <span class="badge text-bg-${TYPE_COLORS[c.type]}">${TYPE_LABELS[c.type]}</span>
			<div class="small text-secondary">${c.year ?? "année inconnue"} · ${esc(c.genres.join(", "))}</div>
		</li>`).join("") + `</ol>`;
}

document.getElementById("comparer").addEventListener("click", () => {
	comparer(document.getElementById("contenu").value);
});

chargerContenus();
