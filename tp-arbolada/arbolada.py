#%%
import csv
import numpy as np

#%%

# funcion para leer indice correspondiente a la columna del csv
def obtener_indice(nombre_archivo,nombre_columna):
    
    with open(nombre_archivo, 'r', encoding = 'utf-8') as file:
        filas = csv.reader(file)
        encabezado = next(filas)
        indice = encabezado.index(next(x for x in encabezado if x == nombre_columna))
        
    return indice


def leer_parque(nombreArchivo, parque):
    
    with open(nombreArchivo, "r", encoding = 'utf-8') as file_csv:
        lista_dic = []
        filas = csv.reader(file_csv)
        next(filas)
        indice_parque = obtener_indice(nombreArchivo, 'espacio_ve')
        indice_arbol = obtener_indice(nombreArchivo, 'id_arbol')
        for fila in filas:
            if fila[indice_parque] == parque:
                dic = {fila[indice_arbol]:  fila}
                lista_dic.append(dic)
                
    return lista_dic

      
def especies(lista_arboles):
     
    lista_especies = []
    for arbol in lista_arboles:
        datos_arbol = list(arbol.values())[0]
        indice_nombre_com = obtener_indice("arbolado-en-espacios-verdes.csv", "nombre_com")
        lista_especies.append(datos_arbol[indice_nombre_com])
    
    return set(lista_especies)


def contar_ejemplares(lista_arboles):
    
    dic_ejemplares = {}
    indice_nombre_com = obtener_indice("arbolado-en-espacios-verdes.csv", "nombre_com")
    
    for arbol in lista_arboles:
        datos_arbol = list(arbol.values())[0]
        if datos_arbol[indice_nombre_com] in dic_ejemplares:
            dic_ejemplares[datos_arbol[indice_nombre_com]] += 1
        else:
            dic_ejemplares[datos_arbol[indice_nombre_com]] = 1
        
    return dic_ejemplares


def obtener_alturas(lista_arboles, especie):
    
    lista_alturas = []
    indice_altura_tot = obtener_indice("arbolado-en-espacios-verdes.csv", "altura_tot")
    
    for arbol in lista_arboles:
        datos_arbol = list(arbol.values())[0]
        if especie in datos_arbol:
            lista_alturas.append(float(datos_arbol[indice_altura_tot]))
                                 
    return lista_alturas


def obtener_inclinaciones(lista_arboles, especie):
    
    lista_inclinaciones = []
    indice_inclinacion = obtener_indice('arbolado-en-espacios-verdes.csv', 'inclinacio')

    for arbol in lista_arboles:
        datos_arbol = list(arbol.values())[0]
        if especie in datos_arbol:
            lista_inclinaciones.append(float(datos_arbol[indice_inclinacion]))

    return lista_inclinaciones

def especimen_mas_inclinado(lista_arboles):
    
    especimenes = list(especies(lista_arboles))
    esp_inclinacion = []
    
    for especimen in especimenes:
        esp_inclinacion.append([especimen, max(obtener_inclinaciones(lista_arboles, especimen))])
        
    esp_mas_inclinado = max(esp_inclinacion, key = lambda x: x[1])
    
    return esp_mas_inclinado

def especie_promedio_mas_inclinado(lista_arboles):
    
    especimenes = list(especies(lista_arboles))
    esp_inclinacion_promedio = []
    
    for especimen in especimenes:
        esp_inclinacion_promedio.append([especimen, np.mean(obtener_inclinaciones(lista_arboles, especimen))])
        
    esp_mas_inclinado_promedio = max(esp_inclinacion_promedio, key = lambda x: x[1])
    
    return esp_mas_inclinado_promedio

    
#%%

## ------------EJERCICIO 1-----------------------------------------------------
print("\nEJERCICIO 1\n")

arboles_gralPaz = leer_parque("arbolado-en-espacios-verdes.csv",'GENERAL PAZ')
print("Cantidad de arboles en parque general paz = ", len(arboles_gralPaz))

# -------------EJERCICIO 2-----------------------------------------------------
print("\nEJERCICIO 2\n")
especies_gralPaz = especies(arboles_gralPaz)
print("Las especies en el parque General Paz son:", especies_gralPaz)

# -------------EJERCICIO 3-----------------------------------------------------
print("\nEJERCICIO 3\n")
arboles_gralPaz = leer_parque("arbolado-en-espacios-verdes.csv",'GENERAL PAZ')
ejemplares_gralPaz = contar_ejemplares(arboles_gralPaz)
print("Cantidad ejemplares de Jacarandá en parque General Paz: ", ejemplares_gralPaz["Jacarandá"], '\n')

