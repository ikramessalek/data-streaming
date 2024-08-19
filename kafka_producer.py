import json
import requests
import logging
<<<<<<< HEAD
import threading
import time
from kafka import KafkaProducer
import praw

# Configuration des clés API
API_KEY_NASDAQ = 'MLfw6ggQMsmsQNdgnaBz'
API_KEY_NEWS = '49c02fcde33f41a4b5c093011c4e7b91'

# Configuration Kafka
KAFKA_BROKER = 'localhost:9092'
NEWS_TOPIC = 'news_topic'
KPI_TOPIC = 'kpi_topic'
REDDIT_TOPIC = 'reddit_comments'

# Configuration des paramètres
COMPANY_SYMBOLS = [
    {'name': 'Apple Inc.', 'symbol': 'AAPL'},
    {'name': 'Microsoft Corp.', 'symbol': 'MSFT'}
]
UPDATE_INTERVAL = 30
REDDIT_INTERVAL = 60

# Initialisation du producteur Kafka
producer = KafkaProducer(
    bootstrap_servers=[KAFKA_BROKER],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Initialisation de Reddit
reddit = praw.Reddit(
    client_id='XfZOeNraKU5wNGl9OIwU7w',
    client_secret='YKEbb1NMnmwBqcyLt-lqR2YaCqJHug',
    user_agent='my_reddit_app_v1'
)
=======
from kafka import KafkaProducer
from time import sleep, time

# Configuration
API_KEY_NASDAQ = 'MLfw6ggQMsmsQNdgnaBz'  # Remplacez par votre clé API pour Nasdaq Data Link
API_KEY_NEWS = '49c02fcde33f41a4b5c093011c4e7b91'  # Remplacez par votre clé API pour NewsAPI

COMPANY_SYMBOLS = [
    {'name': 'Apple Inc.', 'symbol': 'AAPL'},
    {'name': 'Microsoft Corp.', 'symbol': 'MSFT'},
    # Ajoutez les autres entreprises ici...
]

KAFKA_BROKER = 'localhost:9092'
KAFKA_TOPIC_KPI = 'kpi_topic'
KAFKA_TOPIC_NEWS = 'news_topic'

NEWS_API_URL = f'https://newsapi.org/v2/top-headlines?country=us&apiKey={API_KEY_NEWS}'
UPDATE_INTERVAL = 30  # Intervalle de récupération des actualités en secondes
>>>>>>> 8cf87c3ec2fae89642cc348e311cb7ccace931b3

# Configuration du logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')

<<<<<<< HEAD
=======
# Configuration du Kafka producer
producer = KafkaProducer(
    bootstrap_servers=[KAFKA_BROKER],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

>>>>>>> 8cf87c3ec2fae89642cc348e311cb7ccace931b3
# Fonction pour récupérer et envoyer les KPIs
def fetch_kpis():
    logging.info("Début de la récupération des KPIs.")
    for symbol in COMPANY_SYMBOLS:
        company_name = symbol['name']
        symbol_code = symbol['symbol']
        api_url = f'https://data.nasdaq.com/api/v3/datasets/WIKI/{symbol_code}.json'
<<<<<<< HEAD
        params = {'api_key': API_KEY_NASDAQ, 'collapse': 'daily', 'transform': 'normalize'}
=======
        params = {
            'api_key': API_KEY_NASDAQ,
            'collapse': 'daily',
            'transform': 'normalize'
        }
        
>>>>>>> 8cf87c3ec2fae89642cc348e311cb7ccace931b3
        try:
            response = requests.get(api_url, params=params)
            response.raise_for_status()
            data = response.json()
            time_series = data.get('dataset', {}).get('data', [])
<<<<<<< HEAD
            if not time_series:
                logging.warning("Aucune donnée pour %s.", company_name)
                continue
            for record in time_series:
                kpi = {
                    'company_name': company_name,
                    'date': record[0],
=======
            
            if not time_series:
                logging.warning("Aucune donnée de série temporelle trouvée pour %s.", company_name)
                continue
            
            for record in time_series:
                timestamp = record[0]  # Date
                kpi = {
                    'company_name': company_name,
                    'date': timestamp,
>>>>>>> 8cf87c3ec2fae89642cc348e311cb7ccace931b3
                    'open': float(record[1]),
                    'high': float(record[2]),
                    'low': float(record[3]),
                    'close': float(record[4]),
                    'volume': int(record[5])
                }
<<<<<<< HEAD
                producer.send(KPI_TOPIC, kpi)
                logging.info("KPI envoyé: %s", kpi)
        except requests.RequestException as e:
            logging.error("Erreur KPIs %s: %s", company_name, e)

# Fonction pour récupérer et envoyer les actualités
def fetch_and_store_news():
    logging.info("Récupération des actualités...")
    try:
        response = requests.get(f'https://newsapi.org/v2/top-headlines?country=us&apiKey={API_KEY_NEWS}')
        response.raise_for_status()
        articles = response.json().get('articles', [])
        logging.info(f"Fetched {len(articles)} articles.")
=======
                producer.send(KAFKA_TOPIC_KPI, kpi)
                logging.info("KPI envoyé au topic Kafka: %s", kpi)
        except requests.RequestException as e:
            logging.error("Erreur lors de la récupération des KPIs pour %s : %s", company_name, e)

# Fonction pour récupérer et envoyer les actualités
def fetch_and_store_news():
    logging.info("Fetching news from API...")
    try:
        response = requests.get(NEWS_API_URL)
        response.raise_for_status()
        articles = response.json().get('articles', [])
        logging.info(f"Fetched {len(articles)} articles.")

>>>>>>> 8cf87c3ec2fae89642cc348e311cb7ccace931b3
        for article in articles:
            news = {
                'title': article['title'],
                'description': article.get('description', ''),
                'url': article['url'],
                'published_at': article.get('publishedAt', ''),
                'source_name': article['source'].get('name', ''),
                'author': article.get('author', '')
            }
<<<<<<< HEAD
            producer.send(NEWS_TOPIC, news)
            logging.info("Article envoyé: %s", news['title'])
        producer.flush()
        logging.info("Articles envoyés à Kafka.")
    except requests.RequestException as e:
        logging.error("Erreur lors de la récupération des actualités: %s", e)

# Fonction pour récupérer les commentaires Reddit
def get_reddit_comments(subreddit, query):
    submissions = reddit.subreddit(subreddit).search(query, sort='relevance', limit=5)
    results = []
    for submission in submissions:
        submission.comments.replace_more(limit=0)
        for comment in submission.comments.list():
            results.append({
                'submission_title': submission.title,
                'comment_body': comment.body,
                'comment_date': time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(comment.created_utc)),
                'submission_url': submission.url
            })
    return results

# Fonction principale du producteur
=======
            producer.send(KAFKA_TOPIC_NEWS, news)
            logging.info(f"Article envoyé au topic Kafka: {news['title']}")
        
        producer.flush()
        logging.info("Articles sent to Kafka.")
    except requests.RequestException as e:
        logging.error(f"Error fetching news: {str(e)}")

# Fonction principale qui exécute les deux récupérations périodiquement
>>>>>>> 8cf87c3ec2fae89642cc348e311cb7ccace931b3
def run_producer():
    while True:
        fetch_kpis()
        fetch_and_store_news()
<<<<<<< HEAD
        # Publier les commentaires Reddit toutes les REDDIT_INTERVAL secondes
        while True:
            comments = get_reddit_comments('all', 'news')
            for comment in comments:
                producer.send(REDDIT_TOPIC, comment)
                logging.info("Commentaire envoyé: %s", comment['submission_title'])
            producer.flush()
            logging.info(f"Attente de {REDDIT_INTERVAL} secondes...")
            time.sleep(REDDIT_INTERVAL)

# Exécution du producteur
if __name__ == "__main__":
    run_producer()

=======
        logging.info(f"Sleeping for {UPDATE_INTERVAL} seconds...")
        sleep(UPDATE_INTERVAL)

if __name__ == "__main__":
    logging.info("Starting KPI and news producer...")
    try:
        run_producer()
    except KeyboardInterrupt:
        logging.info("Producer interrupted and shutting down.")
>>>>>>> 8cf87c3ec2fae89642cc348e311cb7ccace931b3

