from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import datetime
import re

MONTHS_RU = {
    "января": "01",
    "февраля": "02",
    "марта": "03",
    "апреля": "04",
    "мая": "05",
    "июня": "06",
    "июля": "07",
    "августа": "08",
    "сентября": "09",
    "октября": "10",
    "ноября": "11",
    "декабря": "12"
}

def parse_events():
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")  # УБРАТЬ КОММЕНТАРИЙ, ЕСЛИ ХОЧЕШЬ СКРЫТЫЙ РЕЖИМ
    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 10)

    driver.get("https://ticketon.kz/karaganda/concerts")

    # НАЖИМАЕМ "ПОКАЗАТЬ ЕЩЁ", ПОКА КНОПКА ЕСТЬ
    while True:
        try:
            show_more_button = wait.until(EC.element_to_be_clickable(
                (By.XPATH, '//button[.//span[text()[contains(., "Показать ещё")]]]')))
            driver.execute_script("arguments[0].scrollIntoView(true);", show_more_button)
            time.sleep(1)  # ДАЁМ ВРЕМЯ НА ПРОКРУТКУ
            show_more_button.click()
            time.sleep(2)
        except TimeoutException:
            break

    # ИЩЕМ ВСЕ ССЫЛКИ НА КАРТОЧКИ
    links_elements = driver.find_elements(
            By.CSS_SELECTOR,
            ".DetailedList_contentContainer__CXnpM a.DetailedCardWrapper_eventItem__ZS8dA"
        )
    event_links = [link.get_attribute("href") for link in links_elements]

    # ЕСЛИ ССЫЛКА ОТНОСИТЕЛЬНАЯ — ДОБАВЛЯЕМ ДОМЕН
    event_links = [
        link if link.startswith("http") else f"https://ticketon.kz{link}"
        for link in event_links
    ]

    # ПРОХОДИМСЯ ПО ВСЕМ ССЫЛКАМ
    for link in event_links:
        print(f"Открываем: {link}")
        driver.get(link)
        time.sleep(2)

        try:
            # НАЗВАНИЕ СОБЫТИЯ
            try:
                title = driver.find_element(By.XPATH, '//div[contains(@class, "_ontentDetails_title")]/h1').text
            except NoSuchElementException:
                title = ""
            
            # Если название пустое, пропускаем эту страницу
            if not title:
                print(f"Отсутствует название для {link}, пропускаем парсинг этой страницы.")
                continue
            
            # ЖАНР
            try:
                genre = driver.find_element(By.XPATH, '//li[h5[text()="Жанр"]]//span').text
            except NoSuchElementException:
                genre = ""
            
            # ВОЗРАСТНОЕ ОГРАНИЧЕНИЕ
            try:
                age_rating = driver.find_element(By.XPATH, '//li[h5[text()="Возрастное ограничение"]]//span').text
            except NoSuchElementException:
                age_rating = ""
            
            # ПРОДОЛЖИТЕЛЬНОСТЬ
            try:
                duration = driver.find_element(By.XPATH, '//li[h5[text()="Продолжительность"]]//span').text
            except NoSuchElementException:
                duration = ""
            
            # ОПИСАНИЕ
            try:
                description = driver.find_element(By.XPATH, '//div[h5[text()="Описание"]]//div[@class="Description_descriptionText__574Xi"]//p').text
            except NoSuchElementException:
                description = ""
            
            # МЕСТО ПРОВЕДЕНИЯ
            try:
                venue_address = driver.find_element(By.XPATH, '//li[h5[text()="Место проведения"]]//span').text
            except NoSuchElementException:
                venue_address = ""
            
            url = link  # предполагаем, что картинка будет по той же ссылке

            # XPATH ДЛЯ ПОЛУЧЕНИЯ ССЫЛКИ НА ПОСТЕР
            poster_url = driver.find_element(By.XPATH, '//div[contains(@class, "_ontentDetails_poster")]/descendant::img').get_attribute("src")

            # ПАРСИНГ СЕАНСОВ
            session_elements = driver.find_elements(By.XPATH, '//li[contains(@class, "EventRow_scheduleItem__Ww9vv")]')
            sessions = []

            for session in session_elements:
                try:
                    # День
                    day = session.find_element(
                        By.XPATH,
                        './/div[contains(@class, "Date_dateWrapper__Bbx2I")]//div[contains(@class, "Date_day__")]'
                    ).text

                    # Месяц
                    month_text = session.find_element(
                        By.XPATH,
                        './/div[contains(@class, "Date_dateWrapper__Bbx2I")]//div[contains(@class, "Date_dateText__")]//div[1]'
                    ).text.lower()

                    # Преобразуем в YYYY-MM-DD
                    month_number = MONTHS_RU.get(month_text, "01")
                    year = datetime.datetime.now().year
                    date = f"{year}-{month_number}-{int(day):02d}"

                except NoSuchElementException:
                    date = ""

                try:
                    time_ = session.find_element(
                        By.XPATH,
                        './/button[contains(@class, "TicketButton_button__GyFwq")]//span[contains(@class, "TicketButton_text__HwCFn")]'
                    ).text
                except NoSuchElementException:
                    time_ = ""

                try:
                    price = session.find_element(
                        By.XPATH,
                        './/div[contains(@class, "PriceColumn_priceColumn__842sT")]//div'
                    ).text
                    if price:
                        price = re.sub(r'[^\d]', '', price)
                except NoSuchElementException:
                    price = ""

                if date or time_ or price:
                    sessions.append({
                        'date': date,
                        'time': time_,
                        'price': price
                    })

            print("СОБЫТИЕ:", title)
            print("ЖАНР:", genre)
            print("ВОЗРАСТНОЕ ОГРАНИЧЕНИЕ:", age_rating)
            print("ПРОДОЛЖИТЕЛЬНОСТЬ:", duration)
            print("ОПИСАНИЕ:", description)
            print("МЕСТО ПРОВЕДЕНИЯ:", venue_address)
            print("СЕАНСЫ:", sessions)
            print("URL:", poster_url)
            print("===")

        except Exception as e:
            print(f"Ошибка при обработке {link}: {e}")

        driver.back()
        time.sleep(2)

    driver.quit()
