# -*- coding: utf-8 -*-
"""
Solicitudes para contitución de nuevas empresas en SBS
"""
from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import pandas as pd
import re
from datetime import datetime

def scrape_sbs():
    url = "https://www.sbs.gob.pe/avisos-y-convocatorias-sbs/solicitudes-de-organizacion-de-nuevas-empresas"
    service = EdgeService(EdgeChromiumDriverManager().install())
    options = Options()
    options.headless = True  # Ejecutar en modo headless
    driver = webdriver.Edge(service=service, options=options)

    try:
        # Abrir la página web
        driver.get(url)

        # Esperar explícitamente a que el contenido se cargue
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, "dnn_ctr29805_HtmlModule_lblContent"))
        )

        # Definir las rutas XPath para las fechas y noticias
        fecha_xpath_template = '//*[@id="dnn_ctr29805_HtmlModule_lblContent"]/div/p[{}]/strong'
        noticia_xpath_template = '//*[@id="dnn_ctr29805_HtmlModule_lblContent"]/div/p[{}]/span'

        fechas = []
        noticias = []

        for i in [3, 6, 9, 12]:
            fecha_xpath = fecha_xpath_template.format(i)
            noticia_xpath = noticia_xpath_template.format(i - 1)

            try:
                # Extraer la fecha
                fecha_element = driver.find_element(By.XPATH, fecha_xpath)
                fechas.append(fecha_element.text.strip())

                # Extraer la noticia
                noticia_element = driver.find_element(By.XPATH, noticia_xpath)
                noticias.append(noticia_element.text.strip())
            except NoSuchElementException:
                continue

    except TimeoutException:
        print("El contenido no se cargó a tiempo.")
        return None

    finally:
        # Cerrar el navegador
        driver.quit()

    # Crear un DataFrame con los datos extraídos
    df = pd.DataFrame({
        'Fecha_sbs': fechas,
        'Noticias': noticias
    })

    # Función para extraer la fecha y convertirla al formato deseado
    def extract_date(fecha_sbs):
        match = re.search(r'(Enero|Febrero|Marzo|Abril|Mayo|Junio|Julio|Agosto|Septiembre|Octubre|Noviembre|Diciembre) \d{4}', fecha_sbs)
        if match:
            month_year = match.group(0)
            month, year = month_year.split()
            month_dict = {
                'Enero': '01', 'Febrero': '02', 'Marzo': '03', 'Abril': '04',
                'Mayo': '05', 'Junio': '06', 'Julio': '07', 'Agosto': '08',
                'Septiembre': '09', 'Octubre': '10', 'Noviembre': '11', 'Diciembre': '12'
            }
            day = datetime.now().day
            return datetime.strptime(f"{day:02d}/{month_dict[month]}/{year}", "%d/%m/%Y")
        return None

    # Crear la nueva columna "Fecha"
    df['Fecha'] = df['Fecha_sbs'].apply(extract_date)

    # Convertir la columna "Fecha" al formato de fecha
    df['Fecha'] = pd.to_datetime(df['Fecha'], format="%d/%m/%Y")

    return df

# Llamar a la función y mostrar el DataFrame
extra_SBS = scrape_sbs()
if extra_SBS is not None:
    print(extra_SBS)
else:
    print("No se encontraron datos.")
    
"-------------------------------------//////////////////////-------------------------------"    
    
"SBS normativa"
    
import pandas as pd
import logging
from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
from webdriver_manager.microsoft import EdgeChromiumDriverManager

