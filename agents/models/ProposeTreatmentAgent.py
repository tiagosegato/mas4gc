
# Classe do agent PTA (Propose Treatment Agent)

from pade.misc.utility import display_message, start_loop
from pade.core.agent import Agent
from pade.acl.messages import ACLMessage
from pade.acl.aid import AID

from agents.behaviours import CompRequest


class ProposeTreatmentAgent(Agent): 
    def __init__(self, aid, proxGlicemia, aplicacao):
        
        super(ProposeTreatmentAgent, self).__init__(aid=aid, debug=False)
        self.proxGlicemia = proxGlicemia
        self.aplicacao = aplicacao

        self.comport_request = CompRequest(self)
        self.behaviours.append(self.comport_request)
    

    def calcProxGlicemia(self):
        print(f'Próxima glicemia será de: {self.proxGlicemia} mg/dL')

    def calcularTratamento(self):
        print("Tratamento X")

    def emitirAlerta(self):
        print(f'ALERTA: Aplicar {self.aplicacao} de Insulina')

pta = ProposeTreatmentAgent('190', '2')

pta.calcProxGlicemia()
pta.calcularTratamento()
pta.emitirAlerta()