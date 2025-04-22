from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import datetime
import re
from app.db import get_db
from app.services.save_utils import save_event_and_session
from sqlalchemy.orm import Session as SQLAlchemySession

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
    # Настройки и запуск Selenium
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")
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

    # Извлекаем сессию из генератора
    db = next(get_db())  # Получаем сессию из генератора

    # ПРОХОДИМСЯ ПО ВСЕМ ССЫЛКАМ
    for link in event_links:
        print(f"Открываем: {link}")
        driver.get(link)
        time.sleep(2)

        try:
            try:
                title = driver.find_element(By.XPATH, '//div[contains(@class, "_ontentDetails_title")]/h1').text
                print(f"Найдено название: {title}")
            except NoSuchElementException:
                title = ""
                print("Название не найдено")
            
            if not title:
                continue  # Пропускаем событие, если нет названия

            try:
                genre = driver.find_element(By.XPATH, '//li[h5[text()="Жанр"]]//span').text
                print(f"Найден жанр: {genre}")
            except NoSuchElementException:
                genre = ""
                print("Жанр не найден")

            try:
                age_rating = driver.find_element(By.XPATH, '//li[h5[text()="Возрастное ограничение"]]//span').text
                print(f"Найдено возрастное ограничение: {age_rating}")
            except NoSuchElementException:
                age_rating = ""
                print("Возрастное ограничение не найдено")

            try:
                duration = driver.find_element(By.XPATH, '//li[h5[text()="Продолжительность"]]//span').text
                print(f"Найдена продолжительность: {duration}")
            except NoSuchElementException:
                duration = ""
                print("Продолжительность не найдена")

            try:
                description = driver.find_element(By.XPATH, '//div[h5[text()="Описание"]]//div[@class="Description_descriptionText__574Xi"]//p').text
                print(f"Найдено описание: {description}")
            except NoSuchElementException:
                description = ""
                print("Описание не найдено")

            url = link
            type_event = 'Кино'
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
                    print(f"Найдена дата: {date}")
                except NoSuchElementException:
                    date = ""
                    print("Дата не найдена")

                try:
                    # Адрес
                    venue_address = row.find_element(By.XPATH, './/div[contains(@class, "CinemaInfo_address__")]').text
                    print(f"Найден адрес сеанса: {venue_address}")
                except NoSuchElementException:
                    venue_address = ""
                    print("Адрес сеанса не найден")

                # Список билетов с временем и ценой
                ticket_wrappers = row.find_elements(By.XPATH, './/div[contains(@class, "TicketsList_ticketWrapper__")]')

                for wrapper in ticket_wrappers:
                    try:
                        time_ = wrapper.find_element(By.XPATH, './/span[contains(@class, "TicketButton_text__")]').text
                        print(f"Найдено время сеанса: {time_}")
                    except NoSuchElementException:
                        time_ = ""
                        print("Время сеанса не найдено")

                    try:
                        # Ищем ВСЕ div с классом TicketsList_info__, берём второй
                        price_elements = wrapper.find_elements(By.XPATH, './/div[contains(@class, "TicketsList_info__")]')
                        price = price_elements[1].text if len(price_elements) > 1 else ""
                        if price:
                            price = re.sub(r'[^\d]', '', price)
                            print(f"Найдена цена: {price}")
                    except NoSuchElementException:
                        price = ""
                        print("Цена не найдена")

                    if date or time_ or price:
                        # Сохраняем каждый сеанс в базе данных
                        save_event_and_session(db, title, genre, age_rating, duration, description, url, type_event, poster_url, date, venue_address, time_, price)

            print(f"СОБЫТИЕ: {title}")
            print(f"ЖАНР: {genre}")
            print(f"ВОЗРАСТНОЕ ОГРАНИЧЕНИЕ: {age_rating}")
            print(f"ПРОДОЛЖИТЕЛЬНОСТЬ: {duration}")
            print(f"ОПИСАНИЕ: {description}")
            print(f"МЕСТО ПРОВЕДЕНИЯ: {venue_address}")
            print(f"СЕАНСЫ: {sessions}")
            print(f"URL: {poster_url}")
            print("===")

        except Exception as e:
            print(f"Ошибка при обработке {link}: {e}")

        driver.back()
        time.sleep(2)

    driver.quit()


"""
from app.services import parsing_cinema, parsing_concerts, parsing_theatres

if __name__ == "__main__":
    print("🔽 Парсинг кино...")
    parsing_cinema.parse_events()

    print("🔽 Парсинг концертов...")
    parsing_concerts.parse_events()

    print("🔽 Парсинг театров...")
    parsing_theatres.parse_events()

    print("✅ Парсинг завершён.")
"""