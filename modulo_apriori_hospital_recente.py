
class class_apriori:

    def carrega_dataset(hospital, convenio, tipo_glosa):
        # Banco de dados
        import cx_Oracle
        import pandas as pd
        import unicodedata

        # Função para remover a acentuação
        def remover_acentuacao(texto):
            return ''.join(c for c in unicodedata.normalize('NFD', texto) if unicodedata.category(c) != 'Mn')

        # Remover a acentuação do tipo_glosa
        var_hospital_sem_acentos = remover_acentuacao(hospital)
        var_convenio_sem_acentos = remover_acentuacao(convenio)
        tipo_glosa_sem_acentos = remover_acentuacao(tipo_glosa)

        # Conectando ao banco de dados
        uid = "****"    # Usuário
        pwd = "*******"   # Senha
        db = "****"  # String de conexão do Oracle, configurado no cliente Oracle, arquivo tnsnames.ora
        
        connection = cx_Oracle.connect(uid + "/" + pwd + "@" + db)  # Cria a conexão
        cursor = connection.cursor()  # Cria um cursor

        querystring = f"""SELECT /*+parallel(9)*/ HOSPITAL,
                                 REGIONAL,
                                 I_ITEM_CATEGORIA AS TIPO_DESPESA,
                                 SETOR_N1,
                                 SETOR_N2,
                                 TIPO_GRUPO,
                                 TIPO_ATENDIMENTO,
                                 CONVENIO,
                                 TIPO_GLOSA,
                                 SUM(QTD_LINHAS_GLOSA) AS QTD_LINHAS_GLOSA
                          FROM TASY.TB_GLOSA_APRIORI_RECENTE
                          WHERE MES_RECEBIMENTO = ADD_MONTHS (TRUNC (SYSDATE, 'MM'), -1)
                          AND FNC_ACENTUACAO(HOSPITAL) = '{var_hospital_sem_acentos}'
                          AND FNC_ACENTUACAO(CONVENIO) = '{var_convenio_sem_acentos}'
                          AND FNC_ACENTUACAO(TIPO_GLOSA) = '{tipo_glosa_sem_acentos}'
                          GROUP BY HOSPITAL,
                                   REGIONAL,
                                   I_ITEM_CATEGORIA,
                                   SETOR_N1,
                                   SETOR_N2,
                                   TIPO_GRUPO,
                                   TIPO_ATENDIMENTO,
                                   CONVENIO,
                                   TIPO_GLOSA
                          ORDER BY HOSPITAL, CONVENIO, TIPO_GLOSA
                  """

        # Executar a query com variáveis
        cursor.execute(querystring)
        nome_colunas = [row[0] for row in cursor.description]

        base = pd.DataFrame(cursor.execute(str(querystring)), columns=nome_colunas)  # Consulta SQL
        base = base.fillna(0)

        base['TIPO_DESPESA'] = base['TIPO_DESPESA'] + "/" + 'TIPO_DESPESA'
        base['SETOR_N1'] = base['SETOR_N1'] + "/" + 'SETOR_N1'
        base['SETOR_N2'] = base['SETOR_N2'] + "/" + 'SETOR_N2'
        base['TIPO_GRUPO'] = base['TIPO_GRUPO'] + "/" + 'TIPO_GRUPO'
        base['TIPO_ATENDIMENTO'] = base['TIPO_ATENDIMENTO'] + "/" + 'TIPO_ATENDIMENTO'
        
        return base