arboles_losAndes = leer_parque("arbolado-en-espacios-verdes.csv",'ANDES, LOS')
ejemplares_losAndes = contar_ejemplares(arboles_losAndes)
print("Cantidad ejemplares de Tilos en parque Los Andes: ", ejemplares_losAndes["Tilo"], '\n')

arboles_centenario = leer_parque("arbolado-en-espacios-verdes.csv",'CENTENARIO')
ejemplares_centenario = contar_ejemplares(arboles_centenario)
print("Cantidad ejemplares de Laurel en parque Centenario: ", ejemplares_centenario["Laurel"])

# -------------EJERCICIO 4-----------------------------------------------------
print("\nEJERCICIO 4\n")

arboles_gralPaz = leer_parque("arbolado-en-espacios-verdes.csv",'GENERAL PAZ')
alt_jac_gralPaz = obtener_alturas(arboles_gralPaz,'Jacarandá')
arboles_losAndes = leer_parque("arbolado-en-espacios-verdes.csv",'ANDES, LOS')
alt_jac_losAndes = obtener_alturas(arboles_losAndes,'Jacarandá')
arboles_centenario = leer_parque("arbolado-en-espacios-verdes.csv",'CENTENARIO')
alt_jac_centenario = obtener_alturas(arboles_centenario,'Jacarandá')


print("Tabla indicando diferentes medidas de la inclinacion del especimen Jacaranda en diferentes parques\n")
columna1 = ['Medida','Max','Prom']
columna2 = ['General Paz', round(max(alt_jac_gralPaz),2), round(np.mean(alt_jac_gralPaz),2)]
columna3 = ['Los Andes', round(max(alt_jac_losAndes),2), round(np.mean(alt_jac_losAndes),2)]
columna4 = ['Centenario', round(max(alt_jac_centenario),2), round(np.mean(alt_jac_centenario),2)]

tabla = ''
for i in range(len(columna1)):
    tabla += '{:<13} {:<13} {:<13} {:<13}\n'.format(columna1[i], columna2[i], columna3[i], columna4[i])
print(tabla)

# -------------EJERCICIO 5-----------------------------------------------------
print("\nEJERCICIO 5\n")

arboles_gralPaz = leer_parque("arbolado-en-espacios-verdes.csv",'GENERAL PAZ')
inc_jac_gralPaz = obtener_inclinaciones(arboles_gralPaz,'Jacarandá')
print("Especimen: Jacarandá, lista con la inclinacion de los ejemplares en parque Gral Paz:", inc_jac_gralPaz)

# -------------EJERCICIO 6-----------------------------------------------------
print("\nEJERCICIO 6\n")

arboles_centenario = leer_parque('arbolado-en-espacios-verdes.csv', 'CENTENARIO')
esp_mas_inclinado = especimen_mas_inclinado(arboles_centenario)
print("Especimen mas inclinado en Parque Centenario: ", esp_mas_inclinado[0], "- Inclinacion: ", esp_mas_inclinado[1], "grados\n")

arboles_losAndes = leer_parque('arbolado-en-espacios-verdes.csv', 'ANDES, LOS')
esp_mas_inclinado = especimen_mas_inclinado(arboles_losAndes)
print("Especimen mas inclinado en Parque Los Andes: ", esp_mas_inclinado[0], "- Inclinacion: ", esp_mas_inclinado[1], "grados\n")

arboles_gralPaz = leer_parque('arbolado-en-espacios-verdes.csv', 'GENERAL PAZ')
esp_mas_inclinado = especimen_mas_inclinado(arboles_gralPaz)
print("Especimen mas inclinado en Parque General Paz: ", esp_mas_inclinado[0], "- Inclinacion: ", esp_mas_inclinado[1], "grados\n")
#--------------EJERCICIO 7-----------------------------------------------------
print("\nEJERCICIO 7\n")

arboles_gralPaz = leer_parque('arbolado-en-espacios-verdes.csv', 'ANDES, LOS')
esp_prom_mas_inclinado = especie_promedio_mas_inclinado(arboles_gralPaz)
print("La inclinacion promedio en el parque Los Andes del especimen", esp_prom_mas_inclinado[0], "es ", esp_prom_mas_inclinado[1], 'grados')






#%%

