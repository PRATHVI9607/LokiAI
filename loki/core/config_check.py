"""
Lightweight config validation (issue #80).

Not a full schema — just catches the misconfigurations that cause confusing
runtime behaviour (wrong types, out-of-range thresholds) and logs clear WARNINGs
at startup instead of failing mysteriously later. Never raises; returns the list
of problems found.
"""

import logging
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


def _num(d: Dict[str, Any], path: str, lo: float, hi: float, problems: List[str]) -> None:
    keys = path.split(".")
    node: Any = d
    for k in keys:
        if not isinstance(node, dict) or k not in node:
            return  # key absent — defaults apply, nothing to validate
        node = node[k]
    if not isinstance(node, (int, float)) or isinstance(node, bool):
        problems.append(f"{path} should be a number (got {type(node).__name__})")
    elif not (lo <= node <= hi):
        problems.append(f"{path}={node} is out of range [{lo}, {hi}]")


def validate_config(config: Dict[str, Any]) -> List[str]:
    """Return a list of human-readable config problems (empty = all good)."""
    problems: List[str] = []

    _num(config, "llm.temperature", 0.0, 2.0, problems)
    _num(config, "llm.max_tokens", 1, 32000, problems)
    _num(config, "llm.ollama_timeout", 1, 600, problems)
    _num(config, "llm.bandit.epsilon", 0.0, 1.0, problems)
    _num(config, "wakeword.rms_threshold", 0.0, 1.0, problems)
    _num(config, "audio.vad_aggressiveness", 0, 3, problems)
    _num(config, "ui.port", 1, 65535, problems)
    _num(config, "proactive.check_interval", 1, 3600, problems)

    device = config.get("whisper", {}).get("device")
    if device is not None and device not in ("auto", "cpu", "cuda"):
        problems.append(f"whisper.device='{device}' must be auto|cpu|cuda")

    for p in problems:
        logger.warning(f"config: {p}")
    return problems
