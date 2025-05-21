# models.py

from database import get_db_connection
import datetime # Para trabalhar com datas e horas

# --- Classe Produto ---
# Essa classe vai representar a tabela 'produtos' no nosso banco de dados.
# Cada objeto 'Produto' será uma linha nessa tabela.
class Produto:
    def __init__(self, id=None, nome=None, sku=None, unidade_medida=None, codigo_barras=None):
        self.id = id
        self.nome = nome
        self.sku = sku
        self.unidade_medida = unidade_medida
        self.codigo_barras = codigo_barras # Campo para o código de barras

    # Método para SALVAR um NOVO produto no banco de dados
    def save(self):
        conn = get_db_connection()
        if conn is None:
            return False

        cursor = conn.cursor()
        try:
            # Comando SQL para INSERIR um novo produto, incluindo o codigo_barras
            cursor.execute(
                """
                INSERT INTO produtos (nome, sku, unidade_medida, codigo_barras)
                VALUES (%s, %s, %s, %s) RETURNING id;
                """,
                (self.nome, self.sku, self.unidade_medida, self.codigo_barras)
            )
            self.id = cursor.fetchone()[0]
            conn.commit()
            print(f"Produto '{self.nome}' salvo com sucesso! ID: {self.id}")
            return True
        except Exception as e:
            conn.rollback()
            print(f"Erro ao salvar produto: {e}")
            return False
        finally:
            cursor.close()
            conn.close()

    # Método para ATUALIZAR um produto EXISTENTE no banco de dados
    def update(self):
        if self.id is None:
            print("Erro: ID do produto não definido para atualização.")
            return False

        conn = get_db_connection()
        if conn is None:
            return False

        cursor = conn.cursor()
        try:
            # Comando SQL para ATUALIZAR um produto pelo ID, incluindo o codigo_barras
            cursor.execute(
                """
                UPDATE produtos
                SET nome = %s, sku = %s, unidade_medida = %s, codigo_barras = %s
                WHERE id = %s;
                """,
                (self.nome, self.sku, self.unidade_medida, self.codigo_barras, self.id)
            )
            conn.commit()
            print(f"Produto ID {self.id} atualizado com sucesso!")
            return True
        except Exception as e:
            conn.rollback()
            print(f"Erro ao atualizar produto: {e}")
            return False
        finally:
            cursor.close()
            conn.close()

    # Método para PEGAR TODOS os produtos do banco de dados
    @staticmethod
    def get_all():
        conn = get_db_connection()
        if conn is None:
            return []

        cursor = conn.cursor()
        try:
            # Comando SQL para SELECIONAR todos os produtos, incluindo o codigo_barras
            cursor.execute("SELECT id, nome, sku, unidade_medida, codigo_barras FROM produtos ORDER BY nome;")
            produtos_data = cursor.fetchall()
            # Transforma as linhas do banco em objetos 'Produto', passando o codigo_barras
            return [Produto(id=p[0], nome=p[1], sku=p[2], unidade_medida=p[3], codigo_barras=p[4]) for p in produtos_data]
        except Exception as e:
            print(f"Erro ao buscar produtos: {e}")
            return []
        finally:
            cursor.close()
            conn.close()

    # Método para PEGAR UM produto específico pelo ID
    @staticmethod
    def get_by_id(product_id):
        conn = get_db_connection()
        if conn is None:
            return None

        cursor = conn.cursor()
        try:
            # Seleciona um produto pelo ID, incluindo o codigo_barras
            cursor.execute("SELECT id, nome, sku, unidade_medida, codigo_barras FROM produtos WHERE id = %s;", (product_id,))
            product_data = cursor.fetchone()
            if product_data:
                # Retorna um objeto Produto com o codigo_barras
                return Produto(id=product_data[0], nome=product_data[1], sku=product_data[2], unidade_medida=product_data[3], codigo_barras=product_data[4])
            return None
        except Exception as e:
            print(f"Erro ao buscar produto por ID: {e}")
            return None
        finally:
            cursor.close()
            conn.close()

    # Método para DELETAR um produto
    def delete(self):
        if self.id is None:
            print("Erro: ID do produto não definido para exclusão.")
            return False

        conn = get_db_connection()
        if conn is None:
            return False

        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM produtos WHERE id = %s;", (self.id,))
            conn.commit()
            print(f"Produto ID {self.id} deletado com sucesso!")
            return True
        except Exception as e:
            conn.rollback()
            print(f"Erro ao deletar produto: {e}")
            return False
        finally:
            cursor.close()
            conn.close()


