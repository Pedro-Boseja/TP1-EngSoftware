from .classUsuario import Usuario
import pymysql
import config

class Aluno(Usuario):
    def __init__(self, email, senha, nome, matricula):
        """
        Inicializa a instância da classe Aluno, que herda de Usuario.
        O atributo 'type' é automaticamente definido como 3 para Aluno.
        """
        super().__init__(email, senha, tipo=3)
        self.__nome = nome
        self.__matricula = matricula

    def salvar_no_banco(self):
        """
        Salva o aluno no banco de dados MySQL via PyMySQL.
        """
        try:
            conn = pymysql.connect(
                host='localhost',
                user='root',
                password=config.senha_banco,
                database='sistema_avaliacao',
                cursorclass=pymysql.cursors.DictCursor
            )
            cursor = conn.cursor()

            # Cria a tabela se não existir
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS sistema_avaliacao.Alunos (
                    email VARCHAR(255) PRIMARY KEY,
                    senha VARCHAR(255) NOT NULL,
                    nome VARCHAR(255) NOT NULL,
                    matricula VARCHAR(50) NOT NULL,
                    tipo INT NOT NULL
                )
            ''')

            if self._is_email_ja_cadastrado(self.get_email()):
                return False

            # Insere o aluno
            cursor.execute('''
                INSERT INTO sistema_avaliacao.Alunos (email, senha, nome, matricula, tipo)
                VALUES (%s, %s, %s, %s, %s)
            ''', (
                self.get_email(),
                self.get_senha(),
                self.get_nome(),
                self.get_matricula(),
                self.get_type()
            ))

            conn.commit()
            return True  # sucesso
        except Exception as e:
            return False
        finally:
            conn.close()

    def get_nome(self):
        return self.__nome

    def get_matricula(self):
        return self.__matricula
    
    def _is_email_ja_cadastrado(self, email):
        """
        Verifica se o email já existe no banco de dados.
        """
        conn = pymysql.connect(
            host='localhost',
            user='root',
            password=config.senha_banco,
            database='sistema_avaliacao',
            cursorclass=pymysql.cursors.DictCursor
        )
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM sistema_avaliacao.Alunos WHERE email = %s', (email,))
        result = cursor.fetchone()
        conn.close()
        return result is not None

    def __repr__(self):
        return f"Aluno(email={self.get_email()}, nome={self.__nome}, matricula={self.__matricula}, tipo={self.get_type()})"
