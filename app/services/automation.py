import os
import time
import random
from app.services.prompt_builder import construir_prompt

# -----------------------------------------------------------------------
# Centralize all Gemini selectors here for easy maintenance.
# If Gemini updates its UI, only this dict needs to change.
# -----------------------------------------------------------------------
SELECTORS = {
    # Text input area
    'input_area': (
        'div.ql-editor[contenteditable="true"], '
        'rich-textarea div[contenteditable="true"], '
        'div[contenteditable="true"][data-placeholder]'
    ),
    # Upload/attach button — Gemini changes these often; listed from most to least specific
    'upload_button': (
        'button[aria-label="Upload image"], '
        'button[aria-label="Adicionar imagem"], '
        'button[aria-label="Add image"], '
        'button[aria-label="Upload file"], '
        'button[aria-label="Attach files"], '
        'button[aria-label="Adicionar arquivos"], '
        'button[aria-label*="upload" i], '
        'button[aria-label*="attach" i], '
        'button[aria-label*="image" i], '
        'button[aria-label*="imagem" i], '
        'button[aria-label*="foto" i], '
        'button[data-tooltip*="image" i], '
        'button[data-tooltip*="imagem" i], '
        'button[jsname="QzBQNd"], '
        'input[type="file"]'
    ),
    # Expand/add button that may reveal an upload menu ("+", "Add content", etc.)
    'expand_button': (
        'button[aria-label="Add to conversation"], '
        'button[aria-label="Adicionar à conversa"], '
        'button[aria-label*="add content" i], '
        'button[aria-label*="adicionar conteúdo" i], '
        'button[aria-label*="more options" i], '
        'button[aria-label*="mais opções" i], '
        'button[jsname="r3TZHf"], '
        'button[data-test-id="add-content-button"]'
    ),
    # Menu items that appear after clicking expand button
    'upload_menu_item': (
        '[role="menuitem"][aria-label*="upload" i], '
        '[role="menuitem"][aria-label*="image" i], '
        '[role="menuitem"][aria-label*="imagem" i], '
        '[role="menuitem"][aria-label*="computer" i], '
        '[role="menuitem"][aria-label*="computador" i], '
        '[role="menuitem"][aria-label*="foto" i], '
        '[role="option"][aria-label*="upload" i], '
        '[role="option"][aria-label*="image" i]'
    ),
    # Send button
    'send_button': (
        'button[aria-label="Send message"], '
        'button[aria-label="Enviar mensagem"], '
        'button[aria-label="Submit"], '
        'button.send-button, '
        'button[jsname="Qxtp9"], '
        'mat-icon-button[aria-label*="send" i]'
    ),
    'generated_image': (
        'img-gen-image img, '
        'div.image-gen-response img, '
        'model-response img[src], '
        '.response-content img[src]'
    ),
    'login_check': (
        'div.ql-editor, '
        'rich-textarea, '
        'div[contenteditable="true"]'
    ),
}

GEMINI_URL = 'https://gemini.google.com/app'

# Dedicated profile folder stored inside the project — never conflicts with open Chrome.
_PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
PROFILE_PATH = os.path.join(_PROJECT_ROOT, 'chrome_profile')


