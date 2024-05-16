import sqlite3

# cria banco usuario.db SQlite remedio.db
conexao = sqlite3.connect('remedio.db')

# executar comandos SQL
cursor = conexao.cursor()

# criar a tabela remedio
comando_sql = """
CREATE TABLE IF NOT EXISTS remedio (
    id INTEGER PRIMARY KEY,
    nome TEXT,
    quantidade INTEGER,
    dosagem TEXT,
    validade DATE,
    usuario_id INTEGER,
    FOREIGN KEY (usuario_id) REFERENCES usuario(id)
)
"""
# executar o comando SQL
cursor.execute(comando_sql)

# fechar a conexão
conexao.commit()
conexao.close()
