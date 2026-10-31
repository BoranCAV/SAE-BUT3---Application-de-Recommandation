from flask import Blueprint, jsonify, request, abort
from app.services.ContentService import ContentService

catalogue_bp = Blueprint('catalogue', __name__)


@catalogue_bp.route('/', methods=['GET'])
def contents():
	"""catalogue avec filtres optionnels en query params"""
	cs = ContentService()
	ctype = request.args.get('type')
	genre = request.args.get('genre')
	limit = request.args.get('limit', default=100, type=int)

	if ctype:
		data = cs.getContentsByType(ctype)
	elif genre:
		data = cs.getContentsByGenre(genre)
	else:
		data = cs.getAllContents(limit=limit)

	return jsonify([c.to_dict() for c in data])


@catalogue_bp.route('/<int:content_id>', methods=['GET'])
def content_detail(content_id):
	cs = ContentService()
	content = cs.getContentById(content_id)
	if not content:
		abort(404, description=f"contenu {content_id} introuvable")
	return jsonify(content[0].to_dict())


@catalogue_bp.route('/genres', methods=['GET'])
def genres():
	cs = ContentService()
	return jsonify([g.to_dict() for g in cs.getAllGenres()])