#####################################################################################################    
        
    def carrega_dataset_hospitais():
        # Banco de dados
        import cx_Oracle
        import pandas as pd
        
        # Conectando ao banco de dados
        uid = "****"    # Usuário
        pwd = "*******"   # Senha
        db = "****"  # String de conexão do Oracle, configurado no cliente Oracle, arquivo tnsnames.ora
        
        connection = cx_Oracle.connect(uid + "/" + pwd + "@" + db)  # Cria a conexão
        cursor = connection.cursor()  # Cria um cursor

        querystring_hospital = """SELECT /*+PARALLEL(8)*/ DISTINCT HOSPITAL
                                  FROM TASY.TB_GLOSA_APRIORI_RECENTE
                                  WHERE MES_RECEBIMENTO = ADD_MONTHS (TRUNC (SYSDATE, 'MM'), -1)
                                  AND CONVENIO IN ('BRADESCO','SUL AMERICA') AND TIPO_GLOSA IN ('Codificação','Precificação')
                                  ORDER BY HOSPITAL"""

        # Executar a query com variáveis
        cursor.execute(querystring_hospital)
        nome_colunas_hospital = [row[0] for row in cursor.description]

        hospitais = pd.DataFrame(cursor.execute(str(querystring_hospital)), columns=nome_colunas_hospital)  # Consulta SQL

        return hospitais


#####################################################################################################    

    def carrega_dataset_combinacoes():
            # Banco de dados
            import cx_Oracle
            import pandas as pd
            
            # Conectando ao banco de dados
            uid = "****"    # Usuário
            pwd = "*******"   # Senha
            db = "****"  # String de conexão do Oracle, configurado no cliente Oracle, arquivo tnsnames.ora
            
            connection = cx_Oracle.connect(uid + "/" + pwd + "@" + db)  # Cria a conexão
            cursor = connection.cursor()  # Cria um cursor

            querystring_combinacoes = """SELECT /*+PARALLEL(8)*/ DISTINCT HOSPITAL, CONVENIO, TIPO_GLOSA
                                         FROM TASY.TB_GLOSA_APRIORI_RECENTE
                                         WHERE MES_RECEBIMENTO = ADD_MONTHS (TRUNC (SYSDATE, 'MM'), -1)
                                         AND CONVENIO IN ('BRADESCO','SUL AMERICA') AND TIPO_GLOSA IN ('Codificação','Precificação')
                                         ORDER BY HOSPITAL, CONVENIO, TIPO_GLOSA"""

            # Executar a query com variáveis
            cursor.execute(querystring_combinacoes)
            nome_colunas_combinacoes = [row[0] for row in cursor.description]

            combinacoes = pd.DataFrame(cursor.execute(str(querystring_combinacoes)), columns=nome_colunas_combinacoes)  # Consulta SQL

            return combinacoes
    
