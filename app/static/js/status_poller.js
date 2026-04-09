/* ===== status_poller.js — Polls job status and updates UI ===== */

let pollingInterval = null;

function iniciarPolling(jobId) {
    pollingInterval = setInterval(() => verificarStatus(jobId), 2000);
}

async function verificarStatus(jobId) {
    try {
        const res = await fetch(`/api/status-job/${jobId}`);
        if (!res.ok) return;
        const data = await res.json();

        const progressBar = document.getElementById('progress-bar');
        const mensagem = document.getElementById('mensagem-status');

        progressBar.style.width = data.progresso + '%';
        mensagem.textContent = data.mensagem || '';

        if (data.status === 'concluido') {
            pararPolling();
            window.location.href = `/resultado?job_id=${jobId}`;
        } else if (data.status === 'erro') {
            pararPolling();
            mostrarErro(data.erro || 'Ocorreu um erro durante a geração.');
        } else if (data.status === 'cancelado') {
            pararPolling();
            document.getElementById('section-progresso').style.display = 'none';
            document.getElementById('btn-gerar').disabled = false;
            mensagem.textContent = 'Geração cancelada.';
        }
    } catch (e) {
        // Network hiccup — keep polling
    }
}

function pararPolling() {
    if (pollingInterval) {
        clearInterval(pollingInterval);
        pollingInterval = null;
    }
}
