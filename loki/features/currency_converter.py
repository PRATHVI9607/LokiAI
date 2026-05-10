"""
CurrencyConverter — live exchange rates + unit conversion.
Uses exchangerate-api open endpoint; falls back to LLM if unavailable.
"""

import logging
import re
import requests
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from loki.core.brain import LokiBrain

logger = logging.getLogger(__name__)

# Unit conversion factors → base SI unit
UNIT_MAP: dict[str, tuple[str, float]] = {
    # Length → metres
    "mm": ("length", 0.001), "cm": ("length", 0.01), "m": ("length", 1.0),
    "km": ("length", 1000.0), "in": ("length", 0.0254), "ft": ("length", 0.3048),
    "yd": ("length", 0.9144), "mi": ("length", 1609.344),
    # Weight → kg
    "mg": ("weight", 1e-6), "g": ("weight", 0.001), "kg": ("weight", 1.0),
    "lb": ("weight", 0.453592), "oz": ("weight", 0.0283495), "t": ("weight", 1000.0),
    # Temperature handled separately
    "c": ("temperature", 1.0), "f": ("temperature", 1.0), "k": ("temperature", 1.0),
    # Volume → litres
    "ml": ("volume", 0.001), "l": ("volume", 1.0), "cup": ("volume", 0.236588),
    "pint": ("volume", 0.473176), "gallon": ("volume", 3.78541),
    # Speed → m/s
    "mph": ("speed", 0.44704), "kph": ("speed", 0.277778), "knot": ("speed", 0.514444),
    # Data → bytes
    "kb": ("data", 1024), "mb": ("data", 1048576), "gb": ("data", 1073741824),
    "tb": ("data", 1099511627776),
}


class CurrencyConverter:
    def __init__(self, brain: Optional["LokiBrain"] = None):
        self._brain = brain
        self._rates: dict = {}

    def _ask(self, prompt: str) -> str:
        if not self._brain:
            return ""
        return "".join(self._brain.ask(prompt))

    def _fetch_rates(self, base: str = "USD") -> dict:
        if self._rates.get("base") == base:
            return self._rates
        try:
            url = f"https://open.er-api.com/v6/latest/{base.upper()}"
            resp = requests.get(url, timeout=6)
            data = resp.json()
            if data.get("result") == "success":
                self._rates = {"base": base.upper(), "rates": data["rates"]}
                return self._rates
        except Exception as e:
            logger.warning(f"Exchange rate fetch failed: {e}")
        return {}

    def convert_currency(self, amount: float, from_currency: str, to_currency: str) -> dict:
        """Convert an amount between two currencies using live rates."""
        from_c = from_currency.upper().strip()
        to_c = to_currency.upper().strip()

        rates_data = self._fetch_rates(from_c)
        if rates_data and "rates" in rates_data:
            rate = rates_data["rates"].get(to_c)
            if rate:
                converted = round(amount * rate, 4)
                return {
                    "success": True,
                    "message": f"{amount} {from_c} = {converted} {to_c}",
                    "data": {"amount": amount, "from": from_c, "to": to_c, "converted": converted, "rate": rate},
                }

        # LLM fallback
        prompt = f"Convert {amount} {from_c} to {to_c}. Give just the numeric result and the currency symbol."
        result = self._ask(prompt).strip()
        return {"success": True, "message": result or f"Could not convert {from_c} to {to_c}.", "data": {}}

    def convert_unit(self, amount: float, from_unit: str, to_unit: str) -> dict:
        """Convert between physical units (length, weight, temperature, etc.)."""
        fu = from_unit.lower().strip()
        tu = to_unit.lower().strip()

        fi = UNIT_MAP.get(fu)
        ti = UNIT_MAP.get(tu)

        if fi and ti and fi[0] == ti[0]:
            category = fi[0]
            if category == "temperature":
                result = self._convert_temperature(amount, fu, tu)
            else:
                result = round(amount * fi[1] / ti[1], 6)
            return {
                "success": True,
                "message": f"{amount} {from_unit} = {result} {to_unit}",
                "data": {"amount": amount, "from": from_unit, "to": to_unit, "result": result},
            }

        # LLM fallback for unknown units
        prompt = f"Convert {amount} {from_unit} to {to_unit}. Return only the numeric result and unit."
        result = self._ask(prompt).strip()
        return {"success": True, "message": result or f"Could not convert {from_unit} to {to_unit}.", "data": {}}

    @staticmethod
    def _convert_temperature(value: float, from_u: str, to_u: str) -> float:
        if from_u == to_u:
            return value
        if from_u == "c" and to_u == "f":
            return round(value * 9 / 5 + 32, 2)
        if from_u == "f" and to_u == "c":
            return round((value - 32) * 5 / 9, 2)
        if from_u == "c" and to_u == "k":
            return round(value + 273.15, 2)
        if from_u == "k" and to_u == "c":
            return round(value - 273.15, 2)
        if from_u == "f" and to_u == "k":
            return round((value - 32) * 5 / 9 + 273.15, 2)
        if from_u == "k" and to_u == "f":
            return round((value - 273.15) * 9 / 5 + 32, 2)
        return value
