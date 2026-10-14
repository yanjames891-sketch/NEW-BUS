from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Configuração e inicialização do banco de dados
def init_db():
    conn = sqlite3.connect('veiculos.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS veiculos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            modelo TEXT NOT NULL,
            marca TEXT NOT NULL,
            ano INTEGER NOT NULL,
            placa TEXT NOT NULL UNIQUE,
            preco REAL NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Rota Principal: Exibe formulário e lista de veículos
@app.route('/')
def index():
    conn = sqlite3.connect('veiculos.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM veiculos ORDER BY id DESC')
    veiculos = cursor.fetchall()
    conn.close()
    return render_template('index.html', veiculos=veiculos)

# Rota para Cadastrar Veículo
@app.route('/cadastrar', methods=['POST'])
def cadastrar():
    modelo = request.form['modelo']
    marca = request.form['marca']
    ano = request.form['ano']
    placa = request.form['placa']
    preco = request.form['preco']

    conn = sqlite3.connect('veiculos.db')
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO veiculos (modelo, marca, ano, placa, preco)
            VALUES (?, ?, ?, ?, ?)
        ''', (modelo, marca, ano, placa, preco))
        conn.commit()
    except sqlite3.IntegrityError:
        pass  # Evita erro de placa duplicada
    finally:
        conn.close()

    return redirect(url_for('index'))

# Rota para Deletar Veículo
@app.route('/deletar/<int:id>')
def deletar(id):
    conn = sqlite3.connect('veiculos.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM veiculos WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)