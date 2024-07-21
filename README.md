# Urbanu Web

Este é o projeto Urbanu Web, uma aplicação Flask para gerenciar solicitações municipais.

## Requisitos

- Python 3.7 ou superior
- Virtualenv

## Instalação

### 1. Clone o repositório:
   sh
   git clone https://github.com/jacielbarros/urbanu-web.git
   cd urbanu-web

### 2. Crie um ambiente virtual:

  python -m venv venv

### 3. Ative o ambiente virtual:

* No Windows:
  
   venv\Scripts\activate
  
* No macOS/Linux:

  source venv/bin/activate

### 4. Instale as dependências:


pip install -r requirements.txt

### 5. Configure o banco de dados:

  * Edite o arquivo config.py para configurar sua conexão com o banco de dados.
  * Execute as migrações do banco de dados:
      flask db upgrade

### 6. Execute a aplicação:
   
  flask run

A aplicação estará disponível em http://127.0.0.1:5000.

# Estrutura do projeto

  * app/ - Diretório principal da aplicação Flask.
  * app/templates/ - Arquivos HTML.
  * app/static/ - Arquivos estáticos (CSS, JavaScript, imagens).
  * app/forms.py - Formulários Flask-WTF.
  * app/models.py - Modelos SQLAlchemy.
  * app/routes.py - Rotas da aplicação.
  * config.py - Configurações da aplicação.
  * run.py - Script para executar a aplicação.

# Contribuição

1. Fork o repositório.
2. Crie uma nova branch (git checkout -b feature/nova-funcionalidade).
3. Faça commit das suas alterações (git commit -am 'Adiciona nova funcionalidade').
4. Envie para a branch (git push origin feature/nova-funcionalidade).
5. Abra um Pull Request.


# Licença

Este projeto está licenciado sob a Licença MIT.
