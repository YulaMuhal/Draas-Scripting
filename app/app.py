from flask import Flask, request, render_template
import psycopg2
import bcrypt
import os

app = Flask(__name__)

# Pegando dados do Supabase a partir de variáveis de ambiente
DB_HOST = os.environ.get('DB_HOST')
DB_NAME = os.environ.get('DB_NAME')
DB_USER = os.environ.get('DB_USER')
DB_PASS = os.environ.get('DB_PASS')

conn = psycopg2.connect(
    host=DB_HOST,
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASS
)

@app.route('/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        consentimento = request.form.get('consentimento')

        if not consentimento:
            return "É necessário aceitar a política de privacidade."

        senha_hash = bcrypt.hashpw(senha.encode(), bcrypt.gensalt())

        cur = conn.cursor()
        cur.execute("INSERT INTO usuarios (nome, email, senha) VALUES (%s, %s, %s)", (nome, email, senha_hash))
        conn.commit()
        cur.close()
        return "Usuário registrado com sucesso!"

    return render_template('form.html')
