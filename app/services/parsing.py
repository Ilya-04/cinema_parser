from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from time import sleep

chrome_driver_path = r'E:\КарТУ\3 курс\6 семестр\Промышленное программирование\Практика\cinema_parser\chromedriver.exe'

options = Options()
options.headless = True  # Работать без графического интерфейса

service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service, options=options)

driver.get('https://ticketon.kz/karaganda/event/tuapshrp-2025?item_list_name=%D0%A1%D0%BE%D0%B1%D1%8B%D1%82%D0%B8%D1%8F&item_list_id=allEvents&index=1')

sleep(2)

# Скопированный XPath
event_xpath = '//*[@id="__next"]/div/main/section[2]/div/div/div[2]/div[3]/div/div/ul[2]/li[1]/p/span'  # Вставь свой XPath сюда

# Найдём все события
events = driver.find_elements(By.XPATH, event_xpath)

# Выводим найденные события
for event in events:
    title = event.text
    print(f'Парсинг события: {title}')

driver.quit()
