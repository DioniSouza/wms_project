import os
from dotenv import load_dotenv
import psycopg2
from psycopg2 import OperationalError

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Função para conectar ao banco de dados
def get_db_connection():
    try:
        connection = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            port=os.getenv("DB_PORT")
        )
        print("Conexão com o banco de dados PostgreSQL estabelecida com sucesso!")
        return connection
    except OperationalError as e:
        print(f"Erro ao conectar ao banco de dados PostgreSQL: {e}")
        return None

# Exemplo de uso (opcional, só para testar a conexão)
if __name__ == "__main__":
    conn = get_db_connection()
    if conn:
        conn.close()
        print("Conexão com o banco de dados fechada.")