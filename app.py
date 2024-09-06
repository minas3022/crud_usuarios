from flask import Flask, render_template, request, redirect, url_for, flash
from flask_bcrypt import Bcrypt
import psycopg2

app = Flask(__name__)
app.secret_key = "secret_key"
bcrypt = Bcrypt(app)

# Configuração do banco de dados PostgreSQL
def get_db_connection():
    conn = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="123456",
        host="localhost"
    )
    return conn

# Página inicial (Lista de usuários)
@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM usuarios')
    usuarios = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('index.html', usuarios=usuarios)

# Criar um novo usuário
@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        usuario = request.form['usuario']
        senha = request.form['senha']
        hashed_senha = bcrypt.generate_password_hash(senha).decode('utf-8')

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO usuarios (usuario, senha) VALUES (%s, %s)',
                       (usuario, hashed_senha))
        conn.commit()
        cursor.close()
        conn.close()
        flash('Usuário criado com sucesso!', 'success')
        return redirect(url_for('index'))

    return render_template('create.html')

# Atualizar um usuário
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM usuarios WHERE id = %s', (id,))
    usuario = cursor.fetchone()

    if request.method == 'POST':
        novo_usuario = request.form['usuario']
        nova_senha = request.form['senha']
        hashed_senha = bcrypt.generate_password_hash(nova_senha).decode('utf-8')

        cursor.execute('UPDATE usuarios SET usuario = %s, senha = %s WHERE id = %s',
                       (novo_usuario, hashed_senha, id))
        conn.commit()
        flash('Usuário atualizado com sucesso!', 'success')
        return redirect(url_for('index'))

    cursor.close()
    conn.close()
    return render_template('update.html', usuario=usuario)

# Deletar um usuário
@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM usuarios WHERE id = %s', (id,))
    conn.commit()
    cursor.close()
    conn.close()
    flash('Usuário deletado com sucesso!', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
