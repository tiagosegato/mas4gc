
# Classe do agent PAA (Patient Analyzer Agent)
from pade.misc.utility import display_message
from pade.core.agent import Agent
from pade.acl.messages import ACLMessage
from pade.acl.aid import AID
from pade.behaviours.protocols import FipaRequestProtocol
from pade.behaviours.protocols import TimedBehaviour

import connection
import pickle

# Comportamentos temporais do Agente PAA
class ComportTemporal(TimedBehaviour):

    def __init__(self, agent, time, message):
        super(ComportTemporal, self).__init__(agent, time)
        self.message = message

    def on_time(self):
        super(ComportTemporal, self).on_time()
        self.agent.send(self.message) # envia msg de tempo em tempo


# Solicitações do agente PAA (FIPA)
class CompRequest(FipaRequestProtocol):
    def __init__(self, agent, message):
        super(CompRequest, self).__init__(agent=agent, message=message, is_initiator=True)

    def handle_inform(self, message):
        display_message(self.agent.aid.localname, message.content)

# CLASSE PAA
class PatientAnalyzerAgent(Agent): 
    def __init__(self, aid, pta_agent_name):
        super(PatientAnalyzerAgent, self).__init__(aid=aid)

        # mensagem que requisita algo ao agente PTA
        message = ACLMessage(ACLMessage.REQUEST) #cria a mensagem por meio da classe ACLMessage
        message.set_protocol(ACLMessage.FIPA_REQUEST_PROTOCOL) #seta o protocolo da msg
        message.add_receiver(AID(name=pta_agent_name)) #adiciona pra quem a mensagem vai

        ##########
        # consultarGlycon(self)
        # consultando dados específicos do último paciente cadastrado
        document = connection.collection.find({}, {"_id": 0, "nome": 1, "glicemia.valorGlicemia": 1 }).sort("updateDate", -1).limit(1)
        
        # nome, quantidade de coletas e as glicemias
        paciente = document[0]["nome"]
        coletas = len(document[0]["glicemia"])
        glicemias = document[0]["glicemia"]
        
        # exibindo os dados coletados
        print('')
        print('Paciente encontrado:')
        print('Paciente: ', paciente)
        print('Quantidade de Coletas: ', coletas)
        print('Glicemias coletadas: ', glicemias)
        print('')

        #situacaoPaciente = gerarRelatorioAvaliacao(self)
        if coletas == 1:
        #pega apenas o valor da glicemia coletada
            for x in glicemias[0].values():
                glicemia = int(x)

            # mostra a situação de acordo com a tabela
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
            else: print('glicemia inválida!')

        elif coletas > 1:
            #caso tenha mais de uma glicemia coletada
            for x in document:
                #TODO calcular as probabilidades de hipo e hiper futuras
                print("calcular próxima glicemia, com base nos dados:")
                print(x)

        #gerando o Relatório de Avaliação para enviar ao PTA
        self.situacaoPaciente = {'Paciente': paciente, 'Situacao':situacao }
        ##########

        message.set_content(self.situacaoPaciente) # seta o conteúdo na mensagem

        # executa o que está implementado no CompRequest2 a cada ?? segundos
        self.comport_request = CompRequest(self, message) #instancia o comportamento de request
        self.comport_temp = ComportTemporal(self, 3.0, message) #instanciando a classe ComportTemporal

        #adiciona os comportamentos a variável behaviours
        self.behaviours.append(self.comport_request)
        self.behaviours.append(self.comport_temp)


    # FAZ A CONSULTA DOS PACIENTES E GLICEMIA NO GLYCON
    #def consultarGlycon(self):


    # COM BASE NA GLICEMIA DO PACIENTE VERIFICA QUAL A SUA SITUAÇÃO (HIPO, HIPER, ETC...)
    #def gerarRelatorioAvaliacao(self, document, paciente, coletas, glicemias):
