/* ===== main.js — Form logic, upload preview, form submission ===== */

let fotosEscolhidas = [];
let jobAtivo = null;

const dropZone = document.getElementById('drop-zone');
const inputFotos = document.getElementById('input-fotos');
const previewContainer = document.getElementById('preview-container');
const contadorFotos = document.getElementById('contador-fotos');
const btnGerar = document.getElementById('btn-gerar');
const btnPastaPadrao = document.getElementById('btn-pasta-padrao');
const inputPasta = document.getElementById('input-pasta');
const selectTema = document.getElementById('select-tema');
const inputQtd = document.getElementById('input-quantidade');
const erroGlobal = document.getElementById('erro-global');
const sectionProgresso = document.getElementById('section-progresso');
const btnCancelar = document.getElementById('btn-cancelar');

// ---- Load themes ----
async function carregarTemas() {
    try {
        const res = await fetch('/api/temas');
        const temas = await res.json();
        selectTema.innerHTML = '<option value="">Selecione um tema...</option>';
        temas.forEach(t => {
            const opt = document.createElement('option');
            opt.value = t.id;
            opt.textContent = t.label;
            selectTema.appendChild(opt);
        });
    } catch (e) {
        selectTema.innerHTML = '<option value="">Erro ao carregar temas</option>';
    }
}

// ---- Drop zone ----
dropZone.addEventListener('click', () => inputFotos.click());
dropZone.addEventListener('dragover', e => { e.preventDefault(); dropZone.classList.add('dragging'); });
dropZone.addEventListener('dragleave', () => dropZone.classList.remove('dragging'));
dropZone.addEventListener('drop', e => {
    e.preventDefault();
    dropZone.classList.remove('dragging');
    adicionarFotos(Array.from(e.dataTransfer.files));
});
inputFotos.addEventListener('change', () => {
    adicionarFotos(Array.from(inputFotos.files));
    inputFotos.value = '';
});

function adicionarFotos(novos) {
    const permitidos = ['image/jpeg', 'image/jpg', 'image/png', 'image/webp'];
    novos.forEach(f => {
        if (!permitidos.includes(f.type)) return;
        if (fotosEscolhidas.length >= 5) return;
        fotosEscolhidas.push(f);
    });
    renderizarPreviews();
    atualizarBotao();
}

function removerFoto(index) {
    fotosEscolhidas.splice(index, 1);
    renderizarPreviews();
    atualizarBotao();
}

function renderizarPreviews() {
    if (fotosEscolhidas.length === 0) {
        previewContainer.style.display = 'none';
        contadorFotos.style.display = 'none';
        return;
    }

    previewContainer.style.display = 'flex';
    contadorFotos.style.display = 'block';
    contadorFotos.textContent = `${fotosEscolhidas.length} de 5 foto(s) selecionada(s)`;

    previewContainer.innerHTML = '';
    fotosEscolhidas.forEach((f, i) => {
        const div = document.createElement('div');
        div.className = 'preview-item';

        const img = document.createElement('img');
        img.src = URL.createObjectURL(f);
        img.alt = f.name;

        const btn = document.createElement('button');
        btn.className = 'preview-remove';
        btn.type = 'button';
        btn.innerHTML = '&times;';
        btn.addEventListener('click', () => removerFoto(i));

        div.appendChild(img);
        div.appendChild(btn);
        previewContainer.appendChild(div);
    });
}

// ---- Validation & button state ----
function atualizarBotao() {
    const valido = fotosEscolhidas.length >= 1
        && selectTema.value !== ''
        && inputPasta.value.trim() !== ''
        && inputQtd.value >= 1;
    btnGerar.disabled = !valido;
}

selectTema.addEventListener('change', atualizarBotao);
inputPasta.addEventListener('input', atualizarBotao);
inputQtd.addEventListener('input', atualizarBotao);

// ---- Escolher pasta (abre janela nativa do SO) ----
btnPastaPadrao.addEventListener('click', async () => {
    btnPastaPadrao.disabled = true;
    btnPastaPadrao.textContent = 'Abrindo...';
    try {
        const res = await fetch('/api/escolher-pasta');
        const data = await res.json();
        if (data.pasta) {
            inputPasta.value = data.pasta;
            atualizarBotao();
        }
    } catch (e) {
        console.error('Erro ao abrir seletor de pasta:', e);
    } finally {
        btnPastaPadrao.disabled = false;
        btnPastaPadrao.textContent = 'Escolher pasta';
    }
});

// ---- Form submission ----
document.getElementById('form-geracao').addEventListener('submit', async e => {
    e.preventDefault();
    erroGlobal.style.display = 'none';

    const formData = new FormData();
    fotosEscolhidas.forEach(f => formData.append('fotos[]', f));
    formData.append('tema', selectTema.value);
    formData.append('quantidade', inputQtd.value);
    formData.append('pasta_destino', inputPasta.value.trim());

    btnGerar.disabled = true;
    sectionProgresso.style.display = 'block';
    document.getElementById('mensagem-status').textContent = 'Enviando fotos...';
    document.getElementById('progress-bar').style.width = '0%';

    try {
        const res = await fetch('/api/iniciar-geracao', { method: 'POST', body: formData });
        const data = await res.json();

        if (!res.ok || data.erro) {
            mostrarErro(data.erro || 'Erro ao iniciar geração.');
            return;
        }

        jobAtivo = data.job_id;
        iniciarPolling(jobAtivo);
    } catch (err) {
        mostrarErro('Erro de conexão: ' + err.message);
    }
});

// ---- Cancel ----
btnCancelar.addEventListener('click', async () => {
    if (!jobAtivo) return;
    await fetch(`/api/cancelar-job/${jobAtivo}`, { method: 'POST' });
});

// ---- Helpers ----
function mostrarErro(msg) {
    erroGlobal.textContent = msg;
    erroGlobal.style.display = 'block';
    sectionProgresso.style.display = 'none';
    btnGerar.disabled = false;
    window.scrollTo(0, 0);
}

carregarTemas();
