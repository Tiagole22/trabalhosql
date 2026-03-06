from flask import Flask, request, jsonify

app = Flask(__name__)

db_usuarios = []

@app.route('/usuarios', methods=['GET', 'POST'])
def gerenciar_usuarios():
    if request.method == 'POST':
        dados = request.json
        novo_usuario = {
            "id": len(db_usuarios) + 1, 
            "nome": dados.get("nome"), 
            "email": dados.get("email")
        }
        db_usuarios.append(novo_usuario)
        return jsonify(novo_usuario), 201
    return jsonify(db_usuarios), 200

@app.route('/usuarios/<int:id_usuario>', methods=['GET', 'PUT', 'DELETE'])
def operacoes_usuario(id_usuario):
    usuario = next((u for u in db_usuarios if u["id"] == id_usuario), None)
    if not usuario:
        return jsonify({"erro": "Nao encontrado"}), 404
        
    if request.method == 'GET':
        return jsonify(usuario), 200
        
    if request.method == 'PUT':
        dados = request.json
        usuario.update({
            "nome": dados.get("nome", usuario["nome"]), 
            "email": dados.get("email", usuario["email"])
        })
        return jsonify(usuario), 200
        
    if request.method == 'DELETE':
        db_usuarios.remove(usuario)
        return '', 204

if __name__ == '__main__':
    app.run(port=5001)