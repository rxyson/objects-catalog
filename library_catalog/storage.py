import json
from dataclasses import asdict

from .catalog import Catalog
from .exceptions import DamagedFileError, UnsupportedFormatVersionError, CatalogError
from .models import Book

FORMAT_VERSION = 1


def save_catalog(catalog: Catalog, path: str) -> None:
    """Сохраняет каталог в JSON-файл."""

    items = [asdict(book) for book in catalog]
    data = dict(format_version=FORMAT_VERSION, items=items)
    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)


def load_catalog(catalog: Catalog, path: str) -> None:
    """Загружает книги из JSON-файла в каталог."""
    
    try:
        with open(path, encoding="utf-8") as file:
            data = json.load(file)
    except json.JSONDecodeError as error:
        raise DamagedFileError(f"Файл {path} не является корректным JSON.") from error

    if not isinstance(data, dict):
        raise DamagedFileError(f"Файл {path} не соответствует ожидаемому формату.")

    if data.get("format_version") != FORMAT_VERSION:
        raise UnsupportedFormatVersionError(f"Файл {path} имеет неподдерживаемую версию формата.")

    if not isinstance(data.get("items"), list):
        raise DamagedFileError(f"Файл {path} не содержит корректный список книг.")

    draft = Catalog()
    for raw in data["items"]:
        if not isinstance(raw, dict):
            raise DamagedFileError(f"Файл {path} содержит некорректные данные книги.")
        try:
            draft.add(Book(**raw))
        except (TypeError, CatalogError) as error:
            raise DamagedFileError(f"Файл {path} содержит некорректные данные книги.") from error

    catalog.clear()
    for book in draft:
        catalog.add(book)
