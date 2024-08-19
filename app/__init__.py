from flask import Flask, render_template
from app.controllers.news_controller import bp as news_bp
from app.controllers.main_controller import main_bp
from app.controllers.comments_controller import comment_bp
from kafka_config import Config

def create_app():
    app = Flask(__name__, static_folder='static', template_folder='templates')
    
    # Configuration de l'application
    app.config.from_object(Config)

    # Enregistrement des blueprints
    app.register_blueprint(news_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(comment_bp)

    @app.route('/')
    def home():
        return render_template('projet.html')

    @app.route('/news')
    def news_page():
        return render_template('index.html')

    @app.route('/kpi')
    def kpi_page():
        return render_template('index1.html')
    
    @app.route('/comment')
    def comment_page():
        return render_template('comments.html')

    return app