# --- Classe Endereco ---
# Vai representar a tabela 'enderecos' no banco.
class Endereco:
    def __init__(self, id=None, corredor=None, prateleira=None, nivel=None, posicao=None):
        self.id = id
        self.corredor = corredor
        self.prateleira = prateleira
        self.nivel = nivel
        self.posicao = posicao

    # Método para montar o endereço completo (ex: A-01-02-03)
    def get_full_address(self):
        parts = [str(self.corredor), str(self.prateleira), str(self.nivel), str(self.posicao)]
        return "-".join(filter(None, parts))

    def save(self):
        conn = get_db_connection()
        if conn is None: return False
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                INSERT INTO enderecos (corredor, prateleira, nivel, posicao)
                VALUES (%s, %s, %s, %s) RETURNING id;
                """,
                (self.corredor, self.prateleira, self.nivel, self.posicao)
            )
            self.id = cursor.fetchone()[0]
            conn.commit()
            print(f"Endereço '{self.get_full_address()}' salvo com sucesso! ID: {self.id}")
            return True
        except Exception as e:
            conn.rollback()
            print(f"Erro ao salvar endereço: {e}")
            return False
        finally:
            cursor.close()
            conn.close()

    def update(self):
        if self.id is None:
            print("Erro: ID do endereço não definido para atualização.")
            return False
        conn = get_db_connection()
        if conn is None: return False
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                UPDATE enderecos
                SET corredor = %s, prateleira = %s, nivel = %s, posicao = %s
                WHERE id = %s;
                """,
                (self.corredor, self.prateleira, self.nivel, self.posicao, self.id)
            )
            conn.commit()
            print(f"Endereço ID {self.id} atualizado com sucesso!")
            return True
        except Exception as e:
            conn.rollback()
            print(f"Erro ao atualizar endereço: {e}")
            return False
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_all():
        conn = get_db_connection()
        if conn is None: return []
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT id, corredor, prateleira, nivel, posicao FROM enderecos ORDER BY corredor, prateleira, nivel, posicao;")
            enderecos_data = cursor.fetchall()
            return [Endereco(id=e[0], corredor=e[1], prateleira=e[2], nivel=e[3], posicao=e[4]) for e in enderecos_data]
        except Exception as e:
            print(f"Erro ao buscar endereços: {e}")
            return []
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_by_id(endereco_id):
        conn = get_db_connection()
        if conn is None: return None
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT id, corredor, prateleira, nivel, posicao FROM enderecos WHERE id = %s;", (endereco_id,))
            endereco_data = cursor.fetchone()
            if endereco_data:
                return Endereco(id=endereco_data[0], corredor=endereco_data[1], prateleira=endereco_data[2], nivel=endereco_data[3], posicao=endereco_data[4])
            return None
        except Exception as e:
            print(f"Erro ao buscar endereço por ID: {e}")
            return None
        finally:
            cursor.close()
            conn.close()

    def delete(self):
        if self.id is None:
            print("Erro: ID do endereço não definido para exclusão.")
            return False
        conn = get_db_connection()
        if conn is None: return False
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM enderecos WHERE id = %s;", (self.id,))
            conn.commit()
            print(f"Endereço ID {self.id} deletado com sucesso!")
            return True
        except Exception as e:
            conn.rollback()
            print(f"Erro ao deletar endereço: {e}")
            return False
        finally:
            cursor.close()
            conn.close()

