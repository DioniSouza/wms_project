# app.py

from flask import Flask, render_template, request, redirect, url_for, flash
from database import get_db_connection
from models import Produto, Endereco, ItemEstoque,Movimentacao# Importa a classe Produto do nosso models.py (renomeado)
import datetime

app = Flask(__name__)
app.secret_key = 'Leao2025' # Necessário para usar flash messages

# Rota principal (já existente)
@app.route('/')
def index():
    conn = get_db_connection()
    if conn:
        conn.close()
        db_status = "Conectado ao PostgreSQL com sucesso!"
    else:
        db_status = "Falha ao conectar ao PostgreSQL."
    return render_template('index.html', db_status=db_status)

# --- ROTAS PARA PRODUTOS ---

# Rota para listar todos os produtos
@app.route('/produtos')
def listar_produtos():
    produtos = Produto.get_all() # Pega todos os produtos usando o método do models.py
    return render_template('products.html', produtos=produtos)

# Rota para exibir o formulário de cadastro de novo produto
@app.route('/produtos/novo', methods=['GET', 'POST'])
def adicionar_produto():
    if request.method == 'POST':
        # Se o método for POST, o formulário foi enviado
        nome = request.form['nome']
        sku = request.form['sku']
        unidade_medida = request.form['unidade_medida']
        codigo_barras = request.form['codigo_barras']

        # Cria um novo objeto Produto com os dados do formulário
        novo_produto = Produto(nome=nome, sku=sku, unidade_medida=unidade_medida, codigo_barras=codigo_barras)

        # Tenta salvar o produto no banco de dados
        if novo_produto.save():
            flash('Produto adicionado com sucesso!', 'success') # Mensagem de sucesso
            return redirect(url_for('listar_produtos')) # Redireciona para a lista de produtos
        else:
            flash('Erro ao adicionar produto. Verifique os dados.', 'danger') # Mensagem de erro

    # Se o método for GET, exibe o formulário vazio
    return render_template('add_product.html')

# Isso garante que o servidor Flask só rode quando o arquivo app.py for executado diretamente
if __name__ == '__main__':
    app.run(debug=True)

    # --- Rotas para Endereços ---

# Rota para listar todos os endereços
@app.route('/enderecos')
def listar_enderecos():
    enderecos = Endereco.get_all()
    return render_template('addresses.html', enderecos=enderecos)

# Rota para exibir o formulário de novo endereço e processar a adição
@app.route('/enderecos/novo', methods=['GET', 'POST'])
def adicionar_endereco():
    if request.method == 'POST':
        # Pega os dados do formulário
        corredor = request.form['corredor'].strip()
        prateleira = request.form['prateleira'].strip()
        nivel = request.form['nivel'].strip()
        posicao = request.form['posicao'].strip()

        # Validação básica
        if not corredor or not prateleira:
            flash('Corredor e Prateleira são campos obrigatórios!', 'error')
            return render_template('add_address.html',
                                   corredor=corredor, prateleira=prateleira,
                                   nivel=nivel, posicao=posicao)

        # Cria um novo objeto Endereco
        novo_endereco = Endereco(
            corredor=corredor,
            prateleira=prateleira,
            nivel=nivel,
            posicao=posicao
        )

        # Tenta salvar o endereço no banco de dados
        if novo_endereco.save():
            flash('Endereço adicionado com sucesso!', 'success')
            return redirect(url_for('listar_enderecos')) # Redireciona para a lista
        else:
            flash('Erro ao adicionar endereço. Verifique o log do servidor.', 'error')
            return render_template('add_address.html',
                                   corredor=corredor, prateleira=prateleira,
                                   nivel=nivel, posicao=posicao)
    # Se for GET, apenas exibe o formulário vazio
    return render_template('add_address.html')
# --- Rotas para Itens de Estoque ---

# Rota para listar todos os itens de estoque
@app.route('/estoque')
def listar_itens_estoque():
    itens_estoque = ItemEstoque.get_all()
    return render_template('stock_items.html', itens_estoque=itens_estoque)

