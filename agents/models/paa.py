
# Classe do agent PAA (Patient Analyzer Agent)
from pade.misc.utility import display_message
from pade.core.agent import Agent
from pade.acl.messages import ACLMessage
from pade.acl.aid import AID
from pade.behaviours.protocols import FipaRequestProtocol
import connection
from datetime import datetime
import pickle
import numpy as np
import pandas as pd
import json
from sklearn.linear_model import LinearRegression


class CompRequest(FipaRequestProtocol):
    """FIPA Request Behaviour do agente PAA"""
    def __init__(self, agent):
        super(CompRequest, self).__init__(agent=agent, message=None, is_initiator=False)

    def handle_request(self, message):
        super(CompRequest, self).handle_request(message)
        display_message(self.agent.aid.localname, message.content)
        
        # consulta novos pacientes no Glycon
        situacaoPaciente = relatorioAvaliacao(self)

        #respondendo ao PTA com a situação dos pacientes
        reply = message.create_reply()
        reply.set_performative(ACLMessage.INFORM)
        reply.set_content(situacaoPaciente)
        self.agent.send(reply)


class PAAgent(Agent):
    def __init__(self, aid):
        super(PAAgent, self).__init__(aid=aid, debug=False)
        
        self.comport_request = CompRequest(self)
        self.behaviours.append(self.comport_request)


