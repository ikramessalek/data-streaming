import json
import sqlite3
import logging
import threading
from kafka import KafkaConsumer

# Configuration
KAFKA_BROKER = 'localhost:9092'
NEWS_TOPIC = 'news_topic'
KPI_TOPIC = 'kpi_topic'
DATABASE = 'data.db'

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')

# Configure Kafka consumers
news_consumer = KafkaConsumer(
    NEWS_TOPIC,
    bootstrap_servers=[KAFKA_BROKER],
    group_id='news_group',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

kpi_consumer = KafkaConsumer(
    KPI_TOPIC,
    bootstrap_servers=[KAFKA_BROKER],
    group_id='kpi_group',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

def init_db():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()

        # Création de la table news
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS news (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                description TEXT,
                url TEXT UNIQUE,
                published_at TEXT,
                source_name TEXT,
                author TEXT
            )
        ''')

        # Création de la table kpi
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS kpis (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                company_name TEXT,
                date TEXT,
                open REAL,
                high REAL,
                low REAL,
                close REAL,
                volume INTEGER
            )
        ''')

        conn.commit()
        logging.info("Base de données initialisée.")

def insert_news_into_db(article):
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR IGNORE INTO news (title, description, url, published_at, source_name, author)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            article['title'],
            article.get('description', ''),
            article['url'],
            article.get('published_at', ''),
            article['source_name'],
            article.get('author', '')
        ))
        conn.commit()
        logging.info("Article inséré dans la base de données: %s", article['title'])

def store_kpi(kpi):
    logging.debug("Storing KPI in database: %s", kpi)
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO kpis (company_name, date, open, high, low, close, volume)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            kpi.get('company_name'),
            kpi.get('date'),
            kpi.get('open'),
            kpi.get('high'),
            kpi.get('low'),
            kpi.get('close'),
            kpi.get('volume')
        ))
        conn.commit()
        logging.info("KPI stocké dans la base de données: %s", kpi)

def consume_news():
    logging.info("Consuming messages from 'news_topic'...")
    for message in news_consumer:
        logging.info("Raw message received: %s", message.value)
        try:
            article = message.value
            insert_news_into_db(article)
        except Exception as e:
            logging.error("Error inserting article into database: %s", str(e))

def consume_kpis():
    logging.info("Consuming messages from 'kpi_topic'...")
    for message in kpi_consumer:
        logging.debug("Message reçu: %s", message.value)
        try:
            kpi = message.value
            store_kpi(kpi)
        except Exception as e:
            logging.error("Error inserting KPI into database: %s", str(e))

if __name__ == "__main__":
    init_db()
    logging.info("Kafka consumers started.")

    # Démarrage des threads pour consommer les messages des deux topics
    news_thread = threading.Thread(target=consume_news)
    kpi_thread = threading.Thread(target=consume_kpis)

    news_thread.start()
    kpi_thread.start()

    # Assurez-vous que les threads continuent à s'exécuter
    news_thread.join()
    kpi_thread.join()


