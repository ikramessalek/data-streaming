import os

class Config:
    # Clé secrète pour les sessions Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'dba6e181c1e41096fc436dbde5274be1')  # Utilise une valeur par défaut si la variable d'environnement n'est pas définie

    # Configuration de la base de données
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///db.sqlite3')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Configuration Kafka
    KAFKA_BROKER = os.getenv('KAFKA_BROKER', 'localhost:9092')
    KAFKA_TOPIC = os.getenv('KAFKA_TOPIC', 'news_topic')

    # Configuration de l'API de nouvelles
    NEWS_API_KEY = os.getenv('NEWS_API_KEY', '49c02fcde33f41a4b5c093011c4e7b91')
    NEWS_API_URL = f'https://newsapi.org/v2/top-headlines?country=us&apiKey={NEWS_API_KEY}'

