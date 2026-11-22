from collections.abc import Iterator
from .exceptions import DuplicateIDError, ObjectNotFoundError
from .models import Book


class Catalog:
    """Каталог книг библиотеки."""

    def __init__(self) -> None:
        self._items: dict[str, Book] = {}

    def __len__(self) -> int:
        return len(self._items)

    def add(self, item: Book) -> None:
        if item.item_id in self._items:
            raise DuplicateIDError(f"Книга с ID '{item.item_id}' уже существует в каталоге.")
        self._items[item.item_id] = item

    def get(self, item_id: str) -> Book:
        if item_id not in self._items:
            raise ObjectNotFoundError(f"Книга с ID '{item_id}' не найдена в каталоге.")
        return self._items[item_id]

    def __contains__(self, item_id: str) -> bool:
        if item_id in self._items:
            return True
        return False

    def remove(self, item_id: str) -> None:
        if item_id not in self._items:
            raise ObjectNotFoundError(f"Книга с ID '{item_id}' не найдена в каталоге.")
        else:
            del self._items[item_id]
 
    def __iter__(self) -> Iterator[Book]:
        return iter(self._items.values())

    