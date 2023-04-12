# -*- coding: utf-8 -*-
"""
Materia: Laboratorio de datos - FCEyN - UBA
Clase  : Clase SQL. Script clase.
Autor  : Pablo Turjanski
Fecha  : 2023-03-07
"""

# Importamos bibliotecas
import pandas as pd
from inline_sql import sql, sql_val

def main():

    print()
    print("# =============================================================================")
    print("# Creamos los datasets que vamos a utilizar en este programa")
    print("# =============================================================================")
    
    # Ejercicios AR-PROJECT, SELECT, RENAME
    empleado       = get_empleado()
    # Ejercicios AR-UNION, INTERSECTION, MINUS
    alumnosBD      = get_alumnosBD()
    alumnosTLeng   = get_alumnosTLeng()
    # Ejercicios AR-CROSSJOIN
    persona        = get_persona_ejemploCrossJoin()
    nacionalidades = get_nacionalidades()
    # Ejercicios ¿Mismos Nombres?
    se_inscribe_en=get_se_inscribe_en_ejemploMismosNombres()
    materia       =get_materia_ejemploMismosNombres()
    # Ejercicio JOIN múltiples tablas
    vuelo      = pd.read_csv("~/Descargas/vuelo.csv")    
    aeropuerto = pd.read_csv("~/Descargas/aeropuerto.csv")    
    pasajero   = pd.read_csv("~/Descargas/pasajero.csv")    
    reserva    = pd.read_csv("~/Descargas/reserva.csv")    
    # Ejercicio JOIN tuplas espúreas
    empleadoRol= pd.read_csv("~/Descargas/empleadoRol.csv")    
    rolProyecto= pd.read_csv("~/Descargas/rolProyecto.csv")    
    # Ejercicios funciones de agregación, LIKE, Elección, Subqueries y variables de Python
    examen     = pd.read_csv("~/Descargas/examen.csv")
    # Ejercicios de manejo de valores NULL
    examen03 = pd.read_csv("~/Descargas/examen03.csv")
    
    
    
    print()
    print("# =============================================================================")
    print("# Ejemplo inicial")
    print("# =============================================================================")
    
    print(empleado)

    consultaSQL = """
                   SELECT DISTINCT DNI, Salario
                   FROM empleado;
                  """


    dataframeResultado = sql^ consultaSQL
    
    print(dataframeResultado)


    print()
    print("# =============================================================================")
    print("# Ejercicios AR-PROJECT <-> SELECT")
    print("# =============================================================================")
    
    consigna    = "a.- Listar DNI y Salario de empleados "
    consultaSQL = """
                   SELECT DISTINCT DNI, Salario
                   FROM empleado;
                  """
    imprimirEjercicio(consigna, [empleado], consultaSQL)    
    
    # -----------
    consigna    = "b.- Listar Sexo de empleados "
    consultaSQL = """
                    SELECT DISTINCT Sexo
                    FROM empleado
                  """
    imprimirEjercicio(consigna, [empleado], consultaSQL)    

    # -----------
    consigna    = "c.- Listar Sexo de empleados (sin DISTINCT)"
    consultaSQL = """
                    SELECT Sexo
                    FROM empleado

                  """
    imprimirEjercicio(consigna, [empleado], consultaSQL)    

    print()
    print("# =============================================================================")
    print("# Ejercicios AR-SELECT <-> WHERE")
    print("# =============================================================================")
    
    consigna    = "a.- Listar de EMPLEADO sólo aquellos cuyo sexo es femenino"
    consultaSQL = """
                   SELECT *
                   FROM empleado
                   WHERE Sexo = 'F'
                  """
    imprimirEjercicio(consigna, [empleado], consultaSQL)    

    # -----------
    consigna    = "b.- Listar de EMPLEADO aquellos cuyo sexo es femenino y su salario es mayor a $15.000"
    consultaSQL = """
                    SELECT *
                   FROM empleado
                   WHERE Sexo = 'F'AND Salario > 15000
                  """
    imprimirEjercicio(consigna, [empleado], consultaSQL)    
    
    
    print()
    print("# =============================================================================")
    print("# Ejercicios AR-RENAME <-> AS")
    print("# =============================================================================")
    
    consigna    = """a.- Listar DNI y Salario de EMPLEADO, y renombrarlos como id e Ingreso"""
    consultaSQL = """
                    SELECT DISTINCT DNI as id, Salario as Ingreso
                    from empleado
                  """
    
    imprimirEjercicio(consigna, [empleado], consultaSQL)    
    
    print()
    print("# =============================================================================")
    print("# Ejercicios AR-UNION, INTERSECTION, MINUS <-> UNION, INTERSECTION, EXCEPT")
    print("# =============================================================================")

    consigna    = """a1.- Listar a los alumnos que cursan BDs o TLENG"""

    consultaSQL = """
                    SELECT DISTINCT *
                    FROM alumnosBD
                    UNION
                    SELECT DISTINCT *
                    FROM alumnosTLeng
                  """

    imprimirEjercicio(consigna, [alumnosBD, alumnosTLeng], consultaSQL)    


    # -----------
    consigna    = """a2.- Listar a los alumnos que cursan BDs o TLENG (usando UNION ALL)"""
    
    consultaSQL = """
                      SELECT DISTINCT *
                    FROM alumnosBD
                    UNION ALL
                    SELECT DISTINCT *
                    FROM alumnosTLeng
                  """

    imprimirEjercicio(consigna, [alumnosBD, alumnosTLeng], consultaSQL)    


    # -----------
    consigna    = """b.- Listar a los alumnos que cursan simultáneamente BDs y TLENG"""
    
    consultaSQL = """
                    SELECT DISTINCT *
                    FROM alumnosBD
                    INTERSECT
                    SELECT DISTINCT *
                    FROM alumnosTLeng
                  """

    imprimirEjercicio(consigna, [alumnosBD, alumnosTLeng], consultaSQL)    

    
    # -----------
    consigna    = """c.- Listar a los alumnos que cursan BDs y no cursan TLENG """
    
    consultaSQL = """
                    SELECT DISTINCT *
                    FROM alumnosBD
                    EXCEPT
                    SELECT DISTINCT *
                    FROM alumnosTLeng
                  """

    imprimirEjercicio(consigna, [alumnosBD, alumnosTLeng], consultaSQL)    
    
    
    print("# =============================================================================")
    print("# Ejercicios AR-... JOIN <-> ... JOIN")
    print("# =============================================================================")

    consigna    = """a1.- Listar el producto cartesiano entre las tablas persona y nacionalidades"""
    
    consultaSQL = """
                    SELECT DISTINCT *
                    FROM persona
                    CROSS JOIN nacionalidades
                  """

    imprimirEjercicio(consigna, [persona, nacionalidades], consultaSQL)


    # -----------
    consigna    = """a2.- Listar el producto cartesiano entre las tablas persona y nacionalidades (sin usar CROSS JOIN)"""
    
    consultaSQL = """
                SELECT DISTINCT *
                FROM persona, nacionalidades

                  """

    imprimirEjercicio(consigna, [persona, nacionalidades], consultaSQL)


    # ---------------------------------------------------------------------------------------------- 
    # Carga los nuevos datos del dataframe persona para los ejercicios de AR-INNER y LEFT OUTER JOIN
    # ----------------------------------------------------------------------------------------------
    persona        = get_persona_ejemplosJoin()
    # ----------------------------------------------------------------------------------------------
  
    consigna    = """b1.- Vincular las tablas persona y nacionalidades a través de un INNER JOIN"""
    
    consultaSQL = """
                    SELECT DISTINCT *
                    FROM persona
                    INNER JOIN nacionalidades
                    ON nacionalidad=IDN
                  """

    imprimirEjercicio(consigna, [persona, nacionalidades], consultaSQL)


    # -----------
    consigna    = """b2.- Vincular las tablas persona y nacionalidades (sin usar INNER JOIN)"""
    
    consultaSQL = """
                 SELECT DISTINCT *
                 FROM persona, nacionalidades
                 WHERE nacionalidad=IDN
                  """

    imprimirEjercicio(consigna, [persona, nacionalidades], consultaSQL)


    # -----------
    consigna    = """c.- Vincular las tablas persona y nacionalidades a través de un LEFT OUTER JOIN"""
    
    consultaSQL = """
                   SELECT DISTINCT *
                   FROM persona
                   OUTTER JOIN nacionalidades
                   ON nacionalidad=IDN
                  """

    imprimirEjercicio(consigna, [persona, nacionalidades], consultaSQL)
    

    print("# =============================================================================")
    print("# Ejercicios SQL - ¿Mismos Nombres?")
    print("# =============================================================================")

    consigna    = """a.- Vincular las tablas Se_inscribe_en y Materia. Mostrar sólo LU y Nombre de materia"""
    
    consultaSQL = """
                    SELECT DISTINCT LU,Nombre
                    FROM se_inscribe_en
                    INNER JOIN materia
                    ON materia.codigo_materia=se_inscribe_en.codigo_materia
                  """

    imprimirEjercicio(consigna, [persona, nacionalidades], consultaSQL)
    
    
    print("# =============================================================================")
    print("# Ejercicios SQL - Join de varias tablas en simultáneo")
    print("# =============================================================================")

    consigna    = """a.- Vincular las tablas Reserva, Pasajero y Vuelo. Mostrar sólo Fecha de reserva, hora de salida del vuelo y nombre de pasajero."""
    
    consultaSQL = """

                  """

    imprimirEjercicio(consigna, [reserva, pasajero, vuelo], consultaSQL)

    
    print("# =============================================================================")
    print("# Ejercicios SQL - Tuplas espúreas")
    print("# =============================================================================")

    consigna    = """a.- Vincular (JOIN)  EmpleadoRol y RolProyecto para obtener la tabla original EmpleadoRolProyecto"""
    
    consultaSQL = """
                    SELECT DISTINCT *
                    FROM empleadoRol
                    INNER JOIN rolProyecto
                    ON empleadoRol.rol = rolProyecto.rol
                  """

    imprimirEjercicio(consigna, [empleadoRol, rolProyecto], consultaSQL)

    print("# =============================================================================")
    print("# Ejercicios SQL - Funciones de agregación")
    print("# =============================================================================")

    consigna    = """a.- Usando sólo SELECT contar cuántos exámenes fueron rendidos (en total)"""
    
    consultaSQL = """
                     SELECT count(*) as cantidadExamenes
                     FROM examen
                  """

    imprimirEjercicio(consigna, [examen], consultaSQL)


    # -----------
    consigna    = """b1.- Usando sólo SELECT contar cuántos exámenes fueron rendidos en cada Instancia"""
    
    consultaSQL = """

                  """

    imprimirEjercicio(consigna, [examen], consultaSQL)


    # -----------
    consigna    = """b2.- Usando sólo SELECT contar cuántos exámenes fueron rendidos en cada Instancia (ordenado por instancia)"""
    
    consultaSQL = """
                    SELECT instancia, count(*) as asistieron
                    FROM examen 
                    GROUP BY instancia
                    ORDER BY instancia ASC
                  """

    imprimirEjercicio(consigna, [examen], consultaSQL)


    # -----------
    consigna    = """b3.- Ídem ejercicio anterior, pero mostrar sólo las instancias a las que asistieron menos de 4 Estudiantes"""
    
    consultaSQL = """
                     SELECT instancia, count(*) as asistieron
                    FROM examen 
                    GROUP BY instancia
                    HAVING asistieron < 4
                    ORDER BY instancia ASC
                  """

    imprimirEjercicio(consigna, [examen], consultaSQL)


    # -----------
    consigna    = """c.- Mostrar el promedio de edad de los estudiantes en cada instancia de examen"""
    
    consultaSQL = """
                    SELECT instancia, avg(edad) as promedioEdad
                    FROM examen
                    GROUP BY instancia
                    ORDER BY instancia ASC
                  """

    imprimirEjercicio(consigna, [examen], consultaSQL)


    print("# =============================================================================")
    print("# Ejercicios SQL - LIKE")
    print("# =============================================================================")

    consigna    = """a1.- Mostrar cuál fue el promedio de notas en cada instancia de examen, sólo para instancias de parcial."""

    consultaSQL = """
                    SELECT instancia, avg(nota) as promedioNotas
                    FROM examen 
                    GROUP BY instancia
                    HAVING instancia = 'Parcial-01' or instancia = 'Parcial-02'
                    ORDER BY instancia ASC
                  """
  

    imprimirEjercicio(consigna, [examen], consultaSQL)


    # -----------
    consigna    = """a2.- Mostrar cuál fue el promedio de notas en cada instancia de examen, sólo para instancias de parcial. Esta vez usando LIKE."""
    
    consultaSQL = """
                    SELECT instancia, avg(nota) as promedioNotas
                    FROM examen 
                    GROUP BY instancia
                    HAVING instancia LIKE 'Parcial%'
                    ORDER BY instancia ASC
                  """

    imprimirEjercicio(consigna, [examen], consultaSQL)


    print("# =============================================================================")
    print("# Ejercicios SQL - Eligiendo")
    print("# =============================================================================")

    consigna    = """a1.- Listar a cada alumno que rindió el Parcial-01 y decir si aprobó o no (se aprueba con nota >=4)."""
    
    consultaSQL = """
                    SELECT Nombre, nota, CASE WHEN nota >= 4 then 'aprobo' ELSE 'no aprobo' END as estado
                    from examen 
                  """

    imprimirEjercicio(consigna, [examen], consultaSQL)


    # -----------
    consigna    = """a2.- Modificar la consulta anterior para que informe cuántos estudiantes aprobaron/reprobaron en cada instancia."""
    
    consultaSQL = """

                  """

    imprimirEjercicio(consigna, [examen], consultaSQL)


    print("# =============================================================================")
    print("# Ejercicios SQL - Subqueries")
    print("# =============================================================================")

    consigna    = """a.- Listar los alumnos que en cada instancia obtuvieron una nota mayor al promedio de dicha instancia"""
    
    consultaSQL = """

                  """


    imprimirEjercicio(consigna, [examen], consultaSQL)


    # -----------
    consigna    = """b.- Listar los alumnos que en cada instancia obtuvieron la mayor nota de dicha instancia"""
    
    consultaSQL = """

                  """

    imprimirEjercicio(consigna, [examen], consultaSQL)


    # -----------
    consigna    = """c.- Listar el nombre, instancia y nota sólo de los estudiantes que no rindieron ningún Recuperatorio"""
    
    consultaSQL = """

                  """

    imprimirEjercicio(consigna, [examen], consultaSQL)


    print("# =============================================================================")
    print("# Ejercicios SQL - Integrando variables de Python")
    print("# =============================================================================")

    consigna    = """a.- Mostrar Nombre, Instancia y Nota de los alumnos cuya Nota supera el umbral indicado en la variable de Python umbralNota"""
    
    umbralNota = 7
    
    consultaSQL = """

                  """

    print(sql^ consultaSQL)
    # imprimirEjercicio(consigna, [examen], consultaSQL)


    print("# =============================================================================")
    print("# Ejercicios SQL - Manejo de NULLs")
    print("# =============================================================================")

    consigna    = """a.- Listar todas las tuplas de Examen03 cuyas Notas son menores a 9"""
    
    consultaSQL = """

                  """


    imprimirEjercicio(consigna, [examen03], consultaSQL)


    # -----------
    consigna    = """b.- Listar todas las tuplas de Examen03 cuyas Notas son mayores o iguales a 9"""
    
    consultaSQL = """

                  """


    imprimirEjercicio(consigna, [examen03], consultaSQL)


    # -----------
    consigna    = """c.- Listar el UNION de todas las tuplas de Examen03 cuyas Notas son menores a 9 y las que son mayores o iguales a 9"""
    
    consultaSQL = """

                  """


    imprimirEjercicio(consigna, [examen03], consultaSQL)


    # -----------
    consigna    = """d1.- Obtener el promedio de notas"""
    
    consultaSQL = """

                  """


    imprimirEjercicio(consigna, [examen03], consultaSQL)


    # -----------
    consigna    = """d2.- Obtener el promedio de notas (tomando a NULL==0)"""
    
    consultaSQL = """

                  """


    imprimirEjercicio(consigna, [examen03], consultaSQL)

    print("# =============================================================================")
    print("# Ejercicios SQL - Desafío")
    print("# =============================================================================")

    consigna    = """a.- Mostrar para cada estudiante las siguientes columnas con sus datos: Nombre, Sexo, Edad, Nota-Parcial-01, Nota-Parcial-02, Recuperatorio-01 y , Recuperatorio-02"""
    
    # ... Paso 1: Obtenemos los datos de los estudiantes
    consultaSQL = """

                  """

    datosEstudiantes = sql^ consultaSQL
    
    # ... Paso 2: Agregamos las notas del Parcial-01
    consultaSQL = """

                  """

    datosHastaParcial01 = sql^ consultaSQL

    # ... Paso 3: Agregamos las notas del Parcial-02
    consultaSQL = """

                  """

    datosHastaParcial02 = sql^ consultaSQL

    # ... Paso 4: Agregamos las notas del Recuperatorio-01
    consultaSQL = """

                  """

    datosHastaRecuperatorio01 = sql^ consultaSQL

    # ... Paso 5: Agregamos las notas del Recuperatorio-02
    consultaSQL = """

                  """

    datosHastaRecuperatorio02 = sql^ consultaSQL

    desafio_01 = datosHastaRecuperatorio02

    imprimirEjercicio(consigna, [examen], consultaSQL)


    # -----------
    consigna    = """b.- Agrega al ejercicio anterior la columna Estado, que informa si el alumno aprobó la cursada (APROBÓ/NO APROBÓ). Se aprueba con 4."""
    
    consultaSQL = """

                  """

    desafio_02 = sql^ consultaSQL
    
    imprimirEjercicio(consigna, [examen], consultaSQL)


