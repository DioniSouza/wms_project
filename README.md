# WMS Project (Sistema de Gerenciamento de Armazém)

Este é um projeto de um Sistema de Gerenciamento de Armazém (WMS - Warehouse Management System) desenvolvido com Flask e PostgreSQL. O objetivo é fornecer uma base sólida para rastrear produtos, gerenciar endereços de estoque, controlar itens em estoque com suas quantidades e validades, e registrar todas as movimentações.

---

## 🚀 Funcionalidades Atuais (MVP - Minimum Viable Product)

* **Gestão de Produtos:**
    * Cadastro de novos produtos com nome, SKU, unidade de medida e código de barras.
    * Listagem de todos os produtos cadastrados.
    * Edição e exclusão de produtos (futuro).
* **Gestão de Endereços:**
    * Cadastro de novos endereços de estoque (corredor, prateleira, nível, posição).
    * Listagem de todos os endereços cadastrados.
    * Edição e exclusão de endereços (futuro).
* **Gestão de Itens em Estoque:**
    * Registro de itens específicos em um determinado endereço (lote, quantidade, validade, etc.).
    * Visibilidade do estoque atual.
* **Registro de Movimentações:**
    * Log de todas as entradas e saídas de itens do estoque.
* **Conectividade com PostgreSQL:** Utiliza `psycopg2` para interagir diretamente com o banco de dados.
* **Variáveis de Ambiente:** Configuração segura do banco de dados via arquivo `.env`.

---

## 🛠️ Tecnologias Utilizadas

* **Backend:** Python 3.x
    * **Framework Web:** Flask
    * **Conexão com Banco de Dados:** `psycopg2-binary`
    * **Variáveis de Ambiente:** `python-dotenv`
* **Banco de Dados:** PostgreSQL
* **Frontend (básico):** HTML, Jinja2 (para templates Flask)
* **Ambiente de Desenvolvimento:**
    * Ambiente Virtual Python (`venv`)
    ---

    wms_project/
├── venv/                 # Ambiente virtual Python
├── .env                  # Variáveis de ambiente (credenciais do banco de dados)
├── app.py                # Aplicação Flask principal e rotas
├── database.py           # Módulo para gerenciar a conexão com o banco de dados
├── models.py             # Definição dos modelos de dados (classes Python que mapeiam as tabelas do DB)
├── create_tables.py      # Script para criar as tabelas no PostgreSQL
├── requirements.txt      # Dependências do projeto Python
├── static/               # Arquivos estáticos (CSS, JS, imagens - futuro)
│   └── css/
│   └── js/
└── templates/            # Arquivos de template HTML
└── index.html        # Página inicial
└── products.html     # Página para listar produtos (futuro)
└── add_product.html  # Página para adicionar produto (futuro)
└── addresses.html    # Página para listar endereços (futuro)
└── add_address.html  # Página para adicionar endereço (futuro)

* **`app.py`**: O coração da aplicação Flask. Define as rotas (URLs) e as funções que respondem a essas rotas, renderizando os templates HTML e interagindo com os modelos de dados.
* **`database.py`**: Encapsula a lógica de conexão com o PostgreSQL, lendo as credenciais do `.env`. Isso garante que a lógica de conexão seja centralizada e reutilizável.
* **`models.py`**: Define as classes Python (`Produto`, `Endereco`, `ItemEstoque`, `Movimentacao`) que representam as tabelas no banco de dados. Cada classe contém métodos para operações CRUD (Create, Read, Update, Delete) básicas, facilitando a interação com o PostgreSQL de forma orientada a objetos. **Já inclui a implementação para o campo `codigo_barras` nos métodos da classe `Produto`.**
* **`create_tables.py`**: Um script autônomo para inicializar o esquema do banco de dados. Ele contém os comandos SQL DDL (Data Definition Language) para criar todas as tabelas necessárias, **incluindo a coluna `codigo_barras` na tabela `produtos`**.
* **`.env`**: Armazena informações sensíveis, como as credenciais do banco de dados, fora do código-fonte para segurança e fácil configuração em diferentes ambientes.
* **`templates/`**: Contém os arquivos HTML que o Flask renderiza e envia para o navegador do usuário.
* **`static/`**: Destinado a arquivos estáticos como CSS, JavaScript e imagens para estilizar e adicionar interatividade ao frontend.

---

## ⚙️ Configuração e Instalação

Siga os passos abaixo para configurar e rodar o projeto em seu ambiente.

### 1. Pré-requisitos