def scrape_sbs():
    url = "https://www.sbs.gob.pe/app/pp/INT_CN/Paginas/Busqueda/BusquedaPortal.aspx"
    service = EdgeService(EdgeChromiumDriverManager().install())
    options = Options()
    options.headless = True  # Ejecutar en modo headless
    driver = webdriver.Edge(service=service, options=options)

    logging.basicConfig(level=logging.INFO)
    
    try:
        # Abrir la página web
        driver.get(url)
        logging.info("Página web abierta con éxito.")

        # Esperar explícitamente a que el contenido se cargue
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CLASS_NAME, "rgMasterTable"))
        )
        logging.info("Contenido cargado con éxito.")

        # Tomar una captura de pantalla para verificar el contenido cargado
        driver.save_screenshot('screenshot.png')
        logging.info("Captura de pantalla tomada.")

        # Definir las rutas XPath para los datos
        norma_xpath_template = '//*[@id="ctl00_ContentPlaceHolder1_rdgUltimaVersionNormas_ctl00__{}"]/td[2]'
        definicion_xpath_template = '//*[@id="ctl00_ContentPlaceHolder1_rdgUltimaVersionNormas_ctl00__{}"]/td[4]'
        tipo_xpath_template = '//*[@id="ctl00_ContentPlaceHolder1_rdgUltimaVersionNormas_ctl00__{}"]/td[5]'
        fecha_xpath_template = '//*[@id="ctl00_ContentPlaceHolder1_rdgUltimaVersionNormas_ctl00__{}"]/td[8]'
        sistema_xpath_template = '//*[@id="ctl00_ContentPlaceHolder1_rdgUltimaVersionNormas_ctl00__{}"]/td[7]'

        normas = []
        definiciones = []
        tipos = []
        fechas = []
        sistemas = []

        # Obtener el número de filas dinámicamente
        rows = driver.find_elements(By.XPATH, '//*[@id="ctl00_ContentPlaceHolder1_rdgUltimaVersionNormas_ctl00"]/tbody/tr')
        num_rows = len(rows)

        # Iterar sobre las filas
        for i in range(num_rows):
            try:
                norma_xpath = norma_xpath_template.format(i)
                definicion_xpath = definicion_xpath_template.format(i)
                tipo_xpath = tipo_xpath_template.format(i)
                fecha_xpath = fecha_xpath_template.format(i)
                sistema_xpath = sistema_xpath_template.format(i)

                # Extraer los datos
                norma_element = driver.find_element(By.XPATH, norma_xpath)
                definicion_element = driver.find_element(By.XPATH, definicion_xpath)
                tipo_element = driver.find_element(By.XPATH, tipo_xpath)
                fecha_element = driver.find_element(By.XPATH, fecha_xpath)
                sistema_element = driver.find_element(By.XPATH, sistema_xpath)

                normas.append(norma_element.text.strip())
                definiciones.append(definicion_element.text.strip())
                tipos.append(tipo_element.text.strip())
                fechas.append(fecha_element.text.strip())
                sistemas.append(sistema_element.text.strip())
            except NoSuchElementException:
                logging.warning(f"Elemento no encontrado en la posición {i}.")
                continue

    except TimeoutException:
        logging.error("El contenido no se cargó a tiempo.")
        return None
    except WebDriverException as e:
        logging.error(f"Error del WebDriver: {e}")
        return None
    finally:
        # Cerrar el navegador
        driver.quit()
        logging.info("Navegador cerrado.")

    # Crear un DataFrame con los datos extraídos
    df = pd.DataFrame({
        'Norma': normas,
        'Definición': definiciones,
        'Tipo': tipos,
        'Fecha': fechas,
        'Sistema': sistemas
    })

    # Convertir la columna "Fecha" al formato de fecha
    df['Fecha'] = pd.to_datetime(df['Fecha'], format="%d/%m/%Y", errors='coerce')

    # Lista de palabras clave a buscar en la columna 'Definición'
    keywords = [
        "cambiario", "crediticio", "inversiones", "derivados", "cobertura", "liquidez", 
        "riesgo de modelo", "riesgo de crédito", "actuarial", "SISCO", "riesgo de mercado", 
        "Riesgo Social", "Anexo", "Riesgo Cambiario", "Riesgo de Liquidez", "Riesgo País", 
        "Gestión Integral de Riesgos", "Informe de riesgos", "Reserva de Riesgos en Curso", 
        "Aspectos Actuariales", "Reservas Matemáticas", "reservas técnicas", 
        "Reserva Técnica", "reservas técnicas del seguro complementario", 
        "Estimación de Primas", "SCTR", "Anexos 7", "Anexo N° 8", "Anexo N° 16", 
        "Anexo N° 7"
    ]

    # Filtrar el DataFrame para incluir solo las filas que contienen las palabras clave en la columna 'Definición'
    filtered_df = df[df['Definición'].str.contains('|'.join(keywords), case=False)]

    return df, filtered_df

# Llamar a la función y mostrar los DataFrames
sbs, filtered_sbs = scrape_sbs()
if sbs is not None:
    print("DataFrame completo:")
    print(sbs)
    print("\nDataFrame filtrado:")
    print(filtered_sbs)
else:
    print("No se encontraron datos.")
   
    
"-------------------------------- SMV normativa ---------------------------------------"

import pandas as pd
import logging
from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import re

