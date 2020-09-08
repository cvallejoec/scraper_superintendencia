from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import time
#To databse connections
import pandas as pd
import mysql.connector
import sshtunnel
# Garbage collector
import gc

# Nombre de archivo de identificaciones
FILE_NAME = './identificaciones/nombre-archivo.csv'

# Nombres de tablas
TABLA_ACCIONISTAS = 'superintendencia_accionistas'

# Direcciones de XPath
URL = 'https://appscvsmovil.supercias.gob.ec/PortalInfor/consultaPrincipal.zul'
IDENTIFICACION_BUTTON = '//span[@class="z-radio"]'
PARAMETRO_LABEL = '//i[@class="z-combobox"]/input'
COMBOBOX_ITEMS = '//table[@class="z-combobox-cave"]//td[@class="z-comboitem-text"]'
BUSCAR_BUTTON = '//td[@class="z-button-cm"]'
NOMBRE_TITULO = '//span[@class="z-label"]'
ACCIONISTAS_BUTTON = '//img[@src="images/accionistas.png"]'
ROW_ACCIONISTAS = '//tbody[@class="z-treechildren"]//tr'
CELLS_ACCIONISTAS = './/td/div/.'
CLOSE_MODAL = '//div[@class="z-window-modal-icon-img"]'
NUEVA_CONSULTA_BUTTON = '(//td[@class="z-button-cm"])[1]'

# Obtiene lista de identificaciones a partir de un .csv
def get_identificaciones():
    df = pd.read_csv(FILE_NAME, dtype=str)
    return df.values.tolist()

# Conexión con la base de datos, para utilizarlo solo se invoca a la función y se envía un query
def data_base(query):
    with sshtunnel.SSHTunnelForwarder(
        ('192.168.0.1', 3000),  # IP Servidor SSH, y puerto
        ssh_username = 'admin', # Usuario SSH
        ssh_password = '*53rv1d0rPr0p10*',  # Password SSH
        remote_bind_address = ('127.0.0.1', 3306)   # Dirección de Base de Datos (usualmente no cambia)
    ) as tunnel:
        connection = mysql.connector.connect(
            user = 'root',   #   Usuario Base de Datos
            password = 'root_password',  # Password Base de Datos
            host = '127.0.0.1', # IP de base de datos (usualmente no cambia)
            port = tunnel.local_bind_port, # No cambiar
            database = 'my_data_base', # Nombre de Base de Datos
        )
        try:
            cursor = connection.cursor()
            cursor.execute(query)
            cursor.close()
            connection.close()
        except Exception as e:
            print(e)

# Permite ver si un elemento se muestra visible, en un máximo de 30 segundos
def is_visible(driver, locator, timeout = 30):
    try:
        WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.XPATH, locator)))
        return True
    except:
        return False
    
# Ingreso al menú principal, desde donde se llaman a los demás submenúes 
def ingreso_menu(driver, identificacion, requerimientos):
    print(f'Accediendo a información de: {identificacion}')

    try:
        identificacion_button = driver.find_elements_by_xpath(IDENTIFICACION_BUTTON)[1].click()

        parametro = driver.find_elements_by_xpath(PARAMETRO_LABEL)[0]
        time.sleep(1)
        parametro.send_keys(identificacion)
        if not is_visible(driver, COMBOBOX_ITEMS, 5): 
            parametro.clear()
            return []
        parametro.send_keys(Keys.RETURN)

        buscar_button = driver.find_elements_by_xpath(BUSCAR_BUTTON)[0].click()

        time.sleep(2)
        if not is_visible(driver, NOMBRE_TITULO, 10): nueva_consulta(driver)
        empresa = {
            'identificacion': identificacion,
            'nombre': driver.find_elements_by_xpath(NOMBRE_TITULO)[0].text
        }

        for requerimiento in requerimientos:
            if requerimiento == 'accionistas':
                get_accionistas(driver, empresa)
                pass
            if requerimiento == 'administradores':
                pass

            nueva_consulta(driver)
    except TimeoutError as timeout:
        print('Tiempo excedido en ingreso_menu - primer try')
        print(timeout)
        

