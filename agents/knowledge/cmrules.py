from experta import *
from bson.objectid import ObjectId
import pymongo
import connection
from datetime import datetime, timedelta


class BloodGlucose(Fact):

    """ Informações sobre controle glicêmico"""
    ### ESCALA DE VALORES GLICÊMICOS (Medidadas isoladas - apenas glicemia)
    '''
     VALORES  |      EPISÓDIO            | COLETA    
      0-30    | Hipoglicemia Grave       | 1h     
      30-40   | Hipoglicemia Grave       | 2h
      40-50   | Hipoglicemia Leve        | 2h
      50-60   | Hipoglicemia Leve        | 4h 
      60-70   | Hipoglicemia Leve        | 4h
      70-80   | Normoglicemia            | 6h
      80-90   | Normoglicemia            | 8h
      90-120  | Normoglicemia            | 8h
      120-140 | Normoglicemia            | 8h
      140-160 | Hiperglicemia Leve       | 6h
      160-180 | Hiperglicemia Leve       | 4h
      180-200 | Hiperglicemia Grave      | 4h
      200-220 | Hiperglicemia Grave      | 2h
      220-240 | Hiperglicemia Grave      | 2h
      240-250 | Hiperglicemia Grave      | 1h
      > 250   | Hiperglicemia Gravíssima | 1h

    EXTRA
    regra 1 = 1 glicemia fora do alvo -> coletar novamente em 1h
    regra 2 = 2 fora - diminui 2 hs do padrão
    e assim sucessivamente... 

    ''' 
    pass
 
class CollectionMonitor(KnowledgeEngine):

    # 11 REGRAS #
    # COLETAS DE ACORDO COM SITUAÇÃO ATUAL
    @Rule(AND(BloodGlucose(glicemia=MATCH.glicemia), TEST(lambda glicemia: glicemia >= 0 and glicemia <= 30), 
              BloodGlucose(idPaciente=MATCH.idPaciente), BloodGlucose(dataHora=MATCH.dataHora)))
    def cm_rule1(self, idPaciente, dataHora):
        monitoramento = dataHora + timedelta(hours=1)
        print('Próxima coleta: ', monitoramento)
        print('')
        response = connection.collection.update_one({ "_id": idPaciente }, { "$set": { "monitoramento": monitoramento } }) 

    @Rule(AND(BloodGlucose(glicemia=MATCH.glicemia), TEST(lambda glicemia: glicemia > 30 and glicemia <= 50), 
              BloodGlucose(idPaciente=MATCH.idPaciente), BloodGlucose(dataHora=MATCH.dataHora)))
    def cm_rule2(self, idPaciente, dataHora):
        monitoramento = dataHora + timedelta(hours=2)
        print('Próxima coleta: ', monitoramento)
        print('')
        response = connection.collection.update_one({ "_id": idPaciente }, { "$set": { "monitoramento": monitoramento } })

    @Rule(AND(BloodGlucose(glicemia=MATCH.glicemia), TEST(lambda glicemia: glicemia > 50 and glicemia <= 70), 
              BloodGlucose(idPaciente=MATCH.idPaciente), BloodGlucose(dataHora=MATCH.dataHora)))
    def cm_rule3(self, idPaciente, dataHora):
        monitoramento = dataHora + timedelta(hours=4)
        print('Próxima coleta: ', monitoramento)
        print('')
        response = connection.collection.update_one({ "_id": idPaciente }, { "$set": { "monitoramento": monitoramento } })

    @Rule(AND(BloodGlucose(glicemia=MATCH.glicemia), TEST(lambda glicemia: glicemia > 70 and glicemia <= 80), 
              BloodGlucose(idPaciente=MATCH.idPaciente), BloodGlucose(dataHora=MATCH.dataHora)))
    def cm_rule4(self, idPaciente, dataHora):
        monitoramento = dataHora + timedelta(hours=6)
        print('Próxima coleta: ', monitoramento)
        print('')
        response = connection.collection.update_one({ "_id": idPaciente }, { "$set": { "monitoramento": monitoramento } })

    @Rule(AND(BloodGlucose(glicemia=MATCH.glicemia), TEST(lambda glicemia: glicemia > 80 and glicemia <= 140), 
              BloodGlucose(idPaciente=MATCH.idPaciente), BloodGlucose(dataHora=MATCH.dataHora)))
    def cm_rule5(self, idPaciente, dataHora):
        monitoramento = dataHora + timedelta(hours=8)
        print('Próxima coleta: ', monitoramento)
        print('')
        response = connection.collection.update_one({ "_id": idPaciente }, { "$set": { "monitoramento": monitoramento } })

    @Rule(AND(BloodGlucose(glicemia=MATCH.glicemia), TEST(lambda glicemia: glicemia > 140 and glicemia <= 160), 
              BloodGlucose(idPaciente=MATCH.idPaciente), BloodGlucose(dataHora=MATCH.dataHora)))
    def cm_rule6(self, idPaciente, dataHora):
        monitoramento = dataHora + timedelta(hours=6)
        print('Próxima coleta: ', monitoramento)
        print('')
        response = connection.collection.update_one({ "_id": idPaciente }, { "$set": { "monitoramento": monitoramento } })

    @Rule(AND(BloodGlucose(glicemia=MATCH.glicemia), TEST(lambda glicemia: glicemia > 160 and glicemia <= 200), 
              BloodGlucose(idPaciente=MATCH.idPaciente), BloodGlucose(dataHora=MATCH.dataHora)))
    def cm_rule7(self, idPaciente, dataHora):
        monitoramento = dataHora + timedelta(hours=4)
        print('Próxima coleta: ', monitoramento)
        print('')
        response = connection.collection.update_one({ "_id": idPaciente }, { "$set": { "monitoramento": monitoramento } })

    @Rule(AND(BloodGlucose(glicemia=MATCH.glicemia), TEST(lambda glicemia: glicemia > 200 and glicemia <= 240), 
              BloodGlucose(idPaciente=MATCH.idPaciente), BloodGlucose(dataHora=MATCH.dataHora)))
    def cm_rule8(self, idPaciente, dataHora):
        monitoramento = dataHora + timedelta(hours=2)
        print('Próxima coleta: ', monitoramento)
        print('')
        response = connection.collection.update_one({ "_id": idPaciente }, { "$set": { "monitoramento": monitoramento } })

    @Rule(AND(BloodGlucose(glicemia=MATCH.glicemia), TEST(lambda glicemia: glicemia > 240), 
              BloodGlucose(idPaciente=MATCH.idPaciente), BloodGlucose(dataHora=MATCH.dataHora)))
    def cm_rule9(self, idPaciente, dataHora):
        monitoramento = dataHora + timedelta(hours=1)
        print('Próxima coleta: ', monitoramento)
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