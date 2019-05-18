def validarlogin(cursor, nome, senha):
    # Executar o SQL
    cursor.execute(f'select idfuncionarios from funcionarios WHERE nome = "{nome} " and senha = "{senha}"')

    # Recuperando o retorno do BD
    funcionarios = cursor.fetchone()

    cursor.close()

    # Retornar os dados
    return funcionarios

def incluir_anuncio(cursor,conn,nome,marca,ano,cor,preco):
    cursor.execute(f'INSERT into concessionaria.carros (nome,marca,ano,cor,preco) VALUES ("{nome}","{marca}","{ano}","{cor}","{preco}")')
    conn.commit()

def excluir_anuncio(cursor,conn,idcarro):
    print(idcarro)
    cursor.execute(f'DELETE FROM concessionaria.carros WHERE idcarro = "{idcarro}')
    conn.commit()

def get_carros(cursor):

    # Executar o SQL
    cursor.execute(f'SELECT carros.nome,carros.marca,carros.ano,carros.cor,carros.preco FROM carros')

    # Recuperando o retorno do BD
    carros = cursor.fetchall()

    # Retornar os dados
    return carros