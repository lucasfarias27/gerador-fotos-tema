import os
from flask import Blueprint, request, jsonify, current_app
from app.services.job_manager import job_manager
from app.utils.file_handler import salvar_uploads, garantir_pasta_destino
from app.utils.validators import validar_arquivos, validar_quantidade, validar_tema
from config import Config

api_bp = Blueprint('api', __name__)


@api_bp.route('/temas', methods=['GET'])
def listar_temas():
    temas = [
        {'id': key, 'label': value['label']}
        for key, value in Config.THEMES.items()
    ]
    return jsonify(temas)


@api_bp.route('/iniciar-geracao', methods=['POST'])
def iniciar_geracao():
    fotos = request.files.getlist('fotos[]')
    tema = request.form.get('tema', '').strip()
    quantidade_str = request.form.get('quantidade', '1').strip()
    pasta_destino = request.form.get('pasta_destino', '').strip()

    # Validações
    erro_arquivos = validar_arquivos(fotos, Config.MAX_UPLOAD_FILES, Config.ALLOWED_EXTENSIONS)
    if erro_arquivos:
        return jsonify({'erro': erro_arquivos}), 400

    erro_tema = validar_tema(tema, Config.THEMES)
    if erro_tema:
        return jsonify({'erro': erro_tema}), 400

    erro_qtd, quantidade = validar_quantidade(quantidade_str)
    if erro_qtd:
        return jsonify({'erro': erro_qtd}), 400

    if not pasta_destino:
        pasta_destino = current_app.config['DEFAULT_DOWNLOAD_FOLDER']

    if not garantir_pasta_destino(pasta_destino):
        return jsonify({'erro': f'Não foi possível criar a pasta de destino: {pasta_destino}'}), 400

    # Salvar uploads temporários
    job_id, fotos_paths = salvar_uploads(fotos, current_app.config['UPLOAD_FOLDER'])

    # Criar e iniciar job
    job_manager.criar_job(job_id, fotos_paths, tema, quantidade, pasta_destino)

    return jsonify({'job_id': job_id, 'status': 'iniciado'})


@api_bp.route('/status-job/<job_id>', methods=['GET'])
def status_job(job_id):
    status = job_manager.obter_status(job_id)
    if status is None:
        return jsonify({'erro': 'Job não encontrado'}), 404
    return jsonify(status)


@api_bp.route('/cancelar-job/<job_id>', methods=['POST'])
def cancelar_job(job_id):
    sucesso = job_manager.cancelar_job(job_id)
    if not sucesso:
        return jsonify({'erro': 'Job não encontrado ou já finalizado'}), 404
    return jsonify({'cancelado': True})


@api_bp.route('/escolher-pasta', methods=['GET'])
def escolher_pasta():
    """Opens a native OS folder picker and returns the selected path."""
    try:
        import tkinter as tk
        from tkinter import filedialog
        root = tk.Tk()
        root.withdraw()
        root.wm_attributes('-topmost', True)
        folder = filedialog.askdirectory(title='Escolha a pasta para salvar as imagens')
        root.destroy()
        if folder:
            return jsonify({'pasta': os.path.normpath(folder)})
        return jsonify({'pasta': ''})
    except Exception as e:
        return jsonify({'erro': str(e), 'pasta': ''}), 500
