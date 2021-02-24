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

    #usar o gAlvo para testes
    @Rule(AND(BloodGlucose(glicemia='gAlvo'), NOT(BloodGlucose(idPaciente='0'))))
    def bg_gAlvo(self):
        recomendacao = "Manter observação"
        
        bg = BloodGlucose()
        valores = bg.items.idPaciente
    
        print('Valores:', valores)
        print(recomendacao)
        print('')

    @Rule(BloodGlucose(glicemia='semGlicemia'))
    def bg_sem(self):
        recomendacao = "Paciente necessita de coleta!"
        print(recomendacao)
        print('')

    @Rule(BloodGlucose(glicemia='hipoG'))
    def bg_hipoG(self):
        recomendacao = "Aplicar 4 ampolas de glicose a 50% IV"
        print(recomendacao)
        print('')

    @Rule(BloodGlucose(glicemia='hipoL'))
    def bg_hipoL(self):
        recomendacao = "Aplicar 2 ampolas de glicose a 50% IV"
        print(recomendacao)
        print('')

    '''
    @Rule(BloodGlucose(glicemia='gAlvo'))
    def bg_gAlvo(self):
        recomendacao = "Manter observação"
        print(recomendacao)
    '''

    @Rule(BloodGlucose(glicemia='hiperL'))
    def bg_hiperL(self):
        recomendacao = "Aplicar 2 unidade de insulina regular SC"
        print(recomendacao)
        print('')

    @Rule(BloodGlucose(glicemia='hiperG'))
    def bg_hiperG(self):
        recomendacao = "Aplicar 4 unidade de insulina regular SC"
        print(recomendacao)
        print('')

    @Rule(BloodGlucose(glicemia='hiperGG'))
    def bg_hiperGG(self):
        recomendacao = "Aplicar 6 unidade de insulina regular SC"
        print(recomendacao)
        print('')

    @Rule(BloodGlucose(glicemia='gInvalida'))
    def bg_invalida(self):
        recomendacao = "Glicemia Inválida!"
        print(recomendacao)
        print('')

    
# Atualizando situacao do paciente no BD
#def fazerRecomendacao(idPaciente, recomendacao):    
    #response = connection.collection.update_one({ "_id": ObjectId(idPaciente) }, { "$set": { "recomendacao": recomendacao } }) 
    #print(recomendacao)
