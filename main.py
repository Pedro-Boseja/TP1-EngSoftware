from flask import Flask, render_template, request, session, redirect, url_for, flash
import pymysql
from Models.Classes.classAdmin import Admin  
from Models.Classes.classAluno import Aluno  
from Models.Classes.classProfessor import Professor  
from Models.Classes.classDisciplina import Disciplina  

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

# Função para verificar se o usuário existe no banco de dados
def verificar_usuario(email, senha):
    """
    Verifica se o email e senha correspondem a um usuário.
    Retorna o tipo do usuário se encontrado, ou None se não houver correspondência.
    """
    conn = conectar_banco()
    cursor = conn.cursor()

    query = """
        SELECT tipo FROM sistema_avaliacao.Professores WHERE email = %s AND senha = %s
        UNION ALL
        SELECT tipo FROM sistema_avaliacao.Alunos WHERE email = %s AND senha = %s
        UNION ALL
        SELECT tipo FROM sistema_avaliacao.Administradores WHERE email = %s AND senha = %s
    """

    # Como temos 3 blocos WHERE iguais, precisamos passar os parâmetros 3 vezes
    cursor.execute(query, (email, senha, email, senha, email, senha))
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

@app.route('/disciplinas', methods=['GET'])
def listar_disciplinas():
    ordenar = request.args.get('ordenar', 'nome')  # Padrão é ordenar por nome
    conn = conectar_banco()
    cursor = conn.cursor()

    # Filtra as disciplinas com base na ordenação
    if ordenar == 'codigo':
        cursor.execute("SELECT * FROM sistema_avaliacao.Disciplinas ORDER BY codigo ASC")
    else:
        cursor.execute("SELECT * FROM sistema_avaliacao.Disciplinas ORDER BY nome ASC")

    disciplinas = cursor.fetchall()
    conn.close()

    # Verifica se o usuário logado é um administrador
    is_admin = session.get('tipo') == 1  # 1 representa Administrador

    return render_template('disciplinas.html', disciplinas=disciplinas, ordenar=ordenar, session=session, is_admin=is_admin)

@app.route('/editar_disciplina/<codigo>', methods=['GET', 'POST'])
def editar_disciplina(codigo):
    conn = conectar_banco()
    cursor = conn.cursor()

    # Busca a disciplina com o código fornecido
    cursor.execute("SELECT * FROM sistema_avaliacao.Disciplinas WHERE codigo = %s", (codigo,))
    disciplina = cursor.fetchone()
    conn.close()

    if not disciplina:
        flash('Disciplina não encontrada.', 'error')
        return redirect(url_for('listar_disciplinas'))

    if request.method == 'POST':
        # Atualiza os dados da disciplina
        nome = request.form.get('nome')
        cursor.execute("UPDATE sistema_avaliacao.Disciplinas SET nome = %s WHERE codigo = %s", (nome, codigo))
        conn.commit()
        conn.close()
        flash('Disciplina atualizada com sucesso!', 'success')
        return redirect(url_for('listar_disciplinas'))

    return render_template('editar_disciplina.html', disciplina=disciplina)

@app.route('/excluir_disciplina/<codigo>')
def excluir_disciplina(codigo):
    Disciplina.excluir_disciplina(codigo)
    return redirect(url_for('disciplinas'))

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
        
        novo_admin = Admin(email=email, senha=senha)
        sucesso = novo_admin.salvar_no_banco()

        if sucesso:
            return render_template('cadastrar_admin.html', sucesso=True)
        else:
            return render_template('cadastrar_admin.html', erro="Erro ao cadastrar administrador. Verifique se o e-mail já está cadastrado.")

    return render_template('cadastrar_admin.html')

@app.route('/cadastrar_aluno', methods=['GET', 'POST'])
def cadastrar_aluno():
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')
        nome = request.form.get('nome')
        matricula = request.form.get('matricula')

        novo_aluno = Aluno(email=email, senha=senha, nome=nome, matricula=matricula) 
        sucesso = novo_aluno.salvar_no_banco()

        if sucesso:
            return render_template('cadastrar_aluno.html', sucesso=True)
        else:
            return render_template('cadastrar_aluno.html', erro="Erro ao cadastrar aluno. Verifique se o e-mail já está cadastrado.")
        
    return render_template('cadastrar_aluno.html')

@app.route('/cadastrar_professor', methods=['GET', 'POST'])
def cadastrar_professor():
    if request.method == 'POST':
        nome = request.form.get('nome')
        matricula = request.form.get('matricula')
        email = request.form.get('email')
        senha = request.form.get('senha')

        novo_professor = Professor(nome=nome, matricula=matricula, email=email, senha=senha)
        sucesso = novo_professor.salvar_no_banco()

        if sucesso:
            return render_template('cadastrar_professor.html', sucesso=True)
        else:
            return render_template('cadastrar_professor.html', erro="Erro ao cadastrar professor. Verifique se o e-mail já está cadastrado.")

    return render_template('cadastrar_professor.html')

@app.route('/cadastrar_disciplina', methods=['GET', 'POST'])
def cadastrar_disciplina():
    if request.method == 'POST':
        codigo = request.form.get('codigo')
        nome = request.form.get('nome')
        nova_disciplina = Disciplina(codigo=codigo, nome=nome)
        return render_template('cadastrar_disciplina.html', sucesso=True)
    
    return render_template('cadastrar_disciplina.html')

@app.route('/usuarios')
def listar_usuarios():
    tipo_filtro = request.args.get('tipo')
    conn = conectar_banco()
    cursor = conn.cursor()

    if tipo_filtro in ['1', '2', '3']:
        tipo_filtro = int(tipo_filtro)
        query = """
            SELECT email, tipo FROM sistema_avaliacao.Professores WHERE tipo = %s
            UNION ALL
            SELECT email, tipo FROM sistema_avaliacao.Alunos WHERE tipo = %s
            UNION ALL
            SELECT email, tipo FROM sistema_avaliacao.Administradores WHERE tipo = %s
        """
        cursor.execute(query, (tipo_filtro, tipo_filtro, tipo_filtro))
    else:
        cursor.execute("""
            SELECT email, tipo FROM sistema_avaliacao.Professores
            UNION ALL
            SELECT email, tipo FROM sistema_avaliacao.Alunos
            UNION ALL
            SELECT email, tipo FROM sistema_avaliacao.Administradores
        """)

    usuarios = cursor.fetchall()
    conn.close()

    return render_template('usuarios.html', usuarios=usuarios, tipo_selecionado=tipo_filtro, session=session)

@app.route('/editar_usuario/<email>', methods=['GET', 'POST'])
def editar_usuario(email):
    if request.method == 'POST':
        nova_senha = request.form.get('senha')

        conn = conectar_banco()
        cursor = conn.cursor()
        query = """
            UPDATE sistema_avaliacao.Professores SET senha = %s WHERE email = %s
            UNION ALL
            UPDATE sistema_avaliacao.Alunos SET senha = %s WHERE email = %s
            UNION ALL
            UPDATE sistema_avaliacao.Administradores SET senha = %s WHERE email = %s
        """
        cursor.execute(query, (nova_senha, email))
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
