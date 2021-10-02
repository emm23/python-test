#librerias
import pandas as pd
import numpy as np
import datetime
import os
import sqlite3
from sqlite3 import Error
from sqlalchemy import create_engine 

#convierte en mayusculas una serie
def mayusculas(serie):
  if(type(serie)==str):
      return serie.str.upper()
  else:
      return serie

#calcula la edad dada una fecha
def edad(fecha):
  anio, mes, dia = fecha.split('-')
  fecha_actual = datetime.datetime.now()
  anio_actual, mes_actual, dia_actual = fecha_actual.year, fecha_actual.month, fecha_actual.day
  edad = anio_actual - int(anio)
  if(mes_actual < int(mes) or dia_actual < int(dia)):
      edad-=1
  return edad

#asignar etiquetas dependiendo de los rangos de edad
def grupo_edad(edad):
  if(edad<=20):
      return 1
  elif(edad>=21 and edad<=30):
      return 2
  elif(edad>=31 and edad<=40):
      return 3
  elif(edad>=41 and edad<=50):
      return 4
  elif(edad>=51 and edad<=60):
      return 5
  elif(edad>60):
      return 6

#calculo de los dias de deuda
def deuda_atraso(fecha_deuda):
  fecha_actual = datetime.datetime.now()
  anio, mes, dia = fecha_deuda.split('-')
  fecha_fomato_deuda = datetime.datetime(int(anio), int(mes), int(dia))
  return int(str(fecha_actual-fecha_fomato_deuda).split(' ')[0])

#convierte la fecha (string) a datetime
def dato_tiempo(fecha):
  anio, mes, dia = fecha.split('-')
  return datetime.datetime(int(anio), int(mes), int(dia))

#recibir direccion
direccion = input("Escribe la ruta del archivo csv: ")

#cargar el archivo csv
dataframe = pd.read_csv(direccion, delimiter=';', usecols=['fiscal_id', 'first_name', 'last_name', 'gender', 'fecha_nacimiento', 'fecha_vencimiento', 'deuda', 'direccion', 'correo', 'estatus_contacto', 'prioridad', 'telefono'], encoding='utf-8')

#eliminacion de na, definicion de los tipos de datos y cambios de nombre
dataframe.dropna(inplace=True)
tipos_dataframe = dataframe.astype({'fiscal_id':'string', 'first_name':'string', 'last_name':'string', 'gender':'string', 'fecha_nacimiento':'string', 'fecha_vencimiento':'string', 'deuda':np.uint64, 'direccion':'string', 'correo':'string', 'estatus_contacto':'string', 'prioridad':np.uint64, 'telefono':np.uint64})
tipos_dataframe = tipos_dataframe.rename(columns={'fecha_nacimiento':'birth_date', 'fecha_vencimiento':'due_date', 'deuda':'due_balance', 'direccion':'address', 'correo':'email', 'estatus_contacto':'status', 'prioridad':'priority', 'telefono':'phone'})

#normalizacion y procesamiento de los datos
tipos_dataframe_norm = tipos_dataframe.apply(mayusculas)
tipos_dataframe_norm['age'] = tipos_dataframe_norm['birth_date'].apply(edad)
tipos_dataframe_norm['age_group'] = tipos_dataframe_norm['age'].apply(grupo_edad)
tipos_dataframe_norm['delinquency'] = tipos_dataframe_norm['due_date'].apply(deuda_atraso)

#cambio a tipo de dato date
tipos_dataframe_norm['birth_date'] = tipos_dataframe_norm['birth_date'].apply(dato_tiempo)

#ruta de los archivos de salida
ruta=os.getcwd()
ruta_salida = ruta+'/output/'

#guardar archivos con resultados
tipos_dataframe_norm[['fiscal_id', 'first_name', 'last_name', 'gender', 'birth_date', 'age', 'age_group', 'due_date', 'delinquency', 'due_balance', 'address']].to_excel(os.path.join(ruta_salida,'clientes.xlsx'))
tipos_dataframe_norm[['fiscal_id', 'email', 'status', 'priority']].to_excel(os.path.join(ruta_salida,'emails.xlsx'))
tipos_dataframe_norm[['fiscal_id', 'phone','status', 'priority']].to_excel(os.path.join(ruta_salida,'phone.xlsx'))

#conexion, creacion, e insercion en la base de datos
base_datos = 'database.db3'
conexion = sqlite3.connect(base_datos)
engine = create_engine('sqlite://', echo=False)
tipos_dataframe_norm[['fiscal_id', 'first_name', 'last_name', 'gender', 'birth_date', 'age', 'age_group', 'due_date', 'delinquency', 'due_balance', 'address']].to_sql(name='customers', con=engine, if_exists='append')
tipos_dataframe_norm[['fiscal_id', 'email', 'status', 'priority']].to_sql(name='emails', con=engine, if_exists='append')
tipos_dataframe_norm[['fiscal_id', 'phone','status', 'priority']].to_sql(name='phones', con=engine, if_exists='append')