def scrape_smv():
    url = "https://www.smv.gob.pe/ServicioConsultaNormas/Frm_Resoluciones?data=28E2BCB3AAF0F6112BFB80F90A370B9923A973B3D2"
    service = EdgeService(EdgeChromiumDriverManager().install())
    options = Options()
    options.headless = True  # Ejecutar en modo headless
    driver = webdriver.Edge(service=service, options=options)

    logging.basicConfig(level=logging.INFO)
    
    try:
        # Abrir la página web
        driver.get(url)
        logging.info("Página web abierta con éxito.")

        # Esperar explícitamente a que el contenido se cargue
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, "MainContent_lisAnio"))
        )
        logging.info("Contenido cargado con éxito.")

        # Seleccionar el año actual en el desplegable
        select_anio = Select(driver.find_element(By.ID, "MainContent_lisAnio"))
        select_anio.select_by_visible_text("2025")
        logging.info("Año seleccionado con éxito.")

        # Hacer clic en el botón de consulta
        driver.find_element(By.ID, "btnConsultar").click()
        logging.info("Botón de consulta clicado con éxito.")

        # Esperar a que la tabla se cargue
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, "MainContent_grdCabecera_lblCabDato3_0"))
        )
        logging.info("Tabla cargada con éxito.")

        # Inicializar listas para almacenar los datos extraídos
        cabecera_datos = []
        subcabecera_datos = []

        # Iterar sobre los elementos del 0 al 9 y extraer los datos
        for i in range(10):
            try:
                cabecera_xpath = f'//*[@id="MainContent_grdCabecera_lblCabDato3_{i}"]'
                subcabecera_xpath = f'//*[@id="MainContent_grdCabecera_grdSubCabecera_{i}_lblCabDato4_0"]'

                cabecera_element = driver.find_element(By.XPATH, cabecera_xpath)
                subcabecera_element = driver.find_element(By.XPATH, subcabecera_xpath)

                cabecera_datos.append(cabecera_element.text.strip())
                subcabecera_datos.append(subcabecera_element.text.strip())
            except NoSuchElementException:
                logging.warning(f"Elemento no encontrado en la posición {i}.")
                continue

    except TimeoutException:
        logging.error("El contenido no se cargó a tiempo.")
        return None
    except WebDriverException as e:
        logging.error(f"Error del WebDriver: {e}")
        return None
    finally:
        # Cerrar el navegador
        driver.quit()
        logging.info("Navegador cerrado.")

    # Crear un DataFrame con los datos extraídos
    df = pd.DataFrame({
        'Norma': cabecera_datos,
        'Definición': subcabecera_datos
    })

    # Función para extraer la fecha
    def extract_date(norma):
        match = re.search(r'\d{2}/\d{2}/\d{4}', norma)
        return match.group(0) if match else None

    # Crear la nueva columna "Fecha"
    df['Fecha'] = df['Norma'].apply(extract_date)

    return df

# Llamar a la función y mostrar el DataFrame
smv = scrape_smv()
if smv is not None:
    print("DataFrame de salida:")
    print(smv)
else:
    print("No se encontraron datos.")    
    
       
"--------------///// SBS Pre Publicaciones /////---------------------------------"
 
import pandas as pd
import logging
from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
from webdriver_manager.microsoft import EdgeChromiumDriverManager

def scrape_sbs():
    base_url = "https://www.sbs.gob.pe/app/pp/PreProyectos/interno.asp?n="
    urls = [f"{base_url}{i:02}" for i in range(1, 14) if i not in [5, 7, 8, 9, 10]]
    sistema_mapping = {
        "01": "Normas Generales",
        "02": "Sistema Financiero",
        "03": "Sistema de Seguros",
        "04": "Sistema Privado de Pensiones",
        "06": "Otras entidades",
        "11": "PLAFT",
        "12": "COOPAC",
        "13": "AFOCAT"
    }

    service = EdgeService(EdgeChromiumDriverManager().install())
    options = Options()
    options.headless = True  # Ejecutar en modo headless
    driver = webdriver.Edge(service=service, options=options)

    logging.basicConfig(level=logging.INFO)

    data = {sistema: [] for sistema in sistema_mapping.values()}

    try:
        for url in urls:
            try:
                driver.get(url)
                logging.info(f"Página web {url} abierta con éxito.")

                # Esperar explícitamente a que el contenido se cargue
                WebDriverWait(driver, 30).until(
                    EC.presence_of_element_located((By.XPATH, '//table/tbody/tr[3]/td[2]/div/a/u/strong'))
                )
                logging.info("Contenido cargado con éxito.")

                try:
                    elemento1 = driver.find_element(By.XPATH, '//table/tbody/tr[3]/td[2]/div/a/u/strong').text.strip()
                    fecha1 = driver.find_element(By.XPATH, '/html/body/table/tbody/tr/td/div/table/tbody/tr/td/table/tbody/tr[3]/td[2]/div/i').text.strip()
                except NoSuchElementException:
                    elemento1 = None
                    fecha1 = None

                try:
                    elemento2 = driver.find_element(By.XPATH, '//table/tbody/tr[4]/td[2]/div/a/u/strong').text.strip()
                    fecha2 = driver.find_element(By.XPATH, '/html/body/table/tbody/tr/td/div/table/tbody/tr/td/table/tbody/tr[4]/td[2]/div/i').text.strip()
                except NoSuchElementException:
                    elemento2 = None
                    fecha2 = None

                sistema = sistema_mapping[url.split("=")[-1]]

                if elemento1 or elemento2:
                    if elemento1:
                        data[sistema].append({'Definición': elemento1, 'Fecha2': fecha1})
                    if elemento2:
                        data[sistema].append({'Definición': elemento2, 'Fecha2': fecha2})
            except (TimeoutException, WebDriverException) as e:
                logging.warning(f"Error al cargar la página {url}: {e}")
                continue
    finally:
        # Cerrar el navegador
        driver.quit()
        logging.info("Navegador cerrado.")

    # Crear DataFrames con los datos extraídos y eliminar los vacíos
    dataframes = {sistema: pd.DataFrame(info) for sistema, info in data.items() if info}

    # Agregar la columna 'Fecha' y actualizar 'Fecha2'
    for df in dataframes.values():
        df['Fecha'] = df['Fecha2'].apply(lambda x: x.split('-')[0].strip('()'))
        df['Fecha2'] = df['Fecha2'].apply(lambda x: x.split('-')[1].strip('()'))

        # Convertir las columnas 'Fecha' y 'Fecha2' a formato de fecha
        df['Fecha'] = pd.to_datetime(df['Fecha'], format='%d/%m/%Y')
        df['Fecha2'] = pd.to_datetime(df['Fecha2'], format='%d/%m/%Y')

        # Agregar la columna 'Norma' con el valor 'Pre publicación SBS'
        df['Norma'] = 'Pre publicación SBS'

    return dataframes

