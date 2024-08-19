from flask import Blueprint, request, jsonify, render_template, current_app
import sqlite3
import logging
from app.models.news_model import get_news_query, fetch_news

bp = Blueprint('news', __name__)

@bp.route('/news')
def index():
    return render_template('index.html')

@bp.route('/api/news', methods=['GET'])
def api_news():
    try:
        author_filter = request.args.get('author', '')
        source_filter = request.args.get('source', '')
        date_start_filter = request.args.get('date_start', '')
        date_end_filter = request.args.get('date_end', '')
        keyword = request.args.get('keyword', '')

        query, params = get_news_query(author_filter, source_filter, date_start_filter, date_end_filter, keyword)
        news = fetch_news(query, params)

        if not news:
            return jsonify({'message': 'Aucune donnée trouvée avec les filtres appliqués.'})

        news_list = [
            {
                'title': row[0],
                'description': row[1],
                'url': row[2],
                'published_at': row[3],
                'source_name': row[4],
                'author': row[5]
            } for row in news
        ]

        return jsonify(news_list)
    except Exception as e:
        logging.error(f"Error fetching news: {str(e)}")
        return jsonify({'error': str(e)}), 500

@bp.route('/api/sources', methods=['GET'])
def api_sources():
    try:
        with sqlite3.connect(current_app.config['DATABASE']) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT DISTINCT source_name FROM news')
            sources = [row[0] for row in cursor.fetchall()]
        return jsonify(sources)
    except Exception as e:
        logging.error(f"Error fetching sources: {str(e)}")
        return jsonify({'error': str(e)}), 500

@bp.route('/api/authors', methods=['GET'])
def api_authors():
    try:
        with sqlite3.connect(current_app.config['DATABASE']) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT DISTINCT author FROM news')
            authors = [row[0] for row in cursor.fetchall()]
        return jsonify(authors)
    except Exception as e:
        logging.error(f"Error fetching authors: {str(e)}")
        return jsonify({'error': str(e)}), 500