* **Python 3.x** (verifique com `python3 --version`)
* **PostgreSQL** instalado e rodando em sua máquina.
    * No Garuda Linux, você pode instalá-lo via Pacman: `sudo pacman -S postgresql`
    * Inicie e habilite o serviço:
        ```bash
        sudo systemctl start postgresql
        sudo systemctl enable postgresql
        ```

### 2. Clonar o Repositório (se for o caso)

Se este projeto estiver em um repositório Git, clone-o:

```bash
git clone [https://github.com/seu-usuario/wms_project.git](https://github.com/seu-usuario/wms_project.git)
cd wms_project

Configurar o Banco de Dados PostgreSQL
3.1. Criar o Usuário e o Banco de Dados
Conecte-se ao PostgreSQL como o usuário padrão postgres (que tem privilégios de superusuário) e crie o banco de dados e um usuário específico para o projeto.

Bash

sudo -u postgres psql
Dentro do prompt postgres=#, execute os seguintes comandos:

SQL

CREATE DATABASE wms_db;
CREATE USER wms_user WITH PASSWORD 'sua_senha_secreta'; -- Escolha uma senha forte!
GRANT ALL PRIVILEGES ON DATABASE wms_db TO wms_user;
\q
wms_db: Nome do banco de dados do projeto.
wms_user: Nome do usuário que o aplicativo Flask usará para se conectar.
sua_senha_secreta: A senha para o wms_user. Anote-a, você precisará dela no próximo passo.
3.2. Conceder Permissões de Criação no Schema public
O wms_user precisa de permissão para criar tabelas no schema padrão public do wms_db.

Bash

sudo -u postgres psql -d wms_db
Dentro do prompt wms_db=#, execute:

SQL

GRANT CREATE ON SCHEMA public TO wms_user;
\q
4. Configurar Variáveis de Ambiente (.env)
Crie um arquivo chamado .env na raiz do projeto (wms_project/). Este arquivo conterá as credenciais do seu banco de dados.

# .env
DB_HOST=localhost
DB_NAME=wms_db
DB_USER=wms_user
DB_PASSWORD=sua_senha_secreta # Use a mesma senha que você definiu acima
DB_PORT=5432
5. Configurar o Ambiente Python
5.1. Criar e Ativar o Ambiente Virtual
É altamente recomendável usar um ambiente virtual para isolar as dependências do projeto.

Bash

python3 -m venv venv
source venv/bin/activate
(Você verá (venv) no seu prompt do terminal, indicando que o ambiente virtual está ativo.)

5.2. Instalar Dependências
Com o ambiente virtual ativado, instale as bibliotecas necessárias:

Bash

pip install -r requirements.txt
6. Criar/Atualizar as Tabelas do Banco de Dados
Agora que o banco de dados e o ambiente Python estão configurados, você pode criar (ou recriar, se o esquema mudou) as tabelas.

Importante: Se você modificou o esquema das tabelas (como adicionar a coluna codigo_barras), é essencial remover as tabelas existentes e recriá-las para que as mudanças sejam aplicadas. Isso apagará todos os dados existentes.

Remover tabelas existentes (necessário se o esquema mudou ou na primeira configuração):

Bash

sudo -u postgres psql -d wms_db
Dentro do prompt wms_db=#, execute:

SQL

DROP TABLE IF EXISTS movimentacoes CASCADE;
DROP TABLE IF EXISTS itens_estoque CASCADE;
DROP TABLE IF EXISTS produtos CASCADE;
DROP TABLE IF EXISTS enderecos CASCADE;
\q
Criar as tabelas (com o ambiente virtual ativado):

Bash

python create_tables.py
Você deverá ver a mensagem de sucesso indicando que as tabelas foram criadas.

▶️ Como Rodar o Projeto
Certifique-se de que o ambiente virtual está ativado:

Bash

source venv/bin/activate
Inicie o servidor Flask:

Bash

flask run
# Ou:
# python app.py
Você verá uma mensagem indicando que o servidor está rodando, geralmente em http://127.0.0.1:5000/.

Acesse a aplicação no seu navegador:
Abra seu navegador e vá para http://127.0.0.1:5000/.

🤝 Contribuição
Contribuições são bem-vindas! Se você tiver sugestões, melhorias ou encontrar bugs, sinta-se à vontade para abrir uma issue ou enviar um pull request.

📜 Licença
Este projeto é distribuído sob a licença MIT License.

📧 Contato
Se tiver alguma dúvida, entre em contato:
Dioni Souza - 