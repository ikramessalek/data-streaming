from flask import Flask, render_template
from app.controllers.news_controller import bp as news_bp
<<<<<<< HEAD
from app.controllers.main_controller import main_bp
from app.controllers.comments_controller import comment_bp
from kafka_config import Config
=======
from app.controllers.main_controller import main_bp  # Importation correcte du blueprint
from kafka_config import Config  # Assurez-vous que ce chemin est correct
>>>>>>> 8cf87c3ec2fae89642cc348e311cb7ccace931b3

def create_app():
    app = Flask(__name__, static_folder='static', template_folder='templates')
    
    # Configuration de l'application
    app.config.from_object(Config)

    # Enregistrement des blueprints
    app.register_blueprint(news_bp)
<<<<<<< HEAD
    app.register_blueprint(main_bp)
    app.register_blueprint(comment_bp)
=======
    app.register_blueprint(main_bp)  # Enregistrement du blueprint main_bp
>>>>>>> 8cf87c3ec2fae89642cc348e311cb7ccace931b3

    @app.route('/')
    def home():
        return render_template('projet.html')

    @app.route('/news')
    def news_page():
        return render_template('index.html')

    @app.route('/kpi')
    def kpi_page():
        return render_template('index1.html')
<<<<<<< HEAD
    
    @app.route('/comment')
    def comment_page():
        return render_template('comments.html')
=======
>>>>>>> 8cf87c3ec2fae89642cc348e311cb7ccace931b3

    return app