class GeminiAutomation:

    def executar(self, job, tema_config: dict, atualizar_progresso_fn, imagem_salva_fn):
        from playwright.sync_api import sync_playwright

        os.makedirs(PROFILE_PATH, exist_ok=True)

        with sync_playwright() as p:
            browser = p.chromium.launch_persistent_context(
                user_data_dir=PROFILE_PATH,
                headless=False,
                args=['--start-maximized', '--disable-blink-features=AutomationControlled'],
                ignore_default_args=['--enable-automation'],
            )

            page = browser.new_page()

            try:
                # Check login before starting
                page.goto(GEMINI_URL, wait_until='domcontentloaded', timeout=30000)
                page.wait_for_timeout(3000)

                if not self._esta_logado(page):
                    raise Exception(
                        'Você precisa fazer login no Google na janela que abriu. '
                        'Faça login e depois clique em Gerar novamente.'
                    )

                for i in range(job.quantidade):
                    if job.cancel_event.is_set():
                        break

                    atualizar_progresso_fn(i, job.quantidade, f'Gerando imagem {i + 1} de {job.quantidade}...')

                    foto_path = job.fotos_paths[i % len(job.fotos_paths)]
                    prompt_text = construir_prompt(tema_config, i + 1, job.quantidade)

                    self._nova_conversa(page)
                    self._anexar_imagem(page, foto_path)
                    self._digitar_e_enviar(page, prompt_text)
                    self._aguardar_geracao(page)

                    caminho_salvo = self._baixar_imagem(page, job.pasta_destino, i + 1)
                    if caminho_salvo:
                        imagem_salva_fn(caminho_salvo)

                    atualizar_progresso_fn(i + 1, job.quantidade)

                    # Human-like delay between generations
                    if i < job.quantidade - 1 and not job.cancel_event.is_set():
                        time.sleep(random.uniform(2.5, 4.0))

            finally:
                browser.close()

    def _esta_logado(self, page) -> bool:
        try:
            page.wait_for_selector(SELECTORS['input_area'], timeout=8000)
            return True
        except Exception:
            return False

    def _nova_conversa(self, page):
        try:
            page.goto(GEMINI_URL, wait_until='domcontentloaded', timeout=20000)
            page.wait_for_selector(SELECTORS['input_area'], timeout=15000)
            page.wait_for_timeout(1500)
        except Exception:
            # Fallback: just reload
            page.reload(wait_until='domcontentloaded')
            page.wait_for_timeout(2000)

    def _anexar_imagem(self, page, foto_path: str):
        # Strategy 1: set files directly on any file input (Playwright can target hidden inputs)
        try:
            if page.locator('input[type="file"]').count() > 0:
                page.locator('input[type="file"]').first.set_input_files(foto_path)
                page.wait_for_timeout(2000)
                return
        except Exception:
            pass

        # Strategy 2: click expand/add button to reveal upload menu, then find upload item
        for expand_sel in SELECTORS['expand_button'].split(', '):
            expand_sel = expand_sel.strip()
            try:
                btn = page.locator(expand_sel).first
                if btn.count() == 0:
                    continue
                btn.wait_for(state='visible', timeout=2000)
                btn.click()
                page.wait_for_timeout(1000)
                for item_sel in SELECTORS['upload_menu_item'].split(', '):
                    item_sel = item_sel.strip()
                    try:
                        item = page.locator(item_sel).first
                        if item.count() == 0:
                            continue
                        item.wait_for(state='visible', timeout=2000)
                        with page.expect_file_chooser(timeout=8000) as fc_info:
                            item.click()
                        fc_info.value.set_files(foto_path)
                        page.wait_for_timeout(2000)
                        return
                    except Exception:
                        continue
                # Menu opened but no item matched — close it and try next strategy
                page.keyboard.press('Escape')
                page.wait_for_timeout(500)
            except Exception:
                continue

        # Strategy 3: click upload button directly and handle file chooser dialog
        for selector in SELECTORS['upload_button'].split(', '):
            selector = selector.strip()
            try:
                btn = page.locator(selector).first
                if btn.count() == 0:
                    continue
                btn.wait_for(state='visible', timeout=3000)
                with page.expect_file_chooser(timeout=8000) as fc_info:
                    btn.click()
                fc_info.value.set_files(foto_path)
                page.wait_for_timeout(2000)
                return
            except Exception:
                continue

        # Strategy 4: force-reveal hidden file inputs via JS, then set files
        try:
            page.evaluate("""
                () => {
                    document.querySelectorAll('input[type="file"]').forEach(el => {
                        el.removeAttribute('hidden');
                        el.style.cssText = (
                            'display:block!important;visibility:visible!important;'
                            'opacity:1!important;position:fixed!important;'
                            'top:0!important;left:0!important;'
                            'width:1px!important;height:1px!important;z-index:99999!important;'
                        );
                    });
                }
            """)
            page.wait_for_timeout(500)
            if page.locator('input[type="file"]').count() > 0:
                page.locator('input[type="file"]').first.set_input_files(foto_path)
                page.wait_for_timeout(2000)
                return
        except Exception:
            pass

        # Strategy 5: copy image to Windows clipboard via PowerShell, then Ctrl+V into input
        if self._colar_via_clipboard_windows(page, foto_path):
            return

        # Debug dump — printed to console to help identify correct selectors
        try:
            debug_info = page.evaluate("""
                () => {
                    const out = [];
                    document.querySelectorAll('button').forEach((btn, i) => {
                        const label = btn.getAttribute('aria-label') || '';
                        const jsname = btn.getAttribute('jsname') || '';
                        const tid = btn.getAttribute('data-test-id') || '';
                        const txt = btn.textContent?.trim()?.slice(0, 40) || '';
                        if (label || jsname || tid)
                            out.push(`BTN[${i}] label="${label}" jsname="${jsname}" tid="${tid}" txt="${txt}"`);
                    });
                    document.querySelectorAll('input').forEach((inp, i) => {
                        out.push(`INPUT[${i}] type="${inp.type}" name="${inp.name}" id="${inp.id}"`);
                    });
                    return out.slice(0, 60).join('\\n');
                }
            """)
            print('[automation] ===== DEBUG: elementos na página =====')
            print(debug_info)
            print('[automation] =====================================')
        except Exception as de:
            print(f'[automation] Debug dump falhou: {de}')

        raise Exception(
            'Não foi possível encontrar o botão de upload de imagem no Gemini. '
            'A interface pode ter mudado. Verifique os seletores em automation.py.'
        )

    def _colar_via_clipboard_windows(self, page, foto_path: str) -> bool:
        """Copy image to Windows clipboard via PowerShell, then paste into Gemini input."""
        import subprocess
        foto_path_win = foto_path.replace('/', '\\')
        ps_script = (
            'Add-Type -AssemblyName System.Windows.Forms; '
            'Add-Type -AssemblyName System.Drawing; '
            f'[System.Windows.Forms.Clipboard]::SetImage('
            f'[System.Drawing.Image]::FromFile(\'{foto_path_win}\'))'
        )
        try:
            result = subprocess.run(
                ['powershell', '-NoProfile', '-Command', ps_script],
                capture_output=True, timeout=15,
            )
            if result.returncode != 0:
                print(f'[automation] PowerShell clipboard error: {result.stderr.decode(errors="ignore")}')
                return False

            # Focus input and paste
            input_area = page.locator(SELECTORS['input_area']).first
            input_area.wait_for(state='visible', timeout=8000)
            input_area.click()
            page.wait_for_timeout(600)
            page.keyboard.press('Control+v')
            page.wait_for_timeout(3000)
            return True
        except Exception as e:
            print(f'[automation] Clipboard paste falhou: {e}')
            return False

    def _digitar_e_enviar(self, page, prompt_text: str):
        input_area = page.locator(SELECTORS['input_area']).first
        input_area.wait_for(state='visible', timeout=15000)
        input_area.click()
        page.wait_for_timeout(500)
        input_area.fill(prompt_text)
        page.wait_for_timeout(random.uniform(400, 800))

        # Try send button first, fallback to Enter key
        sent = False
        for selector in SELECTORS['send_button'].split(', '):
            selector = selector.strip()
            try:
                btn = page.locator(selector).first
                if btn.count() == 0:
                    continue
                btn.wait_for(state='visible', timeout=3000)
                btn.click()
                sent = True
                break
            except Exception:
                continue

        if not sent:
            # Fallback: press Enter
            input_area.press('Enter')

    def _aguardar_geracao(self, page):
        # Wait for generated image to appear (up to 3 minutes)
        try:
            page.wait_for_selector(SELECTORS['generated_image'], timeout=180000)
        except Exception:
            raise Exception(
                'Tempo esgotado aguardando a geração da imagem. '
                'O Gemini pode estar lento ou o seletor mudou.'
            )
        # Extra buffer to ensure image is fully loaded
        page.wait_for_timeout(2000)

    def _baixar_imagem(self, page, pasta_destino: str, numero: int) -> str | None:
        try:
            img = page.locator(SELECTORS['generated_image']).last
            src = img.get_attribute('src')

            if not src:
                return None

            filename = f'imagem_{numero:03d}.jpg'
            filepath = os.path.join(pasta_destino, filename)

            # Use Playwright's authenticated request context to fetch the image
            response = page.context.request.get(src)
            if response.ok:
                with open(filepath, 'wb') as f:
                    f.write(response.body())
                return filepath
            else:
                # Fallback: screenshot just the image element
                img.screenshot(path=filepath)
                return filepath

        except Exception as e:
            print(f'[automation] Erro ao baixar imagem {numero}: {e}')
            return None
