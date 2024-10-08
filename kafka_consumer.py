import json
import sqlite3
import logging
import threading
from kafka import KafkaConsumer

<<<<<<< HEAD
# Configuration Kafka
KAFKA_BROKER = 'localhost:9092'
NEWS_TOPIC = 'news_topic'
KPI_TOPIC = 'kpi_topic'
REDDIT_TOPIC = 'reddit_comments'
=======
# Configuration
KAFKA_BROKER = 'localhost:9092'
NEWS_TOPIC = 'news_topic'
KPI_TOPIC = 'kpi_topic'
>>>>>>> 8cf87c3ec2fae89642cc348e311cb7ccace931b3
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

<<<<<<< HEAD
reddit_consumer = KafkaConsumer(
    REDDIT_TOPIC,
    bootstrap_servers=[KAFKA_BROKER],
    group_id='reddit_group',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

# Fonction pour initialiser la base de données
=======
>>>>>>> 8cf87c3ec2fae89642cc348e311cb7ccace931b3
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

<<<<<<< HEAD
        # Création de la table kpis
=======
        # Création de la table kpi
>>>>>>> 8cf87c3ec2fae89642cc348e311cb7ccace931b3
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

<<<<<<< HEAD
        # Création de la table comments
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS comments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                submission_title TEXT,
                comment_body TEXT,
                comment_date TEXT,
                submission_url TEXT
            )
        ''')

        conn.commit()
        logging.info("Base de données initialisée.")

# Fonction pour insérer des actualités dans la base de données
=======
        conn.commit()
        logging.info("Base de données initialisée.")

>>>>>>> 8cf87c3ec2fae89642cc348e311cb7ccace931b3
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

<<<<<<< HEAD
# Fonction pour stocker les KPIs dans la base de données
def store_kpi(kpi):
=======
def store_kpi(kpi):
    logging.debug("Storing KPI in database: %s", kpi)
>>>>>>> 8cf87c3ec2fae89642cc348e311cb7ccace931b3
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

<<<<<<< HEAD
# Fonction pour stocker les commentaires Reddit dans la base de données
def store_reddit_comments(comment):
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO comments (submission_title, comment_body, comment_date, submission_url)
            VALUES (?, ?, ?, ?)
        ''', (
            comment['submission_title'],
            comment['comment_body'],
            comment['comment_date'],
            comment['submission_url']
        ))
        conn.commit()
        logging.info("Commentaire stocké dans la base de données: %s", comment['submission_title'])

# Consommateur d'actualités
def consume_news():
    logging.info("Consommation des messages de 'news_topic'...")
    for message in news_consumer:
        logging.info("Message brut reçu: %s", message.value)
=======
def consume_news():
    logging.info("Consuming messages from 'news_topic'...")
    for message in news_consumer:
        logging.info("Raw message received: %s", message.value)
>>>>>>> 8cf87c3ec2fae89642cc348e311cb7ccace931b3
        try:
            article = message.value
            insert_news_into_db(article)
        except Exception as e:
<<<<<<< HEAD
            logging.error("Erreur lors de l'insertion de l'article dans la base de données: %s", str(e))

# Consommateur de KPIs
def consume_kpis():
    logging.info("Consommation des messages de 'kpi_topic'...")
=======
            logging.error("Error inserting article into database: %s", str(e))

def consume_kpis():
    logging.info("Consuming messages from 'kpi_topic'...")
>>>>>>> 8cf87c3ec2fae89642cc348e311cb7ccace931b3
    for message in kpi_consumer:
        logging.debug("Message reçu: %s", message.value)
        try:
            kpi = message.value
            store_kpi(kpi)
        except Exception as e:
<<<<<<< HEAD
            logging.error("Erreur lors de l'insertion du KPI dans la base de données: %s", str(e))

# Consommateur de commentaires Reddit
def consume_reddit_comments():
    logging.info("Consommation des messages de 'reddit_comments'...")
    for message in reddit_consumer:
        logging.debug("Message reçu: %s", message.value)
        try:
            comment = message.value
            store_reddit_comments(comment)
        except Exception as e:
            logging.error("Erreur lors de l'insertion du commentaire dans la base de données: %s", str(e))

# Exécution des consommateurs
if __name__ == "__main__":
    init_db()
    logging.info("Démarrage des consommateurs Kafka.")

    # Démarrage des threads pour consommer les messages des trois topics
    news_thread = threading.Thread(target=consume_news)
    kpi_thread = threading.Thread(target=consume_kpis)
    reddit_thread = threading.Thread(target=consume_reddit_comments)

    news_thread.start()
    kpi_thread.start()
    reddit_thread.start()
=======
            logging.error("Error inserting KPI into database: %s", str(e))

if __name__ == "__main__":
    init_db()
    logging.info("Kafka consumers started.")

    # Démarrage des threads pour consommer les messages des deux topics
    news_thread = threading.Thread(target=consume_news)
    kpi_thread = threading.Thread(target=consume_kpis)

    news_thread.start()
    kpi_thread.start()
>>>>>>> 8cf87c3ec2fae89642cc348e311cb7ccace931b3

    # Assurez-vous que les threads continuent à s'exécuter
    news_thread.join()
    kpi_thread.join()
<<<<<<< HEAD
    reddit_thread.join()
=======
>>>>>>> 8cf87c3ec2fae89642cc348e311cb7ccace931b3


