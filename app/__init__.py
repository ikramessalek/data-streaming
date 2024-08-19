from flask import Flask, render_template
from app.controllers.news_controller import bp as news_bp
from app.controllers.main_controller import main_bp  # Importation correcte du blueprint
from kafka_config import Config  # Assurez-vous que ce chemin est correct

def create_app():
    app = Flask(__name__, static_folder='static', template_folder='templates')
    
    # Configuration de l'application
    app.config.from_object(Config)

    # Enregistrement des blueprints
    app.register_blueprint(news_bp)
    app.register_blueprint(main_bp)  # Enregistrement du blueprint main_bp

    @app.route('/')
    def home():
        return render_template('projet.html')

    @app.route('/news')
    def news_page():
        return render_template('index.html')

    @app.route('/kpi')
    def kpi_page():
        return render_template('index1.html')

    return app