# Rota para exibir o formulário de novo item de estoque (GET) e processar a adição (POST)
@app.route('/estoque/novo', methods=['GET', 'POST'])
def adicionar_item_estoque():
    # Precisamos buscar todos os produtos e endereços existentes para os dropdowns
    produtos = Produto.get_all()
    enderecos = Endereco.get_all()

    if request.method == 'POST':
        produto_id = request.form['produto_id']
        endereco_id = request.form['endereco_id']
        lote = request.form['lote'].strip()
        quantidade = request.form['quantidade'].strip()
        data_validade_str = request.form['data_validade'].strip()

        # Validação básica
        if not produto_id or not endereco_id or not lote or not quantidade:
            flash('Produto, Endereço, Lote e Quantidade são campos obrigatórios!', 'error')
            return render_template('add_stock_item.html',
                                   produtos=produtos, enderecos=enderecos,
                                   produto_id=produto_id, endereco_id=endereco_id,
                                   lote=lote, quantidade=quantidade,
                                   data_validade=data_validade_str)
        try:
            quantidade = int(quantidade)
            if quantidade <= 0:
                flash('A quantidade deve ser um número inteiro positivo.', 'error')
                raise ValueError("Quantidade inválida")
        except ValueError:
            flash('A quantidade deve ser um número válido.', 'error')
            return render_template('add_stock_item.html',
                                   produtos=produtos, enderecos=enderecos,
                                   produto_id=produto_id, endereco_id=endereco_id,
                                   lote=lote, quantidade=request.form['quantidade'].strip(), # Usa a string original para preencher o campo
                                   data_validade=data_validade_str)

        data_validade = None
        if data_validade_str:
            try:
                data_validade = datetime.datetime.strptime(data_validade_str, '%Y-%m-%d').date()
            except ValueError:
                flash('Formato de data de validade inválido. Use AAAA-MM-DD.', 'error')
                return render_template('add_stock_item.html',
                                       produtos=produtos, enderecos=enderecos,
                                       produto_id=produto_id, endereco_id=endereco_id,
                                       lote=lote, quantidade=quantidade,
                                       data_validade=data_validade_str)

        novo_item = ItemEstoque(
            produto_id=produto_id,
            endereco_id=endereco_id,
            lote=lote,
            quantidade=quantidade,
            data_validade=data_validade
        )

        if novo_item.save():
            flash('Item de estoque adicionado com sucesso!', 'success')
            return redirect(url_for('listar_itens_estoque'))
        else:
            flash('Erro ao adicionar item de estoque. Verifique o log do servidor.', 'error')
            return render_template('add_stock_item.html',
                                   produtos=produtos, enderecos=enderecos,
                                   produto_id=produto_id, endereco_id=endereco_id,
                                   lote=lote, quantidade=quantidade,
                                   data_validade=data_validade_str)
    # Se for GET, apenas exibe o formulário vazio
    return render_template('add_stock_item.html', produtos=produtos, enderecos=enderecos)

# --- Rotas para Movimentações ---

# Rota para listar todas as movimentações
@app.route('/movimentacoes')
def listar_movimentacoes():
    movimentacoes = Movimentacao.get_all()
    return render_template('movimentacoes.html', movimentacoes=movimentacoes)

