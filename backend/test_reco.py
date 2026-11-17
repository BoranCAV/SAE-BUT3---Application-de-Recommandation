from prepa_db import setup_database
from app.services.ContentService import ContentService
from app.services.RecoService import RecoService

setup_database()

cs = ContentService()
rs = RecoService()

contenus = cs.getAllContents()
aot = [c for c in contenus if c.title == "Attack on Titan"][0]

results = rs.recoContenu(aot.id, 10)
titres = [c.title for c in results]

assert "Fullmetal Alchemist: Brotherhood" in titres
assert "Breaking Bad" in titres
assert titres.index("Fullmetal Alchemist: Brotherhood") < titres.index("Breaking Bad")

for c in contenus:
	recos = rs.recoContenu(c.id, 10)
	assert c.id not in [r.id for r in recos], f"{c.title} présent dans ses propres résultats"

assert rs.recoContenu(999999, 5) == []

print("[+] tests reco contenu ok")
