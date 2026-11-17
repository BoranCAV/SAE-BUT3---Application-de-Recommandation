import time
import statistics
from flask import Blueprint, jsonify
from app.services.ContentService import ContentService
from app.services.RecoService import RecoService

benchmark_bp = Blueprint('benchmark', __name__)

@benchmark_bp.route('/', methods=['GET'])
def run_bench():
	cs = ContentService()
	rs = RecoService()
	contenus = cs.getAllContents(limit=1000)
	
	if not contenus:
		return jsonify({"error": "Base de données vide"}), 400

	echantillon = contenus[:5]
	temps = []

	for c in echantillon:
		start = time.perf_counter()
		rs.recoContenu(c.id, 10)
		end = time.perf_counter()
		temps.append((end - start) * 1000)

	return jsonify({
		"temps_min": round(min(temps), 2),
		"temps_max": round(max(temps), 2),
		"temps_moyen": round(statistics.mean(temps), 2),
		"nb_contenus": len(contenus)
	})
