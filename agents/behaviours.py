from pade.misc.utility import display_message
from pade.core.agent import Agent
from pade.acl.messages import ACLMessage
from pade.acl.aid import AID
from pade.behaviours.protocols import FipaRequestProtocol
from pade.behaviours.protocols import TimedBehaviour

### CLASSES DE COMPORTAMENTOS FIPA ###

# comportamentos temporais do Agente PAA
class ComportTemporal(TimedBehaviour):

    def __init__(self, agent, time, message):
        super(ComportTemporal, self).__init__(agent, time)
        self.message = message

    def on_time(self):
        super(ComportTemporal, self).on_time()
        self.agent.send(self.message) # envia msg de tempo em tempo


# comportamento de requisição do Agent PTA
class CompRequest(FipaRequestProtocol):
    def __init__(self, agent):
        super(CompRequest, self).__init__(agent=agent, message=None, is_initiator=False)

    # esse método é executada quando chega uma mensagem do tipo request
    def handle_request(self, message): 

        super(CompRequest, self).handle_request(message)
        display_message(self.agent.aid.localname, message.content)# conteúdo da msg recebida!!!

        # efetua os cálculos (TRATAMENTO) que tem que efetuar...
        ##############
        
        ##############

        reply = message.create_reply() # responde a quem solicitou
        reply.set_performative(ACLMessage.INFORM) # setando o rótulo da mensagem (INFORM)
        reply.set_content("PTA -> PAA: Relatório de Avaliação Recebido!") # seta o conteúdo 
        self.agent.send(reply) # envia o reply

#FIPA Request Behaviour of the PAA agent
class CompRequest2(FipaRequestProtocol):
    def __init__(self, agent, message):
        super(CompRequest2, self).__init__(agent=agent, message=message, is_initiator=True)

    def handle_inform(self, message):
        display_message(self.agent.aid.localname, message.content)

