from flask import Flask, render_template, send_from_directory, request, redirect, url_for, jsonify, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'chave_secreta'

# Adiciona o ícone nas páginas
@app.route('/favicon.ico')
def favicon():
    return send_from_directory('./static', 'favicon.ico', mimetype='image/vnd.microsoft.icon')

# Página home
@app.route("/")
def home():
    return render_template("index.html")

# Página cadastro do usuário
@app.route("/cadastro")
def cadastro():
    return render_template("cadastro.html")

# Página cadastro de medicamentos
@app.route("/medicamentos")
def medicamentos():
    return render_template("medicamentos.html")

# Página de consulta de medicamentos para doação
@app.route("/consulta")
def consulta():
    # Consulta banco de dados usuario.db
    conn_usuario = sqlite3.connect('usuario.db')
    cursor_usuario = conn_usuario.cursor()
    cursor_usuario.execute('SELECT * FROM usuario')
    usuarios = cursor_usuario.fetchall()
    conn_usuario.close()

    # Consulta banco de dados remedio.db
    conn_remedio = sqlite3.connect('remedio.db')
    cursor_remedio = conn_remedio.cursor()
    cursor_remedio.execute('SELECT * FROM remedio')
    remedios = cursor_remedio.fetchall()
    conn_remedio.close()

    # Exibe os remédios para doação de todos os cadastrados
    return render_template('consulta.html', usuarios=usuarios, remedios=remedios)

# Página de login
@app.route("/login")
def login():
    return render_template("login.html")    

# Página sucesso
@app.route("/sucesso")
def sucesso():
    return render_template("sucesso.html")

# CADASTRO DO USUÁRIO
@app.route('/submit_cadastro', methods=['POST'])
def submit_cadastro():
    nome = request.form['nome']
    email = request.form['email']
    telefone = request.form['telefone']
    senha = request.form['senha']

    # Conecta com SQLite
    conn = sqlite3.connect('usuario.db')
    cursor = conn.cursor()

    # Inserir dados na tabela SQLite.
    cursor.execute('''INSERT INTO usuario (nome, email, telefone, senha)
                      VALUES (?, ?, ?, ?)''', (nome, email, telefone, senha))

    # Commit e fechar conexão
    conn.commit()
    conn.close()
    
    # Redireciona para página medicamentos.html
    return redirect(url_for('medicamentos'))  

# CADASTRO DE MEDICAMENTOS
@app.route('/submit_remedio', methods=['POST'])
def submit_remedio():  
    nome = request.form['nome'].upper()
    quantidade = request.form['quantidade']
    dosagem = request.form['dosagem']
    validade = request.form['validade']
   
    # Pega o ID do usuário para relacionamento do banco de dados usuario.db
    user_id = session.get('usuario_id')   

    # Conecta com SQLite
    conn = sqlite3.connect('remedio.db')
    cursor = conn.cursor()
  
    # Inserir dados na tabela SQLite pegando ID do banco de dados usuario.db
    cursor.execute('''INSERT INTO remedio (usuario_id, nome, quantidade, dosagem, validade)
                      VALUES (?, ?, ?, ?, ?)''', (user_id, nome, quantidade, dosagem, validade))

    # Commit e fechar conexão
    conn.commit()
    conn.close()
    
    # Redireciona para página sucesso.html
    return redirect(url_for('sucesso'))

# LOGIN
@app.route("/submit_login", methods=['POST'])
def submit_login():
    email = request.form['email']
    senha = request.form['senha']

    # Conecta com SQLite
    conn = sqlite3.connect('usuario.db')
    cursor = conn.cursor()

    # Consulta o banco de dados usuario.db
    cursor.execute("SELECT * FROM usuario WHERE email = ? AND senha = ?", (email, senha))
    dados = cursor.fetchall()

    # Se usuário existir, armazena informações na sessão e redireciona
    if dados:
        session['usuario_id'] = dados[0][0]
        session['nome_usuario'] = dados[0][1]
        return redirect(url_for('consulta'))
    else:
        error_msg = "Email ou senha inválidos. Tente novamente."
        return render_template('login.html', error=error_msg)

    conn.close()

# GET DATA
@app.route('/get_data', methods=['GET'])
def get_data():
    conn = sqlite3.connect('remedio.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM remedio')
    data = cursor.fetchall()
    conn.close()
    return jsonify(data)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=9000, debug=True)
