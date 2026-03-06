from flask import Flask, render_template, request, flash, redirect, url_for
import requests
import os

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'chave_ultra_secreta')

URL_PEDIDOS = os.getenv('URL_PEDIDOS', 'http://127.0.0.1:5002')
URL_USUARIOS = os.getenv('URL_USUARIOS', 'http://127.0.0.1:5001')

@app.route('/')
def index():
    try:
        pedidos = requests.get(f'{URL_PEDIDOS}/pedidos').json()
    except:
        pedidos = []
    
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
            requests.post(f'{URL_USUARIOS}/usuarios', json=novo_usuario)
            flash("Usuario cadastrado com sucesso!", "success")
        except:
            flash("Erro ao conectar com o servico de usuarios.", "danger")
        return redirect(url_for('gerenciar_usuarios'))

    try:
        lista_usuarios = requests.get(f'{URL_USUARIOS}/usuarios').json()
    except:
        lista_usuarios = []
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
            requests.post(f'{URL_PEDIDOS}/pedidos', json=dados_pedido)
            flash("Pedido criado com sucesso!", "success")
        except:
            flash("Erro de conexao com o servico de pedidos.", "danger")
        return redirect(url_for('historico'))

    # Busca usuarios para preencher o select do formulario
    try:
        usuarios = requests.get(f'{URL_USUARIOS}/usuarios').json()
    except:
        usuarios = []
    
    return render_template('novo_pedido.html', usuarios=usuarios)

@app.route('/historico')
def historico():
    try:
        pedidos = requests.get(f'{URL_PEDIDOS}/pedidos').json()
    except:
        pedidos = []
    return render_template('historico.html', pedidos=pedidos)

if __name__ == '__main__':
    app.run(port=5000)