# --- Classe ItemEstoque ---
# Representa um lote específico de um produto em um endereço, com sua validade.
# Ex: 100 parafusos (Produto) no endereço A-01-01-01 (Endereco) com validade 2025-12-31.
class ItemEstoque:
    def __init__(self, id=None, produto_id=None, endereco_id=None, quantidade=None, data_entrada=None, data_validade=None, lote=None):
        self.id = id
        self.produto_id = produto_id
        self.endereco_id = endereco_id
        self.quantidade = quantidade
        self.data_entrada = data_entrada if data_entrada else datetime.date.today()
        self.data_validade = data_validade
        self.lote = lote

    def save(self):
        conn = get_db_connection()
        if conn is None: return False
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                INSERT INTO itens_estoque (produto_id, endereco_id, quantidade, data_entrada, data_validade, lote)
                VALUES (%s, %s, %s, %s, %s, %s) RETURNING id;
                """,
                (self.produto_id, self.endereco_id, self.quantidade, self.data_entrada, self.data_validade, self.lote)
            )
            self.id = cursor.fetchone()[0]
            conn.commit()
            print(f"Item de estoque ID {self.id} salvo com sucesso!")
            return True
        except Exception as e:
            conn.rollback()
            print(f"Erro ao salvar item de estoque: {e}")
            return False
        finally:
            cursor.close()
            conn.close()

    def update(self):
        if self.id is None:
            print("Erro: ID do item de estoque não definido para atualização.")
            return False
        conn = get_db_connection()
        if conn is None: return False
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                UPDATE itens_estoque
                SET produto_id = %s, endereco_id = %s, quantidade = %s, data_entrada = %s, data_validade = %s, lote = %s
                WHERE id = %s;
                """,
                (self.produto_id, self.endereco_id, self.quantidade, self.data_entrada, self.data_validade, self.lote, self.id)
            )
            conn.commit()
            print(f"Item de estoque ID {self.id} atualizado com sucesso!")
            return True
        except Exception as e:
            conn.rollback()
            print(f"Erro ao atualizar item de estoque: {e}")
            return False
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_all():
        conn = get_db_connection()
        if conn is None: return []
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                SELECT
                    ie.id, p.nome, e.corredor, e.prateleira, e.nivel, e.posicao,
                    ie.quantidade, ie.data_entrada, ie.data_validade, ie.lote,
                    p.id as produto_id, e.id as endereco_id
                FROM itens_estoque ie
                JOIN produtos p ON ie.produto_id = p.id
                JOIN enderecos e ON ie.endereco_id = e.id
                ORDER BY p.nome, e.corredor, e.prateleira;
                """
            )
            itens_data = cursor.fetchall()
            return [
                {
                    'id': item[0],
                    'produto_nome': item[1],
                    'endereco_completo': f"{item[2]}-{item[3]}-{item[4]}-{item[5]}",
                    'quantidade': item[6],
                    'data_entrada': item[7],
                    'data_validade': item[8],
                    'lote': item[9],
                    'produto_id': item[10],
                    'endereco_id': item[11]
                }
                for item in itens_data
            ]
        except Exception as e:
            print(f"Erro ao buscar itens de estoque: {e}")
            return []
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_by_id(item_id):
        conn = get_db_connection()
        if conn is None: return None
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                SELECT
                    ie.id, ie.produto_id, ie.endereco_id, ie.quantidade,
                    ie.data_entrada, ie.data_validade, ie.lote
                FROM itens_estoque ie
                WHERE ie.id = %s;
                """, (item_id,)
            )
            item_data = cursor.fetchone()
            if item_data:
                return ItemEstoque(id=item_data[0], produto_id=item_data[1], endereco_id=item_data[2],
                                   quantidade=item_data[3], data_entrada=item_data[4],
                                   data_validade=item_data[5], lote=item_data[6])
            return None
        except Exception as e:
            print(f"Erro ao buscar item de estoque por ID: {e}")
            return None
        finally:
            cursor.close()
            conn.close()

    def delete(self):
        if self.id is None:
            print("Erro: ID do item de estoque não definido para exclusão.")
            return False
        conn = get_db_connection()
        if conn is None: return False
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM itens_estoque WHERE id = %s;", (self.id,))
            conn.commit()
            print(f"Item de estoque ID {self.id} deletado com sucesso!")
            return True
        except Exception as e:
            conn.rollback()
            print(f"Erro ao deletar item de estoque: {e}")
            return False
        finally:
            cursor.close()
            conn.close()


# --- Classe Movimentacao ---
# Registra cada entrada ou saída de um item de estoque.
class Movimentacao:
    def __init__(self, id=None, item_estoque_id=None, tipo_movimentacao=None, quantidade=None, data_movimentacao=None):
        self.id = id
        self.item_estoque_id = item_estoque_id
        self.tipo_movimentacao = tipo_movimentacao
        self.quantidade = quantidade
        self.data_movimentacao = data_movimentacao if data_movimentacao else datetime.datetime.now()

    def save(self):
        conn = get_db_connection()
        if conn is None: return False
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                INSERT INTO movimentacoes (item_estoque_id, tipo_movimentacao, quantidade, data_movimentacao)
                VALUES (%s, %s, %s, %s) RETURNING id;
                """,
                (self.item_estoque_id, self.tipo_movimentacao, self.quantidade, self.data_movimentacao)
            )
            self.id = cursor.fetchone()[0]
            conn.commit()
            print(f"Movimentação ID {self.id} salva com sucesso!")
            return True
        except Exception as e:
            conn.rollback()
            print(f"Erro ao salvar movimentação: {e}")
            return False
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_all():
        conn = get_db_connection()
        if conn is None: return []
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                SELECT
                    m.id, m.tipo_movimentacao, m.quantidade, m.data_movimentacao,
                    ie.lote, p.nome, e.corredor, e.prateleira, e.nivel, e.posicao
                FROM movimentacoes m
                JOIN itens_estoque ie ON m.item_estoque_id = ie.id
                JOIN produtos p ON ie.produto_id = p.id
                JOIN enderecos e ON ie.endereco_id = e.id
                ORDER BY m.data_movimentacao DESC;
                """
            )
            movimentacoes_data = cursor.fetchall()
            return [
                {
                    'id': m[0],
                    'tipo': m[1],
                    'quantidade': m[2],
                    'data': m[3],
                    'lote': m[4],
                    'produto_nome': m[5],
                    'endereco_completo': f"{m[6]}-{m[7]}-{m[8]}-{m[9]}"
                }
                for m in movimentacoes_data
            ]
        except Exception as e:
            print(f"Erro ao buscar movimentações: {e}")
            return []
        finally:
            cursor.close()
            conn.close()