# =============================================================================
# FUNCIONES PARA LA GENERACIÓN DE DATAFRAMES 
# =============================================================================
def get_empleado():
    # Genera el dataframe "empleado" que contiene las siguientes columnas 
    # (en el orden mencionado):
        # 1. DNI
        # 2. Nombre
        # 3. Sexo
        # 4. Salaro
        
    # ... Creamos el dataframe vacío (sólo con los nombres de sus columnas)
    empleado = pd.DataFrame(columns = ['DNI', 'Nombre', 'Sexo', 'Salario'])
    # ... Agregamos cada una de las filas al dataFrame
    empleado = pd.concat([empleado,pd.DataFrame([
        {'DNI' : 20222333, 'Nombre' : 'Diego' , 'Sexo' : 'M', 'Salario' : 20000.0},
        {'DNI' : 33456234, 'Nombre' : 'Laura' , 'Sexo' : 'F', 'Salario' : 25000.0},
        {'DNI' : 45432345, 'Nombre' : 'Marina', 'Sexo' : 'F', 'Salario' : 10000.0}
                                                ])
                        ])
    return empleado


def get_alumnosBD():
    # Genera el dataframe "alumnosBD" que contiene las siguientes columnas 
    # (en el orden mencionado):
        # 1. ID
        # 2. Nombre
        
    # ... Creamos el dataframe vacío (sólo con los nombres de sus columnas)
    alumnosBD = pd.DataFrame(columns = ['ID', 'Nombre'])
    # ... Agregamos cada una de las filas al dataFrame
    alumnosBD = pd.concat([alumnosBD,pd.DataFrame([
        {'ID' : 1, 'Nombre' : 'Diego' },
        {'ID' : 2, 'Nombre' : 'Laura' },
        {'ID' : 3, 'Nombre' : 'Marina'}
                                                    ])
                        ])
    return alumnosBD


