import pandas as pd 
import re 
import textdistance

#Hago una limpieza de los datos, trabajando con cada set de datos.

#%%
op_organicos = pd.read_csv('padron-de-operadores-organicos-certificados.csv', encoding = 'latin-1')
loc_censales = pd.read_csv('localidades-censales.csv')
dic_cod_dep = pd.read_csv('diccionario_cod_depto.csv')
dic_clases = pd.read_csv('diccionario_clae2.csv')
salario_sp = pd.read_csv('w_median_depto_priv_clae2.csv')
#%% 
# FUNCIONES QUE USAMOS

def eliminar_duplicados(df):
    #toma un df y elimina todos los registros duplicados del mismo
    df.drop_duplicates(inplace = True)
    

def corregir_plural(palabra):
    if re.search(r'S$', palabra):
        return palabra[:-1]
    else:
        return palabra

def cantidad_nulls(df, columna):
    cantidad_nulos = df[columna].isnull().sum()
    return cantidad_nulos 


def detectar_typos(lista, threshold=0.9):
    pares_similares = []
    for i in range(len(lista)):
        for j in range(i+1, len(lista)):
            string1 = str(lista[i])
            string2 = str(lista[j])
            similaridad = textdistance.jaro_winkler(string1, string2)
            if similaridad >= threshold:
                pares_similares.append((string1, string2))
    return pares_similares


def reemplazar_en_df(valor, palabras_clave):
    for palabra in palabras_clave:
        if palabra in valor:
            return palabra
    return valor

def eliminar_espacios_extras(string):
    #elimino espacios extras entre palabras de un string
    return re.sub("\s+", " ", string)

def eliminar_parentesis(string):
    # Eliminar los paréntesis que no estén cerrados
    string = re.sub(r'[\(\)]', '', string)
    # Reemplazar los espacios en blanco múltiples por uno solo
    string = re.sub(r'\s+', ' ', string.strip())
    
    return string

def pasar_a_minuscula_sin_tildes(string):
    
    string = string.lower()
    string = re.sub('[á]', 'a', string)
    string = re.sub('[é]', 'e', string)
    string = re.sub('[í]', 'i', string)
    string = re.sub('[ó]', 'o', string)
    string = re.sub('[ú]', 'u', string)
    return string

def corregir_df(df):
    
    df1 = df.copy()
    #a todas las columnas del df las dejo en minuscula y sin tilde
    for col in df1.columns:
        #verifico que tome columnas que se le pueden aplicar funciones de string
        if df1[col].dtype == 'O':
            df1[col] = df[col].apply(lambda x: pasar_a_minuscula_sin_tildes(str(x)))
    return df1

def crear_id_unico(df, columna):
    #crea un id unico para cada valor diferentes de la columna que le pasan
    #devuelve una serie de pandas con el id
    return pd.factorize(df[columna])[0]
#%%

# ----- PADRON OPERADOR ORGANICO --------
print("---------PADRON OPERADORES ORGANICOS--------")
#rename de las columnas
op_organicos.rename(columns = {'rubro':'rubro_desc','categoria':'categoria_desc',
                               'Certificadora_id':'certificadora_id','razón social':'razon_social'}, inplace = True)

op_organicos.columns
#%%

#cambio los tipos de datos en el df
op_organicos.dtypes
op_organicos['provincia'] = op_organicos['provincia'].astype(str)
op_organicos['departamento'] = op_organicos['departamento'].astype(str)
op_organicos['localidad'] = op_organicos['localidad'].astype(str)
op_organicos['rubro_desc'] = op_organicos['rubro_desc'].astype(str)
op_organicos['productos'] = op_organicos['productos'].astype(str)
op_organicos['categoria_desc'] = op_organicos['categoria_desc'].astype(str)
op_organicos['certificadora_deno'] = op_organicos['certificadora_deno'].astype(str)
op_organicos['establecimiento'] = op_organicos['establecimiento'].astype(str)

op_organicos.dtypes

