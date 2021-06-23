from experta import *
from bson.objectid import ObjectId
import pymongo
import connection


class BloodGlucose(Fact):

    """ Informações sobre controle glicêmico"""
    ### ESCALA DE VALORES GLICÊMICOS (Medidadas isoladas - apenas glicemia)
    '''
     CÓDIGO |      EPISÓDIO            |   VALORES      |          TRATAMENTO  
    hipoG   | Hipoglicemia Grave       | 0 até 40       | 4 ampolas de glicose a 50% IV
    hipoL   | Hipoglicemia Leve        | > 40 até 70    | 2 ampolas de glicose a 50% IV
    gAlvo   | Glicemia Normal          | > 70 até 140   | manter observação
    hiperL  | Hiperglicemia Leve       | > 140 até 180  | 2 unidade de insulina regular SC
    hiperG  | Hiperglicemia Grave      | > 180 até 250  | 4 unidade de insulina regular SC
    hiperGG | Hiperglicemia Gravíssima | acima de 250   | 6 unidade de insulina regular SC

    ''' 
    pass
 
class GlicemicControl(KnowledgeEngine):

    # 14 REGRAS #
    # GLICEMIAS DE ACORDO COM SITUAÇÃO ATUAL
    @Rule(AND(BloodGlucose(situacao='hipoG'), BloodGlucose(idPaciente=MATCH.idPaciente)))
    def bg_hipoG(self, idPaciente):
        tratamento = "Glicose: 4 AMP - 50% IV"
        print(tratamento)
        print('') 
        response = connection.collection.update_one({ "_id": idPaciente }, { "$set": { "tratamento": tratamento } }) 

    @Rule(AND(BloodGlucose(situacao='hipoL'), BloodGlucose(idPaciente=MATCH.idPaciente)))
    def bg_hipoL(self, idPaciente):
        tratamento = "Glicose: 2 AMP - 50% IV"
        print(tratamento)
        print('') 
        response = connection.collection.update_one({ "_id": idPaciente }, { "$set": { "tratamento": tratamento } }) 

    @Rule(AND(BloodGlucose(situacao='gAlvo'), BloodGlucose(idPaciente=MATCH.idPaciente)))
    def bg_gAlvo(self, idPaciente):
        tratamento = "Manter Observação"
        print(tratamento)
        print('') 
        response = connection.collection.update_one({ "_id": idPaciente }, { "$set": { "tratamento": tratamento } }) 

    @Rule(AND(BloodGlucose(situacao='hiperL'), BloodGlucose(idPaciente=MATCH.idPaciente)))
    def bg_hiperL(self, idPaciente):
        tratamento = "Insulina Regular: 2 UN - SC"
        print(tratamento)
        print('') 
        response = connection.collection.update_one({ "_id": idPaciente }, { "$set": { "tratamento": tratamento } }) 

    @Rule(AND(BloodGlucose(situacao='hiperG'), BloodGlucose(idPaciente=MATCH.idPaciente)))
    def bg_hiperG(self, idPaciente):
        tratamento= "Insulina Regular: 4 UN - SC"
        print(tratamento)
        print('') 
        response = connection.collection.update_one({ "_id": idPaciente }, { "$set": { "tratamento": tratamento } }) 

    @Rule(AND(BloodGlucose(situacao='hiperGG'), BloodGlucose(idPaciente=MATCH.idPaciente)))
    def bg_hiperGG(self, idPaciente):
        tratamento = "Insulina Regular: 6 UN - SC"
        print(tratamento)
        print('') 
        response = connection.collection.update_one({ "_id": idPaciente }, { "$set": { "tratamento": tratamento } })  


    # GLICEMIAS DE ACORDO COM PREVISÃO 
    # TODO tem diferença glicemia e previsão da glicemia?
    @Rule(AND(BloodGlucose(situacao='prevHipoG'), BloodGlucose(idPaciente=MATCH.idPaciente)))
    def bg_prevHipoG(self, idPaciente):
        tratamento = "Glicose: 4 AMP - 50% IV (Prev. 4h)"
        print(tratamento)
        print('') 
        response = connection.collection.update_one({ "_id": idPaciente }, { "$set": { "tratamento": tratamento } }) 

    @Rule(AND(BloodGlucose(situacao='prevHipoL'), BloodGlucose(idPaciente=MATCH.idPaciente)))
    def bg_prevHipoL(self, idPaciente):
        tratamento = "Glicose: 2 AMP - 50% IV (Prev. 4h)"
        print(tratamento)
        print('') 
        response = connection.collection.update_one({ "_id": idPaciente }, { "$set": { "tratamento": tratamento } }) 

    @Rule(AND(BloodGlucose(situacao='prevgAlvo'), BloodGlucose(idPaciente=MATCH.idPaciente)))
    def bg_prevgAlvo(self, idPaciente):
        tratamento = "Manter Observação (Prev. 4h)"
        print(tratamento)
        print('') 
        response = connection.collection.update_one({ "_id": idPaciente }, { "$set": { "tratamento": tratamento } }) 

    @Rule(AND(BloodGlucose(situacao='prevHiperL'), BloodGlucose(idPaciente=MATCH.idPaciente)))
    def bg_prevHiperL(self, idPaciente):
        tratamento = "Insulina Regular: 2 UN - SC (Prev. 4h)"
        print(tratamento)
        print('') 
        response = connection.collection.update_one({ "_id": idPaciente }, { "$set": { "tratamento": tratamento } }) 

    @Rule(AND(BloodGlucose(situacao='prevHiperG'), BloodGlucose(idPaciente=MATCH.idPaciente)))
    def bg_prevHiperG(self, idPaciente):
        tratamento = "Insulina Regular: 4 UN - SC (Prev. 4h)"
        print(tratamento)
        print('') 
        response = connection.collection.update_one({ "_id": idPaciente }, { "$set": { "tratamento": tratamento } }) 

    @Rule(AND(BloodGlucose(situacao='prevHiperGG'), BloodGlucose(idPaciente=MATCH.idPaciente)))
    def bg_prevHiperGG(self, idPaciente):
        tratamento = "Insulina Regular: 6 UN - SC (Prev. 4h)"
        print(tratamento)
        print('') 
        response = connection.collection.update_one({ "_id": idPaciente }, { "$set": { "tratamento": tratamento } })  

# GLICEMIAS COM SITUAÇÕES INCOMUNS
    @Rule(AND(BloodGlucose(situacao='semGlicemia'), BloodGlucose(idPaciente=MATCH.idPaciente)))
    def bg_sem(self, idPaciente):
        tratamento = " -- "
        print(tratamento)
        print('') 
        response = connection.collection.update_one({ "_id": idPaciente }, { "$set": { "tratamento": tratamento } }) 

    @Rule(AND(BloodGlucose(situacao='gInvalida'), BloodGlucose(idPaciente=MATCH.idPaciente)))
    def bg_invalida(self, idPaciente):
        tratamento = "Glicemia Inválida!"
        print(tratamento)
        print('') 
        response = connection.collection.update_one({ "_id": idPaciente }, { "$set": { "tratamento": tratamento } }) 

    

