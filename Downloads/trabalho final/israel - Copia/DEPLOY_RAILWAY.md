# Deploy na Railway (3 serviços)

Este projeto tem 3 aplicações Flask:
- `ms_usuarios.py`
- `ms_pedidos.py`
- `frontend.py`

Na Railway, crie **3 Web Services** apontando para o mesmo repositório/pasta.

## 1) Pré-requisitos

1. Subir o projeto para um repositório no GitHub.
2. Entrar na Railway e conectar a conta GitHub.

## 2) Configuração dos serviços

Use os mesmos comandos de build para os 3 serviços:

- **Build Command**:

```bash
pip install -r requirements.txt
```

### Serviço 1: usuários
- **Start Command**:

```bash
gunicorn -b 0.0.0.0:$PORT ms_usuarios:app
```

### Serviço 2: pedidos
- **Start Command**:

```bash
gunicorn -b 0.0.0.0:$PORT ms_pedidos:app
```

### Serviço 3: frontend
- **Start Command**:

```bash
gunicorn -b 0.0.0.0:$PORT frontend:app
```

## 3) Variáveis de ambiente no serviço `frontend`

No frontend, configure:

- `URL_USUARIOS=https://<url-publica-do-servico-usuarios>`
- `URL_PEDIDOS=https://<url-publica-do-servico-pedidos>`
- `FLASK_SECRET_KEY=<uma-chave-forte-opcional>`

> O código já tem fallback para localhost no desenvolvimento, então local continua funcionando.

## 4) Publicação

1. Faça deploy dos serviços de `usuarios` e `pedidos`.
2. Copie as URLs públicas deles.
3. Configure as variáveis no `frontend`.
4. Faça redeploy do `frontend`.

## 5) Observação importante

Os dados estão em memória (listas Python). Se a aplicação reiniciar, os dados serão perdidos.
Para produção real, o próximo passo é usar PostgreSQL.
