---
type: community
cohesion: 0.25
members: 11
---

# CurrencyConverter / .convert_currency() / .convert_unit()

**Cohesion:** 0.25 - loosely connected
**Members:** 11 nodes

## Members
- [[.__init__()_24]] - code - loki/features/currency_converter.py
- [[._ask()_3]] - code - loki/features/currency_converter.py
- [[._fetch_rates()]] - code - loki/features/currency_converter.py
- [[.convert_currency()]] - code - loki/features/currency_converter.py
- [[.convert_unit()]] - code - loki/features/currency_converter.py
- [[Convert an amount between two currencies using live rates.]] - rationale - loki/features/currency_converter.py
- [[Convert between physical units (length, weight, temperature, etc.).]] - rationale - loki/features/currency_converter.py
- [[CurrencyConverter]] - code - loki/features/currency_converter.py
- [[CurrencyConverter — live exchange rates + unit conversion. Uses exchangerate-api]] - rationale - loki/features/currency_converter.py
- [[_convert_temperature()]] - code - loki/features/currency_converter.py
- [[currency_converter.py]] - code - loki/features/currency_converter.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/CurrencyConverter_/_convert_currency_/_convert_unit
SORT file.name ASC
```

## Connections to other communities
- 1 edge to [[_COMMUNITY_LokiApplication  .__init__()  main.py]]
- 1 edge to [[_COMMUNITY_._init_all()  DailyBriefing  .generate()]]
- 1 edge to [[_COMMUNITY_LokiBrain  test_brain.py  .ask()]]

## Top bridge nodes
- [[CurrencyConverter]] - degree 9, connects to 3 communities