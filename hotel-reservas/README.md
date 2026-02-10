# Sistema de Reservas de Hotel - Flask & PostgreSQL

Sistema web completo para gerenciar reservas de hotel, desenvolvido com **Python Flask** e **PostgreSQL**.

## 🎯 Funcionalidades

- ✅ **Gestão de Hóspedes**: Cadastro, edição, visualização e exclusão
- ✅ **Gestão de Quartos**: Controle de quartos, tipos, preços e disponibilidade
- ✅ **Sistema de Reservas**: Criação, cancelamento e finalização de reservas
- ✅ **Dashboard**: Visualização rápida de estatísticas
- ✅ **Busca e Filtros**: Filtros avançados para facilitar a busca
- ✅ **Cálculo Automático**: Cálculo automático de valor total das reservas
- ✅ **Verificação de Disponibilidade**: Valida conflitos de data

## 📋 Requisitos

- Python 3.8+
- PostgreSQL 12+
- pip (gerenciador de pacotes Python)

## 🚀 Instalação

### 1. Criar ambiente virtual
```bash
cd /home/tiago/Documentos/SQL/hotel-reservas
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

### 2. Instalar dependências
```bash
pip install -r requirements.txt
```

### 3. Configurar banco de dados

#### Opção A: PostgreSQL (Recomendado)
```bash
# Criar banco de dados
psql -U postgres -c "CREATE DATABASE hotel_reservas;"

# Editar o arquivo .env com suas credenciais
cat > .env << EOF
DATABASE_URL=postgresql://seu_usuario:sua_senha@localhost:5432/hotel_reservas
SECRET_KEY=sua_chave_secreta_aqui
FLASK_ENV=development
FLASK_DEBUG=True
FLASK_PORT=5000
EOF
```

#### Opção B: SQLite (Para testes rápidos)
```bash
cat > .env << EOF
DATABASE_URL=sqlite:///hotel.db
SECRET_KEY=dev-key-change-later
FLASK_ENV=development
FLASK_DEBUG=True
FLASK_PORT=5000
EOF
```

### 4. Executar a aplicação
```bash
python app.py
```

A aplicação estará disponível em: **http://127.0.0.1:5000**

## 📁 Estrutura do Projeto

```
hotel-reservas/
├── app/
│   ├── __init__.py           # Factory da aplicação
│   ├── models.py             # Modelos SQLAlchemy
│   ├── routes.py             # Rotas e lógica
│   ├── templates/            # Templates HTML
│   │   ├── base.html         # Template base
│   │   ├── index.html        # Dashboard
│   │   ├── hospedes/
│   │   │   ├── listar.html
│   │   │   ├── novo.html
│   │   │   ├── editar.html
│   │   │   └── visualizar.html
│   │   ├── quartos/
│   │   │   ├── listar.html
│   │   │   ├── novo.html
│   │   │   └── editar.html
│   │   └── reservas/
│   │       ├── listar.html
│   │       ├── nova.html
│   │       └── visualizar.html
│   └── static/               # Arquivos estáticos (CSS, JS)
├── app.py                    # Arquivo principal
├── config.py                 # Configurações
├── requirements.txt          # Dependências
├── .env                      # Variáveis de ambiente
└── README.md                 # Este arquivo
```

## 🗄️ Modelos de Dados

### Hospede
- `id`: Identificador único
- `nome`: Nome completo
- `telefone`: Número de telefone
- `email`: Endereço de e-mail
- `data_cadastro`: Data de cadastro

### Quarto
- `id`: Identificador único
- `numero`: Número do quarto
- `tipo`: Tipo (Solteiro, Casal, Suite, etc)
- `preco`: Preço da diária em R$
- `status`: LIVRE ou OCUPADO
- `descricao`: Descrição adicional
- `data_criacao`: Data de criação

### Reserva
- `id`: Identificador único
- `id_hospede`: Referência ao hóspede
- `id_quarto`: Referência ao quarto
- `entrada`: Data de entrada
- `saida`: Data de saída
- `total`: Valor total da reserva
- `status`: ATIVA, CANCELADA ou FINALIZADA
- `data_criacao`: Data de criação

## 🔧 Endpoints Principais

### Hóspedes
- `GET /hospedes` - Listar hóspedes
- `GET /hospedes/novo` - Formulário novo
- `POST /hospedes/novo` - Criar hóspede
- `GET /hospedes/<id>/editar` - Formulário editar
- `POST /hospedes/<id>/editar` - Atualizar hóspede
- `POST /hospedes/<id>/deletar` - Deletar hóspede
- `GET /hospedes/<id>` - Visualizar hóspede

### Quartos
- `GET /quartos` - Listar quartos
- `GET /quartos/novo` - Formulário novo
- `POST /quartos/novo` - Criar quarto
- `GET /quartos/<id>/editar` - Formulário editar
- `POST /quartos/<id>/editar` - Atualizar quarto
- `POST /quartos/<id>/deletar` - Deletar quarto

### Reservas
- `GET /reservas` - Listar reservas
- `GET /reservas/nova` - Formulário nova
- `POST /reservas/nova` - Criar reserva
- `GET /reservas/<id>` - Visualizar reserva
- `POST /reservas/<id>/cancelar` - Cancelar reserva
- `POST /reservas/<id>/finalizar` - Finalizar reserva
- `GET /reservas/api/quartos-disponiveis` - API para quartos disponíveis

## 📊 Scripts SQL

O banco de dados pode ser inicializado com o script em `/home/tiago/Documentos/SQL/script.sql` que contém:
- Criação de tabelas
- Funções para cálculo automático
- Triggers para atualização de status
- Procedures para operações complexas
- Dados de teste

## 🔒 Segurança

- Use uma chave `SECRET_KEY` forte em produção
- Nunca commite o arquivo `.env` com credenciais
- Use HTTPS em produção
- Configure CORS se necessário

## 🐛 Troubleshooting

### Erro de conexão com PostgreSQL
```bash
# Verifique se PostgreSQL está rodando
psql -U postgres

# Verifique a conexão no .env
DATABASE_URL=postgresql://usuario:senha@localhost:5432/hotel_reservas
```

### Erro ao importar módulos
```bash
# Garanta que está no ambiente virtual
source venv/bin/activate

# Reinstale dependências
pip install -r requirements.txt --force-reinstall
```

### Database locked (SQLite)
Feche outras conexões com o banco de dados e tente novamente.

## 📝 Exemplos de Uso

### 1. Cadastrar um novo hóspede
1. Clique em "👥 Hóspedes"
2. Clique em "➕ Novo Hóspede"
3. Preencha os dados
4. Clique em "Salvar"

### 2. Criar uma reserva
1. Clique em "📅 Reservas"
2. Clique em "➕ Nova Reserva"
3. Selecione hóspede e quarto
4. Escolha datas de entrada e saída
5. O sistema calcula automaticamente o total
6. Clique em "Criar Reserva"

### 3. Cancelar uma reserva
1. Acesse a lista de reservas
2. Localize a reserva desejada
3. Clique em "Cancelar"
4. Confirme a ação

## 🔄 Manutenção

### Backup do banco de dados
```bash
pg_dump -U postgres hotel_reservas > backup.sql
```

### Restaurar banco de dados
```bash
psql -U postgres hotel_reservas < backup.sql
```

## 📄 Licença

Este projeto é fornecido como exemplo educacional.

## 👨‍💻 Autor

Sistema desenvolvido com Flask e SQLAlchemy - 2026

---

**Desenvolvido com ❤️ para gerenciar suas reservas!**