# Obtiene todos los accionistas, esta función se invoca desde ingreso_menu()
def get_accionistas(driver, empresa):
    print('Buscando accionistas...')

    if not is_visible(driver, ACCIONISTAS_BUTTON, 5): 
        driver.find_elements_by_xpath(NUEVA_CONSULTA_BUTTON)[0].click()
        return []
    accionistas_button = driver.find_elements_by_xpath(ACCIONISTAS_BUTTON)[0].click()

    if not is_visible(driver, ROW_ACCIONISTAS, 5):
        # Como no apareció ROW_ACCIONISTAS quiere decir que esta identificación no tiene accionistas
        cerrar_modal(driver)
        print('No tiene accionistas')
        return []
    row_accionistas = driver.find_elements_by_xpath(ROW_ACCIONISTAS)


    for accionista in row_accionistas:
        try:
            fila = accionista.find_elements_by_xpath(CELLS_ACCIONISTAS)
            
            identificacion_socio = fila[1].text
            nombre_socio = fila[2].text
            nacionalidad = fila[3].text
            tipo_inversion = fila[4].text
            capital = fila[5].text
            restriccion = fila[6].text

            # Se eleminan a todos los 'subsocios' que aparecen en la tabla
            if identificacion_socio:
                query = f'INSERT INTO {TABLA_ACCIONISTAS} (identificacion, nombre, identificacion_socio, nombre_socio, nacionalidad, tipo_inversion, capital, restriccion) VALUES ("{empresa["identificacion"]}", "{empresa["nombre"]}", "{identificacion_socio}", "{nombre_socio}", "{nacionalidad}", "{tipo_inversion}", "{capital}", "{restriccion}")'
                print(f'Guardando a accionista {identificacion_socio}')
                data_base(query)

        except Exception as e:
            print(e)
            pass
    cerrar_modal(driver)

# Obtiene a todos los administradores
def get_administradores(driver):
    print('Buscando administradores...')
    pass

def cerrar_modal(driver):
    time.sleep(1)
    close_modal = driver.find_elements_by_xpath(CLOSE_MODAL)[0]
    driver.execute_script("arguments[0].click();", close_modal)
    try:
       WebDriverWait(driver, 5).until(EC.invisibility_of_element((By.XPATH, CLOSE_MODAL)))
    except TimeoutError as timeout:
        print('Tiempo excedido en cerrar_modal')
        print(timeout)

# Regresa a la página principal para volver a introducir otra identificación
def nueva_consulta(driver):
    driver.find_elements_by_xpath(NUEVA_CONSULTA_BUTTON)[0].click()
    time.sleep(1)

# Quita el primer caractér de las identificaciones y devuelve un RUC de 13 dígitos
def remove_at(i, s):
  return s[:i] + s[i+1:]

def execute_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--start-maximized--')
    options.add_argument('disable-infobars')
    driver = webdriver.Chrome('./chromedriver.exe', options = options, service_args = ['--ignore-ssl-errors = true'])
    driver.get(URL)
    return driver

if __name__ == '__main__':
    print('Inicializando scraping...')
    identificaciones = get_identificaciones()

    driver = execute_driver()

    print('Programa inicializado.')
    print('HAPPY SCRAPING! \n')

    for index, identificacion in enumerate(identificaciones):
        print(f'\nCiclo: {index + 1}')
        identificacion = identificacion[0]
        # Si es una cédula mayor a 13 caracteres elimina el primer caracter del string
        if len(identificacion) > 13:
            identificacion = remove_at(0, identificacion)
        try:
            ingreso_menu(driver, identificacion, ['accionistas'])
        except TimeoutException as timeout:
            print('Tiempo excedido en __name__ - for')
            print(timeout)
            driver.quit()
            driver = execute_driver()
        except Exception as e:
            print('Error desconocido') 
            print(e)  
            driver.quit()
            driver = execute_driver()

        gc.collect()

    print('Scraper finalizado. Muchas gracias.')