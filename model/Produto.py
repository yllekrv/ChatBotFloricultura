from db.produto_dao import ProdutoDAO

class Produto:
    def __init__(self, id=0, nome=None, descricao=None, valor=0, url_imagem="",
                 tempo_inicio_atendimento=4, tempo_solucao=24):
        self._id = id
        self._nome = nome
        self._descricao = descricao
        self._valor = valor
        self._url_imagem = url_imagem
        self._tempo_inicio_atendimento = tempo_inicio_atendimento
        self._tempo_solucao = tempo_solucao

    # Getters e Setters
    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, novo_id):
        self._id = novo_id

    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, novo_nome):
        self._nome = novo_nome

    @property
    def descricao(self):
        return self._descricao

    @descricao.setter
    def descricao(self, nova_desc):
        self._descricao = nova_desc

    @property
    def valor(self):
        return self._valor

    @valor.setter
    def valor(self, novo_valor):
        self._valor = novo_valor

    @property
    def url_imagem(self):
        return self._url_imagem

    @url_imagem.setter
    def url_imagem(self, nova_url):
        self._url_imagem = nova_url

    @property
    def tempo_inicio_atendimento(self):
        return self._tempo_inicio_atendimento

    @tempo_inicio_atendimento.setter
    def tempo_inicio_atendimento(self, novo_tempo):
        self._tempo_inicio_atendimento = novo_tempo

    @property
    def tempo_solucao(self):
        return self._tempo_solucao

    @tempo_solucao.setter
    def tempo_solucao(self, novo_tempo):
        self._tempo_solucao = novo_tempo

    # Método para representar o objeto como JSON
    def to_json(self):
        return {
            "id": self._id,
            "nome": self._nome,
            "descricao": self._descricao,
            "valor": self._valor,
            "url_imagem": self._url_imagem,
            "tempo_inicio_atendimento": self._tempo_inicio_atendimento,
            "tempo_solucao": self._tempo_solucao
        }

    # Métodos de manipulação usando ServicoDAO
    def gravar(self):
        produto_dao = ProdutoDAO()
        produto_dao.gravar(self)

    def alterar(self):
        produto_dao = ProdutoDAO()
        produto_dao.alterar(self)

    def excluir(self):
        produto_dao = ProdutoDAO()
        produto_dao.excluir(self)

    def consultar(self, termo_busca):
        produto_dao = ProdutoDAO()
        return produto_dao.consultar(termo_busca)
