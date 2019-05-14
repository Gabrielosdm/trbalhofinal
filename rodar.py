# Importando bibliotecas
from flask import Flask, render_template, request
from flaskext.mysql import MySQL
from bd import *

# Instanciando a app Flask
app = Flask(__name__)
# Instanciar o objeto MySQL
mysql = MySQL()
# Ligar o MYSQL ao Flask
mysql.init_app(app)

# Configurando o acesso ao MySQL
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'concessionaria'

@app.route('/')
def principal():
    return render_template('home.html')

@app.route('/funcio_page', methods=['GET','POST'])
def logar():
    if request.method == 'POST':
        # recuperar os parametros
        nome = request.form.get('nome')
        senha = request.form.get('senha')

        # Obtendo o cursor para acessar o BD
        cursor = mysql.get_db().cursor()

        funcionarios = validarlogin(cursor, nome, senha)

        if funcionarios is None:
            return render_template('home.html')

        else:

            return render_template('homefuncionario.html')

    else:
        return render_template('home.html')




# Rodando a app
if __name__ == '__main__':
    app.run(debug=True)
