import json

import pytest

from library_catalog.models import Book
from library_catalog.catalog import Catalog
from library_catalog.storage import save_catalog, load_catalog
from library_catalog.exceptions import DamagedFileError, UnsupportedFormatVersionError


def make_book(item_id="b1", title="Война и мир", category="Роман", year=1869, author="Л.Н. Толстой", pages=1300):
    """Создание книги для тестов."""

    return Book(item_id, title, category, year, author, pages)


def test_round_trip(tmp_path):
    """Сохраненный каталог загружается обратно без изменений."""

    path = tmp_path / "catalog.json"

    catalog = Catalog()
    catalog.add(make_book())
    catalog.add(make_book("b2", "Горе от ума", "Комедия"))
    save_catalog(catalog, path)

    loaded = Catalog()
    load_catalog(loaded, path)

    assert len(loaded) == 2
    assert [book.item_id for book in loaded] == ["b1", "b2"]
    assert loaded.get("b2") == catalog.get("b2")


def test_damaged_json(tmp_path):
    """Сломанный JSON вызывает DamagedFileError."""

    path = tmp_path / "catalog.json"
    path.write_text("ваоваолвоалвоа", encoding="utf-8")
    with pytest.raises(DamagedFileError):
        load_catalog(Catalog(), path)


def test_unknown_version(tmp_path):
    """Неизвестная версия формата вызывает UnsupportedFormatVersionError."""

    path = tmp_path / "catalog.json"
    path.write_text(json.dumps({"format_version": 2, "items": []}), encoding="utf-8")
    with pytest.raises(UnsupportedFormatVersionError):
        load_catalog(Catalog(), path)


def test_no_partial_change(tmp_path):
    """После ошибки загрузки каталог не меняется."""

    path = tmp_path / "catalog.json"
    data = {
        "format_version": 1,
        "items": [
            {"item_id": "b1", "title": "Война и мир", "category": "Роман", "year": 1869, "author": "Л.Н. Толстой", "pages": 1300},
            {"item_id": "b2", "title": "Горе от ума", "category": "Комедия", "year": 1825, "author": "А.С. Грибоедов", "pages": 0},
        ],
    }
    path.write_text(json.dumps(data), encoding="utf-8")

    catalog = Catalog()
    old_book = make_book("old", "Старая книга")
    catalog.add(old_book)

    with pytest.raises(DamagedFileError):
        load_catalog(catalog, path)

    assert [book.item_id for book in catalog] == ["old"]
    assert catalog.get("old") == old_book