#%%
#para todas las columnas de tipo string hago .str.strip() para eliminar posibles espacios al comienzo o al final del string
op_organicos['provincia'] = op_organicos['provincia'].str.strip()
op_organicos['departamento'] = op_organicos['departamento'].str.strip()
op_organicos['localidad'] = op_organicos['localidad'].str.strip()
op_organicos['rubro_desc'] = op_organicos['rubro_desc'].str.strip()
op_organicos['productos'] = op_organicos['productos'].str.strip()
op_organicos['categoria_desc'] = op_organicos['categoria_desc'].str.strip()
op_organicos['certificadora_deno'] = op_organicos['certificadora_deno'].str.strip()
op_organicos['establecimiento'] = op_organicos['establecimiento'].str.strip()

#%%
#estudio valores nulls en las columnas

nulls_por_columna = op_organicos.isnull().sum()
print(nulls_por_columna)

#veamos que valores Nulls no hay, pero hay que estudiar casos de valores que ean posibles nulls

#pais_id y pais lo eliminamos porque a fines del problema no importa y ademas,
#por la fuente de los datos, es redundante

op_organicos.drop(columns = ['pais_id','pais'], inplace = True)

# -----------------LOCALIDAD--------------------
    #%%
#valores detectados nulos: INDEFINIDA, INIDEFINIDO
nulls_loc =len(op_organicos.loc[op_organicos['localidad'].isin(['INDEFINIDO','INDEFINIDA'])])
total_reg = len(op_organicos)

print("Porcentaje nulos en columna 'localidad':", round(nulls_loc*100/total_reg, 3))

#el 94% es indefinido, decision tomada de eliminar la columna.
op_organicos.drop(['localidad'], axis = 1 , inplace = True)

# ----------------- PROVINCIA ------------------
#%%
#provincia no presenta errores en los datos

# ------------------DEPARTAMENTO -----------------
#%%
#en departamento tengo muchos posible errores de tipeo, los verifico.

posibles_typos = detectar_typos(op_organicos['departamento'].unique())
posibles_typos
#analizando los posibles typos, verificamos y creamos un diccionario con los que efectivamente lo son
dic_typos ={'TRES ARGENTOS':'TRES SARGENTOS','LANGUINEO':'LANGUIÑEO',
            'PASO DE INDIOS':'PASO DE LOS INDIOS', 'GUAYMAYEN':'GUAYMALLEN',
            'MALARGUE':'MALARGÜE','SAN PATRICIO DEL CAÑAR':'SAN PATRICIO DEL CHAÑAR'}

op_organicos['departamento'] = op_organicos['departamento'].replace(dic_typos)

set(op_organicos['departamento'].unique())

# ------------------- RUBRO --------------
#%%
#separo los valores de la columna rubro_desc en valores atomicos
op_organicos['rubro_desc'] = op_organicos['rubro_desc'].str.split('/|;|-')
op_organicos = op_organicos.explode('rubro_desc')
op_organicos['rubro_desc'] = op_organicos['rubro_desc'].str.strip()

#chequeo typos
posibles_typos = detectar_typos(op_organicos['rubro_desc'].unique())
posibles_typos

dic_typos = {'AGICULTURA':'AGRICULTURA', 'PROCESAMIENTO CEREALES Y OLEAGINOSAS.':
             'PROCESAMIENTO DE CEREALES Y OLEAGINOSAS', 'SECADERO DE FRUTAS':'SECADO DE FRUTAS',
             'PRODUCTOS PARA EL CUIDADO PERSONAL':'CUIDADO PERSONAL'}

op_organicos['rubro_desc'] = op_organicos['rubro_desc'].replace(dic_typos)    
    
# Leer decision 2 del informa
rubros_tipicos = ['ELABORACION','FRACCIONAMIENTO','PROCESAMIENTO','EXTRACCION','INDUSTRIALIZACION', 'EMPAQUE Y FRIGORIFICO', 'EMPAQUE']

op_organicos['rubro_desc'] = op_organicos['rubro_desc'].apply(lambda x: reemplazar_en_df(x, rubros_tipicos))

