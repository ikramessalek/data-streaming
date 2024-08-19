import json
import requests
import logging
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

# Configuration du logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')

# Configuration du Kafka producer
producer = KafkaProducer(
    bootstrap_servers=[KAFKA_BROKER],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Fonction pour récupérer et envoyer les KPIs
def fetch_kpis():
    logging.info("Début de la récupération des KPIs.")
    for symbol in COMPANY_SYMBOLS:
        company_name = symbol['name']
        symbol_code = symbol['symbol']
        api_url = f'https://data.nasdaq.com/api/v3/datasets/WIKI/{symbol_code}.json'
        params = {
            'api_key': API_KEY_NASDAQ,
            'collapse': 'daily',
            'transform': 'normalize'
        }
        
        try:
            response = requests.get(api_url, params=params)
            response.raise_for_status()
            data = response.json()
            time_series = data.get('dataset', {}).get('data', [])
            
            if not time_series:
                logging.warning("Aucune donnée de série temporelle trouvée pour %s.", company_name)
                continue
            
            for record in time_series:
                timestamp = record[0]  # Date
                kpi = {
                    'company_name': company_name,
                    'date': timestamp,
                    'open': float(record[1]),
                    'high': float(record[2]),
                    'low': float(record[3]),
                    'close': float(record[4]),
                    'volume': int(record[5])
                }
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

        for article in articles:
            news = {
                'title': article['title'],
                'description': article.get('description', ''),
                'url': article['url'],
                'published_at': article.get('publishedAt', ''),
                'source_name': article['source'].get('name', ''),
                'author': article.get('author', '')
            }
            producer.send(KAFKA_TOPIC_NEWS, news)
            logging.info(f"Article envoyé au topic Kafka: {news['title']}")
        
        producer.flush()
        logging.info("Articles sent to Kafka.")
    except requests.RequestException as e:
        logging.error(f"Error fetching news: {str(e)}")

# Fonction principale qui exécute les deux récupérations périodiquement
def run_producer():
    while True:
        fetch_kpis()
        fetch_and_store_news()
        logging.info(f"Sleeping for {UPDATE_INTERVAL} seconds...")
        sleep(UPDATE_INTERVAL)

if __name__ == "__main__":
    logging.info("Starting KPI and news producer...")
    try:
        run_producer()
    except KeyboardInterrupt:
        logging.info("Producer interrupted and shutting down.")

