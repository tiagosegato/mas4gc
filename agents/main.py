from pade.misc.utility import start_loop
from sys import argv
from pade.acl.aid import AID
from models.paa import PAAgent
from models.pta import PTAgent
from models.ama import AMAgent

#INSTANCIANDO OS AGENTES
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

        #AMA
        ama_name = 'AMA_{}@localhost:{}'.format(port + 10000, port + 10000)
        ama_agent = AMAgent(AID(name=ama_name), paa_name)
        agents.append(ama_agent)

        c += 500

    start_loop(agents)


# COMANDO QUE INICIALIZA O AMBIENTE DE EXECUÇÃO DO PADE:
# pade start-runtime --num 1 --port 20000 main.py 
# num = quantidade de vezes que o bloco de código (instanciação) vai ser executado
