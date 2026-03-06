from flask import Flask, request, jsonify
from abc import ABC, abstractmethod
from datetime import datetime

app = Flask(__name__)

db_pedidos = []
db_produtos = []
db_tarefas = []

class Pedido(ABC):
    @abstractmethod
    def get_detalhes(self):
        pass
    
    @abstractmethod
    def get_icone(self):
        pass

class PedidoFisico(Pedido):
    def get_detalhes(self):
        return "Separacao no estoque + Envio via Transportadora"
    def get_icone(self):
        return "bi-box-seam"

class PedidoDigital(Pedido):
    def get_detalhes(self):
        return "Envio automatico de licenca por E-mail"
    def get_icone(self):
        return "bi-cloud-download"

class PedidoServico(Pedido):
    def get_detalhes(self):
        return "Agendamento de consultor especializado"
    def get_icone(self):
        return "bi-calendar-check"

class FactoryPedido:
    @staticmethod
    def criar(tipo):
        tipos = {
            "fisico": PedidoFisico,
            "digital": PedidoDigital,
            "servico": PedidoServico
        }
        classe = tipos.get(tipo)
        return classe() if classe else None

@app.route('/pedidos', methods=['GET', 'POST'])
def gerenciar_pedidos():
    if request.method == 'POST':
        dados = request.json
        tipo = dados.get('tipo')
        objeto_pedido = FactoryPedido.criar(tipo)
        
        if objeto_pedido:
            novo = {
                'id': len(db_pedidos) + 1,
                'cliente_id': dados.get('cliente_id'),
                'produto_id': dados.get('produto_id'),
                'tipo': tipo,
                'desc': objeto_pedido.get_detalhes(),
                'icone': objeto_pedido.get_icone(),
                'data': datetime.now().strftime("%d/%m %H:%M")
            }
            db_pedidos.insert(0, novo)
            return jsonify(novo), 201
        return jsonify({"erro": "Tipo invalido"}), 400
    return jsonify(db_pedidos), 200

@app.route('/produtos', methods=['GET', 'POST'])
def gerenciar_produtos():
    if request.method == 'POST':
        dados = request.json
        novo = {
            "id": len(db_produtos) + 1, 
            "nome": dados.get("nome"), 
            "preco": dados.get("preco")
        }
        db_produtos.append(novo)
        return jsonify(novo), 201
    return jsonify(db_produtos), 200

@app.route('/tarefas', methods=['GET', 'POST'])
def gerenciar_tarefas():
    if request.method == 'POST':
        dados = request.json
        novo = {
            "id": len(db_tarefas) + 1, 
            "descricao": dados.get("descricao"), 
            "status": "pendente"
        }
        db_tarefas.append(novo)
        return jsonify(novo), 201
    return jsonify(db_tarefas), 200

if __name__ == '__main__':
    app.run(port=5002)