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
		}
	} catch (e) {
		showError(e);
	}
}

chargerContenus();
