from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support import expected_conditions as EC
import time

# Declare as variáveis de credenciais e URLs
username = "57451919000119"
password = "EcoWatt!24"
url = "https://www.copel.com/avaweb/paginaLogin/login.jsf"


def coletar_relatorio():
    driver = None  # Inicializa driver como None
    try:
        # Caminho para o geckodriver
        service = Service("geckodriver.exe")

        # Crie um objeto de opções do Firefox
        options = webdriver.FirefoxOptions()

        # Opcional: para usar o modo headless (navegador invisível)
        # options.add_argument("--headless")

        # As linhas abaixo foram removidas para não forçar o modo "limpo"
        # options.set_preference("browser.cache.disk.enable", False)
        # options.set_preference("browser.cache.memory.enable", False)
        # options.set_preference("browser.cache.offline.enable", False)
        # options.set_preference("network.http.use-cache", False)

        # Especifique o caminho do executável do Firefox
        options.binary_location = r"C:\Program Files\Mozilla Firefox\firefox.exe"

        # Inicie o driver com o objeto Service e as opções
        driver = webdriver.Firefox(service=service, options=options)
        driver.get(url)

        wait = WebDriverWait(driver, 180)
        wait.until(EC.presence_of_element_located((By.ID, "formulario:numDoc"))).send_keys(username)
        wait.until(EC.presence_of_element_located((By.ID, "formulario:pass"))).send_keys(password)

        wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "ui-button ui-widget ui-state-default ui-corner-all ui-button-text-only btn btn-lg btn-Login btn-block mt-2"))).click()

        # Espera pela página pós-login.
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".ui-fluid .ui-inputtext")))
        time.sleep(2)

        driver.find_elements(By.CSS_SELECTOR, ".ui-fluid .ui-inputtext")[0].send_keys('88532062')
        time.sleep(5)

        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".ui-widget-content a")))
        time.sleep(2)

        driver.find_element(By.CSS_SELECTOR, ".ui-widget-content a").click()

        time.sleep(10000)

    except Exception as e:
        print(f"Ocorreu um erro: {e}")
    finally:
        if driver:
            driver.quit()  # Garante que o navegador é fechado


coletar_relatorio()