from flask import Blueprint, request
from Controller.produtoCtrl import produtoCtrl
from flask import Flask
from routes.servico import rota_produto 

prod_ctrl = produtoCtrl()
rota_produto = Blueprint('rota_produto', __name__)

app = Flask(__name__)
app.register_blueprint(rota_produto, url_prefix='/produto')

if __name__ == '__main__':
    app.run(debug=True)

# Consultar todos ou um prodiço específico
@rota_produto.route('/', methods=['GET'])
@rota_produto.route('/<produto>', methods=['GET'])
def consultar(produto=None):
    return prod_ctrl.consultar(produto)

# Gravar um prodiço
@rota_produto.route('/', methods=['POST'])
def gravar():
    return prod_ctrl.gravar()

# Alterar um prodiço
@rota_produto.route('/', methods=['PUT'])
@rota_produto.route('/', methods=['PATCH'])
def alterar():
    return prod_ctrl.alterar()

# Excluir um prodiço
@rota_produto.route('/<int:id>', methods=['DELETE'])
def excluir(id):
    return prod_ctrl.excluir(id)



