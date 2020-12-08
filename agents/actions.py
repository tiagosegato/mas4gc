import conexao

# listando apenas nome, data e valor da glicemia de um paciente
def consultarGlycon():
    print('Novo paciente encontrado. Coletando os dados...')
    print('')
    document = conexao.collection.find({}, {"_id": 0, "nome": 1, "glicemia.valorGlicemia": 1 }).sort("updateDate", -1).limit(1)

    paciente = document[0]["nome"]
    coletas = len(document[0]["glicemia"])
    glicemias = document[0]["glicemia"]

    print('Paciente: ', paciente)
    print('Quantidade de Coletas: ', coletas)
    print('Glicemias coletadas: ', glicemias)

    if coletas == 1:
        #pega apenas o valor da glicemia coletada
        for x in glicemias[0].values():
            glicemia = int(x)

        # mostra de acordo com a tabela
        if glicemia >= 0 and glicemia <= 49:
            situacao = 'hypoS'
        elif glicemia >=50 and glicemia <= 99:
            situacao = 'hypoM'
        elif glicemia >=100 and glicemia <= 200:
            situacao = 'normalBG'
        elif glicemia >=201 and glicemia <= 250:
            situacao = 'hyperM'
        elif glicemia >=251 and glicemia <= 300:
            situacao = 'hyperS'
        elif glicemia >=301:
            situacao = 'hyperVS'
        else: print('glicemia inválida!')
        
        print('Situação', situacao)
        print('')

    elif coletas > 1:
        for x in document:
            #TODO
            print("calcular próxima glicemia para os dados:")
            print(x)


# analizar os dados coletados determinando a situação do paciente
def gerarRelatorioAvaliacao():
    
    consultarGlycon()

    relatorio = 'dados'
    
    
    print(relatorio)

    return

### TESTES #####
gerarRelatorioAvaliacao()

### OUTRAS FUNÇÕES ###

#listando primeiro da lista
def listarPrimeiro():
    primeiro = conexao.collection.find_one()
    print(primeiro)

#listando a collection toda
def listarTodos():
    cursor = conexao.collection.find({})
    for document in cursor:
        print(document)

#lista paciente especificado na query
def exibePaciente():
    myquery = { "nome": "João" }
    document = conexao.collection.find(myquery)
    for x in document:
        print(x)

#lista apenas as colunas especificadas
def listarColunas():
    for x in conexao.collection.find({},{ "_id": 0, "nome": 1, "glicemia.dataHoraColeta": 1, "glicemia.valorGlicemia": 1 }):
        print(x)

def listarAtual():
    atual = conexao.collection.find().sort("updateDate", -1)
    for x in atual:
        print(x)
        print('')


