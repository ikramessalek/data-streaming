from flask import Blueprint, render_template, jsonify, request
from ..models.kpis_model import get_dynamic_companies, get_all_companies, get_kpis_filtered

main_bp = Blueprint('main', __name__)

@main_bp.route('/kpi')
def index():
    companies = get_all_companies()
    return render_template('index1.html', companies=companies)

@main_bp.route('/api/kpis', methods=['GET'])
def api_kpis():
    company = request.args.get('company')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    keyword = request.args.get('keyword')
    try:
        kpis = get_kpis_filtered(company, start_date, end_date, keyword)
        return jsonify(kpis)
    except Exception as e:
        main_bp.logger.error(f"Erreur lors de la récupération des KPIs : {str(e)}")
        return jsonify({'error': str(e)}), 500

@main_bp.route('/test_companies', methods=['GET'])
def test_companies():
    companies = get_all_companies()
    return jsonify(companies)

@main_bp.route('/dynamic_companies', methods=['GET'])
def dynamic_companies():
    companies = get_dynamic_companies()
    return jsonify(companies)



