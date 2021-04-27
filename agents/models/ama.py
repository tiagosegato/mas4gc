# Classe do agent AMA (Adjust Monitoring Agent)
from pade.misc.utility import display_message
from pade.core.agent import Agent
from pade.acl.messages import ACLMessage
from pade.acl.aid import AID
from pade.behaviours.protocols import FipaRequestProtocol
from pade.behaviours.protocols import TimedBehaviour
from knowledge.cmrules import BloodGlucose
from knowledge.cmrules import CollectionMonitor
import pickle
from bson.objectid import ObjectId
import pymongo
import connection

class CompRequest(FipaRequestProtocol):
    """FIPA Request Behaviour do agente AMA"""
    def __init__(self, agent, message):
        super(CompRequest, self).__init__(agent=agent, message=message, is_initiator=True)

    def handle_inform(self, message):
        
        #converto de str para dict novamente
        situacaoPaciente_dict = pickle.loads(message.content) 
        display_message(self.agent.aid.localname, situacaoPaciente_dict) 

        # INDICA O TRATAMENTO DE ACORDO COM A REGRA 
        # instancia e chama a classe de regras!
        engine = CollectionMonitor()
        engine.reset()
        situacao = situacaoPaciente_dict['Situacao']
        idPaciente = situacaoPaciente_dict['ID']
        dataHora = situacaoPaciente_dict['DataHora']
        engine.declare(BloodGlucose(glicemia=situacao,  idPaciente=idPaciente, dataHora=dataHora))
        engine.run()


class ComportTemporal(TimedBehaviour):
    """Timed Behaviour do agente AMA"""
    def __init__(self, agent, time, messagex):
        super(ComportTemporal, self).__init__(agent, time)
        self.messagex = messagex

    def on_time(self):
        super(ComportTemporal, self).on_time()
        self.agent.send(self.messagex)

class AMAgent(Agent):
    def __init__(self, aid, paa_name):
        super(AMAgent, self).__init__(aid=aid)

        # cria a mensagem a ser enviada ao PAA a cada ? segundos
        messagex = ACLMessage(ACLMessage.REQUEST)
        messagex.set_protocol(ACLMessage.FIPA_REQUEST_PROTOCOL)
        messagex.add_receiver(AID(name=paa_name))
        messagex.set_content('Qual foi o Intervalo das coletas?')

        self.comport_request = CompRequest(self, messagex)
        self.comport_temp = ComportTemporal(self, 10.0, messagex)

        self.behaviours.append(self.comport_request)
        self.behaviours.append(self.comport_temp)

'''
PAA - consulta dados - relatorio avaliação 

#PreditorAgente - faixa - previsão 10s

PTA - RA - mec inferência(faixa) - tratamento 

AMA - RA - mec inferência(diferença) - frequencia 

'''

