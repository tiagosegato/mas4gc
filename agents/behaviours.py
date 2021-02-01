from pade.misc.utility import display_message, start_loop
from pade.core.agent import Agent
from pade.acl.messages import ACLMessage
from pade.acl.aid import AID
from pade.behaviours.protocols import FipaRequestProtocol
from pade.behaviours.protocols import TimedBehaviour

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
        display_message(self.agent.aid.localname, 'Segue o Relatório:')
        display_message(self.agent.aid.localname, message.content)# precisa receber os dados aqui...
        #efetua os cálculos que tem que efetuar....
        reply = message.create_reply() #método permite apenas responder a quem solicitou, não precisa definir
        reply.set_performative(ACLMessage.INFORM) #setando o rótulo da mensagem (INFORM)
        reply.set_content("Relatório de Avaliação Recebido!") #seta o conteúdo 
        self.agent.send(reply) #envia o reply

#FIPA Request Behaviour of the PAA agent
class CompRequest2(FipaRequestProtocol):
    def __init__(self, agent, message):
        super(CompRequest2, self).__init__(agent=agent, message=message, is_initiator=True)

    def handle_inform(self, message):
        display_message(self.agent.aid.localname, message.content)

