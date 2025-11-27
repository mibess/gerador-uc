# Gerador de Código UC

Aplicação web e API que automatiza a geração do identificador da Unidade Consumidora (UC) seguindo o padrão definido pela REN 1.095/2024 da ANEEL. O projeto expõe uma interface responsiva em Flask, reaproveita o cálculo de dígitos verificadores no backend e disponibiliza também um endpoint JSON para integrações.

## Visão geral

  - Gera sequências de 15 dígitos, calcula os dígitos verificadores N2 e N1 e devolve o código já formatado.
  - Interface única em `templates/index.html` com dropdown filtrável e alertas Toast.
  - API sem recarregamento via `fetch` com rota `/api/gerar-uc`.
  - Assets servidos a partir de `static/` para permitir cache via Nginx.
  - Deploy containerizado com Gunicorn atrás de um proxy reverso Nginx.

## Stack principal

  - Python 3.10 + Flask 3.1 (blueprint único em `app.py`).
  - Template engine Jinja2 + Tailwind CDN para o front-end.
  - Gunicorn como WSGI server em produção.
  - Nginx (arquivo `nginx.conf`) fazendo proxy e servindo estáticos.
  - Docker e Docker Compose 3.8 para empacotamento.

## Estrutura do projeto

```
.
|-- app.py                # rotas Flask, lógica de geração e API
|-- distribuidoras.py     # lista completa (nome, código) usada em memória
|-- templates/
|   \-- index.html        # UI com dropdown customizado, alertas e fetch
|-- static/               # imagens e favicons mantidos fora do pacote
|-- requirements.txt      # dependências de runtime e testes
|-- Dockerfile            # imagem Python + Gunicorn
|-- docker-compose.yml    # orquestra app (Gunicorn) e Nginx
|-- nginx.conf            # reverse proxy + alias /static
\-- replace_script.py     # utilitário para sobrescrever o script do dropdown
```

## Pré-requisitos

  - Python 3.10+
  - Pip
  - (Opcional) Docker 24+ e Docker Compose Plugin

## Execução local (sem Docker)

1.  Crie e ative um ambiente virtual.
    ```bash
    python -m venv .venv
    .\.venv\Scripts\activate
    ```
2.  Instale as dependências.
    ```bash
    pip install -r requirements.txt
    ```
3.  Inicie a aplicação Flask.
    ```bash
    python app.py
    ```
4.  Acesse `http://127.0.0.1:5000` e selecione a distribuidora para gerar o código.

> Dica: exporte `FLASK_ENV=development` para recarregar automaticamente durante o desenvolvimento.

## Execução com Docker Compose

1.  Construa as imagens.
    ```bash
    docker compose build
    ```
2.  Suba os serviços (Gunicorn exposto ao Nginx).
    ```bash
    docker compose up
    ```
3.  Acesse `http://localhost:8095` (porta externa mapeada para o Nginx interno).

O volume nomeado `static_volume` compartilha `static/` entre os containers para preservar assets gerados.

## Endpoints

| Método | Rota | Descrição | Entrada | Resposta |
| :--- | :--- | :--- | :--- | :--- |
| GET | `/` | Renderiza o formulário web. | Query string opcional `distribuidora` (pré-seleção). | HTML |
| POST | `/` | Submete o formulário tradicional para gerar o código. | Campo `distribuidora` enviado via form. | HTML com resultado |
| POST | `/api/gerar-uc` | Endpoint JSON usado pelo front-end. | Body JSON `{"distribuidora": "059"}` ou form-data equivalente. | `200 OK` com `numero_uc`, `nome` etc |

Exemplo de integração:

```bash
curl -X POST http://localhost:5000/api/gerar-uc \
  -H "Content-Type: application/json" \
  -d "{\"distribuidora\": \"059\"}"
```

Resposta:

```json
{
  "numero_uc": "5.123.456.789.059-42",
  "distribuidora": "059",
  "nome": "LIGHT"
}
```

## Testes

Ainda não há suítes prontas, mas o projeto já inclui dependências de teste (`pytest`, `pytest-cov`, `pytest-mock`). Adicione seus testes em `tests/` e execute:

```bash
pytest --cov=app
```

## Scripts e manutenção

  - `distribuidoras.py`: mantenha a relação Nome/Código atualizada conforme publicações da ANEEL. `DISTRIBUIDORAS_ORDENADAS` é calculada em memória ao subir o app.
  - `replace_script.py`: utilitário para substituir o script do dropdown no template quando for necessário atualizar a implementação sem editar manually.
  - `static/`: imagens, favicons e ícones usados pela interface. Ao adicionar novos arquivos lembre-se do volume compartilhado no Docker Compose.

## Personalização

  - Ajuste estilos direto em `templates/index.html` (Tailwind via CDN evita build passos).
  - Se quiser automatizar seeds ou validar UC, extraia `calcular_dv` e `formatar_uc` para outro módulo e reimporte.
  - Para ambientes com TLS, adicione um novo bloco `server` no `nginx.conf` e monte certificados via volumes.

## Licença

Ainda não foi definida.