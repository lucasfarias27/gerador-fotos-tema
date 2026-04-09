from flask import Blueprint, render_template, request

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    return render_template('index.html')


@main_bp.route('/resultado')
def resultado():
    job_id = request.args.get('job_id', '')
    return render_template('resultado.html', job_id=job_id)
