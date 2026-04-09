import os
import uuid
import shutil


def salvar_uploads(files, upload_folder: str) -> tuple[str, list[str]]:
    """Saves uploaded files to a temp job folder. Returns (job_id, list of absolute paths)."""
    job_id = str(uuid.uuid4())
    job_folder = os.path.join(upload_folder, job_id)
    os.makedirs(job_folder, exist_ok=True)

    paths = []
    for i, file in enumerate(files):
        ext = os.path.splitext(file.filename)[1].lower() or '.jpg'
        filename = f'foto_{i + 1:02d}{ext}'
        filepath = os.path.join(job_folder, filename)
        file.save(filepath)
        paths.append(filepath)

    return job_id, paths


def garantir_pasta_destino(path: str) -> bool:
    """Creates the destination folder if it doesn't exist. Returns True on success."""
    try:
        os.makedirs(path, exist_ok=True)
        return True
    except Exception:
        return False


def limpar_uploads(job_id: str):
    """Removes the temporary upload folder for a job."""
    from flask import current_app
    try:
        job_folder = os.path.join(current_app.config['UPLOAD_FOLDER'], job_id)
        if os.path.exists(job_folder):
            shutil.rmtree(job_folder)
    except Exception:
        pass
