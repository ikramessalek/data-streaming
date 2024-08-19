import sqlite3
from flask import current_app
from datetime import datetime

def get_news_query(author_filter='', source_filter='', date_start_filter='', date_end_filter='', keyword_filter=''):
    query = 'SELECT title, description, url, published_at, source_name, author FROM news WHERE 1=1'
    params = []

    if author_filter:
        query += ' AND author LIKE ?'
        params.append(f'%{author_filter}%')

    if source_filter:
        query += ' AND source_name = ?'
        params.append(source_filter)

    if date_start_filter:
        try:
            datetime.strptime(date_start_filter, '%Y-%m-%d')
            query += ' AND published_at >= ?'
            params.append(f'{date_start_filter}T00:00:00Z')
        except ValueError:
            raise ValueError('Invalid start date format. Use YYYY-MM-DD.')

    if date_end_filter:
        try:
            datetime.strptime(date_end_filter, '%Y-%m-%d')
            query += ' AND published_at <= ?'
            params.append(f'{date_end_filter}T23:59:59Z')
        except ValueError:
            raise ValueError('Invalid end date format. Use YYYY-MM-DD.')

    if keyword_filter:
        query += ' AND (title LIKE ? OR description LIKE ?)'
        params.extend([f'%{keyword_filter}%', f'%{keyword_filter}%'])

    return query, params


def fetch_news(query, params):
    with sqlite3.connect(current_app.config['DATABASE']) as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        return cursor.fetchall()

