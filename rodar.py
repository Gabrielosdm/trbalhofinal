import os
from flask import Flask,flash,render_template,request,redirect,url_for,send_file,send_from_directory
from flaskext.mysql import MySQL
from werkzeug.utils import secure_filename
from bd import *

app = Flask(__name__)

UP_FOLDER = 'C:\\Users\\Pichau\\PycharmProjects\\trbalhofinal\\imagens\\carros'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

mysql = MySQL()

mysql.init_app(app)

app.config['UP_FOLDER'] = UP_FOLDER
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'concessionaria'

@app.route('/')
def principal():
    cursor = mysql.get_db().cursor()
    return render_template('home.html', carros=pegar_top10(cursor), base_url='http://127.0.0.1:5000/upload/')

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
    return render_template('adicionar_carro.html')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/confirmar_anuncio', methods=['GET','POST'])
def incluindo_anuncio():
    global filename
    if request.method == 'POST':
        nomecarro=request.form.get('nomecar')
        marcacarro=request.form.get('marcacar')
        anocarro=request.form.get('anocar')
        corcarro=request.form.get('corcar')
        precocarro=request.form.get('precocar')
        top10 = request.form.get('top_choice')
        reservas="0"
        file = request.form.get('file')

        if top10 == "Sim":
            top10 = 1
        else:
            top10 = 0

        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_location = os.path.join(app.config['UP_FOLDER'], filename)
            print(filename)
            print(file_location)
            print(file_location)
            escaped_file_location = file_location.replace('\\', '/')
            print(escaped_file_location)
            file.save(os.path.join(app.config['UP_FOLDER'], filename))


        conn = mysql.connect()
        cursor = conn.cursor()

        incluir_anuncio(cursor,conn,nomecarro,marcacarro,anocarro,corcarro,precocarro,top10,reservas, filename)

        cursor.close()
        conn.close()

        return render_template('adicionar_carro.html')
    else:
        return render_template('homefuncionario.html')

@app.route('/upload/<filename>', methods=['GET','POST'])
def uploads_file(filename):
    return send_from_directory(app.config['UP_FOLDER'],
                               filename)

@app.route('/excluido_anuncio', methods=['GET','POST'])
def excluindo_anuncio():
    if request.method == 'POST':
        iddocarro = request.form.get('iddocarro')

        conn = mysql.connect()
        cursor = conn.cursor()

        excluir_anuncio(cursor,conn,iddocarro)

        cursor.close()
        conn.close()

        return render_template('adicionar_carro.html')
    else:
        return render_template('homefuncionario.html')

@app.route('/incluir_usuario')
def incluir_usu():
    return render_template('incluir_user.html')

@app.route('/incluso', methods=['GET','POST'])
def incluindo():
    if request.method == 'POST':
        nlogin = request.form.get('nlogin')
        nsenha = request.form.get('nsenha')

        conn = mysql.connect()
        cursor = conn.cursor()

        incluir_usuario(cursor, conn, nlogin, nsenha)

        cursor.close()
        conn.close()

        return render_template('incluir_user.html')
    else:
        return render_template('homefuncionario.html')

@app.route('/excluir_funcionario')
def excluir_funcio():
    return render_template('incluir_user.html')

@app.route('/excluido_func', methods=['GET','POST'])
def excluindo_funcionarios():
    if request.method == 'POST':
        iddofuncio = request.form.get('iddofuncio')

        conn = mysql.connect()
        cursor = conn.cursor()

        excluir_user(cursor,conn,iddofuncio)

        cursor.close()
        conn.close()

        return render_template('incluir_user.html')
    else:
        return render_template('homefuncionario.html')



@app.route('/consultacarros', methods=['GET', 'POST'])
def consultacarros():
    if request.method == 'POST':
        buscando = request.form.get('buscando')
        cursor = mysql.get_db().cursor()
        teste = consultar_carros(cursor, buscando)
        if teste is None:
            return render_template('home.html')
        else:
            cursor = mysql.get_db().cursor()
            return render_template('buscado_carro.html', carros=consultar_carros(cursor, buscando), base_url='http://127.0.0.1:5000/upload/')
    return

@app.route('/editar_top10')
def editar_top10():
    cursor = mysql.get_db().cursor()
    return render_template('edit_top10.html')

@app.route('/top10_editado', methods=['GET','POST'])
def top_editado():
    if request.method == 'POST':
        idcar=request.form.get('oid')
        atop10= request.form.get('atop10')
        if atop10 == "Colocar":
            top10 = 1
        else:
            top10 = 0

        conn = mysql.connect()
        cursor = conn.cursor()

        edit_top10(cursor,conn,top10,idcar)

        cursor.close()
        conn.close()

        return render_template('edit_top10.html')
    else:
        return render_template('homefuncionario.html')

@app.route('/reservando/<idcarros>', methods={'GET','POST'})
def reservarr(idcarros):
    cursor = mysql.get_db().cursor()
    return render_template('reservar_carro.html', detalhes=pegar_detalhes(cursor,idcarros))

@app.route('/reservando2/<idcarros>', methods={'GET','POST'})
def reservarrr(idcarros):
    cursor = mysql.get_db().cursor()
    return render_template('reservar_carro.html', detalhes=pegar_detalhesss(cursor,idcarros))

@app.route('/reserva_done/<idcarros>', methods={'GET','POST'})
def reserva_feita(idcarros):
    if request.method == 'POST':
        nomecomp = request.form.get('nomeccomp')
        cpfccomp = request.form.get('cpfccomp')
        emailcomp = request.form.get('emailcomp')
        reserva = "1"

        conn = mysql.connect()
        cursor = conn.cursor()

        reservar(cursor, conn, reserva, idcarros,idcarros)
        add_reserva(cursor, conn, nomecomp, cpfccomp, emailcomp,idcarros)



        return render_template('home.html', carros=pegar_top10(cursor), base_url='http://127.0.0.1:5000/upload/')
    else:
        return render_template('reservar_carro.html')


@app.route('/all_carros')
def all_cars():
    cursor = mysql.get_db().cursor()
    return render_template('todos_carros.html', carros=get_carros(cursor))

@app.route('/all_func')
def all_funcs():
    cursor = mysql.get_db().cursor()
    return render_template('todos_funcio.html', funcionarios=get_funcio(cursor))


@app.route('/all_reserv')
def all_reservs():
    cursor = mysql.get_db().cursor()
    return render_template('todas_reservas.html', reserva=get_reserva(cursor))



# Rodando a app
if __name__ == '__main__':
    app.run(debug=True)