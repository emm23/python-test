# python-test

#### Descripcion.

Construcción de un ETL utilizando el archivo CSV clientes.

#### Modulos.

##### En el proyecto se utilizan los siguientes módulos: 
- Pandas
- Numpy
- Sqlalchemy
- Sqlite3

#### Instalación de dependencias.
La instalación de las dependencias se realiza utilizando el archivo llamado *requirements.txt*.

##### Instrucciones.
- La ejecución del programa se realiza con el comando **python main.py**.
- Después de la ejecución aparecerá una leyenda *Escribe la ruta del archivo csv:* donde escribirá la ruta del archivo CSV. (ej. /Volumes/nuevo/Drive/colektia_evaluacion/clientes.csv).

#### Resultado.

###### El programa tendrá como resultado 3 archivos de tipo *"XLSX"*  guardados en la carpeta **output** llamados:
- Clientes
- Emails
- Phone

###### También tendrá como resultado una base de datos que contiene la misma información de los archivos en Excel. La base de datos está compuesta de 3 tablas:
- Customers
- Emails
- Phones
