from flask import Flask, render_template
from database import get_db_connection # Importa a nossa função de conexão com o banco

app = Flask(__name__)

# Esta é a nossa primeira "rota" ou "endereço" na web.
# Quando alguém acessar a página principal (ex: http://127.0.0.1:5000/),
# essa função será executada.
@app.route('/')
def index():
    # Podemos tentar conectar ao banco de dados aqui para ver se funciona
    conn = get_db_connection()
    if conn:
        conn.close() # Sempre feche a conexão depois de usar!
        db_status = "Conectado ao PostgreSQL com sucesso!"
    else:
        db_status = "Falha ao conectar ao PostgreSQL."

    # render_template busca o arquivo HTML na pasta 'templates'
    return render_template('index.html', db_status=db_status)

# Isso garante que o servidor Flask só rode quando o arquivo app.py for executado diretamente
if __name__ == '__main__':
    app.run(debug=True) # debug=True é ótimo para desenvolvimento, pois reinicia o servidor ao salvar mudanças