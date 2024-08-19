import sqlite3
import logging
from flask import current_app

# Configuration du logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s: %(message)s')

def get_dynamic_companies():
    query = '''
       SELECT company_name, AVG(high - low) as avg_price_change, AVG(volume) as avg_volume
       FROM kpis
       GROUP BY company_name
       ORDER BY avg_price_change DESC;
    '''
    try:
        with sqlite3.connect(current_app.config['DATABASE']) as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            logging.debug("Résultats récupérés pour dynamic companies: %s", rows)
            companies_list = [{
                'company_name': row[0],
                'avg_price_change': row[1],
                'avg_volume': row[2]
            } for row in rows]
            logging.info("Entreprises dynamiques récupérées : %s", companies_list)
            return companies_list
    except sqlite3.Error as e:
        logging.error(f"Erreur lors de l'exécution de la requête : {e}")
        return []

def get_all_companies():
    query = 'SELECT DISTINCT company_name FROM kpis'
    try:
        with sqlite3.connect(current_app.config['DATABASE']) as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            logging.debug("Résultats récupérés pour all companies: %s", rows)
            companies_list = [{'company_name': row[0]} for row in rows]
            logging.info("Toutes les entreprises récupérées : %s", companies_list)
            return companies_list
    except sqlite3.Error as e:
        logging.error(f"Erreur lors de l'exécution de la requête pour récupérer toutes les entreprises : {e}")
        return []

def get_kpis_filtered(company=None, start_date=None, end_date=None, keyword=None):
    query = '''
        SELECT company_name, date, open, high, low, close, volume FROM kpis
        WHERE 1=1
    '''
    params = []
    if company:
        query += ' AND company_name = ?'
        params.append(company)
    if start_date:
        query += ' AND date >= ?'
        params.append(start_date)
    if end_date:
        query += ' AND date <= ?'
        params.append(end_date)
    if keyword:
        query += ' AND (company_name LIKE ? OR open LIKE ? OR high LIKE ? OR low LIKE ? OR close LIKE ? OR volume LIKE ?)'
        params.extend([f'%{keyword}%' for _ in range(6)])
    query += ' ORDER BY date DESC'
    
    try:
        with sqlite3.connect(current_app.config['DATABASE']) as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            rows = cursor.fetchall()
            logging.debug("Résultats récupérés pour KPIs filtrés: %s", rows)
            kpis_list = [{
                'company_name': row[0],
                'date': row[1],
                'open': row[2],
                'high': row[3],
                'low': row[4],
                'close': row[5],
                'volume': row[6]
            } for row in rows]
            logging.info("KPIs filtrés récupérés : %s", kpis_list)
            return kpis_list
    except sqlite3.Error as e:
        logging.error(f"Erreur lors de l'exécution de la requête filtrée : {e}")
        return []

