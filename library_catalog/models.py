from dataclasses import dataclass
from .exceptions import IncorrectEntityError


@dataclass
class Book:
    """Книга в каталоге библиотеки."""

    item_id: str
    title: str
    category: str
    year: int
    author: str
    pages: int

    def __post_init__(self) -> None:
        if not isinstance(self.item_id, str) or not self.item_id.strip():
            raise IncorrectEntityError("Идентификатор книги должен быть непустой строкой.")
        if not isinstance(self.title, str) or not self.title.strip():
            raise IncorrectEntityError("Название книги должно быть непустой строкой.")
        if not isinstance(self.category, str) or not self.category.strip():
            raise IncorrectEntityError("Категория книги должна быть непустой строкой.")
        if not isinstance(self.year, int) or self.year <= 0 or self.year > 2026:
            raise IncorrectEntityError("Год издания книги должен быть целым числом от 1 до текущего года.")
        if not isinstance(self.author, str) or not self.author.strip():
            raise IncorrectEntityError("Автор книги должен быть непустой строкой.")
        if not isinstance(self.pages, int) or self.pages <= 0:
            raise IncorrectEntityError("Количество страниц книги должно быть положительным целым числом.")
