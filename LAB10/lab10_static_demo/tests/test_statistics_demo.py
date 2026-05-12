"""Teste unitare pentru modulul statistics_demo (coverage, typeguard)."""

from __future__ import annotations

import pytest
from typeguard import TypeCheckError, typechecked

from statistics_demo import media_aritmetica, suma_ponderata


@typechecked
def _apel_media(valori: list[float]) -> float:
    return media_aritmetica(valori)


def test_media_aritmetica():
    assert media_aritmetica([1.0, 2.0, 3.0]) == 2.0


def test_media_lista_goala():
    with pytest.raises(ValueError, match="goală"):
        media_aritmetica([])


def test_suma_ponderata():
    assert suma_ponderata([1.0, 2.0], [0.5, 0.5]) == 1.5


def test_suma_ponderata_dimensiuni():
    with pytest.raises(ValueError, match="incompatibile"):
        suma_ponderata([1.0], [1.0, 2.0])


def test_typeguard_decorator_greseste_la_tipuri():
    with pytest.raises(TypeCheckError):
        _apel_media(["nu", "sunt", "numere"])  # type: ignore[arg-type]
