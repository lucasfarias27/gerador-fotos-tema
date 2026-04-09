import threading
from enum import Enum
from app.services.automation import GeminiAutomation
from app.utils.file_handler import limpar_uploads
from config import Config


class JobStatus(Enum):
    PENDENTE = 'pendente'
    EM_PROGRESSO = 'em_progresso'
    CONCLUIDO = 'concluido'
    ERRO = 'erro'
    CANCELADO = 'cancelado'


class Job:
    def __init__(self, job_id, fotos_paths, tema, quantidade, pasta_destino):
        self.job_id = job_id
        self.fotos_paths = fotos_paths
        self.tema = tema
        self.quantidade = quantidade
        self.pasta_destino = pasta_destino
        self.status = JobStatus.PENDENTE
        self.progresso = 0
        self.imagens_geradas = 0
        self.mensagem = 'Aguardando início...'
        self.erro = None
        self.cancel_event = threading.Event()
        self.thread = None
        self.imagens_salvas = []


class _JobManager:
    def __init__(self):
        self._jobs: dict[str, Job] = {}
        self._lock = threading.Lock()

    def criar_job(self, job_id: str, fotos_paths: list, tema: str, quantidade: int, pasta_destino: str):
        job = Job(job_id, fotos_paths, tema, quantidade, pasta_destino)
        with self._lock:
            self._jobs[job_id] = job

        thread = threading.Thread(target=self._executar_job, args=(job,), daemon=True)
        job.thread = thread
        thread.start()

    def _executar_job(self, job: Job):
        tema_config = Config.THEMES.get(job.tema)
        if not tema_config:
            with self._lock:
                job.status = JobStatus.ERRO
                job.erro = f'Tema "{job.tema}" não encontrado.'
            return

        automation = GeminiAutomation()

        def atualizar_progresso(geradas: int, total: int, mensagem: str = None):
            with self._lock:
                job.imagens_geradas = geradas
                job.progresso = int((geradas / total) * 100)
                job.mensagem = mensagem or f'Gerando imagem {geradas} de {total}...'

        def imagem_salva(caminho: str):
            with self._lock:
                job.imagens_salvas.append(caminho)

        with self._lock:
            job.status = JobStatus.EM_PROGRESSO
            job.mensagem = 'Iniciando automação...'

        try:
            automation.executar(job, tema_config, atualizar_progresso, imagem_salva)

            with self._lock:
                if job.cancel_event.is_set():
                    job.status = JobStatus.CANCELADO
                    job.mensagem = 'Geração cancelada.'
                else:
                    job.status = JobStatus.CONCLUIDO
                    job.progresso = 100
                    job.mensagem = f'{job.imagens_geradas} imagem(ns) gerada(s) com sucesso!'
        except Exception as e:
            with self._lock:
                job.status = JobStatus.ERRO
                job.erro = str(e)
                job.mensagem = f'Erro: {str(e)}'
        finally:
            limpar_uploads(job.job_id)

    def obter_status(self, job_id: str) -> dict | None:
        with self._lock:
            job = self._jobs.get(job_id)
            if job is None:
                return None
            return {
                'job_id': job.job_id,
                'status': job.status.value,
                'progresso': job.progresso,
                'imagens_geradas': job.imagens_geradas,
                'imagens_total': job.quantidade,
                'mensagem': job.mensagem,
                'erro': job.erro,
                'imagens_salvas': job.imagens_salvas,
                'pasta_destino': job.pasta_destino,
            }

    def cancelar_job(self, job_id: str) -> bool:
        with self._lock:
            job = self._jobs.get(job_id)
            if job is None:
                return False
            if job.status not in (JobStatus.PENDENTE, JobStatus.EM_PROGRESSO):
                return False
            job.cancel_event.set()
            return True


job_manager = _JobManager()
