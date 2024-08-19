import os

class Config:
    # Chemin vers la base de données SQLite
    DATABASE = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data.db')
    
    # Kafka configurations
    KAFKA_BROKER = 'localhost:9092'
    KAFKA_TOPIC = 'news_topic'
    
    # Autres configurations, si nécessaire
    DEBUG = True  # Mettre à False en production
    TESTING = False

