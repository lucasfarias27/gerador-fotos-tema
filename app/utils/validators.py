def validar_arquivos(files, max_files: int, allowed_extensions: set) -> str | None:
    if not files or all(f.filename == '' for f in files):
        return 'Nenhuma foto enviada.'
    if len(files) > max_files:
        return f'Máximo de {max_files} fotos permitido.'
    for f in files:
        ext = f.filename.rsplit('.', 1)[-1].lower() if '.' in f.filename else ''
        if ext not in allowed_extensions:
            return f'Formato "{ext}" não suportado. Use: {", ".join(allowed_extensions)}.'
    return None


def validar_tema(tema: str, themes: dict) -> str | None:
    if not tema:
        return 'Selecione um tema.'
    if tema not in themes:
        return f'Tema "{tema}" inválido.'
    return None


def validar_quantidade(quantidade_str: str) -> tuple[str | None, int]:
    try:
        quantidade = int(quantidade_str)
        if quantidade < 1 or quantidade > 10:
            return 'A quantidade deve ser entre 1 e 10.', 0
        return None, quantidade
    except (ValueError, TypeError):
        return 'Quantidade inválida.', 0
