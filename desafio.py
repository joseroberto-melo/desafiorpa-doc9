import os
import logging
import pandas as pd
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests

# Configuração de log
logging.basicConfig(
    filename="script_log.log", 
    level=logging.INFO, 
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def setup_driver():
    options = webdriver.ChromeOptions()
    options.add_experimental_option("prefs", {
        "download.default_directory": os.path.abspath("faturas"),
        "plugins.always_open_pdf_externally": True
    })
    logging.info("WebDriver configurado com diretório de download em 'faturas'.")
    return webdriver.Chrome(options=options)

def download_file(url, folder, file_name):
    try:
        response = requests.get(url, stream=True)
        content_type = response.headers.get('Content-Type', '')
        extension = content_type.split('/')[-1]
        if response.status_code == 200 and extension in ["pdf", "jpeg"]:
            file_path = os.path.join(folder, f"{file_name}.{extension}")
            with open(file_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=1024):
                    f.write(chunk)
            logging.info(f"Arquivo baixado com sucesso: {file_path}")
            return file_path
        else:
            logging.error(f"Tipo de conteúdo não suportado ou erro HTTP: {response.status_code}, {content_type}")
    except Exception as e:
        logging.error(f"Erro ao baixar {url}: {e}")
    return None

def main():
    logging.info("Iniciando o processo de extração de dados.")
    driver, data = setup_driver(), []
    driver.get("https://rpachallengeocr.azurewebsites.net")
    logging.info("Acessando o site: https://rpachallengeocr.azurewebsites.net")
    os.makedirs("faturas", exist_ok=True)
    logging.info("Pasta 'faturas' criada com sucesso.")

    try:
        rows = WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.XPATH, "//*[@id='tableSandbox']/tbody/tr"))
        )
        logging.info(f"Tabela carregada com {len(rows)} linhas encontradas.")

        for i, row in enumerate(rows, 1):
            logging.info(f"Processando linha {i}...")
            try:
                cols = row.find_elements(By.TAG_NAME, "td")
                id, venc, link = cols[1].text.strip(), cols[2].text.strip(), cols[3].find_element(By.TAG_NAME, "a").get_attribute("href")
                venc_dt = datetime.strptime(venc, "%d-%m-%Y")

                status = "Ignorado (Vencimento Futuro)" if venc_dt > datetime.now() else "Falha"
                if venc_dt <= datetime.now():
                    logging.info(f"Tentando baixar fatura: ID={id}, Vencimento={venc}, URL={link}")
                    status = "Sucesso" if download_file(link, "faturas", id) else "Falha"

                data.append({
                    "Número da Fatura": id,
                    "Data de Vencimento": venc,
                    "URL da Fatura": link,
                    "Status do Download": status
                })
                logging.info(f"Linha {i} processada: ID={id}, Status={status}")

            except Exception as e:
                logging.error(f"Erro na linha {i}: {e}")

        pd.DataFrame(data).to_csv("resultado.csv", index=False)
        logging.info("Arquivo CSV gerado com sucesso: resultado.csv")

    except Exception as e:
        logging.error(f"Erro geral durante execução: {e}")
    finally:
        logging.info("Encerrando o WebDriver.")
        driver.quit()

if __name__ == "__main__":
    main()
