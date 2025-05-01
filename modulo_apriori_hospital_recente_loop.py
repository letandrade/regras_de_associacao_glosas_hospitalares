
#Apriori

#bibliotecas

#banco de dados
import cx_Oracle

#manipulação
import pandas as pd
import numpy as np
seed = 100

#warnings
import warnings
warnings.simplefilter("ignore")

#associação
from apyori import apriori

#modulo apriori
from modulo_apriori_hospital_recente import class_apriori

# Declarando variáveis usadas para regras 

convenios = ['CONVÊNIO A', 'CONVÊNIO B']

hospitais = class_apriori.carrega_dataset_hospitais()
hospitais = hospitais['HOSPITAL'].tolist()

tipo_glosa = ['Codificação','Precificação']

print('Variáveis importadas.')

# Executar a consulta para buscar as combinações válidas
combinacoes_validas = class_apriori.carrega_dataset_combinacoes()

print('Combinações existentes extraídas.')

# Criando combinações
#combinacoes_validas_set = set(zip(combinacoes_validas['HOSPITAL'], combinacoes_validas['CONVENIO'], combinacoes_validas['TIPO_GLOSA']))
combinacoes_validas_set = set(zip(combinacoes_validas[combinacoes_validas.columns[0]], combinacoes_validas[combinacoes_validas.columns[1]], combinacoes_validas[combinacoes_validas.columns[2]]))

# Lista para armazenar os DataFrames resultantes
base_apriori = []

# Loop para iterar sobre as combinações válidas
for hospital in hospitais:
    for convenio in convenios:
        for tipo in tipo_glosa:
            # Verifica se a combinação (hospital, convênio, tipo de glosa) é válida
            if (hospital, convenio, tipo) in combinacoes_validas_set:
                # Realiza o processo de clusterização para a combinação válida
                df_atual = class_apriori.executa_loop(hospital, convenio, tipo)
                # Empilha o DataFrame da iteração na lista base_apriori
                base_apriori.append(df_atual)
                print(f'Regras do hospital:{hospital}, convênio:{convenio}, tipo_glosa:{tipo}')

# Agora empilha todos os DataFrames da lista base_apriori
base_apriori_df = pd.concat(base_apriori, ignore_index=True)

#Substituindo valores em branco
#base_apriori_df = base_apriori_df.fillna(value='vazio')
#Substituindo valores em branco
base_apriori_df = base_apriori_df.apply(lambda col: col.fillna('vazio') if col.dtype == 'object' else col)

# Agora base_cluster_df é um único DataFrame com todos os dados empilhados
print(base_apriori_df)
print(f'Tamanho de base_cluster: {len(base_apriori_df)}')  # Exibe a quantidade de itens empilhados


# Ajustando o caminho base
caminho_base = r"\\Fscorp05\monitoramento$\08.Desenvolvimento\03.Dashboards\Cluster_Apriori"

# Concatenando o nome do arquivo ao caminho base
nome_do_arquivo_csv = f"{caminho_base}\\base_apriori_por_hospital.csv"

#exportar arquivo
base_apriori_df.to_csv(nome_do_arquivo_csv, index=False, encoding='utf-8')
print('Arquivo base_apriori_por_hospital.csv exportado')

#encerrar
print('Fim do script')