# Llamar a la función y mostrar los DataFrames
dataframes_sbs = scrape_sbs()

# Crear automáticamente los DataFrames fuera del diccionario
for sistema, df in dataframes_sbs.items():
    globals()[f"df_{sistema.replace(' ', '_')}"] = df

# Mostrar los DataFrames creados fuera del diccionario
for sistema in dataframes_sbs.keys():
    print(f"DataFrame fuera del diccionario para el sistema '{sistema}':")
    print(globals()[f"df_{sistema.replace(' ', '_')}"])

# Concatena dataframes hasta este momento
result_df = pd.concat(dataframes_sbs.values())
result_df = pd.concat([result_df, sbs,smv])
result_df = result_df.drop(columns=['Fecha2', 'Sistema', 'Tipo'])
result_df['Fecha'] = pd.to_datetime(result_df['Fecha'])
result_df['Fecha'] = result_df['Fecha'].dt.strftime('%Y-%m-%d %H:%M:%S')


"----------------------------- Filtra data de acuerdo a semana elegida --------------------"
import pandas as pd
from datetime import datetime

# Función para filtrar el DataFrame basado en las semanas especificadas y columnas seleccionadas
def filter_dataframe(df, start_week, end_week):
    # Convertir los inputs de semana al formato datetime
    start_of_week = datetime.strptime(start_week, '%Y-%m-%d')
    end_of_week = datetime.strptime(end_week, '%Y-%m-%d')
    
    # Convertir la columna Fecha al formato datetime manejando diferentes formatos
    df['Fecha'] = pd.to_datetime(df['Fecha'], errors='coerce', format='%Y-%m-%d %H:%M:%S').fillna(pd.to_datetime(df['Fecha'], errors='coerce', format='%d/%m/%Y'))
    
    # Filtrar las filas donde Fecha está dentro del rango especificado (incluyendo los extremos)
    df_filtered = df[(df['Fecha'] >= start_of_week) & (df['Fecha'] <= end_of_week)]
    
    # Seleccionar solo las columnas Definición, Fecha y Norma
    df_filtered = df_filtered[['Definición', 'Fecha', 'Norma']]
    
    return df_filtered


# Inputs    
from datetime import datetime
def validate_date(date_text):
    try:
        return datetime.strptime(date_text, '%Y-%m-%d')
    except ValueError:
        return None
def get_dates():
    while True:
        start_week = input("Semana de inicio (YYYY-MM-DD): ")
        end_week = input("Semana de fin (YYYY-MM-DD): ")
        
        if validate_date(start_week) and validate_date(end_week):
            return start_week, end_week
        else:
            print("Formato de fecha inválido. Por favor ingrese la fecha en el formato 'YYYY-MM-DD'.")
# Obtener las fechas
start_week, end_week = get_dates()
   
# Filtrar el DataFrame
radar_preliminar = filter_dataframe(result_df, start_week, end_week)    
    
    
"xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx TABLA PRELIMINAR SIN OSCE xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

import pandas as pd
from nltk.corpus import wordnet

# Lista de palabras clave
palabras = [
    "actuarial", "riesgo", "scoring", "liquidez", "credito", "valor razonable", "mercado", "IFRS", "niif",
    "gestión integral", "automatización", "financiero", "finanzas", "financiera", "instrumento", "derivado",
    "bono", "acciones", "estimación", "capacitación", "implementación", "dinámica", "contable", "modelo",
    "backtesting", "desarrollo", "seguimiento", "monitoreo", "precio", "contabilidad", "armonización", "inversión"
]

# Función para obtener sinónimos de una palabra
def obtener_sinonimos(palabra):
    sinonimos = set()
    for syn in wordnet.synsets(palabra, lang='spa'):
        for lemma in syn.lemmas(lang='spa'):
            sinonimos.add(lemma.name())
    return sinonimos

# Obtener sinónimos de todas las palabras clave
sinonimos_palabras = set(palabras)
for palabra in palabras:
    sinonimos_palabras.update(obtener_sinonimos(palabra))

# Función para determinar el valor de Scope FRM
def determinar_scope_frm(definicion):
    for palabra in sinonimos_palabras:
        if palabra in definicion.lower():
            return "Si"
    return "No"

# Función para agregar las nuevas columnas y solicitar entrada del usuario
def agregar_columnas(df):
    df['Scope FRM'] = df['Definición'].apply(determinar_scope_frm)
    df['Potencial Servicio'] = df.apply(lambda row: input(f"Definición: {row['Definición']}\nPotencial Servicio (Si/No/En revisión): "), axis=1)
    df['Responsable'] = df.apply(lambda row: input(f"Definición: {row['Definición']}\nResponsable: "), axis=1)
    return df

