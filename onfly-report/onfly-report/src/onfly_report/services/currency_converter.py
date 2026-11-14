"""Conversão de valores para BRL."""

from __future__ import annotations

from decimal import Decimal


def convert_to_brl(amount: Decimal, currency: str, rates: dict[str, Decimal]) -> Decimal:
    """Converte um valor na moeda informada para BRL: amount * rate_to_brl.

    Usa Decimal de ponta a ponta (sem float) e não arredonda; o arredondamento
    acontece apenas na serialização do relatório.
    """
    return amount * rates[currency]
