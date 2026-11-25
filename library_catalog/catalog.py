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
        """Перебирает книги в порядке их добавления в каталог."""
        return iter(self._items.values())

    def find_by_category(self, category: str) -> list[Book]:
        """Возвращает книги по указанной категории."""
        result = []
        for book in self._items.values():
            if book.category == category:
                result.append(book)
        return result

    def find_by_name(self, title: str) -> list[Book]:
        """Возвращает книги по указанному слову."""
        result = []
        for book in self._items.values():
            if title.lower() in book.title.lower():
                result.append(book)
        return result

    def clear(self) -> None:
        """Очищает каталог."""
        self._items.clear()