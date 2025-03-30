# -*- coding: utf-8 -*-
"""
SEMANA ECONOMICA
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

# Inicializar el WebDriver (usando Firefox en este ejemplo)
driver = webdriver.Firefox()

# Función para extraer datos de una sola página
def extract_data_from_page():
    data = []
    for i in range(2, 9):
        # Generar XPaths dinámicamente basados en la iteración
        element1_xpath = f'//*[@id="sectores"]/div[2]/div[1]/div/div[1]/div[{i}]/div[2]/div[1]/a/h2'
        element2_xpath = f'//*[@id="sectores"]/div[2]/div[1]/div/div[1]/div[{i}]/div[2]/div[1]/div[2]'
        element3_xpath = f'//*[@id="sectores"]/div[2]/div[1]/div/div[1]/div[{i}]/div[1]/p/span'
        
        # Extraer elementos usando los XPaths generados
        try:
            element1 = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, element1_xpath))).text
        except:
            element1 = ""
        
        try:
            element2 = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, element2_xpath))).text
        except:
            element2 = ""
        
        try:
            element3 = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, element3_xpath))).text
        except:
            element3 = ""
        
        # Añadir los elementos extraídos a la lista de datos
        data.append({
            'Noticia': element1,
            'Descripción': element2,
            'Fecha': element3
        })
    
    return data

# Función para extraer datos de múltiples páginas
def extract_data_from_multiple_pages(base_url):
    all_data = []
    
    driver.get(base_url)
    
    # Extraer datos de la primera página
    page_data = extract_data_from_page()
    all_data.extend(page_data)
    
    # Lista de XPaths para los enlaces de las siguientes páginas
    next_page_links = [
        '//*[@id="sectores"]/div[2]/div[2]/ul/li[3]/span',
        '//*[@id="sectores"]/div[2]/div[2]/ul/li[4]/a',
        '//*[@id="sectores"]/div[2]/div[2]/ul/li[5]/a'
    ]
    
    # Iterar sobre los enlaces de las siguientes páginas y extraer datos de cada página
    for link in next_page_links:
        try:
            next_page_link = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, link)))
            next_page_link.click()
            
            # Esperar a que la página se cargue completamente
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="sectores"]/div[2]/div[1]/div/div[1]/div[2]/div[2]/div[1]/a/h2')))
            
            # Extraer datos de la siguiente página después de hacer clic en el enlace
            page_data = extract_data_from_page()
            all_data.extend(page_data)
            
        except:
            break
    
    return all_data

# URL base del sitio web
base_url = "https://www.semanaeconomica.pe/economia-finanzas/"
# Extraer datos de múltiples páginas
data = extract_data_from_multiple_pages(base_url)
# Crear un DataFrame a partir de los datos extraídos
economica = pd.DataFrame(data)
# Cerrar el WebDriver
driver.quit()

"""
DIARIO GESTIÓN
"""
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By

# Inicializar el driver para Firefox
driver = webdriver.Firefox()

# Navegar a la URL especificada
driver.get("https://gestion.pe/archivo/economia/")

# Crear listas para almacenar los textos
texts_group1 = []
texts_group2 = []

# Iterar sobre los números del 1 al 30 para ambos grupos de XPaths
for i in range(1, 4):
    xpath_group1 = f'//*[@id="fusion-app"]/div/div[37]/div[2]/div[4]/div/div[1]/div[{i}]/div/div/div[2]/h2/a'
    xpath_group2 = f'//*[@id="fusion-app"]/div/div[37]/div[2]/div[4]/div/div[1]/div[{i}]/div/div/div[1]/p/span[1]'
    
    elements_group1 = driver.find_elements(By.XPATH, xpath_group1)
    elements_group2 = driver.find_elements(By.XPATH, xpath_group2)
    
    for element in elements_group1:
        texts_group1.append(element.text)
    
    for element in elements_group2:
        texts_group2.append(element.text)

# Crear el DataFrame
gestion = pd.DataFrame({
    'Group1': texts_group1,
    'Group2': texts_group2
})

# Cerrar el driver
driver.quit()



"""
NOTAS DE PRENSA SBS
"""
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By

# Inicializar el driver para Firefox
driver = webdriver.Firefox()

# Abrir la página web
driver.get("https://www.sbs.gob.pe/notadeprensa")

# Extraer los elementos
element1 = driver.find_element(By.XPATH, '//*[@id="mvcContainer-27014"]/section/ul/li[1]/article/div/header/h3/a').text
element2 = driver.find_element(By.XPATH, '//*[@id="mvcContainer-27014"]/section/ul/li[2]/article/div/div[2]/p[1]').text
element3 = driver.find_element(By.XPATH, '//*[@id="mvcContainer-27014"]/section/ul/li[2]/article/div/header/div').text

# Crear un DataFrame con los elementos extraídos
data = {
    'Elemento 1': [element1],
    'Elemento 2': [element2],
    'Elemento 3': [element3]
}
notas_sbs = pd.DataFrame(data)

# Guardar el DataFrame en un archivo CSV
#df.to_csv('elementos_extraidos.csv', index=False)

# Cerrar el driver
driver.quit()


"""
GANAMAS
"""



"""
 EL PERUANO NEWS
"""