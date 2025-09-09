from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
import os
import glob
import time
from pathlib import Path

# Declaracao variaveis credenciais e urls
username = "57451919000119"
password = "EcoWatt!24"
url = "https://www.copel.com/avaweb/paginaLogin/login.jsf"


def get_latest_pdf_from_downloads():
    """
    Retorna o caminho completo do arquivo PDF mais recente na pasta de downloads do usuário.
    """
    # 1. Obter o caminho da pasta de downloads
    try:
        downloads_path = str(Path.home() / "Downloads")
    except Exception as e:
        print(f"Não foi possível encontrar a pasta de downloads. Erro: {e}")
        return None

    # 2. Encontrar todos os arquivos .pdf
    list_of_pdfs = glob.glob(os.path.join(downloads_path, "*.pdf"))

    # 3. Encontrar o arquivo mais recente com base na data de modificação
    if not list_of_pdfs:
        print("Nenhum arquivo PDF encontrado na pasta de downloads.")
        return None

    # O `max` com `os.path.getmtime` compara a data de modificação de cada arquivo
    # e retorna o caminho do arquivo mais recente.
    latest_pdf = max(list_of_pdfs, key=os.path.getmtime)

    return latest_pdf


def download_2via_fatura():
    # Inicializando o driver do Chrome
    # Caminho para o chromedriver
    service = Service("chromedriver-win64/chromedriver-win64/chromedriver.exe")

    # Iniciando o driver com o objeto Service
    driver = webdriver.Chrome(service=service)
    # Maximiza a janela do navegador
    driver.maximize_window()
    driver.get(url)

    # Espera explícita até que o campo de user esteja presente
    wait = WebDriverWait(driver, 180)
    wait.until(EC.presence_of_element_located((By.ID, "formulario:numDoc")))
    # Inserindo CNPJ no campo de login
    driver.find_element(By.ID, "formulario:numDoc").send_keys(username)

    campo_senha = wait.until(EC.presence_of_element_located((By.ID, "formulario:pass")))
    campo_senha.send_keys(password)
    campo_senha.send_keys(Keys.RETURN)  # Simula o Enter

    # Agora espera até que a URL mude para a página certa
    wait.until(EC.url_contains("listarUcsDoc.jsf"))



    # Espera explícita até que a barra de Pesquisa esteja presente
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".ui-fluid .ui-inputtext")))
    time.sleep(2)
    # Insira o número na barra de pesquisa
    driver.find_elements(By.CSS_SELECTOR, ".ui-fluid .ui-inputtext")[0].send_keys('88532062')

    #.ui-widget-content a
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".ui-datatable table tbody tr td")))
    time.sleep(2)
    # Encontre o elemento pelo título
    elemento = driver.find_element(By.CSS_SELECTOR, "a[title='Selecionar']")
    # Clique no elemento
    elemento.click()
    time.sleep(3)

    # Acessando Página da Segunda Via da Fatura
    driver.get('https://www.copel.com/avaweb/paginas/segundaViaFatura.jsf')
    time.sleep(3)
    # Clicando no Botão de 2 VIA que abre o form de Download
    elemento = driver.find_element(By.ID, "formSegundaViaFatura:dtListaSegundaViaFaturaDebitoPendente:1:j_idt72")
    elemento.click()
    time.sleep(3)

    # Fazendo o download da Fatura
    elemento = driver.find_element(By.ID, "frmModalSegundaVia:j_idt149")
    elemento.click()
    time.sleep(10)
    driver.close()


def processar_dados_fatura():
    # Inicializando o driver do Chrome
    # Caminho para o chromedriver
    service = Service("chromedriver-win64/chromedriver-win64/chromedriver.exe")

    # Iniciando o driver com o objeto Service
    driver = webdriver.Chrome(service=service)
    # Maximiza a janela do navegador
    driver.maximize_window()
    driver.get('https://desenv.smartdatabi.com.br/ecowatt/login')
    time.sleep(3)

    # Espera explícita até que o campo de user esteja presente
    wait = WebDriverWait(driver, 180)
    wait.until(EC.presence_of_element_located((By.NAME, "email")))
    # Inserindo CNPJ no campo de login
    driver.find_element(By.NAME, "email").send_keys('geovani@dev.com')

    # Espera explícita até que o campo de senha esteja presente
    wait.until(EC.presence_of_element_located((By.ID, "password")))
    # Inserindo senha
    driver.find_element(By.ID, "password").send_keys('master100')

    # Espera explícita até que o botão de ENTRAR esteja presente
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".login100-form-btn")))
    time.sleep(2)
    # Apertando no botão de Entrar
    driver.find_element(By.CSS_SELECTOR, ".login100-form-btn").click()
    time.sleep(3)

    # Acessando página de processamento das faturas de Usina
    driver.get('https://desenv.smartdatabi.com.br/ecowatt/fatura/faturausina/importarfatura/')
    # Espera explícita até que o botão de enviar arquivo esteja presente
    wait.until(EC.presence_of_element_located((By.ID, "import_usina_fatura")))
    driver.find_element(By.ID, "import_usina_fatura").send_keys(get_latest_pdf_from_downloads())
    time.sleep(2)

    # Enviando arquivo PDF
    wait.until(EC.presence_of_element_located((By.ID, "btnSalvar")))
    driver.find_element(By.ID, "btnSalvar").click()
    time.sleep(10)
    driver.close()


# Primeiro, baixe a fatura do site da Copel
download_2via_fatura()

# Espere um pouco para garantir que o download foi concluído
time.sleep(5) 

# Depois, processe a fatura que acabou de ser baixada
processar_dados_fatura()
