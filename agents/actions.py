import conexao

def consultarGlycon():
    #listando apenas um paciente
    print('Novo paciente cadastrado. Coletando os dados...')
    myquery = { "nome": "José da Silva" }
    document = conexao.collection.find(myquery, { "_id": 0, "nome": 1, "glicemia.dataHoraColeta": 1, "glicemia.valorGlicemia": 1 })
    for x in document:
        print(x)


def gerarRelatorioAvaliacao():
    # pegar json
    # separar dados úteis
    # determinar situação paciente 
    return


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



