from pade.misc.utility import display_message, start_loop
from sys import argv
from pade.acl.aid import AID
from agents.models.PatientAnalyzerAgent import PatientAnalyzerAgent
from agents.models.ProposeTreatmentAgent import ProposeTreatmentAgent

#INSTANCIANDO OS AGENTES
if __name__ == '__main__':

    agents = list()
    port = int(argv[1])     
        
    #definindo o nome do agente (composto pelo IP e porta). Cada agente executa em uma porta diferente
    pta_agent_name = 'agent_pta_{}@localhost:{}'.format(port, port)
    pta_agent = ProposeTreatmentAgent(AID(name=pta_agent_name))
    agents.append(pta_agent)
        
    paa_agent_name = 'agent_paa_{}@localhost:{}'.format(port + 1000, port + 1000)
    paa_agent = PatientAnalyzerAgent(AID(name=paa_agent_name), pta_agent_name)
    agents.append(paa_agent)

    start_loop(agents)


# COMANDO QUE INICIALIZA O AMBIENTE DE EXECUÇÃO DO PADE:
# pade start-runtime --num 1 --port 20000 main.py 
# num = quantidade de vezes que o bloco de código (instanciação) vai ser executado