import sqlite3
from datetime import datetime

DATABASE = 'data.db'  # Chemin fixe vers la base de données

def get_comments_query(submission_title='', start_date='', end_date='', keyword=''):
    query = 'SELECT id, submission_title, comment_body, comment_date, submission_url FROM comments WHERE 1=1'
    params = []

    if submission_title:
        query += ' AND submission_title LIKE ?'
        params.append(f'%{submission_title}%')

    if start_date:
        try:
            datetime.strptime(start_date, '%Y-%m-%d')
            query += ' AND comment_date >= ?'
            params.append(f'{start_date}T00:00:00Z')
        except ValueError:
            raise ValueError('Invalid start date format. Use YYYY-MM-DD.')

    if end_date:
        try:
            datetime.strptime(end_date, '%Y-%m-%d')
            query += ' AND comment_date <= ?'
            params.append(f'{end_date}T23:59:59Z')
        except ValueError:
            raise ValueError('Invalid end date format. Use YYYY-MM-DD.')

    if keyword:
        query += ' AND (submission_title LIKE ? OR comment_body LIKE ?)'
        params.extend([f'%{keyword}%', f'%{keyword}%'])

    return query, params

def fetch_comments(query, params):
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        return cursor.fetchall()

