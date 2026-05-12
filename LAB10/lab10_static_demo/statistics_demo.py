"""Demonstrație pentru laboratorul 10 — verificări statice și dinamice."""

from __future__ import annotations

from collections.abc import Sequence


def media_aritmetica(valori: Sequence[float]) -> float:
    """Returnează media aritmetică; ridică ValueError dacă lista este goală."""
    if not valori:
        raise ValueError("Lista este goală.")
    return float(sum(valori) / len(valori))


def suma_ponderata(valori: Sequence[float], ponderi: Sequence[float]) -> float:
    """Întoarce suma ponderată; ridică ValueError dacă dimensiunile nu coincid."""
    if len(valori) != len(ponderi):
        raise ValueError("Dimensiuni incompatibile pentru valori și ponderi.")
    return float(sum(v * p for v, p in zip(valori, ponderi, strict=True)))