# Aplicar la función para agregar las columnas
radar_preliminar = agregar_columnas(radar_preliminar)
"xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
"""
OSCE - WEB SCRAPING
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

# Configuración del navegador para Microsoft Edge
driver = webdriver.Edge()  # Asegúrate de tener el driver de Edge instalado
driver.get("https://prod2.seace.gob.pe/seacebus-uiwd-pub/buscadorPublico/buscadorPublico.xhtml")

# Establecer una espera implícita
driver.implicitly_wait(15)

# Esperar a que el <div> especificado esté presente
tab_panel = WebDriverWait(driver, 60).until(
    EC.presence_of_element_located((By.ID, 'tbBuscador:tab1'))
)

# Función para hacer clic en un elemento con reintentos
def click_element(xpath, retries=3):
    for attempt in range(retries):
        try:
            element = WebDriverWait(tab_panel, 60).until(
                EC.element_to_be_clickable((By.XPATH, xpath))
            )
            driver.execute_script("arguments[0].click();", element)
            return True
        except Exception as e:
            print(f"Error al hacer clic en el elemento: {e}. Intento {attempt + 1} de {retries}")
    return False

# Hacer clic en el desplegable para abrir las opciones
click_element('//*[@id="tbBuscador:idFormBuscarProceso:j_idt47"]/div[3]/span')

# Esperar a que la opción "Servicio" esté presente y hacer clic en ella
click_element('//*[@id="tbBuscador:idFormBuscarProceso:j_idt47_panel"]/div/ul/li[text()="Servicio"]')

# Hacer clic en el botón especificado dentro del <div>
click_element('//*[@id="tbBuscador:idFormBuscarProceso:btnBuscarSelToken"]/span[2]')

# Crear listas para almacenar los datos
element_1_list = []
element_2_list = []
element_3_list = []

# Función para extraer datos de la tabla
def extract_data():
    for i in range(1, 16):
        try:
            element_1 = tab_panel.find_element(By.XPATH, f'//*[@id="tbBuscador:idFormBuscarProceso:dtProcesos_data"]/tr[{i}]/td[2]').text
            element_2 = tab_panel.find_element(By.XPATH, f'//*[@id="tbBuscador:idFormBuscarProceso:dtProcesos_data"]/tr[{i}]/td[7]').text
            element_3 = tab_panel.find_element(By.XPATH, f'//*[@id="tbBuscador:idFormBuscarProceso:dtProcesos_data"]/tr[{i}]/td[3]').text

            # Añadir los datos a las listas
            element_1_list.append(element_1)
            element_2_list.append(element_2)
            element_3_list.append(element_3)
        except Exception as e:
            print(f"Error al extraer datos de la fila {i}: {e}")
            continue

# Extraer datos de la primera página
extract_data()

# Hacer clic en el botón de paginación y extraer datos de las siguientes páginas hasta la página 34
current_page = 1
while current_page < 34:
    if click_element('//*[@id="tbBuscador:idFormBuscarProceso:dtProcesos_paginator_bottom"]/span[5]/span'):
        # Esperar a que la nueva tabla se cargue
        WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="tbBuscador:idFormBuscarProceso:dtProcesos_data"]/tr[1]/td[2]'))
        )
        # Extraer datos de la nueva página
        extract_data()
        current_page += 1
    else:
        print(f"Error en la paginación en la página {current_page}")
        break

# Crear un dataframe ordenado
data = {'Entidad': element_1_list, 'Descripción': element_2_list, 'Publicación': element_3_list}
osce = pd.DataFrame(data)

# Mostrar el dataframe
print(osce)

# Cerrar el navegador
driver.quit()

import pandas as pd

def rename_columns(df, new_names):
    if len(new_names) != 3:
        raise ValueError("La lista de nuevos nombres debe contener exactamente 3 elementos.")
    
    # Renombrar las tres primeras columnas
    df.columns = new_names + list(df.columns[3:])   
    return df

# Uso
new_names = ['Entidad', 'Definición', 'Fecha']
osce = rename_columns(osce, new_names)


"xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx TABLA PRELIMINAR CON OSCE xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
import pandas as pd
from nltk.corpus import wordnet

# Lista de palabras clave
palabras = [
    "actuarial", "riesgo", "scoring", "liquidez", "credito", "valor razonable", "mercado", "IFRS", "niif",
    "gestión integral", "automatización", "financiero", "finanzas", "financiera", "instrumento", "derivado",
    "bono", "acciones", "estimación", "capacitación", "implementación", "dinámica", "contable", "modelo",
    "backtesting", "desarrollo", "seguimiento", "monitoreo", "tasa de interés", "inversiones", "armonización", "inversión"
]

# Función para obtener sinónimos de una palabra
def obtener_sinonimos(palabra):
    sinonimos = set()
    for syn in wordnet.synsets(palabra, lang='spa'):
        for lemma in syn.lemmas(lang='spa'):
            sinonimos.add(lemma.name())
    return sinonimos

def determinar_scope_frm2(df):
    # Lista de palabras para el segundo filtro
    palabras_descarte0 = ["servicio de arrendamiento", "alimentos", "prensa", "vigilancia", "seguridad", "suministro", "metalico", 
                         "videoconferencia", "mantenimiento", "crianza", "bienes", "alojamiento", "agricola", "legal","acreditación",
                         "insumo", "parcela","construcción","esparcimiento","recreación","expediente","sala","espacio","contrataciones","comunicaciones"
                         ,"obra","uniforme","digital","maquinaria","infraestructura","tierra","material", "instalación","acondicionamiento","módulo","logístico"]
    palabras_descarte = set(palabras_descarte0)
    for palabra in palabras_descarte0:
        sinonimos_palabras.update(obtener_sinonimos(palabra))
        
    indices_a_eliminar = []
    for index, row in df.iterrows():
        definicion = row['Definición']
        cumple_condicion = any(palabra in definicion.lower() for palabra in palabras)
        contiene_palabra_descarte = any(palabra in definicion.lower() for palabra in palabras_descarte)
        
        # Eliminar la fila si no cumple la primera condición o si contiene alguna palabra de descarte
        if not cumple_condicion or contiene_palabra_descarte:
            indices_a_eliminar.append(index)
    
    df = df.drop(indices_a_eliminar)
    return df
# osce2 = determinar_scope_frm2(osce)
# Función para agregar las nuevas columnas y solicitar entrada del usuario
def agregar_columnas2(df):
    df = determinar_scope_frm2(df)
    df['Scope FRM'] = df['Definición'].apply(lambda definicion: "Si" if any(palabra in definicion.lower() for palabra in sinonimos_palabras) else "No")
    df['Potencial Servicio'] = df.apply(lambda row: input(f"Definición: {row['Definición']}\nPotencial Servicio (Si/No/En revisión): "), axis=1)
    df['Responsable'] = df.apply(lambda row: input(f"Definición: {row['Definición']}\nResponsable: "), axis=1)
    return df
osce = agregar_columnas2(osce)

"------------------------------- TABLA RESUMEN FINAL -------------------------------------"

import pandas as pd

# Crear el nuevo dataframe con las columnas especificadas
data = {
    "Estado": [
        "Normas Vigentes - SBS",
        "Normas Vigentes - SBS",
        "Normas Vigentes - SBS",
        "OSCE",
        "OSCE",
        "Resoluciones SMV",
        "Circulares BCRP",
        "Pre publicación SBS"
    ],
    "Tipo de Norma": [
        "Resolución SBS",
        "Circular SBS",
        "Oficio Múltiple SBS",
        "RF / OSCE",
        "Actuarial / OSCE",
        "Resolución SMV",
        "Circular BCRP",
        "Pre publicación"
    ],
    "Fecha de Revision": [end_week] * 8,  # Asegúrate de definir 'end_week' antes de usarlo
    "Cantidad": [0] * 8,  # Inicialmente en cero, se actualizará más adelante
    "Scope FRM": [None] * 8,
    "Potencial Servicio": [None] * 8,
    "Responsable": [None] * 8
}

radar_final = pd.DataFrame(data)

# Función para contar la cantidad de ocurrencias en radar_preliminar sin coincidencia exacta
def contar_ocurrencias(tipo_norma, radar_df):
    return radar_df['Norma'].str.contains(tipo_norma, case=False).sum()

# Actualizar la columna Cantidad en el nuevo dataframe
radar_final['Cantidad'] = radar_final['Tipo de Norma'].apply(lambda x: contar_ocurrencias(x, radar_preliminar))

# Función para contar las ocurrencias del valor 'Si' en las columnas especificadas
def contar_si(tipo_norma, radar_df, columna):
    return radar_df[radar_df['Norma'].str.contains(tipo_norma, case=False)][columna].eq('Si').sum()

# Actualizar las columnas 'Scope FRM', 'Potencial Servicio' y 'Responsable' en el nuevo dataframe
radar_final['Scope FRM'] = radar_final['Tipo de Norma'].apply(lambda x: contar_si(x, radar_preliminar, 'Scope FRM'))
radar_final['Potencial Servicio'] = radar_final['Tipo de Norma'].apply(lambda x: contar_si(x, radar_preliminar, 'Potencial Servicio'))

# Función para extraer valores de la columna 'Responsable' y separarlos por coma
def extraer_responsables(tipo_norma, radar_df):
    responsables = radar_df[radar_df['Norma'].str.contains(tipo_norma, case=False)]['Responsable']
    if responsables.notna().any():
        return ', '.join(responsables.dropna().unique())
    else:
        return ''

# Actualizar la columna 'Responsable' en el nuevo dataframe
radar_final['Responsable'] = radar_final['Tipo de Norma'].apply(lambda x: extraer_responsables(x, radar_preliminar))

"-<-<-<-<-<-<-<--<-<-<-<--< CREAR FIGURAS DE LAS TABLAS <-<-<-<-<-<-<-<-<-<-<-<-<-<-<-<-"

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.table import Table
from IPython.display import display, Image
import datetime

# Tus dataframes para convertir en figuras tipo tabla
dataframes = [radar_final]

# Función para ajustar el texto dentro de las celdas
def wrap_text(text, max_width):
    words = text.split()
    wrapped_text = ""
    line = ""
    for word in words:
        if len(line) + len(word) + 1 > max_width:
            wrapped_text += line + "\n"
            line = word
        else:
            if line:
                line += " "
            line += word
    wrapped_text += line
    return wrapped_text

# Función para convertir cada dataframe en una figura tipo tabla y guardarla
def save_dataframes_as_tables(dataframes):
    for i, df in enumerate(dataframes):
        if df.empty:
            print(f"El dataframe {i} está vacío y no se puede convertir en una tabla.")
            continue
        fig, ax = plt.subplots(figsize=(12, 6))  # Ajusta el tamaño de la figura
        ax.axis('tight')
        ax.axis('off')
        table = Table(ax, bbox=[0, 0, 1, 1])
        nrows, ncols = df.shape
        width_ratios = [1] * ncols
        height_ratios = [1] * nrows
        table.add_cell(0, -1, width=1, height=0.3, text="")  # Espacio para el encabezado
        for j, col in enumerate(df.columns):
            table.add_cell(0, j, width=1, height=0.3, text=col, loc='center', facecolor='lightgrey')
        for row in range(nrows):
            for col in range(ncols):
                text = str(df.iloc[row, col])
                wrapped_text = wrap_text(text, 20)  # Ajusta el ancho máximo de texto
                table.add_cell(row + 1, col, width=1, height=0.3, text=wrapped_text, loc='center')
        ax.add_table(table)
        
        # Generar nombre dinámico para la figura tipo tabla
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f'Radar_dataframe_{timestamp}_{i}.png'
        
        plt.savefig(filename, bbox_inches='tight')  # Guarda la figura con ajuste de bordes
        plt.close(fig)  # Cierra la figura para liberar memoria
        display(Image(filename))  # Muestra la imagen en el entorno de Jupyter Notebook

# Llamar a la función para guardar las figuras tipo tabla
save_dataframes_as_tables(dataframes)

# Otra lista de dataframes para guardar en archivo xlsx
Radar_Regulatorio = [radar_final, radar_preliminar,osce]

# Generar nombre dinámico para el archivo xlsx
timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
xlsx_filename = f'Radar_Regulatorio_{timestamp}.xlsx'

# Guardar los dataframes en un archivo xlsx
with pd.ExcelWriter(xlsx_filename) as writer:
    for i, df in enumerate(Radar_Regulatorio):
        df.to_excel(writer, sheet_name=f'DataFrame_{i}', index=False)

# import os
#print(os.getcwd())
"xxxxxxxxxxxxxxxxxxxxxxxxx ENVIAR CORREO AUTOMATICO xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    
# pip install pywin32
import glob
import os
import win32com.client as win32
from datetime import datetime, timedelta

def enviar_correo(destinatario, asunto, cuerpo):
    outlook = win32.Dispatch('outlook.application')
    correo = outlook.CreateItem(0)
    correo.To = destinatario
    correo.Subject = asunto
    correo.Body = cuerpo

    # Fecha límite para los archivos (especifica últimos minutos)
    fecha_limite_imagenes = datetime.now() - timedelta(minutes=3)
    fecha_limite_xlsx = datetime.now() - timedelta(minutes=3)

    # Buscar y adjuntar todos los archivos de imagen en el directorio actual
    for archivo in glob.glob(os.path.join(os.getcwd(), '*')):
        if archivo.endswith(('.png', '.jpg', '.jpeg', '.gif')):
            fecha_creacion = datetime.fromtimestamp(os.path.getctime(archivo))
            if fecha_creacion > fecha_limite_imagenes:
                correo.Attachments.Add(archivo)
        elif archivo.endswith('.xlsx'):
            fecha_creacion = datetime.fromtimestamp(os.path.getctime(archivo))
            if fecha_creacion > fecha_limite_xlsx:
                correo.Attachments.Add(archivo)

    # Enviar el correo
    correo.Send()

# Uso del código
num_filas_columna = osce['Potencial Servicio'].notna().sum()
destinatario = 'francoolivares@kpmg.com'
asunto = 'Radar Regulatorio - prueba piloto python'
if num_filas_columna > 0:
    cuerpo = f"""Buen día,

