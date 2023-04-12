import pandas as pd 
from inline_sql import sql, sql_val


vuelo = pd.read_csv("~/Descargas/vuelo.csv")    
aeropuerto = pd.read_csv("~/Descargas/aeropuerto.csv")    
pasajero = pd.read_csv("~/Descargas/pasajero.csv")    
reserva = pd.read_csv("~/Descargas/reserva.csv")    