-- Criando o schema
CREATE SCHEMA IF NOT EXISTS sistema_avaliacao
DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Selecionando o schema criado
USE sistema_avaliacao;

-- Criando a Tabela Alunos
CREATE TABLE IF NOT EXISTS Alunos (
    matricula INT NOT NULL,
    nome VARCHAR(100) NOT NULL,
    tipo INT NOT NULL,
    email VARCHAR(100) NOT NULL,
    senha VARCHAR(100) NOT NULL,
    PRIMARY KEY (matricula)
);

-- Criando a Tabela Professores
CREATE TABLE IF NOT EXISTS Professores (
    matricula INT NOT NULL,
    nome VARCHAR(100) NOT NULL,
	tipo INT NOT NULL,
    email VARCHAR(100) NOT NULL,
    senha VARCHAR(100) NOT NULL,
    PRIMARY KEY (matricula)
);

-- Criando a Tabela Administradores
CREATE TABLE IF NOT EXISTS Administradores (
	email VARCHAR(100) NOT NULL,
    tipo INT NOT NULL,
    senha VARCHAR(100) NOT NULL,
    PRIMARY KEY (email)
);

-- Criando a Tabela Disciplinas
CREATE TABLE IF NOT EXISTS Disciplinas (
    codigo VARCHAR(6) NOT NULL,
    nome VARCHAR(100) NOT NULL,
    PRIMARY KEY (codigo)
);

-- Criando a Tabela AvaliacaoDisciplinas
CREATE TABLE IF NOT EXISTS AvaliacaoDisciplinas (
    id INT NOT NULL AUTO_INCREMENT,
    codigo VARCHAR(6) NOT NULL,
    nota INT NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (codigo) REFERENCES Disciplinas(codigo) ON DELETE CASCADE
);

-- Criando a Tabela AvaliacaoProfessores
CREATE TABLE IF NOT EXISTS AvaliacaoProfessores (
    id INT NOT NULL AUTO_INCREMENT,
    matricula INT NOT NULL,
    nota INT NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (matricula) REFERENCES Professores(matricula) ON DELETE CASCADE
);

-- Inserindo dados iniciais para professores
INSERT INTO Professores (matricula, nome, tipo, email, senha) VALUES
(1001, 'Carlos Mendes', 2, 'carlosmendes@ufmg.br','cmendes'),
(1002, 'Ana Silva', 2, 'anasilva@ufmg.br','asilva'),
(1003, 'Ricardo Oliveira', 2, 'ricardooliveira@ufmg.br','roliveira'),
(1004, 'Fernanda Costa', 2, 'fernandacosta@ufmg.br','fcosta'),
(1005, 'Marcos Andrade', 2, 'marcosandrade@ufmg.br','mandrade');

-- Inserindo dados iniciais para alunos
INSERT INTO Alunos (matricula, nome, tipo, email, senha) VALUES
(2001, 'João Santos', 3, 'joaosantos@ufmg.br','jsantos'),
(2002, 'Maria Lima', 3, 'marialima@ufmg.br','mlima'),
(2003, 'Lucas Almeida', 3, 'lucasalmeida@ufmg.br','lalmeida'),
(2004, 'Beatriz Souza', 3, 'beatrizsouza@ufmg.br','bsouza'),
(2005, 'Gabriel Pereira', 3, 'gabrielpereira@ufmg.br','gpereira');

-- Inserindo dados iniciais para disciplinas
INSERT INTO Disciplinas (codigo, nome) VALUES
('DCC089', 'Teste de Software'),
('DCC603', 'Engenharia de Software'),
('EMA052', 'Projeto de Aeronaves I'),
('EMA240', 'Materiais Compostos');

-- Inserindo dados iniciais para administradores
INSERT INTO Administradores (email, tipo, senha) VALUES
('pboseja@ufmg.br', 1, 'pboseja'),
('admin@ufmg.br', 1, 'admin'),
('pmattos@ufmg.br', 1, 'pmattos');


