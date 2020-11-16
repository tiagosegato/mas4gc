
from pade.misc.utility import display_message, start_loop
from pade.core.agent import Agent
from pade.acl.messages import ACLMessage
from pade.acl.aid import AID
from pade.behaviours.protocols import FipaRequestProtocol
from pade.behaviours.protocols import TimedBehaviour
from sys import argv

### CLASSE DE COMPORTAMENTOS TEMPORAIS - FIPA ###
#comportamentos de tempo em tempo do Agente PAA
class ComportTemporal(TimedBehaviour):

    def __init__(self, agent, time, message):
        super(ComportTemporal, self).__init__(agent, time)
        self.message = message

    #executa de acordo com o tempo passado (time)
    def on_time(self):
        super(ComportTemporal, self).on_time()
        self.agent.send(self.message) #o que ele faz de tempo em tempo (envia mensagem)


### CLASSES DE PROTOCOLOS - PADRÃO FIPA ###

# Comportamento de Request do Agent PTA
class CompRequest(FipaRequestProtocol):

    def __init__(self, agent):
        super(CompRequest, self).__init__(agent=agent, message=None, is_initiator=False)

    # esse método é executada quando chega uma mensagem do tipo request
    def handle_request(self, message): 
        super(CompRequest, self).handle_request(message)
        display_message(self.agent.aid.localname, 'EvaluationReport received!')
        display_message(self.agent.aid.localname, 'Vou analisar o ER e calcular um novo tratamento...')
        #efetua os cálculos que tem que efetuar....
        reply = message.create_reply() #método permite apenas responder a quem solicitou, não precisa definir
        reply.set_performative(ACLMessage.INFORM) #setando o rótulo da mensagem (INFORM)
        reply.set_content("Recebi seu EvaluationReport, tks! \n") #seta o conteúdo 
        self.agent.send(reply) #envia o reply

class CompRequest2(FipaRequestProtocol):
    """FIPA Request Behaviour of the PAA agent"""
    def __init__(self, agent, message):
        super(CompRequest2, self).__init__(agent=agent, message=message, is_initiator=True)

    def handle_inform(self, message):
        display_message(self.agent.aid.localname, message.content)




#CLASSE QUE DEFINE O AGENTE PAA
class PaaAgent(Agent):
    def __init__(self, aid, pta_agent_name):
        super(PaaAgent, self).__init__(aid=aid)

        # message that requests pta of PTA agent.
        message = ACLMessage(ACLMessage.REQUEST) #cria a mensagem por meio da classe ACLMessage
        message.set_protocol(ACLMessage.FIPA_REQUEST_PROTOCOL) #seta o protocolo da msg
        message.add_receiver(AID(name=pta_agent_name)) #adiciona pra quem a mensagem vai
        message.set_content('EvaluationReport') #seta o conteúdo

        # executa o que está implementado no CompRequest2 a cada 8 segundos
        self.comport_request = CompRequest2(self, message) #instancia o comportamento de request
        self.comport_temp = ComportTemporal(self, 10.0, message) #instanciando a classe ComportTemporal

        #adiciona os comportamentos a variável behaviours
        self.behaviours.append(self.comport_request)
        self.behaviours.append(self.comport_temp)


### CLASSE QUE DEFINE O AGENTE PTA ###
class PtaAgent(Agent):
    def __init__(self, aid):
        super(PtaAgent, self).__init__(aid=aid, debug=False)

        self.comport_request = CompRequest(self)
        self.behaviours.append(self.comport_request)


#INSTANCIANDO OS AGENTES
if __name__ == '__main__':

    agents = list()
    port = int(argv[1]) 
        
    #definindo o nome do agente (composto pelo IP e porta). Cada agente executa em uma porta diferente
    pta_agent_name = 'agent_pta_{}@localhost:{}'.format(port, port)
    pta_agent = PtaAgent(AID(name=pta_agent_name))
    agents.append(pta_agent)
        
    paa_agent_name = 'agent_paa_{}@localhost:{}'.format(port + 1000, port + 1000)
    paa_agent = PaaAgent(AID(name=paa_agent_name), pta_agent_name)
    agents.append(paa_agent)

    start_loop(agents)

# COMANDO QUE INICIALIZA O AMBIENTE DE EXECUÇÃO DO PADE:
# pade start-runtime --num 1 --port 20000 sma-mas4gc.py 
# num = quantidade de vezes que o bloco de código (instanciação) vai ser executado