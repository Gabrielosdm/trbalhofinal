def validarlogin(cursor, nome, senha):
    # Executar o SQL
    cursor.execute(f'select idfuncionarios from funcionarios WHERE nome = "{nome} " and senha = "{senha}"')

    # Recuperando o retorno do BD
    funcionarios = cursor.fetchone()

    cursor.close()

    # Retornar os dados
    return funcionarios

def incluir_anuncio(cursor,conn,nomecar,marcacar,anocar,corcar,precocar,top10,reservas):
    cursor.execute(f'INSERT into concessionaria.carros (nome,marca,ano,cor,preco,top10,reservas) VALUES ("{nomecar}","{marcacar}","{anocar}","{corcar}","{precocar}","{top10}","{reservas}")')
    conn.commit()

def excluir_anuncio(cursor,conn,carroid):
    cursor.execute(f'DELETE FROM concessionaria.carros WHERE idcarros = "{carroid}"')
    conn.commit()

def incluir_usuario(cursor, conn, login, senha):
    cursor.execute(f'INSERT into concessionaria.funcionarios (nome,senha) VALUES ("{login}","{senha}")')
    conn.commit()

def excluir_user(cursor,conn,funcid):
    cursor.execute(f'DELETE FROM concessionaria.funcionarios WHERE idfuncionarios = "{funcid}"')
    conn.commit()


def consultar_carros(cursor, buscando):
    cursor.execute(f'SELECT nome FROM carros WHERE nome = "{buscando}" or marca = "{buscando}"')
    consulta = cursor.fetchall()
    cursor.close()
    return consulta

def edit_top10(cursor,conn,top10,idcarros):
    cursor.execute(f'UPDATE carros SET top10 = "{top10}" WHERE idcarros= "{idcarros}"')
    conn.commit()

def pegar_top10(cursor):
    cursor.execute(f'SELECT * '
                   'FROM carros WHERE top10 = "1"')

    top10 = cursor.fetchall()

    return top10

def pegar_detalhes(cursor,idcarros):
    cursor.execute(f'SELECT * FROM carros WHERE idcarros = "{idcarros}"')

    detalhes= cursor.fetchall()

    return detalhes

def reservar(cursor,conn,reserva,idcar):
    cursor.execute(f'UPDATE carros SET reservas = "{reserva}" WHERE idcarros = "{idcar}"')
    conn.commit()

def add_reserva(cursor, conn, nome, cpf, email):
    cursor.execute(f'INSERT into concessionaria.reservas (nome,cpf,email) VALUES ("{nome}","{cpf}","{email}")')
    conn.commit()

def get_carros(cursor):

    cursor.execute(f'SELECT carros.idcarros,carros.nome,carros.marca,carros.ano,carros.cor,carros.preco FROM carros')

    carros = cursor.fetchall()

    return carros