from app.services import parsing_cinema, parsing_concerts, parsing_theatres

if __name__ == "__main__":
    print("🔽 Парсинг кино...")
    parsing_cinema.parse_events()

    print("🔽 Парсинг концертов...")
    parsing_concerts.parse_events()

    print("🔽 Парсинг театров...")
    parsing_theatres.parse_events()

    print("✅ Парсинг завершён.")
