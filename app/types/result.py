from typing import Any, Generic, TypeAlias, TypeVar

TOK = TypeVar("TOK")
TERR = TypeVar("TERR")

class Ok(Generic[TOK]):
    _value: TOK

    def __init__(self, value: TOK):
        self._value = value

    def is_ok(self) -> bool:
        return True

    def value(self) -> TOK:
        return self._value

class Err(Generic[TERR]):
    _error: TERR

    def __init__(self, error: TERR):
        self._error = error

    def is_ok(self) -> bool:
        return False

    def error(self) -> TERR:
        return self._error

Result: TypeAlias = Ok[TOK] | Err[TERR]
