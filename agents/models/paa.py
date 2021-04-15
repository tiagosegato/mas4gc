
# Classe do agent PAA (Patient Analyzer Agent)
from pade.misc.utility import display_message
from pade.core.agent import Agent
from pade.acl.messages import ACLMessage
from pade.acl.aid import AID
from pade.behaviours.protocols import FipaRequestProtocol
import connection
from datetime import datetime
import pickle
import numpy as np
from scipy import stats
from sklearn.linear_model import LinearRegression


class CompRequest(FipaRequestProtocol):
    """FIPA Request Behaviour do agente PAA"""
    def __init__(self, agent):
        super(CompRequest, self).__init__(agent=agent, message=None, is_initiator=False)

    def handle_request(self, message):
        super(CompRequest, self).handle_request(message)
        display_message(self.agent.aid.localname, 'Possui novos pacientes?')
        
        # consulta novos pacientes no Glycon
        situacaoPaciente = relatorioAvaliacao(self)

        #respondendo ao PTA com a situação dos pacientes
        reply = message.create_reply()
        reply.set_performative(ACLMessage.INFORM)
        reply.set_content(situacaoPaciente)
        self.agent.send(reply)

class PAAgent(Agent):
    def __init__(self, aid):
        super(PAAgent, self).__init__(aid=aid, debug=False)
        
        self.comport_request = CompRequest(self)
        self.behaviours.append(self.comport_request)


# GERA E RELATÓRIO DE AVALIAÇÃO DO PACIENTE - GERANDO A SITUAÇÃO DO PACIENTE
def relatorioAvaliacao(self):
    # consultando dados específicos do último paciente cadastrado
    document = connection.collection.find({},{"_id": 1, "nome": 1, "sexo": 1, "imc": 1, "diabetes": 1, 
    "glicemia.valorGlicemia": 1, "glicemia.dataHoraColeta": 1, "glicemia.ultimaAlimentacao": 1}).sort("updateDate", -1).limit(1)
    
    # dados recuperados na consulta acima
    idPaciente = document[0]["_id"]
    paciente = document[0]["nome"]
    sexo = document[0]["sexo"]
    sexoBin = lambda sexo : int(1) if sexo == "Masculino" else int(0)
    sexo = sexoBin(sexo)
    imc = round(document[0]["imc"])
    diabetes = document[0]["diabetes"]
    diabetesBin = lambda diabetes : int(0) if diabetes == "Não tem" else (int(1) if diabetes == "Ignorado" else int(2))
    diabetes = diabetesBin(diabetes)

    coletas = len(document[0]["glicemia"])

    glicemias = document[0]["glicemia"]
    valoresGlicemia = [int(g['valorGlicemia']) for g in glicemias] # pegando os valores das glicemias 


    if (coletas >0):
        ultimas = valoresGlicemia
        ultimaGlicemia = ultimas[:-1]
        ultimaGlicemia.insert(0,99)
        #ultimaGlicemia = int(valoresGlicemia[coletas-2]) #pega apenas o
    else: ultimaGlicemia = 'Não coletada!'

    horario = document[0]["glicemia"]
    horariosColeta = [h['dataHoraColeta'] for h in horario] # pegando os horários das coletas
    horaColeta=[]
    for h in horariosColeta:
        hc = datetime.strptime(h, "%Y-%m-%d %H:%M")
        horaColeta.append(int(hc.strftime('%H')))

    # convertendo os horários em minutos
    temposColeta = []
    for x in horariosColeta:
        # diferença entre as horas...
        diferenca = (datetime.strptime(x, '%Y-%m-%d %H:%M')
                    - datetime.strptime(horariosColeta[0], '%Y-%m-%d %H:%M')).total_seconds() / 3600 #convertendo em horas
            
        horaUltimaColeta = diferenca # pega apenas a última coleta
        temposColeta.append(int(diferenca)) # adiciona os horários das coletas no array
    
    alimentacao = document[0]["glicemia"]
    ultimaAlimentacao = [int(a['ultimaAlimentacao']) for a in horario] # pegando as ultimas alimentações

    # exibindo os dados coletados
    print('')
    print('DADOS PACIENTE')
    print('ID Paciente: ', idPaciente)
    print('Nome: ', paciente)
    print('Sexo: ', sexo)
    print('IMC: ', imc)
    print('Diabetes: ', diabetes)
    print('')
    print('DADOS COLETAS GLICEMIAS')
    print(coletas, 'Coleta(s)')
    print('Última alimentação: ', ultimaAlimentacao)
    print('Tempo das coletas: ', temposColeta)
    print('Hora Coleta: ', horaColeta)
    print('Glicemias: ', valoresGlicemia)
    print('Última Glicemia: ', ultimaGlicemia)
    #print('Coletas: ', horariosColeta)
    print('')

    # verifica se existem glicemias para aquele paciente    
    if coletas == 0:
        situacao = "semGlicemia" 
    
    # caso tenha apenas uma glicemia coletada
    elif coletas == 1:
        #pega o valor da única glicemia coletada
        glicemia = int(glicemias[0]['valorGlicemia'])

        # compara com a tabela da escala glicêmica
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
        else: situacao = 'gInvalida' 

    #caso tenha mais de uma glicemia coletada
    elif coletas > 1:
        
        # CALCULANDO A PROBABILIDADE DA PRÓXIMA GLICEMIA
        '''
        #carregando os dados
        y = valoresGlicemia #glicemias (mg/dL)
        #x1 = idPaciente
        x2 = sexo #0-feminino/1-masculino
        x3 = imc
        x4 = diabetes #0-não tem/1-ignorado/2-tem diabetes
        x5 = temposColeta #tempo em horas (ex:6h em 6h)
        x6 = horaColeta #hora do dia (manhã, tarde, noite...)
        x7 = ultimaAlimentacao #última alimentação em horas
        x8 = ultimaGlicemia

        x = np.column_stack((x2, x3, x4, x5, x6, x7, x8)) #agrupa as variaveis preditoras

        reg = LinearRegression().fit(x, y) #efetua a regressão

        #apresentando os dados
        print(reg.score(x, y))
        print(reg.coef_)
        print(reg.intercept_)

        glicemia = reg.predict(np.array([[1,22,2,8,20,4,110]])) #tempo, hora, alimentação
        print('A previsão de Glicemia é: ', glicemia)
        '''
        print('Calculando previsão...')
        glicemia = 100

        # compara com a tabela da escala glicêmica
        if glicemia >= 0 and glicemia <= 49:
            situacao = 'prevHipoG'
        elif glicemia >=50 and glicemia <= 99:
            situacao = 'prevHipoL'
        elif glicemia >=100 and glicemia <= 200:
            situacao = 'prevgAlvo'
        elif glicemia >=201 and glicemia <= 250:
            situacao = 'prevHiperL'
        elif glicemia >=251 and glicemia <= 300:
            situacao = 'prevHiperG'
        elif glicemia >=301:
            situacao = 'prevHiperGG'
        else: situacao = 'gInvalida'
    
    #gerando o Relatório de Avaliação para enviar ao PTA
    #pickle.dumps converte o dict para str
    situacaoPaciente = pickle.dumps({'ID':idPaciente, 'Paciente': paciente, 'Situacao':situacao}) 

    return situacaoPaciente
