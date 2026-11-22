class CatalogError(Exception):
    """Базовые ошибки каталога библиотеки."""


class IncorrectEntityError(CatalogError):
    """Ошибка, возникающая при некорректной сущности в каталоге."""


class DuplicateIDError(CatalogError):
    """Ошибка, возникающая при дублировании идентификатора в каталоге."""


class ObjectNotFoundError(CatalogError):
    """Ошибка, возникающая при отсутствии объекта в каталоге."""


class UnsupportedFormatVersionError(CatalogError):
    """Ошибка, возникающая при попытке использовать неподдерживаемую версию формата каталога."""


class DamagedFileError(CatalogError):
    """Ошибка, возникающая при повреждении файла каталога."""