from experta import *
from bson.objectid import ObjectId
import pymongo
import connection


class BloodGlucose(Fact):

    """ Informações sobre controle glicêmico"""
    ### ESCALA DE VALORES GLICÊMICOS (Medidadas isoladas - apenas glicemia)
    '''
     CÓDIGO |      EPISÓDIO            |   VALORES    |    COLETA     |          TRATAMENTO  
    hipoG   | Hipoglicemia Grave       | 0 até 49     | 6 a 24 x dia  | 4 ampolas de glicose a 50% IV
    hipoL   | Hipoglicemia Leve        | 50 até 99    | 3 a 6 x dia   | 2 ampolas de glicose a 50% IV
    gAlvo   | Glicemia Normal          | 100 até 200  | 1 a 3 x dia   | manter observação
    hiperL  | Hiperglicemia Leve       | 201 até 250  | 3 a 6 x dia   | 2 unidade de insulina regular SC
    hiperG  | Hiperglicemia Grave      | 251 até 300  | 6 a 24 x dia  | 4 unidade de insulina regular SC
    hiperGG | Hiperglicemia Gravíssima | acima de 301 | 24 a 48 x dia | 6 unidade de insulina regular SC
    
    Aplicar Insulina Contínua - hipoG
    Cumulativo - media móvel das ultimas 48 horas
    Associativo - com outras comorbidades
    ''' 
    pass
 

class GlicemicControl(KnowledgeEngine):

    # GLICEMIAS DE ACORDO COM SITUAÇÃO ATUAL
    @Rule(AND(BloodGlucose(glicemia='hipoG'), BloodGlucose(idPaciente=MATCH.idPaciente)))
    def bg_hipoG(self, idPaciente):
        recomendacao = "Glicose: 4 AMP - 50% IV"
        print(recomendacao)
        print('') 
        response = connection.collection.update_one({ "_id": idPaciente }, { "$set": { "recomendacao": recomendacao } }) 

    @Rule(AND(BloodGlucose(glicemia='hipoL'), BloodGlucose(idPaciente=MATCH.idPaciente)))
    def bg_hipoL(self, idPaciente):
        recomendacao = "Glicose: 2 AMP - 50% IV"
        print(recomendacao)
        print('') 
        response = connection.collection.update_one({ "_id": idPaciente }, { "$set": { "recomendacao": recomendacao } }) 

    @Rule(AND(BloodGlucose(glicemia='gAlvo'), BloodGlucose(idPaciente=MATCH.idPaciente)))
    def bg_gAlvo(self, idPaciente):
        recomendacao = "Manter Observação"
        print(recomendacao)
        print('') 
        response = connection.collection.update_one({ "_id": idPaciente }, { "$set": { "recomendacao": recomendacao } }) 

    @Rule(AND(BloodGlucose(glicemia='hiperL'), BloodGlucose(idPaciente=MATCH.idPaciente)))
    def bg_hiperL(self, idPaciente):
        recomendacao = "Insulina Regular: 2 UN - SC"
        print(recomendacao)
        print('') 
        response = connection.collection.update_one({ "_id": idPaciente }, { "$set": { "recomendacao": recomendacao } }) 

    @Rule(AND(BloodGlucose(glicemia='hiperG'), BloodGlucose(idPaciente=MATCH.idPaciente)))
    def bg_hiperG(self, idPaciente):
        recomendacao = "Insulina Regular: 4 UN - SC"
        print(recomendacao)
        print('') 
        response = connection.collection.update_one({ "_id": idPaciente }, { "$set": { "recomendacao": recomendacao } }) 

    @Rule(AND(BloodGlucose(glicemia='hiperGG'), BloodGlucose(idPaciente=MATCH.idPaciente)))
    def bg_hiperGG(self, idPaciente):
        recomendacao = "Insulina Regular: 6 UN - SC"
        print(recomendacao)
        print('') 
        response = connection.collection.update_one({ "_id": idPaciente }, { "$set": { "recomendacao": recomendacao } })  


    # GLICEMIAS DE ACORDO COM PREVISÃO
    @Rule(AND(BloodGlucose(glicemia='prevHipoG'), BloodGlucose(idPaciente=MATCH.idPaciente)))
    def bg_prevHipoG(self, idPaciente):
        recomendacao = "Glicose: 4 AMP - 50% IV (Prev. 4h)"
        print(recomendacao)
        print('') 
        response = connection.collection.update_one({ "_id": idPaciente }, { "$set": { "recomendacao": recomendacao } }) 

    @Rule(AND(BloodGlucose(glicemia='prevHipoL'), BloodGlucose(idPaciente=MATCH.idPaciente)))
    def bg_prevHipoL(self, idPaciente):
        recomendacao = "Glicose: 2 AMP - 50% IV (Prev. 4h)"
        print(recomendacao)
        print('') 
        response = connection.collection.update_one({ "_id": idPaciente }, { "$set": { "recomendacao": recomendacao } }) 

    @Rule(AND(BloodGlucose(glicemia='prevgAlvo'), BloodGlucose(idPaciente=MATCH.idPaciente)))
    def bg_prevgAlvo(self, idPaciente):
        recomendacao = "Manter Observação (Prev. 4h)"
        print(recomendacao)
        print('') 
        response = connection.collection.update_one({ "_id": idPaciente }, { "$set": { "recomendacao": recomendacao } }) 

    @Rule(AND(BloodGlucose(glicemia='prevHiperL'), BloodGlucose(idPaciente=MATCH.idPaciente)))
    def bg_prevHiperL(self, idPaciente):
        recomendacao = "Insulina Regular: 2 UN - SC (Prev. 4h)"
        print(recomendacao)
        print('') 
        response = connection.collection.update_one({ "_id": idPaciente }, { "$set": { "recomendacao": recomendacao } }) 

    @Rule(AND(BloodGlucose(glicemia='prevHiperG'), BloodGlucose(idPaciente=MATCH.idPaciente)))
    def bg_prevHiperG(self, idPaciente):
        recomendacao = "Insulina Regular: 4 UN - SC (Prev. 4h)"
        print(recomendacao)
        print('') 
        response = connection.collection.update_one({ "_id": idPaciente }, { "$set": { "recomendacao": recomendacao } }) 

    @Rule(AND(BloodGlucose(glicemia='prevHiperGG'), BloodGlucose(idPaciente=MATCH.idPaciente)))
    def bg_prevHiperGG(self, idPaciente):
        recomendacao = "Insulina Regular: 6 UN - SC (Prev. 4h)"
        print(recomendacao)
        print('') 
        response = connection.collection.update_one({ "_id": idPaciente }, { "$set": { "recomendacao": recomendacao } })  

# GLICEMIAS COM SITUAÇÕES INCOMUNS
    @Rule(AND(BloodGlucose(glicemia='semGlicemia'), BloodGlucose(idPaciente=MATCH.idPaciente)))
    def bg_sem(self, idPaciente):
        recomendacao = "Coleta de Necessária"
        print(recomendacao)
        print('') 
        response = connection.collection.update_one({ "_id": idPaciente }, { "$set": { "recomendacao": recomendacao } }) 

    @Rule(AND(BloodGlucose(glicemia='gInvalida'), BloodGlucose(idPaciente=MATCH.idPaciente)))
    def bg_invalida(self, idPaciente):
        recomendacao = "Glicemia Inválida!"
        print(recomendacao)
        print('') 
        response = connection.collection.update_one({ "_id": idPaciente }, { "$set": { "recomendacao": recomendacao } }) 

    