#examino cantidad de valores nulls 

nulls_rubro =len(op_organicos.loc[op_organicos['rubro_desc'].isin(['SIN DEFINIR','nan'])])
total_reg = len(op_organicos)

print("Porcentaje nulos en columna 'rubro_desc':", round(nulls_rubro*100/total_reg, 3))



#solo el 7% de los datos tienen rubro_desc nulo ('SIN DEFINIR','nan'), los elimino
valores = ['SIN DEFINIR','nan']
op_organicos = op_organicos[~op_organicos['rubro_desc'].isin(valores)]

#op_organicos.loc[op_organicos['rubro_desc'].isin(['SIN DEFINIR','nan']), ['rubro_desc','productos']]

#------------PRODUCTOS-----------
#%%

op_organicos['productos'] = op_organicos['productos'].str.split('[,;/?+Y-]')
op_organicos = op_organicos.explode('productos')
op_organicos['productos'] = op_organicos['productos'].str.strip()
op_organicos.rename(columns = {'productos':'producto_desc'}, inplace = True)

#elimino espacios extras entre palabras
op_organicos['producto_desc'] = op_organicos['producto_desc'].apply(lambda x: eliminar_espacios_extras(str(x)))
#elimino caracter "." cuado se encuentre al final de un sting
op_organicos['producto_desc'] = op_organicos['producto_desc'].apply(lambda x: x.rstrip('.'))


#busco errores de tipografia 
posibles_typos = detectar_typos(op_organicos['producto_desc'].unique())
posibles_typos

#typos principales localizados 
dic_typos = {'AVELLANO':'AVELLANA','CERELAES':'CEREALES','ERBA MATE':'YERBA MATE','ERBA MATE (SUAVE':'YERBA MATE SUAVE',
             'ERBA MATE CANCHADA':'YERBA MATE CANCHADA','ERBA MATE SUAVE':'YERBA MATE SUAVE',
             'ERBA MATE FUERTE':'YERBA MATE FUERTE','ERBA MATE COMPUESTA':'YERBA MATE COMPUESTA',
             'ERBA MATE EN SAQUITOS':'YERBA MATE EN SAQUITOS','FRUTALES':'FRUTA','FRUTO':'FRUTA',
             'GANADERIA OVINA (CARNE':'GANADERIA OVINA (CARNE)','HARINA INTEGRAL (SUPER FINA':'HARINA INTEGRAL SUPER FINA',
             'HARINA INTEGRAL SUPERFINA':'HARINA INTEGRAL SUPER FINA','HARINA SOJA':'HARINA DE SOJA','LAVANDIN':'LAVANDINA',
             'HARINA GIRASOL':'HARINA DE GIRASOL','OELAGINOSAS':'OLEAGINOSAS','PAK CHO':'PAK CHOI','PACK CHOI':'PAK CHOI',
             'PONELO':'POMELO','REMNOLACHA':'REMOLACHA','TE DE ROSA MOSQUETA (SAQUITOS)':'TE DE ROSA MOSQUETA EN SAQUITOS',
             'TE NEGRO (SAQUITOS':'TE NEGRO EN SAQUITOS','ZUCCINI':'ZUCCHINI','ERBA MATE DESPALILLADA':'YERBA MATE DESPALILLADA',
             'ERBA':'YERBA','ERBA MATE SABORIZADA':'YERBA MATE SABORIZADA', 'FRUTOS - FRUTALES':'FRUTA',
             'ERBA MATE CON PALO':'YERBA MATE CON PALO','ELAB ACEITE ROSA MOSQUETA':'ACEITE DE ROSA MOSQUETA','COMPUESTA':'YERBA MATE COMPUESTA',
             'CON PALO':'YERBA MATE CON PALO','COMERCIALIZACION DE CEREALES':'CEREAL','COMERCIALIZACION DE MANI':'MANI','EXTRACCION DE MIEL':'MIEL',
             'FRACCIONAMIENTO DE MIL':'MIEL','NOGALES':'NOGAL','TE VERDE SAQUITOS':'TE VERDE EN SAQUITOS','VD':'VID','CEBOLLA VERDEO':'CEBOLLA DE VERDEO',
             'CEREALES':'CEREAL','SIN PALO':'YERBA MATE SIN PALO'}

