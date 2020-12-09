# MAS4GC

MAS4GC é o acrônimo de MultiAgent System for Glicemic Control e como o próprio nome diz, é um sistema multiagente para controle glicêmico de pacientes internados em UTI.

Para executar este protótipo de SMA basta seguir os seguintes passos:

1 - Instalar (ou ter instalado) o  framework PADE (Python Agent DEvelopment), conforme a documentação: https://pade.readthedocs.io/en/latest/user/instalacao.html#installation-page

2 - Clonar o projeto na sua máquina;

3 - Utilizando o Terminal/Console/CMD acesse o diretório mas4cg/agents
4 - Uma vez na pasta agents execute: pade start-runtime --num 1 --port 20000 sma-mas4gc.py
5 - Ignore o pedido de usuário e senha teclando enter para ambas

A figura 1 representa os passos 3, 4 e 5:
![executando o projeto](https://github.com/tiagosegato/mas4gc/blob/main/imagens/pro-1.png?raw=true)
Figura 1 - Executando o SMA

Na sequência a aplicação já entrará em execução.

A figura 2 representa o framework PADE em execução:
![executando o projeto](https://github.com/tiagosegato/mas4gc/blob/main/imagens/pro-2.png?raw=true)
Figura 2 - PADE em execução

A figura 3 apresenta a troca de mensagens entre os agentes
![executando o projeto](https://github.com/tiagosegato/mas4gc/blob/main/imagens/pro-3.png?raw=true)
Figura 3 - Troca de mensagens entre os agentes
