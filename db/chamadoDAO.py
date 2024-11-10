from model.chamado import Chamado
from conexao import conectar

class ChamadoDAO:
    async def init(self):
        try:
            conexao = await conectar()
            async with conexao.cursor() as cursor:
                sql = """
                    CREATE TABLE IF NOT EXISTS chamado (
                        numero INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
                        data VARCHAR(10) NOT NULL,
                        fk_usu_cpf VARCHAR(14) NOT NULL,
                        CONSTRAINT fk_usuario FOREIGN KEY (fk_usu_cpf) REFERENCES usuario(pk_usu_cpf)
                    )
                """
                await cursor.execute(sql)
            await conexao.commit()
            conexao.close()
        except Exception as erro:
            print(f"Erro ao inicializar tabela chamado: {erro}")

    async def gravar(self, chamado):
        if isinstance(chamado, Chamado):
            try:
                conexao = await conectar()
                async with conexao.cursor() as cursor:
                    await conexao.begin()
                    # Inserir o chamado na tabela
                    sql_chamado = "INSERT INTO chamado(data, fk_usu_cpf) VALUES(%s, %s)"
                    data = datetime.now().strftime("%d/%m/%Y")
                    parametros = (data, chamado.usuario.cpf)
                    await cursor.execute(sql_chamado, parametros)
                    chamado.numero = cursor.lastrowid

                    for prod in chamado.prodicos:
                        sql_prodicos = "INSERT INTO chamado_prodico(fk_cha_numero, fk_prod_id) VALUES(%s, %s)"
                        parametros = (chamado.numero, prod.id)
                        await cursor.execute(sql_prodicos, parametros)
                    
                    await conexao.commit()
                conexao.close()
            except Exception as erro:
                if conexao:
                    await conexao.rollback()
                print(f"Erro ao gravar chamado: {erro}")
