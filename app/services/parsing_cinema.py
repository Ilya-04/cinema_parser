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

    driver.get("https://ticketon.kz/karaganda/cinema")

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
    links_elements = driver.find_elements(By.CSS_SELECTOR, "a.DetailedCardWrapper_eventItem__ZS8dA")
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
                        
            url = link  # предполагаем, что картинка будет по той же ссылке

            # XPATH ДЛЯ ПОЛУЧЕНИЯ ССЫЛКИ НА ПОСТЕР
            poster_url = driver.find_element(By.XPATH, '//div[contains(@class, "_ontentDetails_poster")]/descendant::img').get_attribute("src")


            # ПАРСИНГ СЕАНСОВ
            session_rows = driver.find_elements(By.XPATH, '//div[contains(@class, "ScheduleRow_scheduleRow__o3xf2")]')
            sessions = []

            for row in session_rows:
                try:
                    # Дата
                    day = row.find_element(By.XPATH, './/div[contains(@class, "Date_day__")]').text
                    month_text = row.find_element(By.XPATH, './/div[contains(@class, "Date_dateText__")]/div[1]').text.lower()
                    month_number = MONTHS_RU.get(month_text, "01")
                    year = datetime.datetime.now().year
                    date = f"{year}-{month_number}-{int(day):02d}"
                except NoSuchElementException:
                    date = ""

                try:
                    # Адрес
                    venue_address = row.find_element(By.XPATH, './/div[contains(@class, "CinemaInfo_address__")]').text
                except NoSuchElementException:
                    venue_address = ""

                # Список билетов с временем и ценой
                ticket_wrappers = row.find_elements(By.XPATH, './/div[contains(@class, "TicketsList_ticketWrapper__")]')

                for wrapper in ticket_wrappers:
                    try:
                        time_ = wrapper.find_element(By.XPATH, './/span[contains(@class, "TicketButton_text__")]').text
                    except NoSuchElementException:
                        time_ = ""

                    try:
                        # Ищем ВСЕ div с классом TicketsList_info__, берём второй
                        price_elements = wrapper.find_elements(By.XPATH, './/div[contains(@class, "TicketsList_info__")]')
                        price = price_elements[1].text if len(price_elements) > 1 else ""
                        if price:
                            price = re.sub(r'[^\d]', '', price)
                    except NoSuchElementException:
                        price = ""

                    if date or time_ or price:
                        sessions.append({
                            'date': date,
                            'time': time_,
                            'price': price,
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