#####################################################################################################    

       
    def cria_apriori(base, hospital, convenio, tipo_glosa):
        
        #bibliotecas

        #manipulação
        import pandas as pd
        import numpy as np
        import unicodedata

        #warnings
        import warnings
        warnings.simplefilter("ignore")

        #associação
        from apyori import apriori

    
        #Filtarndo o cluster
        base_apriori = base[(base['HOSPITAL'] == hospital) & (base['CONVENIO']== convenio) & (base['TIPO_GLOSA'] == tipo_glosa)]
        
        #replicando linhas
        linhas_replicadas = []
        
        for index, linha in base_apriori.iterrows():
            qtd = linha['QTD_LINHAS_GLOSA']
            linhas_replicadas.extend([linha] * qtd)
            
        df_replicado = pd.DataFrame(linhas_replicadas)
        df_replicado.reset_index(drop=True, inplace = True)
        base_apriori = df_replicado

        #drop coluna TARGET
        base_apriori = base_apriori.drop(['HOSPITAL','CONVENIO','TIPO_GLOSA','QTD_LINHAS_GLOSA','REGIONAL'], axis=1)
    
        #Formatando a transação
        
        #otimizado
        transactions = base_apriori.apply(lambda row: [str(value) for value in row.values if str(value) != '0'], axis=1).tolist()

    
        rules = apriori(transactions, min_support = 0.02, min_confidence = 0.7)
        results = list(rules)

        #Transferring the list to a table
        results = pd.DataFrame(results)

        #Filtra regras >= 4
        results['filtro'] = [True if len(x)>=4 else False for x in results['items']]
        results = results.loc[results['filtro'] == True]

        #drop o filtro
        results = results.drop('filtro', axis=1)
        results = results.reset_index(drop = True)

        #keep support in a separate data frame so we can use later.. 
        support = results.support
    
        #Formatando o dataset de resultado
        first_values = []
        second_values = []
        third_values = []
        fourth_value = []

        # loop number of rows time and append 1 by 1 value in a separate list.. 
        # first and second element was frozenset which need to be converted in list..
        for i in range(results.shape[0]):
            single_list = results['ordered_statistics'][i][0]
            first_values.append(list(single_list[0]))
            second_values.append(list(single_list[1]))
            third_values.append(single_list[2])
            fourth_value.append(single_list[3])
    

        antecedente = pd.DataFrame(first_values)
        consequente = pd.DataFrame(second_values)
        confidance=pd.DataFrame(third_values,columns=['Confidance'])
        lift=pd.DataFrame(fourth_value,columns=['lift'])
        
        #renomeando colunas
        nome_antecedente = ['ant1','ant2','ant3','ant4','ant5']
        nome_consequente = ['cons1','cons2','cons3','cons4','cons5']


        for i in range(0,antecedente.shape[1]):
            antecedente = antecedente.rename(columns={antecedente.columns[i]: nome_antecedente[i]})
    
    
        for i in range(0,consequente.shape[1]):
            consequente = consequente.rename(columns={consequente.columns[i]: nome_consequente[i]})

        # concat all list together in a single dataframe
        df_final = pd.concat([results['items'],antecedente,consequente,support,confidance,lift], axis=1)
        df_final.fillna(value='vazio', inplace=True)      
            
        #identificando as regras redundantes
        subset = []

        for i in range(0,len(df_final)):
            subset.append(np.sum([df_final['items'][i] <= df_final['items'][j] for j in range(0,len(df_final))],axis=0)>1)
    
       
        subset = pd.DataFrame(subset)
        df_final['redundante'] = subset
        
        #Filtrando as regras não redundantes
        df_final = df_final[df_final['redundante'] == False]
        df_final = df_final.drop('redundante', axis=1)
        df_final = df_final.reset_index(drop = True)
    
        return df_final
        
#####################################################################################################         
        
    def organiza_colunas(n, base):
    
        import numpy as np
        import pandas as pd

        j = n  # variação da coluna
        df = pd.DataFrame(base)

            # Iteração pelas linhas do DataFrame
        for i in range(0, len(df)):
                # Verificando se o valor não é 'vazio' ou NaN
            if df.iloc[i,j] != 'vazio':  #pd.notna(df.iloc[i, j]) and df.iloc[i, j] != 'vazio': 
                    split_value = df.iloc[i, j].split('/')

                    # Verificando o segundo valor da divisão
                    if split_value[1] == 'TIPO_DESPESA':
                        df.iloc[i, df.shape[1] - 5] = split_value[0]
                    elif split_value[1] == 'SETOR_N1':
                        df.iloc[i, df.shape[1] - 4] = split_value[0]
                    elif split_value[1] == 'SETOR_N2':
                        df.iloc[i, df.shape[1] - 3] = split_value[0]
                    elif split_value[1] == 'TIPO_GRUPO':
                        df.iloc[i, df.shape[1] - 2] = split_value[0]
                    elif split_value[1] == 'TIPO_ATENDIMENTO':
                        df.iloc[i, df.shape[1] - 1] = split_value[0]
            else:
                    # Se o valor for vazio ou NaN, substituímos por 'vazio'
                    i = i+1 # df.iloc[i, j] = 'vazio'

        # Substituindo valores vazios ou NaN em todo o DataFrame
        df.replace('',np.nan,inplace = True)
        df.fillna(value='vazio', inplace=True)

        return df

#####################################################################################################       

    def organiza_variaveis(n, base):

        j = n
        df = base
    
        for i in range(0, len(df)):
        
            if df.iloc[i,j] != 'vazio':
            
                df.iloc[i,j] = df.iloc[i,j].split('/')[0] 
                    
        return df
    
