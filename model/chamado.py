from db.ChamadoDAO import ChamadoDAO
class Chamado:
    def __init__(self, numero, data, usuario=None, produtos=None):
        if usuario is None:
            usuario = {"cpf": ""}
        if produtos is None:
            produtos = []
        
        self._numero = numero
        self._data = data
        self._usuario = usuario
        self._produtos = produtos

    # Getters
    @property
    def numero(self):
        return self._numero

    @property
    def data(self):
        return self._data

    @property
    def usuario(self):
        return self._usuario

    @property
    def produtos(self):
        return self._produtos

    # Setters
    @numero.setter
    def numero(self, numero):
        self._numero = numero

    @data.setter
    def data(self, data):
        self._data = data

    @usuario.setter
    def usuario(self, usuario):
        self._usuario = usuario

    @produtos.setter
    def produtos(self, produtos):
        self._produtos = produtos

    # Método toJSON
    def to_json(self):
        return {
            "numero": self._numero,
            "data": self._data,
            "usuario": self._usuario,
            "produtos": self._produtos,
        }

    # Método gravar
    async def gravar(self):
        chamDAO = ChamadoDAO()
        await chamDAO.gravar(self)
