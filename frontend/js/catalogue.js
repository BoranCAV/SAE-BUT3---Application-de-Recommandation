// page catalogue : affiche tous les contenus sous forme de cartes

async function chargerContenus() {
	try {
		const contenus = await api("/catalogue/?limit=1000");
		document.getElementById("compteur").textContent = contenus.length;
		document.getElementById("liste").innerHTML = contenus.map(carte).join("");
	} catch (e) {
		showError(e);
	}
}

function carte(c) {
	const synopsis = c.synopsis && c.synopsis.length > 150 ? c.synopsis.slice(0, 150) + "..." : c.synopsis;
	const affiche = c.cover
		? `<img src="${esc(c.cover)}" class="card-img-top" alt="${esc(c.title)}" style="max-height: 220px; object-fit: cover;">`
		: `<div class="card-img-top bg-secondary-subtle" style="height: 220px;"></div>`;
	return `
	<div class="col-sm-6 col-md-4 col-lg-3">
		<div class="card border-0 shadow-sm h-100">
			${affiche}
			<div class="card-body">
				<h2 class="h6 mb-1">${esc(c.title)}</h2>
				<p class="small text-secondary mb-2">
					<span class="badge text-bg-${TYPE_COLORS[c.type]}">${TYPE_LABELS[c.type]}</span>
					${c.year ?? "année inconnue"} · ${c.score ?? "-"}/10
				</p>
				<p class="small text-secondary mb-2">${esc(c.genres.join(", "))}</p>
				<p class="small mb-0">${esc(synopsis)}</p>
			</div>
		</div>
	</div>`;
}

chargerContenus();
