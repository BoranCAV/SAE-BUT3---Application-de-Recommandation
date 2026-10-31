from flask import Blueprint, jsonify, request, abort
from app.services.RecoService import RecoService

reco_bp = Blueprint('reco', __name__)


@reco_bp.route('/<int:content_id>', methods=['GET'])
def recommend(content_id):
	"""recommandations pour un contenu selon la méthode choisie"""
	method = request.args.get('method', default='contenu')
	n = request.args.get('n', default=10, type=int)

	if method not in RecoService.METHODS:
		abort(400, description=f"méthode inconnue, choisir parmi {RecoService.METHODS}")

	rs = RecoService()
	results, time_ms = rs.recommend(content_id, method, n)
	return jsonify({
		"content_id": content_id,
		"method": method,
		"time_ms": time_ms,
		"results": [c.to_dict() for c in results]
	})
