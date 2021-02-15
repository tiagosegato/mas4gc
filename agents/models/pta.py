
# Classe do agent PTA (Propose Treatment Agent)
from pade.misc.utility import display_message
from pade.core.agent import Agent
from pade.acl.messages import ACLMessage
from pade.acl.aid import AID
from pade.behaviours.protocols import FipaRequestProtocol
from pade.behaviours.protocols import TimedBehaviour
from knowledge.bgrules import GlicemicControl
from knowledge.bgrules import BloodGlucose

import pickle

class CompRequest(FipaRequestProtocol):
    """FIPA Request Behaviour of the PTA agent"""
    def __init__(self, agent, message):
        super(CompRequest, self).__init__(agent=agent, message=message, is_initiator=True)

    def handle_inform(self, message):
        #converto de str para dict novamente
        situacaoPaciente_dict = pickle.loads(message.content) 
        display_message(self.agent.aid.localname, situacaoPaciente_dict) 

        # INDICA O TRATAMENTO DE ACORDO COM A REGRA 

        situacao = situacaoPaciente_dict['Situacao']

        # instancia e chama a classe de regras!
        engine = GlicemicControl()
        engine.reset()
        engine.declare(BloodGlucose(glicemia=situacao))
        engine.run()


class ComportTemporal(TimedBehaviour):
    """Timed Behaviour of the PTA agent"""
    def __init__(self, agent, time, message):
        super(ComportTemporal, self).__init__(agent, time)
        self.message = message

    def on_time(self):
        super(ComportTemporal, self).on_time()
        self.agent.send(self.message)

class PTAgent(Agent):
    def __init__(self, aid, paa_name):
        super(PTAgent, self).__init__(aid=aid)

        message = ACLMessage(ACLMessage.REQUEST)
        message.set_protocol(ACLMessage.FIPA_REQUEST_PROTOCOL)
        message.add_receiver(AID(name=paa_name))
        message.set_content('novos pacientes?')

        self.comport_request = CompRequest(self, message)
        self.comport_temp = ComportTemporal(self, 5.0, message)

        self.behaviours.append(self.comport_request)
        self.behaviours.append(self.comport_temp)
