import aiomysql
from model.Produto import Produto  # Supondo que a classe Produto esteja em Model/Produto.py
from Conexao import conectar  # A função conectar é a que você implementou anteriormente

class ProdutoDAO:

    def __init__(self):
        self.init()

    async def init(self):
        try:
            # Criar a tabela serviço caso ela não exista
            sql = '''
            CREATE TABLE IF NOT EXISTS Produto(
                id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
                nome VARCHAR(100) NOT NULL,
                descricao VARCHAR(200) NOT NULL,
                valor DECIMAL(6,2) NOT NULL,
                urlImagem VARCHAR(250) NOT NULL,
                tempoInicioAtendimento INT NOT NULL,
                tempoSolucao INT NOT NULL
            )
            '''
            conexao = await conectar()
            async with conexao.cursor() as cursor:
                await cursor.execute(sql)
            print("Tabela Serviço iniciada com sucesso!")
        except Exception as erro:
            print("Não foi possível iniciar a tabela serviço: " + str(erro))

    async def gravar(self, Produto):
        if isinstance(Produto, Produto):
            sql = '''
            INSERT INTO Produto(nome, descricao, valor, urlImagem, tempoInicioAtendimento, tempoSolucao)
            VALUES (%s, %s, %s, %s, %s, %s)
            '''
            parametros = (Produto.nome, Produto.descricao, Produto.valor, Produto.urlImagem,
                         Produto.tempoInicioAtendimento, Produto.tempoSolucao)
            conexao = await conectar()
            async with conexao.cursor() as cursor:
                resultado = await cursor.execute(sql, parametros)
                Produto.id = cursor.lastrowid

    async def alterar(self, Produto):
        if isinstance(Produto, Produto):
            sql = '''
            UPDATE Produto SET nome = %s, descricao = %s, valor = %s, urlImagem = %s, 
            tempoInicioAtendimento = %s, tempoSolucao = %s WHERE id = %s
            '''
            parametros = (Produto.nome, Produto.descricao, Produto.valor, Produto.urlImagem,
                         Produto.tempoInicioAtendimento, Produto.tempoSolucao, Produto.id)
            conexao = await conectar()
            async with conexao.cursor() as cursor:
                await cursor.execute(sql, parametros)

    async def excluir(self, Produto):
        if isinstance(Produto, Produto):
            sql = "DELETE FROM Produto WHERE id = %s"
            parametros = (Produto.id,)
            conexao = await conectar()
            async with conexao.cursor() as cursor:
                await cursor.execute(sql, parametros)

    async def consultar(self, termoBusca):
        if not termoBusca:
            termoBusca = ''
        sql = "SELECT * FROM Produto WHERE descricao LIKE %s ORDER BY nome"
        parametros = ('%' + termoBusca + '%',)
        conexao = await conectar()
        async with conexao.cursor() as cursor:
            await cursor.execute(sql, parametros)
            registros = await cursor.fetchall()
        listaProdutos = []
        for registro in registros:
            Produto = Produto(
                id=registro['id'],
                nome=registro['nome'],
                descricao=registro['descricao'],
                valor=registro['valor'],
                urlImagem=registro['urlImagem'],
                tempoInicioAtendimento=registro['tempoInicioAtendimento'],
                tempoSolucao=registro['tempoSolucao']
            )
            listaProdutos.append(Produto)
        return listaProdutos
