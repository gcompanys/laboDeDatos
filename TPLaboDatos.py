import pandas as pd 
import seaborn as sns
from  inline_sql import sql, sql_val
import matplotlib as plt

# Descargo todos los csv 

#%%


op_organicos = pd.read_csv('padron-de-operadores-organicos-certificados-limpio.csv', encoding = 'latin-1')
loc_censales = pd.read_csv('localidades-censales-limpio.csv')
dic_cod_dep = pd.read_csv('diccionario_cod_depto-limpio.csv')
dic_clases = pd.read_csv('diccionario_clae2-limpio.csv')
salario_sp = pd.read_csv('w_median_depto_priv_clae2-limpio.csv')


#elimino registros duplicados en cada uno 

for x in [op_organicos, loc_censales, dic_cod_dep, dic_clases, salario_sp]:
    x.drop_duplicates(inplace = True)


#%%


def crear_id_unico(df, columna):
    #crea un id unico para cada valor diferentes de la columna que le pasan
    #devuelve una serie de pandas con el id
    return pd.factorize(df[columna])[0]

def df_reducido(df, columnas):
    #recibe un dataframe de entrada junto con las columnas que me quiero quedar del mismo
    #columnas tiene que ser una lista de columnas
    nuevo_df = df.loc[:,columnas]
    return nuevo_df

def eliminar_duplicados(df):
    #toma un df y elimina todos los registros duplicados del mismo
    df.drop_duplicates(inplace = True)


#%% Operadores organicos



#creo un id para departamento
op_organicos['departamento_id'] = crear_id_unico(op_organicos, 'departamento')
#creo un id para rubro
op_organicos['rubro_id'] = crear_id_unico(op_organicos, 'rubro_desc')
#creo un id para producto
op_organicos['producto_id'] = crear_id_unico(op_organicos, 'producto_desc')


#pais = df_reducido(op_organicos,['pais_id','pais'])
provincia = df_reducido(op_organicos, ['provincia_id','provincia'])
provincia.rename(columns = {'provincia':'provincia_nombre'}, inplace = True)
certificadora = df_reducido(op_organicos,['certificadora_id','certificadora_deno'])
categoria = df_reducido(op_organicos,['categoria_id','categoria_desc'])
rubro = df_reducido(op_organicos,['rubro_desc','rubro_id'])
producto = df_reducido(op_organicos, ['producto_id','producto_desc','rubro_id'])
padron = df_reducido(op_organicos, ['establecimiento','razon_social','rubro_id','certificadora_id','categoria_id','departamento_id'])
departamento = df_reducido(op_organicos, ['departamento_id','departamento','provincia_id'])

#elimino los duplicados de cada uno 
for df in [provincia,certificadora,categoria,rubro,producto,padron,departamento]:
    eliminar_duplicados(df)


#%% Salario



#para salario_sp separo por la fecha 

salario_sp[['anio', 'mes', 'dia']] = salario_sp['fecha'].str.split('-', expand=True).astype(int)
salario_sp.drop(['fecha'], axis = 1, inplace = True)



salario_sp.rename(columns = {'codigo_depto_indec':'id_depto_indec'}, inplace = True)
depto_indec = df_reducido(salario_sp, ['id_depto_indec','id_provincia_indec'])
#cambio de float a int
depto_indec['id_depto_indec'] = depto_indec['id_depto_indec'].astype(int)
depto_indec['id_provincia_indec'] = depto_indec['id_provincia_indec'].astype(int)
salario_sp.drop(['id_provincia_indec'], axis = 1, inplace =True)


#elimino posibles duplicados
for df in [salario_sp, depto_indec]:
    eliminar_duplicados(df)


#%% DIC CLASES

dic_clases.rename(columns = {'codigo':'codigo_id'}, inplace = True)
codigo_clase = df_reducido(dic_clases, ['codigo_id','codigo_desc'])
dic_clases.drop(['codigo_desc'], axis = 1,  inplace = True)

#elimino posibles duplicados
for df in [dic_clases, codigo_clase]:
    eliminar_duplicados(df)


#%% DIC COD DEPTO


dic_cod_dep

depto_indec2 = df_reducido(dic_cod_dep, ['codigo_depto_indec','nombre_depto_indec','id_provincia_indec'])
prov_indec2 = df_reducido(dic_cod_dep, ['id_provincia_indec','nombre_provincia_indec'])

#elimino posibles duplicados
for df in [depto_indec2, prov_indec2]:
    eliminar_duplicados(df)


#%% LOCALIDADES CENSALES


#creo un id para las coordenadas
loc_censales['coordenadas_id'] = pd.factorize(list(zip(loc_censales['centroide_lat'], loc_censales['centroide_lon'])))[0]
#creo un id para categoria 
loc_censales['categoria_id'] = crear_id_unico(loc_censales, 'categoria')


