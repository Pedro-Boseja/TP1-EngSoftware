<h1 align="center">Sistema de Avaliação de Disciplinas e Professores</h1>

<p align="center">Sistema desenvolvido para que alunos avaliem de forma anônima disciplinas e professores de sua faculdade.</p>

## 📑 Tabela de conteúdos
<!--ts-->
- [💻 Sobre o projeto](#-sobre-o-projeto)
  - [📌 Histórias de usuário](#-histórias-de-usuário)
- [⚙️ Funcionalidades](#-funcionalidades)
- [🚀 Como executar o projeto](#-como-executar-o-projeto)
  - [🔧 Pré-requisitos](#-pré-requisitos)
  - [▶️ Rodando a aplicação](#-rodando-a-aplica%C3%A7%C3%A3o)
- [🛠 Tecnologias](#-tecnologias)
- [🧠 Contribuidores](#-contribuidores)
<!--te-->

## 💻 Sobre o projeto

Este projeto faz parte das atividades práticas da disciplina Engenharia de Software (DCC603). O sistema foi desenvolvido para permitir que estudantes avaliem professores e disciplinas de forma anônima, contribuindo para a melhoria do ensino e auxiliando outros alunos na escolha de disciplinas.

### 📌 Histórias de usuário

- Como administrador, desejo cadastrar estudantes
- Como administrador, desejo cadastrar professores
- Como administrador, desejo cadastrar disciplinas
- Como administrador, desejo excluir estudantes
- Como administrador, desejo excluir professores
- Como administrador, desejo excluir disciplinas
- Como administrador, desejo alterar o nome de disciplinas
- Como administrador, desejo alterar a senha de alunos
- Como administrador, desejo alterar a senha de professores
- Como aluno, desejo avaliar de forma anônima disciplinas
- Como aluno, desejo avaliar de forma anônima professores
- Como usuário, desejo saber a avaliação de disciplinas
- Como usuário, desejo saber a avaliação de professores
- Como usuário, desejo listar e ordenar as disciplinas
- Como usuário, desejo listar e ordenar os professores
- Como administrador, desejo listar e ordenar os usuários

## ⚙️ Funcionalidades

- [x] Cadastro de estudantes
- [x] Cadastro de disciplinas
- [x] Cadastro de professores
- [x] Avaliação anônima de professores
- [x] Avaliação anônima de disciplinas
- [x] Listagem e ordenação de disciplinas por ordem alfabética e de avaliação
- [x] Listagem e ordenação de professores por ordem alfabética e de avaliação

## 🚀 Como executar o projeto

### 🔧 Pré-requisitos

Antes de começar, você vai precisar ter instalado em sua máquina as seguintes ferramentas:
- [Git](https://git-scm.com)
- [Python](https://www.python.org)
- [Flask](https://flask.palletsprojects.com/en/stable/)
- [MySQL Workbench](https://www.mysql.com/products/workbench/)

Além disso, é bom ter um editor para trabalhar com o código, como o [VSCode](https://code.visualstudio.com/).

### ▶️ Rodando a aplicação

1. Clone este repositório.
2. Execute o script `sistema_avaliacao.sql` no [MySQL Workbench](https://www.mysql.com/products/workbench/) para criar o banco de dados.
3. Inclua a senha do seu servidor de banco de dados no arquivo `config.py`.
4. No terminal, execute o comando `python3 main.py`.
5. Acesse a URL de localhost gerada.

## 🛠 Tecnologias

As seguintes ferramentas foram utilizadas na construção do projeto:

- Python
- HTML
- CSS
- MySQL Workbench

## 🧠 Contribuidores

- Gabriel Yoshiharu Sato (full stack)
- Pedro Henrique de Mattos Gomes (full stack)
- Pedro Silveira Polesca Boseja (full stack)
