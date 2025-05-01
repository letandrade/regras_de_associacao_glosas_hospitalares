<h1 align="center"> Regras de Associação para Glosas Hospitalares <br /> </h1>

## **1.0 Visão geral**

No ramo da prestação de serviços de saúde, é comum ouvir falar sobre glosa hospitalar. As glosas correspondem a valores de faturamento que não são recebidos ou são recusados pelas operadoras de saúde (convênios), geralmente devido a problemas de comunicação ou inconsistências nas informações fornecidas pelo prestador. 

Na maioria das vezes, as glosas ocorrem quando os dados enviados pelo prestador não coincidem com os registros da operadora. Por isso, evitar glosas é fundamental para manter a eficiência na gestão financeira das instituições de saúde.

Diante da relevância desse tema, propõe-se a criação de um modelo de regras de associação.

Este projeto aplica uma técnica de aprendizado de máquina não supervisionado, com foco na criação de regras de associação (Apriori), para analisar padrões recorrentes em glosas hospitalares.

Para este caso específico, o objetivo das regras é Identificar variáveis que frequentemente ocorrem juntas em casos de glosa, como tipo de despesa, tipo de atendimento, grupo e setor (nível 1 e 2). Essa abordagem possibilita compreender os principais fatores associados às glosas, tornando a análise mais estratégica e contribuindo para a redução de glosas e otimização do faturamento hospitalar.

## **2.0 Objetivos técnicos**

Desenvolver modelos de regras de associação (Apriori) segmentados por hospital, convênio e tipo de glosa, com o objetivo de identificar padrões e facilitar a análise das principais causas de glosas.

Foi implementada uma estrutura em loop, capaz de gerar automaticamente diferentes regras para cada combinação de hospital, operadora e tipo de glosa. Por exemplo:

Para a base de dados 1, referente ao Hospital A, da Operadora B e do Tipo de Glosa C, foram identificados 50 regras.

Já para a base de dados 2, correspondente ao Hospital E, da Operadora F e do Tipo de Glosa G, foram identificados 100 regras.

Essa rotina de criação dos modelos foi transformada em um processo automático, com a execução do script Python agendada por meio do Agendador de Tarefas do Windows, garantindo a atualização periódica dos dados sem necessidade de intervenção manual.

Além disso, um painel no Power BI será alimentado com os resultados dessas análises, permitindo o acompanhamento semanal da evolução das glosas, com foco na tomada de decisão mais rápida e estratégica por parte das áreas responsáveis.

## **3.0 Ferramentas utilizadas**

SQL: Utilizado para construção da bases de dados.

Python: Utilizado para o processamento e modelagem dos dados, incluindo a criação dos modelos apriori e tratamento das bases segmentadas por hospital, operadora e tipo de glosa. É importante dizer que foi utilizado o ambiente Anaconda.

Agendador de Tarefas do Windows: Responsável pela automação da execução do script Python, garantindo que os modelos sejam atualizados de forma periódica e sem necessidade de intervenção manual.

Power BI: Ferramenta utilizada para a visualização e monitoramento dos resultados. Os dados processados são integrados ao painel para acompanhamento semanal das glosas, facilitando a análise e as correções de glosa.

## **4.0 Desenvolvimento**

Todos os passos a seguir estão detalhados nos módulos e arquivos de texto em anexo.

### **4.1 Construção da base de dados em SQL**

A base de dados foi extraída de um banco de dados, esse script faz a seleção e tratamento de variáveis. 

A query construída foi chamada através da conexão com o banco de dados Oracle executada através da biblioteca cx_oracle.

### **4.2 Módulo de Regras de Associação para Análise de Glosas Hospitalares**


## **5.0 Resultados**
