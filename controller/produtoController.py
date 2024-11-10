from flask import Flask, request, jsonify
#from modelo.servico import Produto  
import model.Produto;

app = Flask(__name__)

class ProdutoCtrl:
    def gravar(self):
        if request.method == "POST" and request.is_json:
            dados = request.get_json()
            # Pseudo-validação
            if dados.get('nome') and dados.get('descricao') and dados.get('valor') >= 0 and \
               dados.get('urlImagem') and dados.get('tempoInicioAtendimento') > 0 and \
               dados.get('tempoSolucao') > 0:
                
                servico = Servico(0, dados['nome'], dados['descricao'], dados['valor'],
                                  dados['urlImagem'], dados['tempoInicioAtendimento'],
                                  dados['tempoSolucao'])
                
                try:
                    produto.gravar()
                    return jsonify({"status": True, "mensagem": "Produto gravado com sucesso!", "id": produto.id}), 201
                except Exception as erro:
                    return jsonify({"status": False, "mensagem": f"Erro ao registrar o produto: {erro}"}), 500
            else:
                return jsonify({"status": False, "mensagem": "Informe todos os dados necessários conforme documentação!"}), 400
        else:
            return jsonify({"status": False, "mensagem": "Formato não permitido!"}), 405

    def alterar(self):
        if request.method in ["PUT", "PATCH"] and request.is_json:
            dados = request.get_json()
            # Pseudo-validação
            if dados.get('id') > 0 and dados.get('nome') and dados.get('descricao') and dados.get('valor') >= 0 and \
               dados.get('urlImagem') and dados.get('tempoInicioAtendimento') > 0 and \
               dados.get('tempoSolucao') > 0:

                produto = Produto(dados['id'], dados['nome'], dados['descricao'], dados['valor'],
                                  dados['urlImagem'], dados['tempoInicioAtendimento'],
                                  dados['tempoSolucao'])
                
                try:
                    produto.alterar()
                    return jsonify({"status": True, "mensagem": "Produto alterado com sucesso!"}), 200
                except Exception as erro:
                    return jsonify({"status": False, "mensagem": f"Erro ao alterar o produto: {erro}"}), 500
            else:
                return jsonify({"status": False, "mensagem": "Informe todos os dados necessários conforme documentação!"}), 400
        else:
            return jsonify({"status": False, "mensagem": "Formato não permitido!"}), 405

    def excluir(self):
        if request.method == "DELETE" and request.is_json:
            id = request.args.get('id', type=int)
            # Pseudo-validação
            if id and id > 0:
                produto = Produto(id)
                try:
                    produto.excluir()
                    return jsonify({"status": True, "mensagem": "Produto excluído com sucesso!"}), 200
                except Exception as erro:
                    return jsonify({"status": False, "mensagem": f"Erro ao excluir o produto: {erro}"}), 500
            else:
                return jsonify({"status": False, "mensagem": "Informe o id na url!"}), 400
        else:
            return jsonify({"status": False, "mensagem": "Formato não permitido!"}), 405

    def consultar(self):
        termo_busca = request.args.get('produto', '')
        if request.method == "GET":
            produto = Produto(0)
            try:
                lista_produtos = produto.consultar(termo_busca)
                return jsonify({"status": True, "listaprodutos": lista_produtos}), 200
            except Exception as erro:
                return jsonify({"status": False, "mensagem": f"Não foi possível recuperar os produtos: {erro}"}), 500
        else:
            return jsonify({"status": False, "mensagem": "Método não permitido!"}), 405

# Configuração das rotas
produto_ctrl = ProdutoCtrl()
app.add_url_rule('/produto/gravar', view_func=produto_ctrl.gravar, methods=['POST'])
app.add_url_rule('/produto/alterar', view_func=produto_ctrl.alterar, methods=['PUT', 'PATCH'])
app.add_url_rule('/produto/excluir', view_func=produto_ctrl.excluir, methods=['DELETE'])
app.add_url_rule('/produto/consultar', view_func=produto_ctrl.consultar, methods=['GET'])

if __name__ == '__main__':
    app.run(debug=True)