def get_alumnosTLeng():
    # Genera el dataframe alumnosTLeng que contiene las siguientes columnas 
    # (en el orden mencionado):
        # 1. ID
        # 2. Nombre
        
    # ... Creamos el dataframe vacío (sólo con los nombres de sus columnas)
    alumnosTLeng = pd.DataFrame(columns = ['ID', 'Nombre'])
    # ... Agregamos cada una de las filas al dataFrame
    alumnosTLeng = pd.concat([alumnosTLeng,pd.DataFrame([
        {'ID' : 2, 'Nombre' : 'Laura'    },
        {'ID' : 4, 'Nombre' : 'Alejandro'}
                                                        ])
                        ])
    return alumnosTLeng


def get_persona_ejemploCrossJoin():
    # Genera el dataframe "persona" que contiene las siguientes columnas 
    # (en el orden mencionado):
        # 1. Nombre
        # 2. Nacionalidad
        
    # ... Creamos el dataframe vacío (sólo con los nombres de sus columnas)
    persona = pd.DataFrame(columns = ['Nombre', 'Nacionalidad'])
    # ... Agregamos cada una de las filas al dataFrame
    persona = pd.concat([persona,pd.DataFrame([
        {'Nombre' : 'Diego'   , 'Nacionalidad' : 'AR'    },
        {'Nombre' : 'Laura'   , 'Nacionalidad' : 'BR'    },
        {'Nombre' : 'Marina'  , 'Nacionalidad' : 'AR'    }
                                              ])
                        ])
    return persona


