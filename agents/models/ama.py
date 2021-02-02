
# Classe do agent AMA (Adjust Monitoring Agent)

class AdjustMonitoringAgent: 
    def __init__(self, freqColeta):
         self.freqColeta = freqColeta

    def calcularPlanoColeta(self):
        print("Plano Coleta")

    def emitirAlerta(self):
        print("ALERTA: Coletar a cada ", self.freqColeta, " horas")

ama = AdjustMonitoringAgent('6h')

ama.calcularPlanoColeta()
ama.emitirAlerta()