#####################################################################################################  


    def gera_string_glosa(hospital, convenio,tipo_glosa, i, df): #Passar regional com ''
        
    
        #I_ITEM_CATEGORIA
    
        if df.iloc[i][df.shape[1]-5] == 'vazio':
    
            var_tipo_despesa = ' IS NOT NULL'
    
        else:
            var_tipo_despesa = "= " + "'" + str(df.iloc[i][df.shape[1]-5]) + "'"
        
        #SETOR_N1
    
        if df.iloc[i][df.shape[1]-4] == 'vazio':
    
            var_setor_n1 = ' IS NOT NULL'
    
        else:
            var_setor_n1 = "= " + "'" + str(df.iloc[i][df.shape[1]-4]) + "'"
        
        #SETOR_N2
    
        if df.iloc[i][df.shape[1]-3] == 'vazio':
    
            var_setor_n2 = ' IS NOT NULL'
    
        else:
            var_setor_n2 = "= " + "'" + str(df.iloc[i][df.shape[1]-3]) + "'"
        
        #TIPO_GRUPO
    
        if df.iloc[i][df.shape[1]-2] == 'vazio':
    
            var_tipo_grupo = ' IS NOT NULL'
    
        else:
            var_tipo_grupo = "= " + "'" + str(df.iloc[i][df.shape[1]-2]) + "'"
        
        #TIPO_ATENDIMENTO
    
        if df.iloc[i][df.shape[1]-1] == 'vazio':
    
            var_tipo_atend = ' IS NOT NULL'
    
        else:
            var_tipo_atend = "= " + "'" + str(df.iloc[i][df.shape[1]-1]) + "'"
      
        
        return f"SELECT /*+parallel(9)*/ SUM(VALOR_GLOSA) FROM TASY.TB_GLOSA_APRIORI_RECENTE WHERE CONVENIO = '{convenio}' AND HOSPITAL = '{hospital}' AND I_ITEM_CATEGORIA {var_tipo_despesa} AND SETOR_N1 {var_setor_n1} AND SETOR_N2 {var_setor_n2} AND TIPO_GRUPO {var_tipo_grupo} AND TIPO_ATENDIMENTO {var_tipo_atend} AND TIPO_GLOSA = '{tipo_glosa}' AND MES_RECEBIMENTO = TRUNC(SYSDATE, 'month') - INTERVAL '1' MONTH"

    
#####################################################################################################    
    
    def gera_string_cobrado(hospital, convenio, tipo_glosa, i, df): #Passar regional com ''
           
        #I_ITEM_CATEGORIA
    
        if df.iloc[i][df.shape[1]-6] == 'vazio':
    
            var_tipo_despesa = ' IS NOT NULL'
    
        else:
            var_tipo_despesa = "= " + "'" + str(df.iloc[i][df.shape[1]-6]) + "'"
        
        #SETOR_N1
    
        if df.iloc[i][df.shape[1]-5] == 'vazio':
    
            var_setor_n1 = ' IS NOT NULL'
    
        else:
            var_setor_n1 = "= " + "'" + str(df.iloc[i][df.shape[1]-5]) + "'"
        
        #SETOR_N2
    
        if df.iloc[i][df.shape[1]-4] == 'vazio':
    
            var_setor_n2 = ' IS NOT NULL'
    
        else:
           var_setor_n2 = "= " + "'" + str(df.iloc[i][df.shape[1]-4]) + "'"
        
        #TIPO_GRUPO
    
        if df.iloc[i][df.shape[1]-3] == 'vazio':
    
            var_tipo_grupo = ' IS NOT NULL'
    
        else:
            var_tipo_grupo = "= " + "'" + str(df.iloc[i][df.shape[1]-3]) + "'"
        
        #TIPO_ATENDIMENTO
    
        if df.iloc[i][df.shape[1]-2] == 'vazio':
    
            var_tipo_atend = ' IS NOT NULL'
    
        else:
            var_tipo_atend = "= " + "'" + str(df.iloc[i][df.shape[1]-2]) + "'"
        
        
        return f"SELECT /*+parallel(9)*/ SUM(ITEM_VALOR_COBRADO) FROM TASY.TB_GLOSA_VALOR_COBRADO_RECENTE WHERE CONVENIO = '{convenio}' AND HOSPITAL = '{hospital}' AND I_ITEM_CATEGORIA {var_tipo_despesa} AND SETOR_N1 {var_setor_n1} AND SETOR_N2 {var_setor_n2} AND TIPO_GRUPO {var_tipo_grupo} AND TIPO_ATENDIMENTO {var_tipo_atend} "