op_organicos['producto_desc'] = op_organicos['producto_desc'].replace(dic_typos)

#elimino parentesis que haya (puede que haya abiertos sin cerrar o cerrados sin abrir)
op_organicos['producto_desc'] = op_organicos['producto_desc'].apply(lambda x: eliminar_parentesis(str(x)))
#vuelvo a eliminar el caracter '.' porque habia casos en que habia puntos dentro de parentesis
op_organicos['producto_desc'] = op_organicos['producto_desc'].apply(lambda x: x.rstrip('.'))
#corrijo plurales
op_organicos['producto_desc'] = op_organicos['producto_desc'].apply(lambda x: corregir_plural(str(x)))

#elimino registro que tengan valores especificos
valores =['nan','S','RUP','SIN PROD','SNBERR','EXTRACCION','','SUS DERIVADO','PINOT GRI']

op_organicos = op_organicos[~op_organicos['producto_desc'].isin(valores)]


#IDEA PRODUCTO_DESC Y RUBRO_DESC
#en los strips por caracteres quedaron registros 'invalidos' ejemplo me puede aparecer zapallo con hortaliza 
#y zapallo con fruticultura. la idea sera agrupar por rubro_desc y producto_desc
#contar la cantidad por cada uno y luego el maximo.y finalmente filtrar por aquellos cuya cantidad = max
#dado que si sucede esto lo mas probable es que hayamos agrupado bien rubro y producto

op_organicos['cantidad_por_rubro'] = op_organicos.groupby(['producto_desc','rubro_desc'])['producto_desc'].transform('count')#.astype(int)
op_organicos['max'] = op_organicos.groupby(['producto_desc'])['cantidad_por_rubro'].transform('max')#.astype(int)
op_organicos = op_organicos.drop(op_organicos[op_organicos['cantidad_por_rubro'] != op_organicos['max']].index)
#elimino las columnas que utilices intermedias
op_organicos.loc[:,['rubro_desc','producto_desc','cantidad_por_rubro','max']].loc[op_organicos['producto_desc'] == 'ZAPALLO']

#----------- RAZON SOCIAL -----------
#%%

op_organicos['razon_social'] = op_organicos['razon_social'].str.strip()
op_organicos['razon_social'] = op_organicos['razon_social'].apply(lambda x: eliminar_espacios_extras(str(x)))

#hay un problema con las sociedades en razon social en sentido de puntos. EJ: SA - S.A - S.A.
dic_soc = {"S.A.": "SA", "S.A": "SA", "S.R.L.": "SRL", "S.R.L": "SRL", "S.H.": "SH", "S.H": "SH"}
for palabra, tipo_soc in dic_soc.items():
    op_organicos["razon_social"] = op_organicos["razon_social"].str.replace(palabra, tipo_soc)

#elimino puntos al final 
op_organicos['razon_social'] = op_organicos['razon_social'].apply(lambda x: x.rstrip('.'))

posibles_typos = detectar_typos(op_organicos['razon_social'].unique())
set(posibles_typos)

