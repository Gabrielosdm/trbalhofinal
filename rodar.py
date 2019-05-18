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
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
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

@app.route('/incluir_anuncio')
def Incluir_anuncio():
    cursor = mysql.get_db().cursor()
    return render_template('adicionar_carro.html',carros=get_carros(cursor))


@app.route('/confirmar_anuncio', methods=['GET','POST'])
def incluindo_anuncio():
    if request.method == 'POST':
        nomecarro=request.form.get('nomecar')
        marcacarro=request.form.get('marcacar')
        anocarro=request.form.get('anocar')
        corcarro=request.form.get('corcar')
        precocarro=request.form.get('precocar')


        conn = mysql.connect()
        cursor = conn.cursor()

        incluir_anuncio(cursor,conn,nomecarro,marcacarro,anocarro,corcarro,precocarro)

        cursor.close()
        conn.close()

        return render_template('adicionar_carro.html')
    else:
        return render_template('homefuncionario.html')

@app.route('/sem_carro')
def Excluir_carro():
    cursor = mysql.get_db().cursor()
    return render_template('excluir_anuncio.html',carros=get_carros(cursor))

@app.route('/excluido_anuncio', methods=['GET','POST'])
def excluindo_anuncio():
    if request.method == 'POST':
        idcar=request.form.get('ex_carro')

        conn = mysql.connect()
        cursor = conn.cursor()

        excluir_anuncio(cursor,conn,idcar)

        cursor.close()
        conn.close()

        return render_template('excluir_anuncio.html')
    else:
        return render_template('homefuncionario.html')



@app.route('/all_carros')
def all_cars():
    cursor = mysql.get_db().cursor()
    return render_template('todos_carros.html', carros=get_carros(cursor))



# Rodando a app
if __name__ == '__main__':
    app.run(debug=True)