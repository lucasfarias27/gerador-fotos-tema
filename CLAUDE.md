# gerador-fotos-tema

## Repositório GitHub

Este projeto está publicado em: https://github.com/lucasfarias27/gerador-fotos-tema

## Sincronização automática com GitHub

Todo arquivo editado ou criado neste projeto é automaticamente sincronizado com o repositório no GitHub via hook do Claude Code configurado em `.claude/settings.json`.

O hook é acionado após cada uso das ferramentas `Edit` ou `Write` e executa:
```bash
git add -A
git commit -m "auto: sync changes"   # só se houver mudanças
git push
```

### Regras de commit manual

Quando criar commits manualmente (não automáticos), use mensagens descritivas seguindo o padrão:
- `feat: descrição` — nova funcionalidade
- `fix: descrição` — correção de bug
- `refactor: descrição` — refatoração sem mudança de comportamento
- `chore: descrição` — ajustes gerais

## Arquivos ignorados pelo git

Os seguintes itens **não** são versionados (definido em `.gitignore`):
- `__pycache__/`, `*.pyc`
- `.env`, `.venv`, `venv/`
- `chrome_profile/` — dados sensíveis do navegador
- `downloads/` — arquivos gerados em runtime
- `app/static/uploads/` — uploads de usuários

## Estrutura do projeto

```
gerador-fotos-tema/
├── app/
│   ├── routes/       # Rotas Flask (main.py, api.py)
│   ├── services/     # Lógica de negócio (automation, job_manager, prompt_builder)
│   ├── static/       # CSS, JS
│   ├── templates/    # HTML (base, index, resultado)
│   └── utils/        # file_handler, validators
├── config.py         # Configurações da aplicação
├── requirements.txt
└── run.py            # Entry point (Flask dev server na porta 5000)
```
