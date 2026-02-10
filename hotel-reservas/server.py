#!/usr/bin/env python3
"""
Sistema de Reservas de Hotel - Versão Simplificada
Usando apenas biblioteca padrão Python (sem dependências externas)
"""

import http.server
import socketserver
import json
import sqlite3
import os
from datetime import datetime
from urllib.parse import parse_qs, urlparse
import threading
import time

# Configurações
HOST = '127.0.0.1'
PORT = 5000
DB_FILE = 'hotel.db'

class HotelDatabase:
    """Gerenciador de banco de dados SQLite"""
    
    def __init__(self, db_file=DB_FILE):
        self.db_file = db_file
        self.init_db()
    
    def get_connection(self):
        """Obter conexão com banco de dados"""
        conn = sqlite3.connect(self.db_file)
        conn.row_factory = sqlite3.Row
        return conn
    
    def init_db(self):
        """Inicializar tabelas do banco de dados"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Tabela de hóspedes
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS hospedes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                telefone TEXT,
                email TEXT,
                data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tabela de quartos
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS quartos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                numero INTEGER UNIQUE NOT NULL,
                tipo TEXT NOT NULL,
                preco REAL NOT NULL,
                status TEXT DEFAULT 'LIVRE',
                descricao TEXT,
                data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tabela de reservas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS reservas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_hospede INTEGER NOT NULL,
                id_quarto INTEGER NOT NULL,
                entrada DATE NOT NULL,
                saida DATE NOT NULL,
                total REAL,
                status TEXT DEFAULT 'ATIVA',
                data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (id_hospede) REFERENCES hospedes(id),
                FOREIGN KEY (id_quarto) REFERENCES quartos(id)
            )
        ''')
        
        conn.commit()
        conn.close()

class HotelAPIHandler(http.server.SimpleHTTPRequestHandler):
    """Handler para requisições HTTP da API"""
    
    db = HotelDatabase()
    
    def do_GET(self):
        """Processar requisições GET"""
        parsed_url = urlparse(self.path)
        path = parsed_url.path
        
        # Rotas da API
        if path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(self.get_home_page().encode('utf-8'))
        
        elif path == '/api/hospedes':
            self.send_json_response(self.get_hospedes())
        
        elif path == '/api/quartos':
            self.send_json_response(self.get_quartos())
        
        elif path == '/api/reservas':
            self.send_json_response(self.get_reservas())
        
        elif path == '/api/dashboard':
            self.send_json_response(self.get_dashboard())
        
        else:
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'erro': 'Endpoint não encontrado'}).encode('utf-8'))
    
    def do_POST(self):
        """Processar requisições POST"""
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length).decode('utf-8')
        parsed_url = urlparse(self.path)
        path = parsed_url.path
        
        try:
            data = json.loads(body) if body else {}
        except:
            data = {}
        
        # Rotas POST
        if path == '/api/hospedes':
            resultado = self.criar_hospede(data)
            self.send_json_response(resultado)
        
        elif path == '/api/quartos':
            resultado = self.criar_quarto(data)
            self.send_json_response(resultado)
        
        elif path == '/api/reservas':
            resultado = self.criar_reserva(data)
            self.send_json_response(resultado)
        
        else:
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'erro': 'Endpoint não encontrado'}).encode('utf-8'))
    
    def send_json_response(self, data):
        """Enviar resposta JSON"""
        self.send_response(200)
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))
    
    def get_hospedes(self):
        """Buscar todos os hóspedes"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM hospedes ORDER BY data_cadastro DESC')
        hospedes = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return hospedes
    
    def get_quartos(self):
        """Buscar todos os quartos"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM quartos ORDER BY numero')
        quartos = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return quartos
    
    def get_reservas(self):
        """Buscar todas as reservas"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT r.*, h.nome, q.numero, q.preco 
            FROM reservas r
            JOIN hospedes h ON r.id_hospede = h.id
            JOIN quartos q ON r.id_quarto = q.id
            ORDER BY r.data_criacao DESC
        ''')
        reservas = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return reservas
    
    def get_dashboard(self):
        """Obter dados do dashboard"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) as count FROM hospedes')
        total_hospedes = cursor.fetchone()['count']
        
        cursor.execute('SELECT COUNT(*) as count FROM quartos')
        total_quartos = cursor.fetchone()['count']
        
        cursor.execute('SELECT COUNT(*) as count FROM reservas WHERE status = "ATIVA"')
        total_reservas_ativas = cursor.fetchone()['count']
        
        cursor.execute('SELECT COUNT(*) as count FROM quartos WHERE status = "LIVRE"')
        quartos_livres = cursor.fetchone()['count']
        
        conn.close()
        
        return {
            'total_hospedes': total_hospedes,
            'total_quartos': total_quartos,
            'total_reservas_ativas': total_reservas_ativas,
            'quartos_livres': quartos_livres,
            'taxa_ocupacao': round((total_quartos - quartos_livres) / total_quartos * 100, 1) if total_quartos > 0 else 0
        }
    
    def criar_hospede(self, data):
        """Criar novo hóspede"""
        try:
            nome = data.get('nome', '').strip()
            telefone = data.get('telefone', '').strip()
            email = data.get('email', '').strip()
            
            if not nome:
                return {'erro': 'Nome é obrigatório'}
            
            conn = self.db.get_connection()
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO hospedes (nome, telefone, email) VALUES (?, ?, ?)',
                (nome, telefone, email)
            )
            conn.commit()
            hospede_id = cursor.lastrowid
            conn.close()
            
            return {
                'sucesso': True,
                'mensagem': f'Hóspede {nome} cadastrado com sucesso!',
                'id': hospede_id
            }
        except Exception as e:
            return {'erro': str(e)}
    
    def criar_quarto(self, data):
        """Criar novo quarto"""
        try:
            numero = data.get('numero')
            tipo = data.get('tipo', '').strip()
            preco = float(data.get('preco', 0))
            descricao = data.get('descricao', '').strip()
            
            if not all([numero, tipo, preco > 0]):
                return {'erro': 'Número, tipo e preço são obrigatórios'}
            
            conn = self.db.get_connection()
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO quartos (numero, tipo, preco, descricao) VALUES (?, ?, ?, ?)',
                (numero, tipo, preco, descricao)
            )
            conn.commit()
            quarto_id = cursor.lastrowid
            conn.close()
            
            return {
                'sucesso': True,
                'mensagem': f'Quarto {numero} cadastrado com sucesso!',
                'id': quarto_id
            }
        except Exception as e:
            return {'erro': str(e)}
    
    def criar_reserva(self, data):
        """Criar nova reserva"""
        try:
            id_hospede = data.get('id_hospede')
            id_quarto = data.get('id_quarto')
            entrada = data.get('entrada')
            saida = data.get('saida')
            
            if not all([id_hospede, id_quarto, entrada, saida]):
                return {'erro': 'Todos os campos são obrigatórios'}
            
            if entrada >= saida:
                return {'erro': 'Data de saída deve ser após entrada'}
            
            conn = self.db.get_connection()
            cursor = conn.cursor()
            
            # Verificar disponibilidade
            cursor.execute('''
                SELECT COUNT(*) as count FROM reservas 
                WHERE id_quarto = ? AND status != "CANCELADA"
                AND ((entrada <= ? AND saida > ?) OR (entrada < ? AND saida >= ?) OR (entrada >= ? AND saida <= ?))
            ''', (id_quarto, entrada, entrada, saida, saida, entrada, saida))
            
            if cursor.fetchone()['count'] > 0:
                conn.close()
                return {'erro': 'Quarto indisponível para essas datas'}
            
            # Obter preço do quarto
            cursor.execute('SELECT preco FROM quartos WHERE id = ?', (id_quarto,))
            quarto = cursor.fetchone()
            if not quarto:
                conn.close()
                return {'erro': 'Quarto não encontrado'}
            
            # Calcular total
            d1 = datetime.strptime(entrada, '%Y-%m-%d')
            d2 = datetime.strptime(saida, '%Y-%m-%d')
            dias = (d2 - d1).days
            total = dias * quarto['preco']
            
            # Criar reserva
            cursor.execute(
                '''INSERT INTO reservas (id_hospede, id_quarto, entrada, saida, total, status) 
                   VALUES (?, ?, ?, ?, ?, ?)''',
                (id_hospede, id_quarto, entrada, saida, total, 'ATIVA')
            )
            conn.commit()
            reserva_id = cursor.lastrowid
            conn.close()
            
            return {
                'sucesso': True,
                'mensagem': 'Reserva criada com sucesso!',
                'id': reserva_id,
                'total': total
            }
        except Exception as e:
            return {'erro': str(e)}
    
    def get_home_page(self):
        """Retornar página HTML inicial"""
        return '''
        <!DOCTYPE html>
        <html lang="pt-BR">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Sistema de Reservas de Hotel</title>
            <style>
                * { margin: 0; padding: 0; box-sizing: border-box; }
                body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; display: flex; justify-content: center; align-items: center; }
                .container { background: white; border-radius: 10px; box-shadow: 0 20px 60px rgba(0,0,0,0.3); width: 90%; max-width: 1000px; padding: 40px; }
                h1 { color: #333; margin-bottom: 10px; }
                .subtitle { color: #666; margin-bottom: 30px; }
                .stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin: 30px 0; }
                .stat-card { background: #f8f9fa; padding: 20px; border-radius: 8px; text-align: center; border-left: 4px solid #667eea; }
                .stat-card h3 { color: #667eea; margin-bottom: 10px; }
                .stat-card .number { font-size: 32px; font-weight: bold; color: #333; }
                .actions { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 15px; margin: 30px 0; }
                button { background: #667eea; color: white; border: none; padding: 12px 20px; border-radius: 5px; cursor: pointer; font-size: 14px; font-weight: 600; transition: background 0.3s; }
                button:hover { background: #764ba2; }
                .api-info { background: #e8f4f8; padding: 15px; border-radius: 5px; margin-top: 30px; }
                .api-info code { background: #f0f0f0; padding: 2px 6px; border-radius: 3px; font-family: monospace; }
                .loading { display: none; color: #667eea; margin: 10px 0; }
                .message { padding: 12px; margin: 10px 0; border-radius: 5px; }
                .success { background: #d4edda; color: #155724; border: 1px solid #c3e6cb; }
                .error { background: #f8d7da; color: #721c24; border: 1px solid #f5c6cb; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🏨 Sistema de Reservas de Hotel</h1>
                <p class="subtitle">Versão Simplificada com API REST</p>
                
                <div class="stats" id="stats">
                    <div class="stat-card">
                        <h3>Hóspedes</h3>
                        <div class="number" id="hospedes">-</div>
                    </div>
                    <div class="stat-card">
                        <h3>Quartos</h3>
                        <div class="number" id="quartos">-</div>
                    </div>
                    <div class="stat-card">
                        <h3>Quartos Livres</h3>
                        <div class="number" id="livres">-</div>
                    </div>
                    <div class="stat-card">
                        <h3>Reservas Ativas</h3>
                        <div class="number" id="reservas">-</div>
                    </div>
                </div>
                
                <div class="actions">
                    <button onclick="criarHospede()">➕ Novo Hóspede</button>
                    <button onclick="criarQuarto()">➕ Novo Quarto</button>
                    <button onclick="criarReserva()">➕ Nova Reserva</button>
                    <button onclick="listarDados()">📋 Listar Dados</button>
                </div>
                
                <div id="message"></div>
                <div class="loading" id="loading">⏳ Carregando...</div>
                <div id="output" style="background: #f5f5f5; padding: 15px; border-radius: 5px; max-height: 300px; overflow-y: auto; margin-top: 20px; display: none;"></div>
                
                <div class="api-info">
                    <h3>📡 API REST Disponível</h3>
                    <p>GET <code>/api/dashboard</code> - Estatísticas do sistema</p>
                    <p>GET <code>/api/hospedes</code> - Listar hóspedes</p>
                    <p>GET <code>/api/quartos</code> - Listar quartos</p>
                    <p>GET <code>/api/reservas</code> - Listar reservas</p>
                    <p>POST <code>/api/hospedes</code> - Criar hóspede</p>
                    <p>POST <code>/api/quartos</code> - Criar quarto</p>
                    <p>POST <code>/api/reservas</code> - Criar reserva</p>
                </div>
            </div>
            
            <script>
                async function fetchAPI(endpoint, method = 'GET', data = null) {
                    const loading = document.getElementById('loading');
                    const message = document.getElementById('message');
                    loading.style.display = 'block';
                    message.innerHTML = '';
                    
                    try {
                        const options = {
                            method: method,
                            headers: {'Content-Type': 'application/json'}
                        };
                        if (data) options.body = JSON.stringify(data);
                        
                        const response = await fetch(endpoint, options);
                        const result = await response.json();
                        loading.style.display = 'none';
                        return result;
                    } catch (error) {
                        loading.style.display = 'none';
                        showMessage('Erro na requisição: ' + error.message, 'error');
                        return null;
                    }
                }
                
                async function atualizarDashboard() {
                    const data = await fetchAPI('/api/dashboard');
                    if (data) {
                        document.getElementById('hospedes').textContent = data.total_hospedes;
                        document.getElementById('quartos').textContent = data.total_quartos;
                        document.getElementById('livres').textContent = data.quartos_livres;
                        document.getElementById('reservas').textContent = data.total_reservas_ativas;
                    }
                }
                
                function criarHospede() {
                    const nome = prompt('Nome do hóspede:');
                    if (!nome) return;
                    const telefone = prompt('Telefone (opcional):');
                    const email = prompt('Email (opcional):');
                    
                    fetchAPI('/api/hospedes', 'POST', { nome, telefone, email }).then(result => {
                        if (result.sucesso) {
                            showMessage(result.mensagem, 'success');
                            atualizarDashboard();
                        } else {
                            showMessage(result.erro, 'error');
                        }
                    });
                }
                
                function criarQuarto() {
                    const numero = prompt('Número do quarto:');
                    if (!numero) return;
                    const tipo = prompt('Tipo (Solteiro, Casal, Suite):');
                    const preco = prompt('Preço da diária (R$):');
                    const descricao = prompt('Descrição (opcional):');
                    
                    fetchAPI('/api/quartos', 'POST', { numero: parseInt(numero), tipo, preco: parseFloat(preco), descricao }).then(result => {
                        if (result.sucesso) {
                            showMessage(result.mensagem, 'success');
                            atualizarDashboard();
                        } else {
                            showMessage(result.erro, 'error');
                        }
                    });
                }
                
                function criarReserva() {
                    const id_hospede = prompt('ID do hóspede:');
                    if (!id_hospede) return;
                    const id_quarto = prompt('ID do quarto:');
                    const entrada = prompt('Data de entrada (YYYY-MM-DD):');
                    const saida = prompt('Data de saída (YYYY-MM-DD):');
                    
                    fetchAPI('/api/reservas', 'POST', { 
                        id_hospede: parseInt(id_hospede), 
                        id_quarto: parseInt(id_quarto), 
                        entrada, 
                        saida 
                    }).then(result => {
                        if (result.sucesso) {
                            showMessage(`${result.mensagem}\\nTotal: R$ ${result.total.toFixed(2)}`, 'success');
                            atualizarDashboard();
                        } else {
                            showMessage(result.erro, 'error');
                        }
                    });
                }
                
                async function listarDados() {
                    const hospedes = await fetchAPI('/api/hospedes');
                    const quartos = await fetchAPI('/api/quartos');
                    const reservas = await fetchAPI('/api/reservas');
                    
                    const output = document.getElementById('output');
                    output.style.display = 'block';
                    output.innerHTML = `
                        <h3>Hóspedes (${hospedes.length})</h3>
                        <pre>${JSON.stringify(hospedes, null, 2)}</pre>
                        <h3>Quartos (${quartos.length})</h3>
                        <pre>${JSON.stringify(quartos, null, 2)}</pre>
                        <h3>Reservas (${reservas.length})</h3>
                        <pre>${JSON.stringify(reservas, null, 2)}</pre>
                    `;
                }
                
                function showMessage(msg, type) {
                    const message = document.getElementById('message');
                    message.innerHTML = `<div class="message ${type}">${msg}</div>`;
                }
                
                // Atualizar dashboard ao carregar
                atualizarDashboard();
                setInterval(atualizarDashboard, 5000);
            </script>
        </body>
        </html>
        '''

def main():
    """Iniciar servidor HTTP"""
    handler = HotelAPIHandler
    
    # Usar IPv4
    socketserver.TCPServer.allow_reuse_address = True
    
    with socketserver.TCPServer((HOST, PORT), handler) as httpd:
        print(f"\n🏨 SISTEMA DE RESERVAS DE HOTEL - Versão Simplificada")
        print(f"{'='*50}")
        print(f"📍 Servidor rodando em: http://{HOST}:{PORT}")
        print(f"📁 Banco de dados: {DB_FILE}")
        print(f"{'='*50}\n")
        print(f"✅ Servidor iniciado com sucesso!")
        print(f"   Abra seu navegador em: http://{HOST}:{PORT}\n")
        print(f"⏹️  Pressione Ctrl+C para parar o servidor\n")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\n❌ Servidor interrompido pelo usuário")
            exit(0)

if __name__ == '__main__':
    main()