# GERA E RELATÓRIO DE AVALIAÇÃO DO PACIENTE - GERANDO A SITUAÇÃO DO PACIENTE
def relatorioAvaliacao(self):

    #### ULTIMO PACIENTE/COLETA #####
    # consultando dados específicos do último paciente cadastrado
    pacienteAtual = connection.collection.find({},{"_id": 1, "nome": 1, "sexo": 1, "imc": 1, "diabetes": 1, 
    "glicemia.valorGlicemia": 1, "glicemia.dataHoraColeta": 1, "glicemia.ultimaAlimentacao": 1}).sort("updateDate", -1).limit(1)
    
    for pa in pacienteAtual:

        idPacienteA = pa["_id"]
        pacienteA = pa["nome"]
        sexo = pa["sexo"]
        
        sexoBin = lambda sexo : int(1) if sexo == "Masculino" else int(0)
        sexoA = sexoBin(sexo)
        
        imcA = round(pa["imc"])
        
        diabetes = pa["diabetes"]
        diabetesBin = lambda diabetes : int(0) if diabetes == "Não tem" else (int(1) if diabetes == "Ignorado" else int(2))
        diabetesA = diabetesBin(diabetes)
        
        coletas = len(pa["glicemia"])

        if (coletas > 0):
            glicemias = pa["glicemia"]
            valoresGlicemiaA = [int(g['valorGlicemia']) for g in glicemias] # pegando os valores das glicemias 
            glicemiaA = valoresGlicemiaA[coletas-1]
            
            ultimaGlicemiaA = int(valoresGlicemiaA[coletas-2]) 

            horario = pa["glicemia"]
            horariosColeta = [h['dataHoraColeta'] for h in horario] # pegando os horários das coletas
            horaColetaA=[]
            for h in horariosColeta:
                dataHoraColetaA = datetime.strptime(h, "%Y-%m-%d %H:%M")
                horaColetaA.append(int(dataHoraColetaA.strftime('%H')))
            horaA = horaColetaA[coletas-1]

            # convertendo os horários em horas
            for x in horariosColeta:
                # diferença entre as horas...
                diferenca = (datetime.strptime(x, '%Y-%m-%d %H:%M')
                            - datetime.strptime(horariosColeta[0], '%Y-%m-%d %H:%M')).total_seconds() / 3600 #convertendo em horas
                    
                tempoA = round(diferenca) 
            
            alimentacao = pa["glicemia"]
            ultimaA = [int(a['ultimaAlimentacao']) for a in horario] # pegando as ultimas alimentações
            ultimaAlimentacaoA = ultimaA[coletas-1]
        else: 
            print('Paciente sem coletas!')
            ultimaAlimentacaoA = '-'
            tempoA = '-'
            horaA = '-'
            glicemiaA = '-'
            ultimaGlicemiaA = '-'
        
    #### TODOS OS PACIENTES #####
    # consultando todos os pacientes para gerar o dataframe
    pacientes = connection.collection.find({},{"_id": 1, "nome": 1, "sexo": 1, "imc": 1, "diabetes": 1, 
    "glicemia.valorGlicemia": 1, "glicemia.dataHoraColeta": 1, "glicemia.ultimaAlimentacao": 1})

    print('')
    #print('DataFrame:')
    dataframe = pd.DataFrame(columns=['codigo', 'sexo', 'imc', 'diabetes', 'tempos', 'hora', 'alimentacao', 
                                      'ultimaglicemia', 'glicemia'])
    
    # dados recuperados na consulta acima
    for p in pacientes:
       
        idPaciente = p["_id"]
        paciente = p["nome"]

        sexo = p["sexo"]
        sexoBin = lambda sexo : int(1) if sexo == "Masculino" else int(0)
        sexo = sexoBin(sexo)

        imc = round(p["imc"])

        diabetes = p["diabetes"]
        diabetesBin = lambda diabetes : int(0) if diabetes == "Não tem" else (int(1) if diabetes == "Ignorado" else int(2))
        diabetes = diabetesBin(diabetes)

        coletas = len(p["glicemia"])

        glicemias = p["glicemia"]
        valoresGlicemia = [int(g['valorGlicemia']) for g in glicemias] # pegando os valores das glicemias 
        
        if (coletas >0):
            ultimas = valoresGlicemia
            ultimaGlicemia = ultimas[:-1]
            ultimaGlicemia.insert(0,99)
            #ultimaGlicemia = int(valoresGlicemia[coletas-2]) #pega apenas o
        else: ultimaGlicemia = 'Não coletada!'

        horario = p["glicemia"]
        horariosColeta = [h['dataHoraColeta'] for h in horario] # pegando os horários das coletas
        horaColeta=[]
        for h in horariosColeta:
            hc = datetime.strptime(h, "%Y-%m-%d %H:%M")
            horaColeta.append(int(hc.strftime('%H')))

        # convertendo os horários em horas
        temposColeta = []
        for x in horariosColeta:
            # diferença entre as horas...
            diferenca = (datetime.strptime(x, '%Y-%m-%d %H:%M')
                        - datetime.strptime(horariosColeta[0], '%Y-%m-%d %H:%M')).total_seconds() / 3600 #convertendo em horas
                
            horaUltimaColeta = diferenca # pega apenas a última coleta
            temposColeta.append(int(diferenca)) # adiciona os horários das coletas no array
        
        alimentacao = p["glicemia"]
        ultimaAlimentacao = [int(a['ultimaAlimentacao']) for a in horario] # pegando as ultimas alimentações

        ### CRIANDO O DATAFRAME ###
        for i in range(coletas):
            df = pd.DataFrame({'codigo':idPaciente,'sexo':sexo, 'imc':imc, 'diabetes':diabetes, 'tempos':temposColeta[i], 
                               'hora':horaColeta[i], 'alimentacao':ultimaAlimentacao[i], 'ultimaglicemia':ultimaGlicemia[i], 
                               'glicemia':valoresGlicemia[i]}, index=[0])
            dataframe = pd.concat([dataframe, df], ignore_index=True)
            dataframe.reset_index()
            i+=1
    
    #print(dataframe)
    #print('')


    ### VERIFICA A QUANTIDADE DE GLICEMIAS COLETADAS ###
    # verifica se existem glicemias para aquele paciente    
    if coletas == 0:
        situacao = "semGlicemia" 
        dataHoraColetaA = "semGlicemia"
    
    # caso tenha apenas uma glicemia coletada
    elif coletas == 1:
        #pega o valor da única glicemia coletada
        glicemia = int(glicemias[0]['valorGlicemia'])

        # compara com a tabela da escala glicêmica
        if glicemia >= 0 and glicemia <= 49:
            situacao = 'hipoG'
        elif glicemia >=50 and glicemia <= 99:
            situacao = 'hipoL'
        elif glicemia >=100 and glicemia <= 200:
            situacao = 'gAlvo'
        elif glicemia >=201 and glicemia <= 250:
            situacao = 'hiperL'
        elif glicemia >=251 and glicemia <= 300:
            situacao = 'hiperG'
        elif glicemia >=301:
            situacao = 'hiperGG'
        else: situacao = 'gInvalida' 

        #TODO criar setup de configuração de variáveis (glicemia, faixa alvo, horas predição, etc...)

    #caso tenha mais de uma glicemia coletada
    elif coletas > 1:
        
        # CALCULANDO A PROBABILIDADE DA PRÓXIMA GLICEMIA
        #carregando o dataset 50x30
        dataframe = pd.read_csv('../data/conj3.csv', header=0, sep=';')
        print(dataframe)

        #recebendo os dados do dataset
        x = dataframe.iloc[:, :-1] #descarta a última coluna (glicemia)
        y = dataframe.iloc[:, -1] #pega apenas a última (glicemia) 

        reg = LinearRegression().fit(x, y) #efetua a regressão
        
        proxPrev = 4 #previsão para daqui 4? horas
        glicemia = reg.predict(np.array([[idPacienteA, sexoA, imcA, diabetesA, tempoA+proxPrev, horaA+proxPrev, 
                                         ultimaAlimentacaoA, glicemiaA]]))
        
        '''
        print('Dados para Previsão')
        print('Nome: ', pacienteA)
        print('Código: ', idPacienteA)
        print('Sexo: ', sexoA)
        print('IMC: ', imcA)
        print('Diabetes: ', diabetesA)
        print('Tempo das coletas: ', tempoA+proxPrev)
        print('Hora Coleta: ', horaA+proxPrev)
        print('Última alimentação: ', ultimaAlimentacaoA)
        print('Glicemia Atual: ', glicemiaA)
        print('Última Glicemia: ', ultimaGlicemiaA)
        print('') '''  
        print('Previsão de Glicemia para', proxPrev,'hs é de: ',glicemia, f'com acurácia de: {reg.score(x, y):6.2f}')
        
        # compara com a tabela da escala glicêmica
        if glicemia >= 0 and glicemia <= 49:
            situacao = 'prevHipoG'
        elif glicemia >=50 and glicemia <= 99:
            situacao = 'prevHipoL'
        elif glicemia >=100 and glicemia <= 200:
            situacao = 'prevgAlvo'
        elif glicemia >=201 and glicemia <= 250:
            situacao = 'prevHiperL'
        elif glicemia >=251 and glicemia <= 300:
            situacao = 'prevHiperG'
        elif glicemia >=301:
            situacao = 'prevHiperGG'
        else: situacao = 'gInvalida'   
    
    #gerando o Relatório de Avaliação para enviar ao PTA
    #pickle.dumps converte o dict para str
    situacaoPaciente = pickle.dumps({'ID':idPacienteA, 'Paciente': pacienteA, 'Situacao':situacao, 'DataHora':dataHoraColetaA}) 

    return situacaoPaciente