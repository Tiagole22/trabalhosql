from flask import Flask, render_template, request, flash, redirect, url_for
import requests
import os

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'chave_ultra_secreta')

URL_PEDIDOS = os.getenv('URL_PEDIDOS', 'http://127.0.0.1:5002')
URL_USUARIOS = os.getenv('URL_USUARIOS', 'http://127.0.0.1:5001')

local_usuarios = []
local_pedidos = []


def obter_usuarios():
    try:
        resposta = requests.get(f'{URL_USUARIOS}/usuarios', timeout=5)
        resposta.raise_for_status()
        return resposta.json()
    except:
        return local_usuarios


def obter_pedidos():
    try:
        resposta = requests.get(f'{URL_PEDIDOS}/pedidos', timeout=5)
        resposta.raise_for_status()
        return resposta.json()
    except:
        return local_pedidos

@app.route('/')
def index():
    pedidos = obter_pedidos()
    
    total = len(pedidos)
    fisicos = sum(1 for p in pedidos if p.get('tipo') == 'fisico')
    digitais = sum(1 for p in pedidos if p.get('tipo') == 'digital')
    servicos = sum(1 for p in pedidos if p.get('tipo') == 'servico')
    
    return render_template('dashboard.html', total=total, fisicos=fisicos, digitais=digitais, servicos=servicos)

@app.route('/usuarios', methods=['GET', 'POST'])
def gerenciar_usuarios():
    if request.method == 'POST':
        novo_usuario = {"nome": request.form['nome'], "email": request.form['email']}
        try:
            resposta = requests.post(f'{URL_USUARIOS}/usuarios', json=novo_usuario, timeout=5)
            resposta.raise_for_status()
            flash("Usuario cadastrado com sucesso!", "success")
        except:
            usuario_local = {
                "id": len(local_usuarios) + 1,
                "nome": novo_usuario["nome"],
                "email": novo_usuario["email"]
            }
            local_usuarios.append(usuario_local)
            flash("Servico de usuarios offline. Cadastro salvo localmente.", "warning")
        return redirect(url_for('gerenciar_usuarios'))

    lista_usuarios = obter_usuarios()
    return render_template('usuarios.html', usuarios=lista_usuarios)

@app.route('/novo', methods=['GET', 'POST'])
def novo_pedido():
    if request.method == 'POST':
        dados_pedido = {
            "cliente_id": request.form['cliente'],
            "produto_id": request.form['produto'],
            "tipo": request.form['tipo']
        }
        try:
            resposta = requests.post(f'{URL_PEDIDOS}/pedidos', json=dados_pedido, timeout=5)
            resposta.raise_for_status()
            flash("Pedido criado com sucesso!", "success")
        except:
            descricoes = {
                "fisico": "Separacao no estoque + Envio via Transportadora",
                "digital": "Envio automatico de licenca por E-mail",
                "servico": "Agendamento de consultor especializado"
            }
            icones = {
                "fisico": "bi-box-seam",
                "digital": "bi-cloud-download",
                "servico": "bi-calendar-check"
            }
            pedido_local = {
                "id": len(local_pedidos) + 1,
                "cliente_id": dados_pedido["cliente_id"],
                "produto_id": dados_pedido["produto_id"],
                "tipo": dados_pedido["tipo"],
                "desc": descricoes.get(dados_pedido["tipo"], "Pedido"),
                "icone": icones.get(dados_pedido["tipo"], "bi-receipt"),
                "data": "agora"
            }
            local_pedidos.insert(0, pedido_local)
            flash("Servico de pedidos offline. Pedido salvo localmente.", "warning")
        return redirect(url_for('historico'))

    # Busca usuarios para preencher o select do formulario
    usuarios = obter_usuarios()
    
    return render_template('novo_pedido.html', usuarios=usuarios)

@app.route('/historico')
def historico():
    pedidos = obter_pedidos()
    return render_template('historico.html', pedidos=pedidos)

if __name__ == '__main__':
    app.run(port=5000)