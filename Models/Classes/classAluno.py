from .classUsuario import Usuario
import pymysql

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
                password='senha',
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
        except pymysql.err.IntegrityError:
            print(f"Aluno com email '{self.get_email()}' já existe.")
            return False
        except Exception as e:
            print(f"Erro ao salvar aluno no banco: {e}")
            return False
        finally:
            conn.close()

    def get_nome(self):
        return self.__nome

    def get_matricula(self):
        return self.__matricula

    def __repr__(self):
        return f"Aluno(email={self.get_email()}, nome={self.__nome}, matricula={self.__matricula}, tipo={self.get_type()})"
