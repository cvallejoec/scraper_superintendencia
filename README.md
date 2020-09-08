# Scraper de Superintendencia del Ecuador

Dada una lista de identificaciones de tipo RUC, este scraper se encarga de extraer cada uno de los accionistas correspondientes a la empresa o ente indicada.

**Índice**

1. [Requerimientos](#id1)
2. [Instalación](#id2)
3. [Uso](#id3)

## Funcionamiento <a name="id1"></a>

- Script hecho en Python que utiliza Selenium como framework para extraer la información.
- Selenium necesita un archivo llamado _chromedriver.exe_ el cual debe estar ubicado en la carpeta del script.
- Se necesita de una base de datos MySQL con conexión SSH para almacenar los datos.

## Instalación <a name="id2"></a>

1. `pip install selenium`
2. `pip install pandas`
3. `pip install mysql-connector-python`
4. `pip install sshtunnel`

## Uso <a name="id3"></a>

- Crear una carpeta llamada _identificaciones_ en la raíz. Aquí dentro deberán estar todas las identificaciones en un formato _.csv_. Deberá parecerse a esto:

```
1112223334
4444555566
7777888899
1111000335
```

- Ejecutar el archivo `structure_data_base.sql` en su base de datos elegida para poder tener la estrucutura de tablas exacta.

- En la función `data_base` ubicar todas las credenciales de acceso servidor SSH y de la Base de Datos.

- Ejecutar el comando
  `python3 main_scraper.py`

**Nota:** El comando de ejecución puede cambiar dependiendo de la versión de python instalada.
