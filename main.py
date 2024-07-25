from fastapi import FastAPI
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
from bs4 import BeautifulSoup

app = FastAPI()

@app.get("/")
def read_powerbi_data():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    service = Service('/path/to/chromedriver')  # Substitua pelo caminho do seu chromedriver

    driver = webdriver.Chrome(service=service, options=chrome_options)
    url = "https://app.powerbi.com/view?r=eyJrIjoiMDJmYTk1NTAtNGNjNi00MDM1LWFhMTgtNjBjNGM2M2VmMTgyIiwidCI6IjlkYmE0ODBjLTRmYTctNDJmNC1iYmEzLTBmYjEzNzVmYmU1ZiJ9"
    driver.get(url)
    time.sleep(15)

    page_source = driver.page_source
    driver.quit()

    soup = BeautifulSoup(page_source, 'html.parser')
    tables = soup.find_all('table')

    data = []
    for table in tables:
        table_data = []
        for row in table.find_all('tr'):
            columns = row.find_all('td')
            row_data = [col.get_text(strip=True) for col in columns]
            table_data.append(row_data)
        data.append(table_data)

    return {"data": data}
