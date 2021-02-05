
# Classe do agent PTA (Propose Treatment Agent)

from pade.core.agent import Agent
from pade.acl.messages import ACLMessage
from pade.acl.aid import AID
from behaviours import CompRequest


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