#####################################################################################################          
       
    def executa_loop(hospital, convenio, tipo_glosa):
        import pandas as pd
        import numpy as np
        
        ################### Apriori ##################################
        base_inicial = class_apriori.carrega_dataset(hospital, convenio, tipo_glosa)
        base_regras = class_apriori.cria_apriori(base_inicial, hospital, convenio, tipo_glosa)
        
        ################## Organizar colunas #########################
        base_regras = pd.DataFrame(base_regras)
        
        # Organizar colunas 
        base_regras['TIPO_DESPESA'] = ''
        base_regras['SETOR_N1'] = ''
        base_regras['SETOR_N2'] = ''
        base_regras['TIPO_GRUPO'] = ''
        base_regras['TIPO_ATENDIMENTO'] = ''
        
        for i in range(1, base_regras.shape[1] - 8):
            class_apriori.organiza_colunas(i, base_regras)
        
        #base_regras.replace('', np.nan, inplace=True)
        #base_regras.fillna(value='vazio', inplace=True)
        base_regras.replace('', np.nan, inplace=True)
        base_regras.fillna(value='vazio')
        
        ################## Organizar variáveis #########################
        for i in range(1, base_regras.shape[1] - 8):
            class_apriori.organiza_variaveis(i, base_regras)

        base_regras = base_regras.drop('items', axis=1)

        ################## Query valor de glosa #########################
        # Banco de dados
        import cx_Oracle
        
        # Conectando ao banco de dados
        uid = "tasy"    # Usuário
        pwd = "rede123"   # Senha
        db = "regra"  # String de conexão do Oracle, configurado no cliente Oracle, arquivo tnsnames.ora
        
        connection = cx_Oracle.connect(uid + "/" + pwd + "@" + db)  # Cria a conexão
        cursor = connection.cursor()  # Cria um cursor
        
        lista_query_glosa = []
        resultado_lista_glosa = [lista_query_glosa.append(pd.DataFrame(cursor.execute(str(class_apriori.gera_string_glosa(hospital, convenio, tipo_glosa, i, base_regras)))).values.tolist()) for i in range(0, len(base_regras))]
        
        base_regras['VALOR_GLOSA'] = [lista_query_glosa[i][0][0] for i in range(0, len(base_regras))]
        
        ################## Query valor cobrado #########################
        lista_query_cobrado = []
        resultado_lista_cobrado = [lista_query_cobrado.append(pd.DataFrame(cursor.execute(str(class_apriori.gera_string_cobrado(hospital, convenio, tipo_glosa, i, base_regras)))).values.tolist()) for i in range(0, len(base_regras))]
        
        base_regras['VALOR_COBRADO'] = [lista_query_cobrado[i][0][0] for i in range(0, len(base_regras))]
        
        base_regras['INDICE_GLOSA'] = (base_regras['VALOR_GLOSA'] / base_regras['VALOR_COBRADO'])
        
        base_regras['CONVENIO'] = convenio
        base_regras['HOSPITAL'] = hospital
        base_regras['TIPO_GLOSA'] = tipo_glosa
        base_regras['support_qtd'] = base_regras['support'] * (base_inicial['QTD_LINHAS_GLOSA'].sum())

        return base_regras

    