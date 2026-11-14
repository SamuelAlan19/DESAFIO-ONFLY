"""Cálculo de noites ocupadas."""

from __future__ import annotations

from datetime import date


def calculate_room_nights(checkin: date, checkout: date, rooms: int) -> int:
    """Calcula noites de quarto: diferença de dias (não inclusiva) vezes quartos.

    A subtração de datas considera mês e ano (ex.: 30/01 -> 02/02 = 3 noites).
    """
    return (checkout - checkin).days * rooms
