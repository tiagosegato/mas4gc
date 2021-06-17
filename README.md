# MAS4GC

MAS4GC é o acrônimo de MultiAgent System for Glicemic Control e como o próprio nome diz, é um sistema multiagente para controle glicêmico de pacientes internados em UTI. Tal projeto foi implementado por meio da linguagem Python e faz uso dos frameworks PADE e Experta.

Nesse repositório está disponível todo o código fonte no diretório _agents_. O dataset utilizado para testes e complemento para o modelo de predição se encontra em _data_. As pastas _pade_ e _experta_ contém os frameworks utilizados. E em _project_ alguns dos diagramas utilizados na modelagem desse projeto, como diagramas de classes, sequência, atividades, a arquitetura da solução e os diagramas da modelagem Tropos.


Para executar este protótipo de SMA basta seguir os seguintes passos:

1 - Instalar (ou ter instalado) o framework PADE (Python Agent DEvelopment), conforme a documentação: https://pade.readthedocs.io/en/latest/user/instalacao.html#installation-page;

2 - Instalar (ou ter instalado) o framework Experta, disponível em: https://experta.readthedocs.io/en/latest/index.html;

3 - Clonar o projeto na sua máquina;

4 - Utilizando o Terminal/Console/CMD acesse o diretório mas4cg/agents;

5 - Uma vez na pasta agents execute: pade start-runtime --num 1 --port 20000 sma-mas4gc.py;

6 - Ignore o pedido de usuário e senha teclando enter para ambas;

A figura 1 representa os passos 4, 5 e 6:
![executando o projeto](https://github.com/tiagosegato/mas4gc/blob/main/others/pro-1.png?raw=true)
Figura 1 - Executando o SMA.

Na sequência a aplicação já entrará em execução.

A figura 2 representa o framework PADE em execução:
![executando o projeto](https://github.com/tiagosegato/mas4gc/blob/main/others/pro-2.png?raw=true)
Figura 2 - PADE em execução.

A figura 3 apresenta o MAS4GC em funcionamento. O primeiro passo é a criação dos três agentes PAA, AMA e PTA. Na sequência o agente PAA recebe as solicitaçÕes de novas coletas, caso tenha ele calcula a previsão desssa glicemia para as próximas 4 horas e informa o respectivo valor. Tal valor é enviado aos agentes PTA e AMA, que por sua vez consulta uma base de regras e por meio do mecanismo de inferência retorna as recomendaçÕes de tratamento e monitoramento mais adequaado de acordo com a situação dos pacientes. 
![executando o projeto](https://github.com/tiagosegato/mas4gc/blob/main/others/pro-3.png?raw=true)
Figura 3 - Funcionamento resumido do MAS4GC.

O MAS4GC faz parte do back-end de um sistema web chamado Glycon (disponível em: http://glycon.herokuapp.com/), esse sistema serve de interface entre os profissionais da saúde com o sistema multiagente. A Figura 4 apresenta as recomendações de monitoramento e tratamento feitas pelo MAS4GC.
![executando o projeto](https://github.com/tiagosegato/mas4gc/blob/main/others/pro-4.png?raw=true)
Figura 4 - Interface do Glycon

Todo o processo pocesso de troca de mensagem entre os sistemas pode ser observado por meio do diagrama de sequências exibido na Figura 5.
![executando o projeto](https://github.com/tiagosegato/mas4gc/blob/main/project/tropos/4-sequence-diagram.png?raw=true)
Figura 5 - Diagrama de Sequência do MAS4GC.

