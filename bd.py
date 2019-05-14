def validarlogin(cursor, nome, senha):
    # Executar o SQL
    cursor.execute('select idfuncionarios from funcionarios WHERE nome = "{nome} " and senha = "{senha}"')

    # Recuperando o retorno do BD
    funcionarios = cursor.fetchall()

    cursor.close()

    # Retornar os dados
    return funcionarios