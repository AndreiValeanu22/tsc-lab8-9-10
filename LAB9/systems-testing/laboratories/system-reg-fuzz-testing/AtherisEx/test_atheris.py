import re
import sys

import pytest

"""
Completați funcțiile de mai jos și observați cum Atheris depistează excepții.

Rulare fuzzing (Linux, cu Atheris instalat): python test_atheris.py
Teste unitare: pytest test_atheris.py -v
"""


def extract_numbers(s: str) -> list:
    """
    Returnează o listă de numere întregi găsite în string.
    Ex: "abc123def45" -> [123, 45]
    """
    parts = re.findall(r"-?\d+", s)
    return [int(p) for p in parts]


def safe_divide_list(numbers: list) -> float:
    """
    Împarte primul număr la al doilea.
    """
    if len(numbers) < 2:
        raise ValueError("Sunt necesare cel puțin două numere pentru împărțire.")
    a, b = numbers[0], numbers[1]
    return float(a) / float(b)


def list_sum(numbers: list) -> int:
    """
    Calculează suma tuturor numerelor din listă.
    """
    return int(sum(numbers))


def process_input(data: bytes):
    """
    Funcția de fuzzing: transformă datele în string și apelează funcțiile de mai sus.
    """
    import atheris  # noqa: PLC0415

    fdp = atheris.FuzzedDataProvider(data)

    input_str = fdp.ConsumeUnicodeNoSurrogates(50)

    numbers = extract_numbers(input_str)

    try:
        safe_divide_list(numbers)
    except (ValueError, ZeroDivisionError):
        pass

    try:
        list_sum(numbers)
    except ValueError:
        pass


def main():
    import atheris  # noqa: PLC0415

    atheris.Setup(sys.argv, process_input)
    atheris.Fuzz()


if __name__ == "__main__":
    main()


class TestAtherisHelpers:
    """Teste unitare pentru funcțiile folosite la fuzzing (fără a rula bucla Atheris)."""

    def test_extract_numbers_basic(self):
        assert extract_numbers("abc123def45") == [123, 45]

    def test_extract_numbers_negative(self):
        assert extract_numbers("a-5b10") == [-5, 10]

    def test_safe_divide_list_ok(self):
        assert safe_divide_list([10, 2]) == 5.0

    def test_safe_divide_list_too_few(self):
        with pytest.raises(ValueError):
            safe_divide_list([1])

    def test_safe_divide_list_zero_divisor(self):
        with pytest.raises(ZeroDivisionError):
            safe_divide_list([1, 0])

    def test_list_sum_empty(self):
        assert list_sum([]) == 0

    def test_list_sum_values(self):
        assert list_sum([1, 2, 3]) == 6