# Rota para exibir o formulário de nova movimentação (GET) e processar a movimentação (POST)
@app.route('/movimentacoes/novo', methods=['GET', 'POST'])
def adicionar_movimentacao():
    # Precisamos buscar todos os itens de estoque existentes para o dropdown
    # O get_all() de ItemEstoque já retorna o nome do produto e endereço completo
    itens_estoque = ItemEstoque.get_all()

    if request.method == 'POST':
        item_estoque_id = request.form['item_estoque_id']
        tipo_movimentacao = request.form['tipo_movimentacao']
        quantidade_str = request.form['quantidade'].strip()

        # Validação básica
        if not item_estoque_id or not tipo_movimentacao or not quantidade_str:
            flash('Todos os campos são obrigatórios!', 'error')
            return render_template('add_movimentacao.html',
                                   itens_estoque=itens_estoque,
                                   item_estoque_id=item_estoque_id,
                                   tipo_movimentacao=tipo_movimentacao,
                                   quantidade=quantidade_str)
        try:
            quantidade = int(quantidade_str)
            if quantidade <= 0:
                flash('A quantidade deve ser um número inteiro positivo.', 'error')
                raise ValueError("Quantidade inválida")
        except ValueError:
            flash('A quantidade deve ser um número válido.', 'error')
            return render_template('add_movimentacao.html',
                                   itens_estoque=itens_estoque,
                                   item_estoque_id=item_estoque_id,
                                   tipo_movimentacao=tipo_movimentacao,
                                   quantidade=quantidade_str)

        # Buscar o item de estoque para verificar a quantidade atual
        # Precisamos de um método para buscar ItemEstoque por ID.
        # Vamos adicionar um get_by_id na classe ItemEstoque no models.py se não tiver
        # Por enquanto, faremos uma busca simples:
        selected_item = None
        for item in itens_estoque:
            if str(item['id']) == item_estoque_id: # item['id'] é int, item_estoque_id é string
                selected_item = item
                break

        if not selected_item:
            flash('Item de estoque selecionado inválido.', 'error')
            return render_template('add_movimentacao.html',
                                   itens_estoque=itens_estoque,
                                   item_estoque_id=item_estoque_id,
                                   tipo_movimentacao=tipo_movimentacao,
                                   quantidade=quantidade_str)

        current_quantity = selected_item['quantidade']
        new_quantity = current_quantity

        if tipo_movimentacao == 'SAIDA':
            if quantidade > current_quantity:
                flash(f'Quantidade de saída ({quantidade}) excede a quantidade atual em estoque ({current_quantity}).', 'error')
                return render_template('add_movimentacao.html',
                                       itens_estoque=itens_estoque,
                                       item_estoque_id=item_estoque_id,
                                       tipo_movimentacao=tipo_movimentacao,
                                       quantidade=quantidade_str)
            new_quantity = current_quantity - quantidade
        elif tipo_movimentacao == 'ENTRADA':
            new_quantity = current_quantity + quantidade

        # Salvar a movimentação
        nova_movimentacao = Movimentacao(
            item_estoque_id=item_estoque_id,
            tipo_movimentacao=tipo_movimentacao,
            quantidade=quantidade
        )

        # Efetuar a atualização da quantidade no estoque
        # Para isso, precisamos criar um objeto ItemEstoque real com o ID
        from models import ItemEstoque # Re-importar para usar o get_by_id se não estiver já no escopo

        # Vamos adicionar um get_by_id na classe ItemEstoque para facilitar isso.
        # (No models.py que te passei anteriormente, não tinha get_by_id para ItemEstoque.
        # Vamos adicionar um get_by_id para ItemEstoque no models.py primeiro, se não tiver!)
        # Se já tiver, ignore o comentário acima.

        # Buscando o objeto ItemEstoque para chamar o método update_quantity
        item_para_atualizar = ItemEstoque.get_by_id(item_estoque_id) # Precisamos deste método!

        if item_para_atualizar and nova_movimentacao.save():
            if item_para_atualizar.update_quantity(new_quantity):
                flash(f'Movimentação de {tipo_movimentacao} de {quantidade} unidades registrada e estoque atualizado com sucesso!', 'success')
                return redirect(url_for('listar_movimentacoes'))
            else:
                flash('Erro ao atualizar quantidade do estoque. Movimentação registrada, mas estoque não atualizado.', 'error')
        else:
            flash('Erro ao registrar movimentação. Verifique o log do servidor.', 'error')

        return render_template('add_movimentacao.html',
                               itens_estoque=itens_estoque,
                               item_estoque_id=item_estoque_id,
                               tipo_movimentacao=tipo_movimentacao,
                               quantidade=quantidade_str)

    # Se for GET, apenas exibe o formulário vazio
    return render_template('add_movimentacao.html', itens_estoque=itens_estoque)    