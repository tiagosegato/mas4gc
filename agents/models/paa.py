
# Classe do agent PAA (Patient Analyzer Agent)
from pade.misc.utility import display_message
from pade.core.agent import Agent
from pade.acl.messages import ACLMessage
from pade.acl.aid import AID
from pade.behaviours.protocols import FipaRequestProtocol
import connection
import pickle
import numpy as np
from scipy import stats
from datetime import datetime


class CompRequest(FipaRequestProtocol):
    """FIPA Request Behaviour do agente PAA"""
    def __init__(self, agent):
        super(CompRequest, self).__init__(agent=agent, message=None, is_initiator=False)

    def handle_request(self, message):
        super(CompRequest, self).handle_request(message)
        display_message(self.agent.aid.localname, 'Possui novos pacientes?')
        
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
    # consultando dados específicos do último paciente cadastrado
    document = connection.collection.find({}, {"_id": 1, "nome": 1, "glicemia.valorGlicemia": 1, "glicemia.dataHoraColeta": 1 }).sort("updateDate", -1).limit(1)

    # dados recuperados na consulta acima
    paciente = document[0]["nome"]
    coletas = len(document[0]["glicemia"])
    glicemias = document[0]["glicemia"]
    idPaciente = document[0]["_id"]
    horariosColeta = [h['dataHoraColeta'] for h in glicemias] # pegando os horários das coletas
    

    # exibindo os dados coletados
    print('')
    print('Paciente: ', paciente)
    print('Quantidade de coletas: ', coletas)
    #print('Glicemias coletadas: ', glicemias)
    #print('Horários coletas: ', horariosColeta)  

    # verifica se existem glicemias para aquele paciente    
    if coletas == 0:
        situacao = "semGlicemia" 
    
    # caso tenha apenas uma glicemia coletada
    elif coletas == 1:
        #pega o valor da única glicemia coletada
        for x in glicemias[0].values():
            glicemia = int(x)

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

    #caso tenha mais de uma glicemia coletada
    elif coletas > 1:

        # convertendo os horários em minutos
        temposColeta = []
        for x in horariosColeta:
            # diferença entre as horas...
            diferenca = (datetime.strptime(x, '%Y-%m-%d %H:%M') - datetime.strptime(horariosColeta[0], '%Y-%m-%d %H:%M')).total_seconds() / 60

            horaUltimaColeta = diferenca # pega apenas a última coleta
            temposColeta.append(diferenca) # adiciona os horários das coletas no array

        # pegando os valores das glicemias
        valoresGlicemia = [int(g['valorGlicemia']) for g in glicemias]

        print('Glicemias coletadas: ', valoresGlicemia)
        print('Horários das coletas: ', temposColeta)
        print('Última coleta: ', horaUltimaColeta)
        print('') 

        # CALCULANDO A PROBABILIDADE DA PRÓXIMA GLICEMIA
        # adicionando os valores dos horários e valores das coletas nos arrays
        x = np.array(temposColeta)
        y = np.array(valoresGlicemia)

        # fazendo o ajuste do modelo (Regressão Linear)
        a, b, r, p_value, std_err = stats.linregress(x, y)
        y_mod = a * x + b # gerando os pontos do modelo

        glicemia = a * (horaUltimaColeta + 240) + b # gerando a prox. glicemia para as próximas 4h
        print('') 
        print(f"A próxima glicemia (4h) será de: {glicemia:6.2f}")
        print('') 

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
    situacaoPaciente = pickle.dumps({'ID':idPaciente, 'Paciente': paciente, 'Situacao':situacao}) 

    return situacaoPaciente