def get_persona_ejemplosJoin():
    # Genera el dataframe "persona" que contiene las siguientes columnas 
    # (en el orden mencionado):
        # 1. Nombre
        # 2. Nacionalidad
        
    # ... Creamos el dataframe vacío (sólo con los nombres de sus columnas)
    persona = pd.DataFrame(columns = ['Nombre', 'Nacionalidad'])
    # ... Agregamos cada una de las filas al dataFrame
    persona = pd.concat([persona,pd.DataFrame([
        {'Nombre' : 'Diego'   , 'Nacionalidad' : 'BR'    },
        {'Nombre' : 'Laura'   , 'Nacionalidad' : None    },
        {'Nombre' : 'Marina'  , 'Nacionalidad' : 'AR'    },
        {'Nombre' : 'Santiago', 'Nacionalidad' : 'UY'    }
                                              ])
                        ])
    return persona


def get_se_inscribe_en_ejemploMismosNombres():
    # Genera el dataframe "se_inscribe_en" que contiene las siguientes columnas 
    # (en el orden mencionado):
        # 1. LU
        # 2. Codigo_materia
        
    # ... Creamos el dataframe vacío (sólo con los nombres de sus columnas)
    se_inscribe_en = pd.DataFrame(columns = ['LU','Codigo_materia'])
    # ... Agregamos cada una de las filas al dataFrame
    se_inscribe_en = pd.concat([se_inscribe_en,pd.DataFrame([
        {'LU':'123/09','Codigo_materia': 1},
        {'LU':' 22/10','Codigo_materia': 1},
        {'LU':' 22/10','Codigo_materia': 2},
        {'LU':'344/09','Codigo_materia': 1}
                                              ])
                        ])
    return se_inscribe_en

