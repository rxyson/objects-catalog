"""Демонстрация работы каталога библиотечных книг."""

from library_catalog.models import Book
from library_catalog.catalog import Catalog
from library_catalog.storage import save_catalog, load_catalog
from library_catalog.exceptions import CatalogError

DEMO_FILE = "demo_catalog.json"


def print_books(title: str, books) -> None:
    """Печатает заголовок и список книг по одной в строке."""
    print(title)
    for book in books:
        print(f"[{book.item_id}] {book.title} — {book.author}, {book.year}, {book.category}, {book.pages} стр.")
    print()


def main() -> None:
    catalog = Catalog()

    catalog.add(Book("b1", "Война и мир", "Роман", 1869, "Л.Н. Толстой", 1300))
    catalog.add(Book("b2", "Горе от ума", "Комедия", 1825, "А.С. Грибоедов", 200))
    catalog.add(Book("b3", "Евгений Онегин", "Роман", 1833, "А.С. Пушкин", 400))
    catalog.add(Book("b4", "Мир Полудня", "Фантастика", 1962, "Стругацкие", 300))
    print(f"Добавлено книг: {len(catalog)}")

    print_books("Все книги:", catalog)

    book = catalog.get("b3")
    print(f"get('b3'): {book.title}")
    print(f"'b2' in catalog: {'b2' in catalog}")
    print(f"'b99' in catalog: {'b99' in catalog}")

    print_books("Категория 'Роман':", catalog.find_by_category("Роман"))
    print_books("Название содержит 'МИР':", catalog.find_by_name("МИР"))

    print("Ошибки:")
    try:
        catalog.add(Book("b1", "Анна Каренина", "Роман", 1877, "Л.Н. Толстой", 864))
    except CatalogError as error:
        print(f"Дубликат ID: {error}")

    try:
        Book("b5", "Пустая книга", "Роман", 2000, "Кто-то", 0)
    except CatalogError as error:
        print(f"Недопустимая книга: {error}")

    try:
        catalog.remove("b99")
    except CatalogError as error:
        print(f"Удаление отсутствующего ID: {error}")
    print()

    catalog.remove("b2")
    print(f"После удаления 'b2' книг: {len(catalog)}")

    save_catalog(catalog, DEMO_FILE)
    print(f"Каталог сохранён в {DEMO_FILE}")

    loaded = Catalog()
    load_catalog(loaded, DEMO_FILE)
    print_books(f"Загружено из {DEMO_FILE} ({len(loaded)} кн.):", loaded)


if __name__ == "__main__":
    main()