provincia_cen = df_reducido(loc_censales, ['provincia_id','provincia_nombre'])
depto_cen = df_reducido(loc_censales, ['departamento_id','departamento_nombre','provincia_id'])
coordenadas_cen = df_reducido(loc_censales, ['coordenadas_id','centroide_lat','centroide_lon'])
municipio_cen = df_reducido(loc_censales, ['municipio_id','municipio_nombre'])
localidad_cen = df_reducido(loc_censales, ['localidad_id','localidad_nombre','municipio_id','departamento_id','categoria_id']) 

#elimino posibles duplicados
for df in [provincia_cen, depto_cen, municipio_cen, localidad_cen, coordenadas_cen]:
    eliminar_duplicados(df)


# Unifico las tablas de provincia, pero teniendo cuidado con los id de las diferentes tablas

# provincia_cen y prov_indec2 tienen los mismos id para cadad provincia, elimino una indistintamente y tengo que trabajar con provincia que tiene diferente indice

resultado = pd.merge(provincia, provincia_cen, on= 'provincia_nombre')

# en resultado puede verse que provincia y provincia_cen tambien tienen los mismos id, por ende puedo quedarme solo con provincia.
#elimino prov_indec2 y provincia_cen
del prov_indec2
del provincia_cen


# ahora renombro los atributos en las otras tablas a id_provincia
depto_indec.rename(columns = {'id_provincia_indec':'provincia_id'}, inplace = True)

# lo mismo pasa con depto_indec y depto_indec2. Me quedo con uno solo (depto_indec2 que tiene tambien los nombres de las provincia)  y lo llamo departamento_indec

departamento_indec = depto_indec2
del depto_indec
del depto_indec2



#%%

#%% EJERCICIOS SQL
salario_sp.columns
op_organicos.columns
dic_clases.columns
loc_censales.columns
dic_cod_dep.columns


#%%1¿Existen provincias que no presentan Operadores Orgánicos Certificados?¿En caso de que sí, cuántas y cuáles son?

cons = '''SELECT DISTINCT d.provincia_id, COUNT(p.razon_social) as cantidad
    FROM departamento as d
    JOIN padron as p ON d.departamento_id = p.departamento_id
    GROUP BY d.provincia_id'''

df = sql^cons


cons1 ='''SELECT DISTINCT  p.provincia_nombre, df.cantidad 
    FROM df
    JOIN provincia as p ON df.provincia_id = p.provincia_id
    '''

df1 = sql^cons1


#%% 2¿Existen departamentos que no presentan Operadores Orgánicos Certificados? ¿En caso de que sí, cuántos y cuáles son?




#%% 3¿Cuál es la actividad que más operadores tiene?

ejiii=ejiii="""SELECT rubro_desc, COUNT(DISTINCT razon_social) as cantidad
FROM op_organicos
GROUP BY rubro_desc
ORDER BY  cantidad DESC
LIMIT 1;"""
dfiii = sql^ejiii
#%% 4¿Cuál fue el salario promedio de esa actividad en 2022? (si hay varios registros de salario, mostrar el más actual de ese año)

#agricultura fue la actividad

cons = """
    SELECT s.mediana_salario, s.anio, s.mes, s.dia
    FROM dic_clases as dc
    JOIN salario_sp as s
    ON dc.clase = s.clase
    WHERE clase_desc LIKE '%agricultura%'
    """
df = sql^cons

#de este resultado me quedo con el que tenga anio mes y dia mas actualizado

cons_res = """
        SELECT df.mediana_salario
        FROM df
        WHERE anio = (SELECT MAX(anio) FROM df) AND mes = (SELECT MAX(mes) FROM df) AND dia = (SELECT MAX(dia) FROM df)
        """

df_res = sql^cons_res

#doy un promedio de los mismo 

df_res.mean()



#%% 5¿Cuál es el promedio anual de los salarios en Argentina y cual es su desvío?, ¿Y a nivel provincial? ¿Se les ocurre una forma de que sean
#comparables a lo largo de los años? ¿Necesitarían utilizar alguna fuente de datos externa secundaria? ¿Cuál?

#promedio anual salarios a nivel pais

cons1 = '''
        SELECT DISTINCT AVG(s.mediana_salario) as promedio, s.anio
        FROM salario_sp as s 
        GROUP BY anio
        '''
#aca tengo el promedio anual a nivel pais
df1 = sql^ cons1

#desvio
cons2 = '''
        SELECT DISTINCT STDEV(s.mediana_salario) as promedio, s.anio
        FROM salario_sp as s 
        GROUP BY anio
        '''
#aca tengo el promedio anual a nivel pais
df2 = sql^ cons2