dic_typos = {'LORENZATI, RUETSCH Y CIA - LR&C SA':'LORENZATI RUETSCH Y CIA. SA',
             'NEOFARMS SRL / GUIDOBONO JOSE MARIA / CALERO GUILLERMO':'NEOFARMS SRL/GUIDOBONO JOSE MARIA/CALERO GUILLERMO',
             'NEOFARMS SRL/GUIDOBONO JOSE MARIA/CALERO GUILLERMO,':'NEOFARMS SRL/GUIDOBONO JOSE MARIA/CALERO GUILLERMO',
             'MASI, TUPUNGATO VIGNETI LA ARBOLEDA SA':'MASI TUPUNGATO VIGNETI LA ARBOLEDA SA',
             'FINCA DEL PARANA DE INGENIERO PIERINO CAMPETELLI':'FINCA DEL PARANA DE PIERINO CAMPETELLI',
             'FERREYRA LIDIA/ ELIZARDO GABRIEL':'FERREYRA LIDIO RAMON/ELIZARDO GABRIEL',
             'ESCARVADOFSKI LIZARDO TOMAS / CERRI ORESTINA':'ESCARVADOFSKI LIZARDO TOMAS/ CERRI ORESTINA',
             'COOPERATIVA AGRICOLA MIXTA DE MONTE CARLO LIMITADA':'COOPERATIVA AGRICOLA MIXTA DE MONTECARLO LIMITADA',
             'COOP. AGRICOLA LTDA. RUIZ DE MONTOYA':'COOP. AGRICOLA RUIZ DE MONTOYA LTDA',
             'CITROMAX SAC.I':'CITROMAX SACI',
             'ANIAYA HILARIO/ ALBERT':'ANIAYA HILARIO/ALBERT',
             'V. Y V. SA':'V Y V ALIMENTOS SA'}

op_organicos['razon_social'] = op_organicos['razon_social'].replace(dic_typos)

#-------- ESTABLECIMIENTO ------------
#%%

#no hago modificaciones sobre establecimiento aunque podria parecer
#que hay un "intercambio" con la columna "razon_social" pero en pocos registros

#tengo columnas donde establcimiento == 'nc' pero al fin del analisis propuesto dejamos esos valores

#finalmente elimino registro duplicados que puedan haber en op_organicos
op_organicos.drop_duplicates(inplace = True)
#y paso todo a minnuscula sin tildes
op_organicos = corregir_df(op_organicos)


#%% -----****SALARIO_SP****-------
print("---------SALARIO SECTOR PRIVADO--------")
#hago un rename de las columnas
salario_sp.columns = ['fecha','codigo_depto_indec','id_provincia_indec','clase','mediana_salario']

salario_sp.info()

#porcentaje ewgistro con valor null en columnas
cant_nulls = len(salario_sp.loc[salario_sp['codigo_depto_indec'].isnull() & salario_sp['id_provincia_indec'].isnull()])
cant_regs = len(salario_sp)
print("\nPorcentaje de registro con nulls en codigo_depto_indec e id_provincia_indec:", cant_nulls*100/cant_regs, "\n")

#los eliminamos porque al no tener esos campos son inutiles dichos registros
salario_sp.dropna(subset=['codigo_depto_indec', 'id_provincia_indec'], inplace=True)

#valores nulls
nulls_por_columna = salario_sp.isnull().sum()
print(nulls_por_columna)

#en la columna mediana salario tengo valores negativos, invalidos. Los elimino
salario_sp = salario_sp[~salario_sp['mediana_salario'] < 0]

#elimino registros duplicados que pueda tener salario_sp
salario_sp.drop_duplicates(inplace = True)
# dejo todo en minuscula y sin tildes 
salario_sp = corregir_df(salario_sp)


#%% ------***DIC_COD_DEPTO***--------
print("---------DICCIONARIO CODIGO DEPARTAMENTO--------")
#hago un rename de las columnas
dic_cod_dep.columns = ['codigo_depto_indec', 'nombre_depto_indec', 'id_provincia_indec','nombre_provincia_indec']

#nulos por columnas
nulls_por_columna = dic_cod_dep.isnull().sum()
print(nulls_por_columna)

set(dic_cod_dep['codigo_depto_indec'].unique())
set(dic_cod_dep['nombre_depto_indec'].unique())

#dejo todo en minuscula y sin tildes
dic_cod_dep = corregir_df(dic_cod_dep)
#elimino (si es que los hay) posibles registros duplicados
dic_cod_dep.drop_duplicates(inplace = True)

#%%-------*****DIC_CLASES*****------------

print("---------DICCIONARIO CLASES--------")
#hago un rename de las columnas 
dic_clases.columns = ['clase','clase_desc','codigo','codigo_desc']