def get_materia_ejemploMismosNombres():
    # Genera el dataframe "materia" que contiene las siguientes columnas 
    # (en el orden mencionado):
        # 1. Codigo_materia
        # 2. Nombre
        
    # ... Creamos el dataframe vacío (sólo con los nombres de sus columnas)
    materia = pd.DataFrame(columns = ['Codigo_materia','Nombre'])
    # ... Agregamos cada una de las filas al dataFrame
    materia = pd.concat([materia,pd.DataFrame([
        {'Codigo_materia': 1, 'Nombre':'Laboratorio de Datos'   },
        {'Codigo_materia': 2, 'Nombre':'Análisis II'   },
        {'Codigo_materia': 3, 'Nombre':'Probabilidad'   }
                                              ])
                        ])
    return materia


def get_nacionalidades():
    # Genera el dataframe "nacionalidades" que contiene las siguientes columnas 
    # (en el orden mencionado):
        # 1. IDN (Id Nacionalidad)
        # 2. Detalle
    
    # ... Creamos el dataframe vacío (sólo con los nombres de sus columnas)
    nacionalidades = pd.DataFrame(columns = ['IDN', 'Detalle'])
    # ... Agregamos cada una de las filas al dataFrame
    nacionalidades = pd.concat([nacionalidades,pd.DataFrame([
        {'IDN' : 'AR', 'Detalle' : 'Agentina'},
        {'IDN' : 'BR', 'Detalle' : 'Brasilera'},
        {'IDN' : 'CH', 'Detalle' : 'Chilena'}
                                                          ])
                        ])
    return nacionalidades

# =============================================================================
# DEFINICION DE FUNCIÓN DE IMPRESIÓN EN PANTALLA
# =============================================================================
# Imprime en pantalla en un formato ordenado:
    # 1. Consigna
    # 2. Cada dataframe de la lista de dataframes de entrada
    # 3. Query
    # 4. Dataframe de salida
def imprimirEjercicio(consigna, listaDeDataframesDeEntrada, consultaSQL):
    
    print("# -----------------------------------------------------------------------------")
    print("# Consigna: ", consigna)
    print("# -----------------------------------------------------------------------------")
    print()
    for i in range(len(listaDeDataframesDeEntrada)):
        print("# Entrada 0",i,sep='')
        print("# -----------")
        print(listaDeDataframesDeEntrada[i])
        print()
    print("# SQL:")
    print("# ----")
    print(consultaSQL)
    print()
    print("# Salida:")
    print("# -------")
    print(sql^ consultaSQL)
    print()
    print("# -----------------------------------------------------------------------------")
    print("# -----------------------------------------------------------------------------")
    print()
    print()


# =============================================================================
# EJECUCIÓN MAIN
# =============================================================================

if __name__ == "__main__":
    main()