#promedio anual salarios a nivel provincial

cons3 = '''
        SELECT DISTINCT s.mediana_salario, d.id_provincia_indec, s.anio
        FROM salario_sp as s 
        JOIN depto_indec as d 
        ON d.id_depto_indec = s.id_depto_indec
        '''

df3 = sql^ cons3

cons4 = '''
        SELECT DISTINCT p.provincia_nombre, df3.anio, AVG(df3.mediana_salario) as promedio
        FROM df3
        JOIN provincia as p 
        ON p.provincia_id = df3.id_provincia_indec
        GROUP BY p.provincia_nombre, df3.anio
        '''

#aca tengo el promedio anual por provincia
df_res4 = sql^ cons4



#%%



#%%

# # Visualizaciones


sns.set_theme(style = 'darkgrid')
sns.set_palette('deep')


# %%J) i) Cantidad de Operadores por provincia


#hecho con sql
eji = '''SELECT DISTINCT d.provincia_id, COUNT(p.razon_social) as cantidad
    FROM departamento as d
    JOIN padron as p ON d.departamento_id = p.departamento_id
    GROUP BY d.provincia_id'''

df = sql^ eji

#ahora al resultado hago un join para tener el nombre de cada provincia y graficar

cons = '''SELECT DISTINCT provincia_nombre, df.cantidad
    FROM df 
    JOIN provincia as p ON df.provincia_id = p.provincia_id'''

df1 = sql ^ cons

sns.barplot(x='cantidad', y='provincia_nombre', data=df1)
plt.title('Cantidad de operadores organicos por provincia')
plt.xlabel('Cantidad de operadores organicos')
plt.ylabel('Provincia')
plt.show()

#hecho con pandas
#mismo operador puede tener varios establecimientos, asi que voy a contar solo por razon social
df1 = padron.loc[:,['razon_social','departamento_id']].merge(departamento, on = 'departamento_id')
df2 = df1.merge(provincia, on = 'provincia_id').loc[:,['razon_social','provincia_nombre']].drop_duplicates()
df2['cantidad_operadores'] = df2.groupby('provincia_nombre')['razon_social'].transform('count')

sns.barplot(x='cantidad_operadores', y='provincia_nombre', data=df2)
plt.title('Cantidad de operadores organicos por provincia')
plt.xlabel('Cantidad de operadores organicos')
plt.ylabel('Provincia')
plt.show()


#%%
# ii) Boxplot, por cada provincia, donde se pueda observar la cantidad de
# productos por operador.

# In[228]:


# ACLARACION: entendiendo el enunciado en sentido literal me quedaban un total de 26 boxplot (uno por provincia) pero con 
#muchisimos operadores y la cantidad de productos por cada uno. Eran graficos que no se entendian
#por ende asumo que lo que se queria era por provincia, ver por operador la cantidad de productos
#osea que en el boxplot por cada provincia se la distribucion de la cantidad de productos por operador

df1 = padron.loc[:,['razon_social','rubro_id','departamento_id','establecimiento']].merge(departamento, left_on = 'departamento_id', right_on = 'departamento_id' )
df2 = df1.merge(provincia, on = "provincia_id").loc[:,['establecimiento','razon_social','provincia_nombre','rubro_id']]
df3 = df2.merge(producto, on = 'rubro_id').loc[:,['establecimiento','razon_social','provincia_nombre','producto_id']]
df3['cantidad_productos'] = df3.groupby(['establecimiento','razon_social','provincia_nombre']).transform('count')
df_res = df3.loc[:,['provincia_nombre','cantidad_productos']].drop_duplicates()

#%%

sns.boxplot(data=df_res, x="cantidad_productos", y="provincia_nombre", hue_order=sorted(df_res["provincia_nombre"].unique()), order=sorted(df_res["provincia_nombre"].unique()))
plt.title('Cantidad de productos por operadores por provincia')
plt.xlabel('Cantidad de productos')
plt.ylabel('Provincia')
plt.show()



#%%
# iii) Relación entre cantidad de emprendimientos certificados de cada provincia y
# el salario promedio en dicha provincia (para la actividad) en el año 2022. En
# caso de existir más de un salario promedio para ese año, mostrar el último
# del año 2022.



salarios_2022 = salario_sp.loc[salario_sp['anio'] == 2022, ['clase','id_depto_indec','mediana_salario','mes','dia']]
#me quedo con el registro mas reciente de cada depto y clase
salario_fil = salarios_2022
salario_fil['max_dia'] = salario_fil.groupby(['clase','id_depto_indec'])['dia'].transform('max')
salario_fil['max_mes'] = salario_fil.groupby(['clase','id_depto_indec'])['mes'].transform('max')
salario_fil = salario_fil.loc[(salario_fil['dia'] == salario_fil['max_dia']) & (salario_fil['mes'] == salario_fil['max_mes']), ['clase','id_depto_indec','mediana_salario']]