A continuación, se comparte el Radar Regulatorio actualizado desde el {start_week} al {end_week}. Se encontro {num_filas_columna} potenciales servicios hasta la fecha. .


Franco Olivares, 
Trainee | Advisory
Financial Risk Management"""

else:
    cuerpo = f"""Buen día,

A continuación, se comparte el Radar Regulatorio actualizado desde el {start_week} al {end_week}. No se encontró potencial servicio hasta la fecha.


Franco Olivares, 
Trainee | Advisory
Financial Risk Management"""

enviar_correo(destinatario, asunto, cuerpo)

"xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
"""
"-------------------- Find dataframe names from environment ---------------------"
# Función para obtener los nombres de todos los objetos en el entorno
def get_all_object_names():
    object_names = list(globals().keys())
    return object_names

# Imprimir los nombres de todos los objetos
print("Objetos en el entorno:")
for name in get_all_object_names():
    print(name)
"""
"XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
"""  
"-------------------------- FIltrar data de acuerdo a semana actual - tiempo real -----------------------"

import pandas as pd
from datetime import datetime, timedelta
# Función para filtrar el DataFrame basado en la semana actual y columnas seleccionadas
def filter_dataframe(df):
    # Obtener la fecha actual y calcular el inicio y fin de la semana
    current_date = datetime.now()
    start_of_week = datetime(current_date.year, current_date.month, current_date.day) - timedelta(days=current_date.weekday())
    start_of_week = start_of_week.replace(hour=0, minute=0, second=0, microsecond=0)
    end_of_week = start_of_week + timedelta(days=6)
    
    # Convertir la columna Fecha al formato datetime
    df['Fecha'] = pd.to_datetime(df['Fecha'])
    
    # Filtrar las filas donde Fecha está dentro de la semana actual (incluyendo los extremos)
    df_filtered = df[(df['Fecha'] >= start_of_week) & (df['Fecha'] <= end_of_week)]
    
    # Seleccionar solo las columnas Definición, Fecha y Sistema
    df_filtered = df_filtered[['Definición', 'Fecha', 'Norma']]    
    return df_filtered

