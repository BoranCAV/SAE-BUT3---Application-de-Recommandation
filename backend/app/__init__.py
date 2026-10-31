import os
from flask import Flask, jsonify


def create_app():
	"""application factory : l'API ne renvoie que du JSON, le front est servi à part"""
	app = Flask(__name__)

	app.config['DATABASE_PATH'] = os.path.join(app.root_path, 'reco.db')
	app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + app.config['DATABASE_PATH']
	app.json.ensure_ascii = False  # garde les accents lisibles dans le JSON

	from app.blueprints import index_bp, catalogue_bp, reco_bp
	app.register_blueprint(index_bp, url_prefix='/api')
	app.register_blueprint(catalogue_bp, url_prefix='/api/catalogue')
	app.register_blueprint(reco_bp, url_prefix='/api/reco')

	@app.after_request
	def autoriser_front(response):
		# le front tourne sur un autre port : on autorise ses requêtes fetch (CORS)
		response.headers['Access-Control-Allow-Origin'] = '*'
		response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
		response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
		return response

	# les erreurs aussi en JSON, sinon le front reçoit une page HTML
	@app.errorhandler(400)
	@app.errorhandler(404)
	def erreur_json(e):
		return jsonify({"error": e.description}), e.code

	return app
