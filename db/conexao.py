import aiomysql
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

async def conectar():
    if hasattr(global_vars, 'pool_conexoes'):
        return await global_vars.pool_conexoes.acquire()
    else:
        pool = await aiomysql.create_pool(
            host=os.getenv("DB_HOST", "localhost"),
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASSWORD", ""),
            db=os.getenv("DB_DATABASE", "chatbot"),
            maxsize=50,  # Limite máximo de conexões
            minsize=0,   # Conexões mínimas ociosas
            pool_recycle=600,  # Tempo limite para ociosidade, em segundos
            autocommit=True
        )

        global_vars.pool_conexoes = pool
        return await global_vars.pool_conexoes.acquire()