# Aplicar la función para filtrar el DataFrame
filtered_df = filter_dataframe(result_df)
print(filtered_df)
"xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
"""




"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import logging
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException

# Configuración del registro
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def setup_driver():
    driver = webdriver.Edge()
    driver.get("https://prod2.seace.gob.pe/seacebus-uiwd-pub/buscadorPublico/buscadorPublico.xhtml")
    return driver

def wait_for_element(driver, by, value, timeout=10):
    for _ in range(3):  # Intentar 3 veces
        try:
            return WebDriverWait(driver, timeout).until(EC.presence_of_element_located((by, value)))
        except (StaleElementReferenceException, TimeoutException) as e:
            logging.warning(f"Reintentando debido a: {e}")
            continue
    raise Exception("Elemento no encontrado después de varios intentos")

def click_element(driver, by, value, timeout=10):
    for _ in range(3):  # Intentar 3 veces
        try:
            element = WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((by, value)))
            element.click()
            return
        except (StaleElementReferenceException, TimeoutException) as e:
            logging.warning(f"Reintentando debido a: {e}")
            continue
    raise Exception("Elemento no se pudo hacer clic después de varios intentos")

def extract_data(driver, tab_panel, element_1_list, element_2_list, element_3_list):
    for i in range(1, 16):
        try:
            element_1 = wait_for_element(driver, By.XPATH, f'//*[@id="tbBuscador:idFormBuscarProceso:dtProcesos_data"]/tr[{i}]/td[2]').text
            element_2 = wait_for_element(driver, By.XPATH, f'//*[@id="tbBuscador:idFormBuscarProceso:dtProcesos_data"]/tr[{i}]/td[7]').text
            element_3 = wait_for_element(driver, By.XPATH, f'//*[@id="tbBuscador:idFormBuscarProceso:dtProcesos_data"]/tr[{i}]/td[3]').text

            element_1_list.append(element_1)
            element_2_list.append(element_2)
            element_3_list.append(element_3)
        except Exception as e:
            logging.error(f"Error extracting data: {e}")
            continue

# Uso de las funciones
driver = setup_driver()
tab_panel = wait_for_element(driver, By.ID, 'tbBuscador:tab1')
click_element(driver, By.XPATH, '//*[@id="tbBuscador:idFormBuscarProceso:j_idt47"]/div[3]/span')
click_element(driver, By.XPATH, '//*[@id="tbBuscador:idFormBuscarProceso:j_idt47_panel"]/div/ul/li[text()="Servicio"]')
click_element(driver, By.XPATH, '//*[@id="tbBuscador:idFormBuscarProceso:btnBuscarSelToken"]/span[2]')

element_1_list = []
element_2_list = []
element_3_list = []

extract_data(driver, tab_panel, element_1_list, element_2_list, element_3_list)

# Paginación
current_page = 1
while current_page < 34:
    try:
        click_element(driver, By.XPATH, '//*[@id="tbBuscador:idFormBuscarProceso:dtProcesos_paginator_bottom"]/span[5]/span')
        wait_for_element(driver, By.XPATH, '//*[@id="tbBuscador:idFormBuscarProceso:dtProcesos_data"]/tr[1]/td[2]')
        extract_data(driver, tab_panel, element_1_list, element_2_list, element_3_list)
        current_page += 1
    except Exception as e:
        logging.error(f"Error during pagination: {e}")
        break

data = {'Entidad': element_1_list, 'Descripción': element_2_list, 'Publicación': element_3_list}
osce = pd.DataFrame(data)
print(osce)
driver.quit()

""" 