from flask import Flask, render_template, request, session, redirect, url_for
import pymysql
from Models.Classes.classAdmin import Admin  # ✅ Import corrigido

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta'

# Função para conectar ao banco
def conectar_banco():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='senha',
        database='sistema_avaliacao',
        cursorclass=pymysql.cursors.DictCursor
    )


def verificar_usuario(email, senha):
    """
    Verifica se o email e senha correspondem a um usuário. Retorna o tipo do usuário se encontrado.
    """
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute("SELECT tipo FROM sistema_avaliacao.Administradores WHERE email = %s AND senha = %s", (email, senha))
    usuario = cursor.fetchone()
    conn.close()

    if usuario:
        return usuario['tipo']
    return None


@app.route('/')
def home():
    return render_template('index.html', session=session)

@app.route('/login')
def login():
    return render_template('login.html', session=session)

@app.route('/disciplinas')
def disciplinas():
    return render_template('disciplinas.html', session=session)

@app.route('/professores')
def professores():
    return render_template('professores.html', session=session)

@app.route('/acesso', methods=['POST'])
def acesso():
    email = request.form.get('email')
    senha = request.form.get('senha')

    tipo_usuario = verificar_usuario(email, senha)

    if tipo_usuario:
        session["email"] = email
        session["tipo"] = tipo_usuario
        return render_template("index.html", session=session)
    else:
        return render_template("login.html", error="Usuário ou senha inválidos.")

@app.route('/cadastrar_admin', methods=['GET', 'POST'])
def cadastrar_admin():
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')
        novo_admin = Admin(email=email, senha=senha)  # Admin já salva no banco no __init__
        return render_template('cadastrar_admin.html', sucesso=True)

    return render_template('cadastrar_admin.html')


@app.route('/usuarios')
def listar_usuarios():
    tipo_filtro = request.args.get('tipo')
    conn = conectar_banco()
    cursor = conn.cursor()

    if tipo_filtro and tipo_filtro in ['1', '2', '3']:
        cursor.execute("SELECT email, tipo FROM sistema_avaliacao.Professores UNION ALL SELECT email, tipo FROM sistema_avaliacao.Alunos UNION ALL SELECT email, tipo FROM sistema_avaliacao.Administradores")
    else:
        cursor.execute("SELECT email, tipo FROM sistema_avaliacao.Professores UNION ALL SELECT email, tipo FROM sistema_avaliacao.Alunos UNION ALL SELECT email, tipo FROM sistema_avaliacao.Administradores")

    usuarios = cursor.fetchall()
    conn.close()

    return render_template('usuarios.html', usuarios=usuarios, tipo_selecionado=tipo_filtro, session=session)


@app.route('/editar_usuario/<email>', methods=['GET', 'POST'])
def editar_usuario(email):
    if request.method == 'POST':
        nova_senha = request.form.get('senha')

        conn = conectar_banco()
        cursor = conn.cursor()
        cursor.execute("UPDATE usuarios SET senha = %s WHERE email = %s", (nova_senha, email))
        conn.commit()
        conn.close()

        return redirect(url_for('listar_usuarios'))

    return render_template('editar_usuario.html', email=email, session=session)


@app.route('/excluir_usuario/<email>', methods=['POST'])
def excluir_usuario(email):
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM usuarios WHERE email = %s", (email,))
    conn.commit()
    conn.close()

    return redirect(url_for('listar_usuarios'))


@app.route('/logout')
def sair():
    session.clear()
    return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(debug=True)
