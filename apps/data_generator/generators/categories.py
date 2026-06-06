def generate_categories() -> list[dict]:
    category_names = [
        "Elektronik",
        "Moda",
        "Ev ve Yaşam",
        "Spor",
        "Kozmetik",
        "Kitap",
        "Oyuncak",
        "Süpermarket",
    ]

    return [{"category_name": name} for name in category_names]
