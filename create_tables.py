# create_tables.py

from database import get_db_connection

def create_tables():
    conn = get_db_connection()
    if conn is None:
        print("Não foi possível conectar ao banco de dados para criar as tabelas.")
        return

    cursor = conn.cursor()

    # Comando SQL para criar a tabela 'produtos'
    # 'SERIAL PRIMARY KEY' significa que o ID será gerado automaticamente e será único.
    # 'VARCHAR(255)' é um texto com no máximo 255 letras/números.
    # 'UNIQUE NOT NULL' significa que o SKU não pode ser repetido e não pode ficar vazio.
    sql_produtos = """
    CREATE TABLE IF NOT EXISTS produtos (
        id SERIAL PRIMARY KEY,
        nome VARCHAR(255) NOT NULL,
        sku VARCHAR(50) UNIQUE NOT NULL,
        unidade_medida VARCHAR(20)
        codigo_barras VARCHAR(50) UNIQUE
    );
    """

    # Comando SQL para criar a tabela 'enderecos'
    sql_enderecos = """
    CREATE TABLE IF NOT EXISTS enderecos (
        id SERIAL PRIMARY KEY,
        corredor VARCHAR(10) NOT NULL,
        prateleira VARCHAR(10) NOT NULL,
        nivel VARCHAR(10),
        posicao VARCHAR(10),
        UNIQUE (corredor, prateleira, nivel, posicao) -- Garante que o endereço completo seja único
    );
    """

    # Comando SQL para criar a tabela 'itens_estoque'
    # 'INTEGER' é para números inteiros.
    # 'DATE' é para datas (ano-mês-dia).
    # 'FOREIGN KEY (produto_id) REFERENCES produtos(id)' linka esta tabela com a tabela 'produtos'.
    # Isso significa que um 'item de estoque' SEMPRE precisa se referir a um 'produto' que existe.
    sql_itens_estoque = """
    CREATE TABLE IF NOT EXISTS itens_estoque (
        id SERIAL PRIMARY KEY,
        produto_id INTEGER NOT NULL,
        endereco_id INTEGER NOT NULL,
        quantidade INTEGER NOT NULL CHECK (quantidade >= 0), -- Quantidade não pode ser negativa
        data_entrada DATE NOT NULL,
        data_validade DATE,
        lote VARCHAR(50),
        FOREIGN KEY (produto_id) REFERENCES produtos(id) ON DELETE CASCADE,
        FOREIGN KEY (endereco_id) REFERENCES enderecos(id) ON DELETE CASCADE
    );
    """

    # Comando SQL para criar a tabela 'movimentacoes'
    # 'TIMESTAMP' é para data e hora.
    sql_movimentacoes = """
    CREATE TABLE IF NOT EXISTS movimentacoes (
        id SERIAL PRIMARY KEY,
        item_estoque_id INTEGER NOT NULL,
        tipo_movimentacao VARCHAR(10) NOT NULL CHECK (tipo_movimentacao IN ('ENTRADA', 'SAIDA')),
        quantidade INTEGER NOT NULL CHECK (quantidade > 0),
        data_movimentacao TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (item_estoque_id) REFERENCES itens_estoque(id) ON DELETE CASCADE
    );
    """

    try:
        print("Criando tabela 'produtos'...")
        cursor.execute(sql_produtos)
        print("Criando tabela 'enderecos'...")
        cursor.execute(sql_enderecos)
        print("Criando tabela 'itens_estoque'...")
        cursor.execute(sql_itens_estoque)
        print("Criando tabela 'movimentacoes'...")
        cursor.execute(sql_movimentacoes)
        conn.commit() # Salva as criações das tabelas no banco
        print("Todas as tabelas foram criadas ou já existem no banco de dados!")
    except Exception as e:
        conn.rollback() # Se der erro, desfaz a criação
        print(f"Erro ao criar tabelas: {e}")
    finally:
        cursor.close()
        conn.close()

# Se você rodar este arquivo diretamente, ele vai criar as tabelas
if __name__ == "__main__":
    create_tables()