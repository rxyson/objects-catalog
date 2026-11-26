import pytest

from library_catalog.models import Book
from library_catalog.catalog import Catalog
from library_catalog.exceptions import DuplicateIDError, IncorrectEntityError, ObjectNotFoundError


def make_book(item_id="b1", title="Война и мир", category="Роман", year=1869, author="Л.Н. Толстой", pages=1300):
    """Создание книги для тестов."""

    return Book(item_id, title, category, year, author, pages)


def make_catalog():
    """Создаёт каталог с тремя книгами для тестов."""

    catalog = Catalog()
    catalog.add(make_book("b1", "Война и мир", "Роман"))
    catalog.add(make_book("b2", "Золотая рыбка", "Сказка"))
    catalog.add(make_book("b3", "Евгений Онегин", "Роман"))
    return catalog


def test_valid_book():
    """Допустимая книга создаётся с переданными значениями."""

    book = make_book()
    assert book.item_id == "b1"
    assert book.title == "Война и мир"
    assert book.pages == 1300


def test_invalid_title():
    """Пустое название недопустимо."""

    with pytest.raises(IncorrectEntityError):
        make_book(title="   ")


def test_invalid_year():
    """Год из будущего недопустим."""

    with pytest.raises(IncorrectEntityError):
        make_book(year=2027)


def test_invalid_pages():
    """Количество страниц не может быть меньше одного."""

    with pytest.raises(IncorrectEntityError):
        make_book(pages=0)


def test_add_and_get():
    """Тест на правильность получения книги и длины каталога."""

    catalog = Catalog()
    book = make_book()
    catalog.add(book)
    assert catalog.get("b1") == book
    assert len(catalog) == 1
    assert "b1" in catalog


def test_duplicate():
    """Тест на дубликат ID."""

    catalog = Catalog()
    book1 = make_book()
    book2 = make_book()
    catalog.add(book1)
    with pytest.raises(DuplicateIDError):
        catalog.add(book2)


def test_get_missing():
    """Получение отсутствующего ID вызывает ошибку."""

    catalog = Catalog()
    with pytest.raises(ObjectNotFoundError):
        catalog.get("b10")


def test_remove():
    """Удалённой книги больше нет в каталоге."""

    catalog = Catalog()
    catalog.add(make_book())
    catalog.remove("b1")
    assert len(catalog) == 0
    assert "b1" not in catalog


def test_remove_missing():
    """Удаление отсутствующего ID вызывает предметное исключение."""

    catalog = Catalog()
    with pytest.raises(ObjectNotFoundError):
        catalog.remove("b10")


def test_find_by_category():
    """Поиск по категории возвращает все книги этой категории."""

    catalog = make_catalog()
    found = catalog.find_by_category("Роман")
    assert [book.item_id for book in found] == ["b1", "b3"]


def test_find_by_name():
    """Поиск по имени находит часть названия без учёта регистра."""

    catalog = make_catalog()
    found = catalog.find_by_name("МИР")
    assert [book.item_id for book in found] == ["b1"]


def test_find_returns_new_list():
    """Изменение результата поиска не меняет каталог."""

    catalog = make_catalog()
    found = catalog.find_by_category("Роман")
    found.clear()
    assert len(catalog) == 3
    assert len(catalog.find_by_category("Роман")) == 2


def test_iteration_order():
    """Книги перебираются в порядке добавления."""

    catalog = make_catalog()
    assert [book.item_id for book in catalog] == ["b1", "b2", "b3"]