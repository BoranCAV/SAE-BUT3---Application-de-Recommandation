from flask import Blueprint, jsonify

index_bp = Blueprint('index', __name__)


@index_bp.route('/', methods=['GET'])
def index():
	"""point d'entrée de l'API : sert aussi à vérifier que le backend répond"""
	return jsonify({
		"app": "SAE reco comparée",
		"version": "0.1.0",
		"routes": [
			"GET /api/catalogue/?type=&genre=&limit=",
			"GET /api/catalogue/<id>",
			"GET /api/catalogue/genres",
			"GET /api/reco/<id>?method=contenu|embeddings&n=10",
		]
	})
