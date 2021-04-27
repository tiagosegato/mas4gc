from experta import *
from bson.objectid import ObjectId
import pymongo
import connection


class BloodGlucose(Fact):

    """ Informações sobre controle glicêmico"""
    ### ESCALA DE VALORES GLICÊMICOS (Medidadas isoladas - apenas glicemia)
    '''
     CÓDIGO |      EPISÓDIO            |   VALORES    |    COLETA      1      2     3     |          TRATAMENTO  
    hipoG   | Hipoglicemia Grave       | 0 até 49     | 6 a 24 x dia  (4h)  (2h)  (1h)    | 4 ampolas de glicose a 50% IV
    hipoL   | Hipoglicemia Leve        | 50 até 99    | 3 a 6 x dia   (8h)  (6h)  (4h)    | 2 ampolas de glicose a 50% IV
    gAlvo   | Glicemia Normal          | 100 até 200  | 1 a 3 x dia   (24h) (16h) (8h)    | manter observação
    hiperL  | Hiperglicemia Leve       | 201 até 250  | 3 a 6 x dia   (8h)  (6h)  (4h)    | 2 unidade de insulina regular SC
    hiperG  | Hiperglicemia Grave      | 251 até 300  | 6 a 24 x dia  (4h)  (2h)  (1h)    | 4 unidade de insulina regular SC
    hiperGG | Hiperglicemia Gravíssima | acima de 301 | 24 a 48 x dia (1h)(45min)(30min)  | 6 unidade de insulina regular SC

    regra 1 = 1 glicemia fora do alvo -> coletar novamente em 1h
    regra 2 = 2 fora - diminui 2 hs do padrão
    e assim sucessivamente... 
    ''' 
    pass
 

