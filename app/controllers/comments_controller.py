import csv
from flask import Blueprint, request, jsonify, render_template, current_app, Response
import sqlite3
from datetime import datetime
import io

comment_bp = Blueprint('comments', __name__)

DATABASE = 'data.db'  # Chemin fixe vers la base de données

def get_comments_query(submission_title='', start_date='', end_date='', keyword='', submission_url=''):
    query = 'SELECT id, submission_title, comment_body, comment_date, submission_url FROM comments WHERE 1=1'
    params = []

    if submission_title:
        query += ' AND submission_title LIKE ?'
        params.append(f'%{submission_title}%')

    if submission_url:
        query += ' AND submission_url LIKE ?'
        params.append(f'%{submission_url}%')

    if start_date:
        try:
            datetime.strptime(start_date, '%Y-%m-%d')
            query += ' AND comment_date >= ?'
            params.append(f'{start_date} 00:00:00')
        except ValueError:
            raise ValueError('Invalid start date format. Use YYYY-MM-DD.')

    if end_date:
        try:
            datetime.strptime(end_date, '%Y-%m-%d')
            query += ' AND comment_date <= ?'
            params.append(f'{end_date} 23:59:59')
        except ValueError:
            raise ValueError('Invalid end date format. Use YYYY-MM-DD.')

    if keyword:
        query += ' AND (submission_title LIKE ? OR comment_body LIKE ?)'
        params.extend([f'%{keyword}%', f'%{keyword}%'])

    return query, params

def fetch_comments(query, params):
    current_app.logger.info(f"Executing query: {query} with params: {params}")
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        results = cursor.fetchall()
        current_app.logger.info(f"Fetched comments: {results}")
        return results

@comment_bp.route('/api/comments', methods=['GET'])
def api_comments():
    submission_title = request.args.get('submission_title', '')
    start_date = request.args.get('start_date', '')
    end_date = request.args.get('end_date', '')
    keyword = request.args.get('keyword', '')
    submission_url = request.args.get('submission_url', '')

    try:
        query, params = get_comments_query(submission_title, start_date, end_date, keyword, submission_url)
        current_app.logger.info(f"Executing API query: {query} with params: {params}")
        comments = fetch_comments(query, params)
        comments_list = [{
            'id': row[0],
            'submission_title': row[1],
            'comment_body': row[2],
            'comment_date': row[3],
            'submission_url': row[4]
        } for row in comments]
        response = jsonify(comments_list)
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    except Exception as e:
        current_app.logger.error(f"Erreur lors de la récupération des commentaires : {str(e)}")
        return jsonify({'error': 'Erreur lors de la récupération des commentaires', 'details': str(e)}), 500

@comment_bp.route('/comments-page', methods=['GET'])
def comments_page():
    return render_template('comments.html')

@comment_bp.route('/download-comments', methods=['GET'])
def download_comments():
    submission_title = request.args.get('submission_title', '')
    start_date = request.args.get('start_date', '')
    end_date = request.args.get('end_date', '')
    keyword = request.args.get('keyword', '')
    submission_url = request.args.get('submission_url', '')

    try:
        query, params = get_comments_query(submission_title, start_date, end_date, keyword, submission_url)
        current_app.logger.info(f"Executing query for CSV: {query} with params: {params}")
        comments = fetch_comments(query, params)

        if not comments:
            current_app.logger.info("No comments found for CSV export")
        
        # Création du fichier CSV
        def generate_csv():
            output = io.StringIO()
            csv_writer = csv.writer(output, quoting=csv.QUOTE_MINIMAL)
            
            # En-tête
            csv_writer.writerow(['ID', 'Titre de la Soumission', 'Commentaire', 'Date du Commentaire', 'URL de la Soumission'])
            
            # Données
            for comment in comments:
                row = [str(c) for c in comment]
                csv_writer.writerow(row)
            
            output.seek(0)
            return output.getvalue()

        # Retourne la réponse avec le contenu CSV
        return Response(
            generate_csv(),
            mimetype='text/csv',
            headers={"Content-Disposition": "attachment;filename=comments.csv"}
        )
    except Exception as e:
        current_app.logger.error(f"Erreur lors de la génération du CSV : {str(e)}")
        return jsonify({'error': 'Erreur lors de la génération du CSV', 'details': str(e)}), 500




