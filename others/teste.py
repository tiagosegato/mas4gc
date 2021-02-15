from pade.misc.utility import display_message, start_loop
from pade.core.agent import Agent
from pade.acl.messages import ACLMessage
from pade.acl.aid import AID
from pade.behaviours.protocols import FipaRequestProtocol
from pade.behaviours.protocols import TimedBehaviour

from datetime import datetime
from sys import argv

import connection

class CompRequest(FipaRequestProtocol):
    """FIPA Request Behaviour of the PAA agent"""
    def __init__(self, agent):
        super(CompRequest, self).__init__(agent=agent, message=None, is_initiator=False)

    def handle_request(self, message):
        super(CompRequest, self).handle_request(message)
        display_message(self.agent.aid.localname, 'Possui novos pacientes?')
        
        situacaoPaciente = consultarGlycon(self)

        reply = message.create_reply()
        reply.set_performative(ACLMessage.INFORM)
        #reply.set_content(now.strftime('%d/%m/%Y - %H:%M:%S'))
        reply.set_content(situacaoPaciente)
        self.agent.send(reply)


class CompRequest2(FipaRequestProtocol):
    """FIPA Request Behaviour of the PTA agent"""
    def __init__(self, agent, message):
        super(CompRequest2, self).__init__(agent=agent, message=message, is_initiator=True)

    def handle_inform(self, message):
        display_message(self.agent.aid.localname, message.content)


class ComportTemporal(TimedBehaviour):
    """Timed Behaviour of the PTA agent"""
    def __init__(self, agent, time, message):
        super(ComportTemporal, self).__init__(agent, time)
        self.message = message

    def on_time(self):
        super(ComportTemporal, self).on_time()
        self.agent.send(self.message)


class PAAgent(Agent):
    def __init__(self, aid):
        super(PAAgent, self).__init__(aid=aid, debug=False)
        self.comport_request = CompRequest(self)
        self.behaviours.append(self.comport_request)

def consultarGlycon(self):
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

            
        ####### gerarRelatorioAvaliacao(self)
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
            # TODO calcular as probabilidades de hipo e hiper futuras
            print("calcular próxima glicemia, com base nos dados:")
            situacao = "a calcular..."
            
        #gerando o Relatório de Avaliação para enviar ao PTA
        situacaoPaciente = "{'Paciente': paciente, 'Situacao':situacao}"
        #TODO como enviar como json ou dict?

        return situacaoPaciente

class PTAgent(Agent):
    def __init__(self, aid, paa_name):
        super(PTAgent, self).__init__(aid=aid)

        message = ACLMessage(ACLMessage.REQUEST)
        message.set_protocol(ACLMessage.FIPA_REQUEST_PROTOCOL)
        message.add_receiver(AID(name=paa_name))
        message.set_content('novos pacientes?')

        self.comport_request = CompRequest2(self, message)
        self.comport_temp = ComportTemporal(self, 20.0, message)

        self.behaviours.append(self.comport_request)
        self.behaviours.append(self.comport_temp)


if __name__ == '__main__':

    agents_per_process = 1
    c = 0
    agents = list()
    for i in range(agents_per_process):
        port = int(argv[1]) + c

        #PAA
        paa_name = 'PAA_{}@localhost:{}'.format(port, port)
        paa_agent = PAAgent(AID(name=paa_name))
        agents.append(paa_agent)
        
        #PTA
        pta_name = 'PTA_{}@localhost:{}'.format(port - 10000, port - 10000)
        pta_agent = PTAgent(AID(name=pta_name), paa_name)
        agents.append(pta_agent)

        c += 500

    start_loop(agents)