class GlicemicControl(KnowledgeEngine):

    # GLICEMIAS DE ACORDO COM SITUAÇÃO ATUAL
    @Rule(AND(BloodGlucose(glicemia='hipoG'), BloodGlucose(idPaciente=MATCH.idPaciente)))
    def bg_hipoG(self, idPaciente):
        tratamento = "Glicose: 4 AMP - 50% IV"
        print(tratamento)
        print('') 
        response = connection.collection.update_one({ "_id": idPaciente }, { "$set": { "tratamento": tratamento } }) 

    @Rule(AND(BloodGlucose(glicemia='hipoL'), BloodGlucose(idPaciente=MATCH.idPaciente)))
    def bg_hipoL(self, idPaciente):
        tratamento = "Glicose: 2 AMP - 50% IV"
        print(tratamento)
        print('') 
        response = connection.collection.update_one({ "_id": idPaciente }, { "$set": { "tratamento": tratamento } }) 

    @Rule(AND(BloodGlucose(glicemia='gAlvo'), BloodGlucose(idPaciente=MATCH.idPaciente)))
    def bg_gAlvo(self, idPaciente):
        tratamento = "Manter Observação"
        print(tratamento)
        print('') 
        response = connection.collection.update_one({ "_id": idPaciente }, { "$set": { "tratamento": tratamento } }) 

    @Rule(AND(BloodGlucose(glicemia='hiperL'), BloodGlucose(idPaciente=MATCH.idPaciente)))
    def bg_hiperL(self, idPaciente):
        tratamento = "Insulina Regular: 2 UN - SC"
        print(tratamento)
        print('') 
        response = connection.collection.update_one({ "_id": idPaciente }, { "$set": { "tratamento": tratamento } }) 

    @Rule(AND(BloodGlucose(glicemia='hiperG'), BloodGlucose(idPaciente=MATCH.idPaciente)))
    def bg_hiperG(self, idPaciente):
        tratamento= "Insulina Regular: 4 UN - SC"
        print(tratamento)
        print('') 
        response = connection.collection.update_one({ "_id": idPaciente }, { "$set": { "tratamento": tratamento } }) 

    @Rule(AND(BloodGlucose(glicemia='hiperGG'), BloodGlucose(idPaciente=MATCH.idPaciente)))
    def bg_hiperGG(self, idPaciente):
        tratamento = "Insulina Regular: 6 UN - SC"
        print(tratamento)
        print('') 
        response = connection.collection.update_one({ "_id": idPaciente }, { "$set": { "tratamento": tratamento } })  


    # GLICEMIAS DE ACORDO COM PREVISÃO
    @Rule(AND(BloodGlucose(glicemia='prevHipoG'), BloodGlucose(idPaciente=MATCH.idPaciente)))
    def bg_prevHipoG(self, idPaciente):
        tratamento = "Glicose: 4 AMP - 50% IV (Prev. 4h)"
        print(tratamento)
        print('') 
        response = connection.collection.update_one({ "_id": idPaciente }, { "$set": { "tratamento": tratamento } }) 

    @Rule(AND(BloodGlucose(glicemia='prevHipoL'), BloodGlucose(idPaciente=MATCH.idPaciente)))
    def bg_prevHipoL(self, idPaciente):
        tratamento = "Glicose: 2 AMP - 50% IV (Prev. 4h)"
        print(tratamento)
        print('') 
        response = connection.collection.update_one({ "_id": idPaciente }, { "$set": { "tratamento": tratamento } }) 

    @Rule(AND(BloodGlucose(glicemia='prevgAlvo'), BloodGlucose(idPaciente=MATCH.idPaciente)))
    def bg_prevgAlvo(self, idPaciente):
        tratamento = "Manter Observação (Prev. 4h)"
        print(tratamento)
        print('') 
        response = connection.collection.update_one({ "_id": idPaciente }, { "$set": { "tratamento": tratamento } }) 

    @Rule(AND(BloodGlucose(glicemia='prevHiperL'), BloodGlucose(idPaciente=MATCH.idPaciente)))
    def bg_prevHiperL(self, idPaciente):
        tratamento = "Insulina Regular: 2 UN - SC (Prev. 4h)"
        print(tratamento)
        print('') 
        response = connection.collection.update_one({ "_id": idPaciente }, { "$set": { "tratamento": tratamento } }) 

    @Rule(AND(BloodGlucose(glicemia='prevHiperG'), BloodGlucose(idPaciente=MATCH.idPaciente)))
    def bg_prevHiperG(self, idPaciente):
        tratamento = "Insulina Regular: 4 UN - SC (Prev. 4h)"
        print(tratamento)
        print('') 
        response = connection.collection.update_one({ "_id": idPaciente }, { "$set": { "tratamento": tratamento } }) 

    @Rule(AND(BloodGlucose(glicemia='prevHiperGG'), BloodGlucose(idPaciente=MATCH.idPaciente)))
    def bg_prevHiperGG(self, idPaciente):
        tratamento = "Insulina Regular: 6 UN - SC (Prev. 4h)"
        print(tratamento)
        print('') 
        response = connection.collection.update_one({ "_id": idPaciente }, { "$set": { "tratamento": tratamento } })  

# GLICEMIAS COM SITUAÇÕES INCOMUNS
    @Rule(AND(BloodGlucose(glicemia='semGlicemia'), BloodGlucose(idPaciente=MATCH.idPaciente)))
    def bg_sem(self, idPaciente):
        tratamento = " -- "
        print(tratamento)
        print('') 
        response = connection.collection.update_one({ "_id": idPaciente }, { "$set": { "tratamento": tratamento } }) 

    @Rule(AND(BloodGlucose(glicemia='gInvalida'), BloodGlucose(idPaciente=MATCH.idPaciente)))
    def bg_invalida(self, idPaciente):
        tratamento = "Glicemia Inválida!"
        print(tratamento)
        print('') 
        response = connection.collection.update_one({ "_id": idPaciente }, { "$set": { "tratamento": tratamento } }) 

    

