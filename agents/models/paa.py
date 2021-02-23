
# Classe do agent PAA (Patient Analyzer Agent)
from pade.misc.utility import display_message
from pade.core.agent import Agent
from pade.acl.messages import ACLMessage
from pade.acl.aid import AID
from pade.behaviours.protocols import FipaRequestProtocol
import connection
import pickle


class CompRequest(FipaRequestProtocol):
    """FIPA Request Behaviour do agente PAA"""
    def __init__(self, agent):
        super(CompRequest, self).__init__(agent=agent, message=None, is_initiator=False)

    def handle_request(self, message):
        super(CompRequest, self).handle_request(message)
        display_message(self.agent.aid.localname, 'Possui novos pacientes?')
        
        # consulta novos pacientes no Glycon
        situacaoPaciente = consultarGlycon(self)

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


def consultarGlycon(self):
    # consultando dados específicos do último paciente cadastrado
    document = connection.collection.find({}, {"_id": 1, "nome": 1, "glicemia.valorGlicemia": 1 }).sort("updateDate", -1).limit(1)
    #document = connection.collection.find({}, sort=[( '_id', pymongo.DESCENDING )])
    
    paciente = document[0]["nome"]
    coletas = len(document[0]["glicemia"])
    glicemias = document[0]["glicemia"]
    idPaciente = document[0]["_id"]

    # exibindo os dados coletados
    print('')
    print('Paciente encontrado:')
    print('Paciente: ', paciente)
    print('Quantidade de Coletas: ', coletas)
    print('Glicemias coletadas: ', glicemias)
    print('')
    
    # TODO SÓ REPETIR SE FOR UMA NOVA COLETA
        
    # verifica se existem glicemias para aquele paciente    
    if coletas == 0:
        situacao = "semGlicemia" 
    
    #caso tenha apenas uma glicemia coletada
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
        #pega o valor da última glicemia coletada
        for x in glicemias[-1].values():
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

        # TODO calcular as probabilidades de hipo e hiper futuras
        print("calcular a probabilidade da próxima glicemia...")
        print('')   
                
    #gerando o Relatório de Avaliação para enviar ao PTA
    #pickle.dumps converte o dict para str
    situacaoPaciente = pickle.dumps({'ID':idPaciente, 'Paciente': paciente, 'Situacao':situacao})

    return situacaoPaciente
