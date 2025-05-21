from database import get_db_connection
import datetime

# -- CLasse Produto ---
Class Produto:
    def __init__(self, id, None, nome=None, sku=None, unidade_medida=None, codigo_barras=None):
        # 'id' é um número único paracada produto
        self.id = id
        # 'nome' éo nomedo produto(ex: Parafuso, porca)
        self.nome = nome
        # 'sku' é o código unico de produto
        self.sku = sku
        # 'unidade_medida' é como contamoso produto("caixa", "unidade","kg")
        self.unidade_medida = unidade_medida
        # 'codigo_barras' é o numero internacional identificador do produto
        self.codigo_barras = codigo de codigo_barras

    def save(self):
        conn = get_db_connection() # Pega aconexão com o banco
        if conn is None:
            return  False # Se não conseguiu conectar, não salva

        cursor = conn.cursor() # 'cursor' é quem vai executar os comandos
        try:
            # Comando SQL para INSERIR um novo produto
            cursor.execute(
                """
                INSERT INTO produtos (nome,sku, unidade_medida)
                VAlues (%s, %s, %s) RETURNING id;
                """,
                (self.nome, self.sku, self.unidade_medida)
                )
            self.id = cursor.fetchone()[0] # Pega o ID gerado pelo banco
            conn.commit() # Confirma amudança no banco(como "salvar de verdade")
            print(f"Produto '{self.nome}' salvo com sucesso" ID: {self.id}")
                  return True
        except Exception as e:
            conn.rollback()# Se der erro, desfaz a operação
            print(f"Erro ao salvar produto: {e}")
            return False
        finally:
            cursor.close() # Fecha o cursor
            conn.close() # Fecha a conxão como banco

# Método para ATUALIZAR um produto EXISTENTE no banco de dados
def update(self):
    if self.id is None
    print("Erro: ID do produto não definido para atualização.")
    return False

    conn= get_db_connection()
    if conn is None:
        return False

    cursor = conn.cursor()
    try:
        # Comando SQL para ATUALIZAR um produto pelo ID
        cursor.execute(
            """
            UPDATE produtos
            SET nome = %s, sku- %s, unidade_medida= %s
            WHERE id = %s;
            """,
            (self.nome, self.sku, self.unidade_medida, self.id)
            )
        conn.commit()
        print(f"Produti ID {self.id} atualizado com sucesso!")
        return True
    except Exception as e:
        conn.rollback()
        print(f"Erro ao atualizar produto: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

# Métodopara PEGAR TODOS os produtos do banco de dados
@staticmethod # Esse método não precisa de um objeto 'Produto' para ser chamado
def get_all():
    conn = get_db_connection()
    if conn is None:
        return [] # Retorna lista vaziase não se conectar

    cursor = conn.cursor()
    try:
        # Comando SQL para SELECIONAR todos os produtos
        cursor.execute("SELECT id, nome, sku, unidade_medida FROM produtos ORDER BY nome;")
        produto_data = cursor.fetchall() # Pega todas as lihas
        # Transforma as linhas do banco em objetos 'Produto'
        return [Prduto(id=p[0], nome=p[1], sku=p[2], unidade_medida=p[3]) for p in produtos_data]
    except Exception as e:
        print(f"Erro ao buscar o ppppproduto: {e}")
        return[]
    finally:
        cursor.close()
        conn.close()


