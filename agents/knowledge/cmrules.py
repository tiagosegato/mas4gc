from experta import *
from bson.objectid import ObjectId
import pymongo
import connection
from datetime import datetime, timedelta


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
 

class CollectionMonitor(KnowledgeEngine):

    # COLETAS DE ACORDO COM SITUAÇÃO ATUAL
    @Rule(AND(BloodGlucose(glicemia='hipoG'), BloodGlucose(idPaciente=MATCH.idPaciente), BloodGlucose(dataHora=MATCH.dataHora)))
    def cm_hipoG(self, idPaciente, dataHora):
        monitoramento = 'Próxima coleta: ' + str(dataHora + timedelta(hours=1))
        print(monitoramento)
        print('')
        response = connection.collection.update_one({ "_id": idPaciente }, { "$set": { "monitoramento": monitoramento } }) 

    @Rule(AND(BloodGlucose(glicemia='hipoL'), BloodGlucose(idPaciente=MATCH.idPaciente), BloodGlucose(dataHora=MATCH.dataHora)))
    def cm_hipoL(self, idPaciente, dataHora):
        monitoramento = 'Próxima coleta: ' + str(dataHora + timedelta(hours=4))
        print(monitoramento)
        print('')
        response = connection.collection.update_one({ "_id": idPaciente }, { "$set": { "monitoramento": monitoramento } }) 

    @Rule(AND(BloodGlucose(glicemia='gAlvo'), BloodGlucose(idPaciente=MATCH.idPaciente), BloodGlucose(dataHora=MATCH.dataHora)))
    def cm_gAlvo(self, idPaciente, dataHora):
        monitoramento = 'Próxima coleta: ' + str(dataHora + timedelta(hours=8))
        print(monitoramento)
        print('')
        response = connection.collection.update_one({ "_id": idPaciente }, { "$set": { "monitoramento": monitoramento } }) 

    @Rule(AND(BloodGlucose(glicemia='hiperL'), BloodGlucose(idPaciente=MATCH.idPaciente), BloodGlucose(dataHora=MATCH.dataHora)))
    def cm_hiperL(self, idPaciente, dataHora):
        monitoramento = 'Próxima coleta: ' + str(dataHora + timedelta(hours=4))
        print(monitoramento)
        print('')
        response = connection.collection.update_one({ "_id": idPaciente }, { "$set": { "monitoramento": monitoramento } }) 

    @Rule(AND(BloodGlucose(glicemia='hiperG'), BloodGlucose(idPaciente=MATCH.idPaciente), BloodGlucose(dataHora=MATCH.dataHora)))
    def cm_hiperG(self, idPaciente, dataHora):
        monitoramento = 'Próxima coleta: ' + str(dataHora + timedelta(hours=1))
        print(monitoramento)
        print('')
        response = connection.collection.update_one({ "_id": idPaciente }, { "$set": { "monitoramento": monitoramento } }) 

    @Rule(AND(BloodGlucose(glicemia='hiperGG'), BloodGlucose(idPaciente=MATCH.idPaciente), BloodGlucose(dataHora=MATCH.dataHora)))
    def cm_hiperGG(self, idPaciente, dataHora):
        monitoramento = 'Próxima coleta: ' + str(dataHora + timedelta(hours=0.5))
        print(monitoramento)
        print('')
        response = connection.collection.update_one({ "_id": idPaciente }, { "$set": { "monitoramento": monitoramento } }) 


    # COLETAS DE ACORDO COM PREVISÃO
    @Rule(AND(BloodGlucose(glicemia='prevHipoG'), BloodGlucose(idPaciente=MATCH.idPaciente), BloodGlucose(dataHora=MATCH.dataHora)))
    def cm_prevHipoG(self, idPaciente, dataHora):
        monitoramento = 'Próxima coleta: ' + str(dataHora + timedelta(hours=1))
        print(monitoramento)
        print('')
        response = connection.collection.update_one({ "_id": idPaciente }, { "$set": { "monitoramento": monitoramento } }) 

    @Rule(AND(BloodGlucose(glicemia='prevHipoL'), BloodGlucose(idPaciente=MATCH.idPaciente), BloodGlucose(dataHora=MATCH.dataHora)))
    def cm_prevHipoL(self, idPaciente, dataHora):
        monitoramento = 'Próxima coleta: ' + str(dataHora + timedelta(hours=4))
        print(monitoramento)
        print('')
        response = connection.collection.update_one({ "_id": idPaciente }, { "$set": { "monitoramento": monitoramento } }) 

    @Rule(AND(BloodGlucose(glicemia='prevgAlvo'), BloodGlucose(idPaciente=MATCH.idPaciente), BloodGlucose(dataHora=MATCH.dataHora)))
    def cm_prevgAlvo(self, idPaciente, dataHora):
        monitoramento = 'Próxima coleta: ' + str(dataHora + timedelta(hours=8))
        print(monitoramento)
        print('')
        response = connection.collection.update_one({ "_id": idPaciente }, { "$set": { "monitoramento": monitoramento } }) 

    @Rule(AND(BloodGlucose(glicemia='prevHiperL'), BloodGlucose(idPaciente=MATCH.idPaciente), BloodGlucose(dataHora=MATCH.dataHora)))
    def cm_prevHiperL(self, idPaciente, dataHora):
        monitoramento = 'Próxima coleta: ' + str(dataHora + timedelta(hours=4))
        print(monitoramento)
        print('')
        response = connection.collection.update_one({ "_id": idPaciente }, { "$set": { "monitoramento": monitoramento } }) 

    @Rule(AND(BloodGlucose(glicemia='prevHiperG'), BloodGlucose(idPaciente=MATCH.idPaciente), BloodGlucose(dataHora=MATCH.dataHora)))
    def cm_prevHiperG(self, idPaciente, dataHora):
        monitoramento = 'Próxima coleta: ' + str(dataHora + timedelta(hours=1))
        print(monitoramento)
        print('')
        response = connection.collection.update_one({ "_id": idPaciente }, { "$set": { "monitoramento": monitoramento } }) 

    @Rule(AND(BloodGlucose(glicemia='prevHiperGG'), BloodGlucose(idPaciente=MATCH.idPaciente), BloodGlucose(dataHora=MATCH.dataHora)))
    def cm_prevHiperGG(self, idPaciente, dataHora):
        monitoramento = 'Próxima coleta: ' + str(dataHora + timedelta(hours=0.5))
        print(monitoramento)
        print('')
        response = connection.collection.update_one({ "_id": idPaciente }, { "$set": { "monitoramento": monitoramento } }) 

# GCOLETAS COM SITUAÇÕES INCOMUNS
    @Rule(AND(BloodGlucose(glicemia='semGlicemia'), BloodGlucose(idPaciente=MATCH.idPaciente)))
    def bg_sem(self, idPaciente):
        tratamento = "Coleta de Necessária"
        print(tratamento)
        print('') 
        response = connection.collection.update_one({ "_id": idPaciente }, { "$set": { "tratamento": tratamento } }) 

    @Rule(AND(BloodGlucose(glicemia='gInvalida'), BloodGlucose(idPaciente=MATCH.idPaciente)))
    def bg_invalida(self, idPaciente):
        tratamento = " -- "
        print(tratamento)
        print('') 
        response = connection.collection.update_one({ "_id": idPaciente }, { "$set": { "tratamento": tratamento } }) 