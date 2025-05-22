
# 📦 WMS Project - Sistema de Gerenciamento de Armazém

Bem-vindo ao **WMS Project**, um sistema simples e funcional para gerenciamento de estoque e armazéns. Desenvolvido com **Python (Flask)** e **PostgreSQL**, este projeto tem como objetivo oferecer uma base robusta para:

- ✅ Controle de produtos
- ✅ Gestão de endereços de armazenamento
- ✅ Acompanhamento de estoque e validade
- ✅ Registro de movimentações de entrada e saída

---

## 🚀 Funcionalidades (MVP)

- 🏷️ **Gestão de Produtos**
- 🗺️ **Gestão de Endereços**
- 📦 **Gestão de Itens em Estoque**
- 🔄 **Registro de Movimentações**
- 🗄️ **Conexão com PostgreSQL via `.env`**

---

## 🛠️ Tecnologias

- **Backend:** Python 3.x + Flask
- **Banco de Dados:** PostgreSQL
- **Frontend (básico):** HTML + Jinja2
- **Bibliotecas:**
  - `psycopg2-binary`
  - `python-dotenv`

---

## 📂 Estrutura do Projeto

```plaintext
wms_project/
├── venv/                 
├── .env                  
├── app.py                
├── database.py           
├── models.py             
├── create_tables.py      
├── requirements.txt      
├── static/               
│   └── css/
│   └── js/
├── templates/            
│   ├── index.html
│   ├── products.html      (futuro)
│   ├── add_product.html   (futuro)
│   ├── addresses.html     (futuro)
│   └── add_address.html   (futuro)
└── README.md
```

---

## ⚙️ Instalação e Configuração

### ✔️ Pré-requisitos

- **Python 3.x**
- **PostgreSQL** instalado e rodando

---

## 🔽 Instalação do PostgreSQL

### 🔸 **Linux (Ex.: Garuda, Ubuntu, etc.):**

```bash
sudo pacman -S postgresql          # Garuda/Arch
# ou
sudo apt install postgresql         # Ubuntu/Debian

sudo systemctl start postgresql
sudo systemctl enable postgresql
```

### 🔸 **Windows:**

1. Baixe em: [https://www.postgresql.org/download/windows/](https://www.postgresql.org/download/windows/)
2. Durante a instalação, defina:
   - Senha para o usuário `postgres`
   - Porta padrão: `5432`
3. Finalize e deixe o PostgreSQL rodando como serviço no Windows.

---

## 🔗 Clone o repositório

```bash
git clone https://github.com/DioniSouza/wms_project.git
cd wms_project
```

No Windows: use Git Bash, CMD ou PowerShell.

---

## 🏗️ Banco de Dados - Configuração

### 🔸 Acesse o PostgreSQL

- **Linux:**

```bash
sudo -u postgres psql
```

- **Windows:**

Abra o **SQL Shell (psql)** ou use uma interface como **pgAdmin**.

---

### 🔸 Crie o Banco de Dados e Usuário

No terminal SQL:

```sql
CREATE DATABASE wms_db;
CREATE USER wms_user WITH PASSWORD 'sua_senha_secreta';
GRANT ALL PRIVILEGES ON DATABASE wms_db TO wms_user;
\q
```

### 🔸 Permissão no Schema (Ambos)

```sql
GRANT CREATE ON SCHEMA public TO wms_user;
\q
```

---

## 🔐 Configuração do `.env`

Na raiz do projeto, crie um arquivo `.env` com:

```dotenv
DB_HOST=localhost
DB_NAME=wms_db
DB_USER=wms_user
DB_PASSWORD=sua_senha_secreta
DB_PORT=5432
```

---

## 🐍 Ambiente Python

### 🔸 Crie e ative o ambiente virtual:

- **Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

- **Windows (CMD/Powershell):**

```cmd
python -m venv venv
venv\Scriptsctivate
```

---

### 🔸 Instale as dependências:

```bash
pip install -r requirements.txt
```

---

## 🗄️ Criação das Tabelas

### 🔸 Se necessário, remova tabelas existentes:

- **Linux:**

```bash
sudo -u postgres psql -d wms_db
```

- **Windows:**

Abra o **SQL Shell (psql)** e conecte-se ao banco `wms_db`.

Execute em ambos:

```sql
DROP TABLE IF EXISTS movimentacoes CASCADE;
DROP TABLE IF EXISTS itens_estoque CASCADE;
DROP TABLE IF EXISTS produtos CASCADE;
DROP TABLE IF EXISTS enderecos CASCADE;
\q
```

---

### 🔸 Crie as tabelas (Ambos):

```bash
python create_tables.py
```

---

## ▶️ Rodando o Projeto

Ative o ambiente virtual:

- **Linux:**

```bash
source venv/bin/activate
```

- **Windows:**

```cmd
venv\Scriptsctivate
```

Inicie o servidor:

```bash
flask run
# ou
python app.py
```

Acesse no navegador:

```
http://127.0.0.1:5000/
```

---

## 🗺️ Roadmap (Próximos passos)

- [ ] CRUD completo para Produtos
- [ ] CRUD completo para Endereços
- [ ] Interface frontend mais amigável (CSS/JS)
- [ ] Busca e filtros
- [ ] Autenticação de usuários
- [ ] Dashboard com métricas

---

## 🤝 Contribuindo

Contribuições são muito bem-vindas! Abra uma issue ou envie um pull request. ✨

---

## 📜 Licença

Distribuído sob a licença MIT.

---

## 👨‍💻 Autor

**Dioni Souza**

- 💼 [LinkedIn](https://www.linkedin.com/in/dioni-souza/)
- 🖥️ [GitHub](https://github.com/DioniSouza)

---