df_sal = salario_fil.merge(departamento_indec, left_on = 'id_depto_indec', right_on ='codigo_depto_indec')
df_sal = df_sal.merge(provincia, right_on = 'provincia_id', left_on = 'id_provincia_indec')
df_sal = df_sal.loc[:,['provincia_nombre','clase','mediana_salario']]

#considero que cada establecimiento es un emprendimiento
df1 = padron.loc[:,['establecimiento','departamento_id']].merge(departamento, on = 'departamento_id')
df2 = df1.merge(provincia, on = 'provincia_id').loc[:,['establecimiento','provincia_nombre']].drop_duplicates()
df2['cantidad_operadores'] = df2.groupby('provincia_nombre')['establecimiento'].transform('count')
df2 = df2.loc[:,['provincia_nombre','cantidad_operadores']]


df_res = df_sal.merge(df2, on ='provincia_nombre')
df_res = df_res.drop_duplicates()


provincias = df_res['provincia_nombre'].unique()

for prov in provincias:
    df_graf = df_res.loc[df_res['provincia_nombre'] == prov]
    sns.relplot(x="mediana_salario", y="cantidad_operadores", sizes=(40, 400), alpha=.5, data=df_graf)
    plt.autoscale()

#quedan graficos no entendibles. 


#%%

# iv) ¿Cuál es la distribución de los salarios promedio en Argentina? Realicen un
# violinplot de los salarios promedio por provincia. Grafiquen el último ingreso
# medio por provincia.


salario = salario_sp.copy()
salario = salario.merge(departamento_indec, left_on = 'id_depto_indec', right_on ='codigo_depto_indec')
salario = salario.merge(provincia, right_on = 'provincia_id', left_on = 'id_provincia_indec')
salario = salario.loc[:,['provincia_nombre','mediana_salario']].drop_duplicates()

provincias = salario['provincia_nombre'].unique()
nfilas = int(np.ceil(len(provincias)/3))
fig, axs = plt.subplots(nrows=nfilas, ncols=3, figsize=(15,5*nfilas))

# Graficar un violinplot por provincia en su respectivo subplot
for i, prov in enumerate(provincias):
    fila = i // 3
    columna = i % 3
    axs[fila, columna].set_title(prov)
    axs[fila, columna].set_ylabel('mediana salario')
    axs[fila, columna].violinplot(salario[salario['provincia_nombre']==prov]['mediana_salario'],showextrema=False)

plt.tight_layout()
plt.show()

#ultimo ingreso
salario_fil = salario_sp.copy()
salario_fil['max_anio'] = salario_fil.groupby(['clase','id_depto_indec'])['anio'].transform('max')
salario_fil['max_dia'] = salario_fil.groupby(['clase','id_depto_indec'])['dia'].transform('max')
salario_fil['max_mes'] = salario_fil.groupby(['clase','id_depto_indec'])['mes'].transform('max')
salario_fil = salario_fil.loc[(salario_fil['dia'] == salario_fil['max_dia']) & (salario_fil['mes'] == salario_fil['max_mes']) & (salario_fil['anio'] == salario_fil['max_anio']), ['clase','id_depto_indec','mediana_salario']]
salario_fil = salario_fil.merge(departamento_indec, left_on = 'id_depto_indec', right_on ='codigo_depto_indec')
salario_fil = salario_fil.merge(provincia, right_on = 'provincia_id', left_on = 'id_provincia_indec')
df_res = df_res.loc[:,['provincia_nombre','mediana_salario']]
#esto me deja el ultimo ingreso por clase, asi que hago un mean de de todas
df_res['mediana_salario'] = df_res.groupby('provincia_nombre')['mediana_salario'].transform('mean')
df_res.drop_duplicates(inplace = True)


y_values = df_res['provincia_nombre']
x_values = df_res['mediana_salario']

# Graficar los puntos
plt.scatter(x_values, y_values)
plt.title('Último ingreso por provincia')
plt.xlabel('Último ingreso')
plt.ylabel('Provincia')

#%%

# se desea que intenten mostrar si existe “ … cierta relación entre el desarrollo
# de la actividad y el salario promedio que perciben los trabajadores del sector privado en
# cada departamento de las provincias argentinas.”

# In[273]:


#quiero en un mismo df clase, mediana salario y departamento
df = salario_sp.loc[:,['id_depto_indec','mediana_salario','clase']].merge(departamento_indec, left_on = 'id_depto_indec', right_on = 'codigo_depto_indec')
df = df.loc[:, ['mediana_salario','nombre_depto_indec','clase']].drop_duplicates()


# In[ ]:






