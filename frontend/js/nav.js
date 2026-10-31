// équivalent du {% include 'nav.html' %} du prof : la même barre est injectée dans chaque page
// le lien actif est déduit du nom du fichier (comme metadata.pagename côté Jinja)

const NAV_ITEMS = [
	["index.html", "Accueil"],
	["catalogue.html", "Catalogue"],
	["reco.html", "Comparer"],
];

const currentPage = location.pathname.split("/").pop() || "index.html";

const links = NAV_ITEMS.map(([href, label]) => `
	<li class="nav-item">
		<a class="nav-link ${href === currentPage ? "active" : ""}" href="${href}">${label}</a>
	</li>`).join("");

document.getElementById("nav").innerHTML = `
<nav class="navbar navbar-expand-lg bg-dark navbar-dark fixed-top shadow-sm">
	<div class="container-fluid">
		<a class="navbar-brand fw-bold" href="index.html">SAE Reco</a>
		<button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarContent">
			<span class="navbar-toggler-icon"></span>
		</button>
		<div class="collapse navbar-collapse" id="navbarContent">
			<ul class="navbar-nav me-auto mb-2 mb-lg-0">${links}</ul>
		</div>
	</div>
</nav>`;