nulls_por_columna = dic_clases.isnull().sum()
print(nulls_por_columna)
#tengo un null en codigo 
dic_clases.loc[dic_clases['codigo'].isna()]
#corresponde con otros sectores

#separo por ; en codigo_clase
dic_clases['codigo_desc'] = dic_clases['codigo_desc'].str.split('[;]')
dic_clases = dic_clases.explode('codigo_desc')
dic_clases['codigo_desc'] = dic_clases['codigo_desc'].str.strip()

#elimino la columna codigo y creo un nuevo indice numero
dic_clases.drop(['codigo'], axis = 1, inplace = True)
dic_clases['codigo'] = crear_id_unico(dic_clases, 'codigo_desc')

#dejo todo en minuscula y sin tildes
dic_clases = corregir_df(dic_clases)
#elimino (si es que los hay) posibles registros duplicados
dic_clases.drop_duplicates(inplace = True)

#%%-------*****LOC_CENSALES***------------

print("---------LOCALIDADES CENSALES--------")

#rename de algunas columnas
loc_censales.rename(columns = {'id':'localidad_id','nombre':'localidad_nombre'}, inplace = True)

#la columna fuente la sacamos dado que es info redundante que no utilizamos
loc_censales.drop(['fuente'],axis=1, inplace = True)

#vemos las columnas
loc_censales.columns

#cantidad de nulls por columna
nulls_por_columna = dic_clases.isnull().sum()
print(nulls_por_columna)

#set(loc_censales['categoria'].unique())
#set(loc_censales['departamento_nombre'].unique())
#set(loc_censales['funcion'].unique())
#set(loc_censales['municipio_nombre'].unique())
#set(loc_censales['provincia_nombre'].unique())
#set(loc_censales['localidad_nombre'].unique())


#Tengo errores en localidad nombre, donde a veces se agrega el depto
#chequeamos algunos y vemos que no coinciden en depto o municipo, por ende no los cambiamos
loc_censales.loc[loc_censales['localidad_nombre'] == 'Parque Norte - Ciudad de los Niños - Villa Pastora - Almirante Brown - Guiñazú N', ['departamento_nombre','municipio_nombre']]
loc_censales.loc[loc_censales['localidad_nombre'] == 'Barrio Gilbert (1º de Mayo) - Tejas Tres', ['departamento_nombre','municipio_nombre']]


#viendo la categoria localidad compuesta no nos da mucha info 
loc_censales.loc[loc_censales['categoria'] == "Componente de localidad compuesta", ['localidad_nombre', 'departamento_nombre']].sample(5)

#cambio el nombre de ciertas provincias para tener consistencia de nombres con los otros dfs
dic_provs = {'Tierra del Fuego, Antártida e Islas del Atlántico Sur':'Tierra del fuego',
             'Ciudad Autónoma de Buenos Aires':'CABA'}

loc_censales['provincia_nombre'] = loc_censales['provincia_nombre'].replace(dic_provs)

#dejo todo en minuscula y sin tildes
loc_censales = corregir_df(loc_censales)
#elimino (si es que los hay) posibles registros duplicados
loc_censales.drop_duplicates(inplace = True)


#veamos que nos indica la columna funcion cuando no es nula
loc_censales.loc[loc_censales['funcion'].isin(['cabecera_departamento', 'capital_pais', 'capital_provincia']),['departamento_nombre','provincia_nombre']]
#%%

#descargo todos los dfs corregidos en archivos de extension .csv

#op_organicos.to_csv('padron-de-operadores-organicos-certificados-limpio.csv', index=False, encoding='utf-8')
#loc_censales.to_csv('localidades-censales-limpio.csv', index=False, encoding='utf-8')
#dic_cod_dep.to_csv('diccionario_cod_depto-limpio.csv', index=False, encoding='utf-8')
#dic_clases.to_csv('diccionario_clae2-limpio.csv', index=False, encoding='utf-8')
#salario_sp.to_csv('w_median_depto_priv_clae2-limpio.csv', index=False, encoding='utf-8')




