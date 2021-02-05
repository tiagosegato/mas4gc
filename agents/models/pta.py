
# Classe do agent PTA (Propose Treatment Agent)
from pade.misc.utility import display_message
from pade.core.agent import Agent
from pade.acl.messages import ACLMessage
from pade.acl.aid import AID
from pade.behaviours.protocols import FipaRequestProtocol
from knowledge.bgrules import GlicemicControl
from knowledge.bgrules import BloodGlucose

# Comportamento de requisição do Agente PTA
class CompRequest(FipaRequestProtocol):
    def __init__(self, agent):
        super(CompRequest, self).__init__(agent=agent, message=None, is_initiator=False)

    # esse método é executada quando chega uma mensagem do tipo request
    def handle_request(self, message): 

        super(CompRequest, self).handle_request(message)
        display_message(self.agent.aid.localname, message.content) # conteúdo da msg recebida!!!
        
        # INDICA O TRATAMENTO DE ACORDO COM A REGRA 
        ##############
        
        situacao = message.content['Situacao'] # TODO preciso pegar  o valor de message.content...

        # instancia e chama a classe de regras!
        engine = GlicemicControl()
        engine.reset()
        engine.declare(BloodGlucose(glicemia=situacao))
        engine.run()

        ##############


        reply = message.create_reply() # responde a quem solicitou
        reply.set_performative(ACLMessage.INFORM) # setando o rótulo da mensagem (INFORM)
        reply.set_content("PTA -> PAA: Relatório de Avaliação Recebido!") # seta o conteúdo 
        self.agent.send(reply) # envia o reply


class ProposeTreatmentAgent(Agent): 
    def __init__(self, aid):
        super(ProposeTreatmentAgent, self).__init__(aid=aid, debug=False)

        self.comport_request = CompRequest(self)
        self.behaviours.append(self.comport_request)

    def calcProxGlicemia(self):
        print(f'Próxima glicemia será de ??? mg/dL')

    def calcularTratamento(self):
        print("Tratamento X")

    def emitirAlerta(self):
        print(f'ALERTA: Aplicar ???? de Insulina')
