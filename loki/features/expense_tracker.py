"""
ExpenseTracker — extract billing info from email text / .eml files and
maintain a local CSV ledger at ~/LokiExpenses/expenses.csv.
"""

import csv
import logging
import re
from datetime import datetime
from email import policy
from email.parser import BytesParser, Parser
from pathlib import Path
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from loki.core.brain import LokiBrain

logger = logging.getLogger(__name__)

DEFAULT_LEDGER = Path.home() / "LokiExpenses" / "expenses.csv"
CSV_HEADERS = ["date", "vendor", "amount", "currency", "category", "description", "source"]

# Heuristic patterns
AMOUNT_PATTERN = re.compile(
    r"(?:total|amount|charged|billed|payment|price|subtotal|grand total)[:\s]*"
    r"(?P<currency>[£$€¥₹]|USD|EUR|GBP|INR|JPY)?\s*"
    r"(?P<amount>\d{1,6}(?:[.,]\d{1,2})?)",
    re.IGNORECASE,
)
CURRENCY_SYMBOL = {"$": "USD", "£": "GBP", "€": "EUR", "¥": "JPY", "₹": "INR"}
DATE_PATTERN = re.compile(
    r"\b(?:\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4}|"
    r"(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.?\s+\d{1,2},?\s+\d{4})\b",
    re.IGNORECASE,
)
VENDOR_PATTERN = re.compile(
    r"(?:from|merchant|vendor|seller|billed by|charged by|store)[:\s]+([A-Za-z0-9 &.,'-]{3,50})",
    re.IGNORECASE,
)


def _parse_eml(path: Path) -> str:
    """Extract plain text from an .eml file."""
    try:
        raw = path.read_bytes()
        msg = BytesParser(policy=policy.default).parsebytes(raw)
        parts = []
        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                payload = part.get_payload(decode=True)
                if payload:
                    parts.append(payload.decode(errors="replace"))
        return "\n".join(parts)
    except Exception as e:
        logger.debug("EML parse error: %s", e)
        return ""


def _heuristic_extract(text: str) -> dict:
    """Extract amount, currency, date, vendor from text using regex."""
    amount, currency = None, "USD"
    date_str, vendor = None, None

    m = AMOUNT_PATTERN.search(text)
    if m:
        raw_amount = m.group("amount").replace(",", ".")
        try:
            amount = float(raw_amount)
        except ValueError:
            pass
        sym = m.group("currency") or ""
        currency = CURRENCY_SYMBOL.get(sym, sym.upper() or "USD")

    d = DATE_PATTERN.search(text)
    if d:
        date_str = d.group(0)

    v = VENDOR_PATTERN.search(text)
    if v:
        vendor = v.group(1).strip()

    # Fallback date
    if not date_str:
        date_str = datetime.now().strftime("%Y-%m-%d")

    return {"amount": amount, "currency": currency, "date": date_str, "vendor": vendor or "Unknown"}


class ExpenseTracker:
    def __init__(self, brain: Optional["LokiBrain"] = None, ledger_path: Optional[str] = None):
        self._brain = brain
        self._ledger = Path(ledger_path).expanduser().resolve() if ledger_path else DEFAULT_LEDGER

    def _llm(self, prompt: str) -> str:
        if not self._brain:
            return ""
        return "".join(self._brain.ask(prompt))

    def _ensure_ledger(self) -> None:
        self._ledger.parent.mkdir(parents=True, exist_ok=True)
        if not self._ledger.exists():
            with open(self._ledger, "w", newline="", encoding="utf-8") as f:
                csv.writer(f).writerow(CSV_HEADERS)

    def _append_row(self, row: dict) -> None:
        self._ensure_ledger()
        with open(self._ledger, "a", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=CSV_HEADERS)
            w.writerow({h: row.get(h, "") for h in CSV_HEADERS})

    def extract_from_text(self, email_text: str, source: str = "manual") -> dict:
        """Extract expense from raw email/receipt text and save to ledger."""
        info = _heuristic_extract(email_text)

        # Use LLM for better extraction if available
        if self._brain and (not info["amount"] or info["vendor"] == "Unknown"):
            prompt = (
                f"Extract expense info from this receipt/email text as JSON.\n"
                f"Fields: date (YYYY-MM-DD), vendor, amount (number), currency (3-letter), category, description\n\n"
                f"TEXT:\n{email_text[:1500]}\n\nReturn only valid JSON."
            )
            import json, re as _re
            raw = self._llm(prompt)
            try:
                match = _re.search(r"\{[^}]+\}", raw, _re.DOTALL)
                if match:
                    parsed = json.loads(match.group())
                    for k in ("amount", "currency", "date", "vendor", "category", "description"):
                        if parsed.get(k) and not info.get(k):
                            info[k] = parsed[k]
                    if parsed.get("amount"):
                        try:
                            info["amount"] = float(str(parsed["amount"]).replace(",", ""))
                        except ValueError:
                            pass
            except Exception:
                pass

        if not info.get("amount"):
            return {"success": False, "message": "Could not detect a payment amount in the provided text."}

        row = {
            "date": info.get("date", datetime.now().strftime("%Y-%m-%d")),
            "vendor": info.get("vendor", "Unknown"),
            "amount": info.get("amount", 0),
            "currency": info.get("currency", "USD"),
            "category": info.get("category", "Uncategorized"),
            "description": info.get("description", "")[:100],
            "source": source,
        }
        self._append_row(row)

        msg = (
            f"Expense recorded: {row['currency']} {row['amount']:.2f} "
            f"from {row['vendor']} on {row['date']} [{row['category']}]"
        )
        return {"success": True, "message": msg, "data": row}

    def extract_from_file(self, file_path: str) -> dict:
        """Extract expense from an .eml or .txt receipt file."""
        fp = Path(file_path).expanduser().resolve()
        if not fp.exists():
            return {"success": False, "message": f"File not found: {fp}"}

        if fp.suffix.lower() == ".eml":
            text = _parse_eml(fp)
        else:
            text = fp.read_text(encoding="utf-8", errors="replace")

        if not text.strip():
            return {"success": False, "message": "File is empty or could not be read."}

        return self.extract_from_text(text, source=fp.name)

    def scan_folder(self, folder: str) -> dict:
        """Scan a folder for .eml receipt files and extract all expenses."""
        base = Path(folder).expanduser().resolve()
        if not base.exists():
            return {"success": False, "message": f"Folder not found: {folder}"}

        files = list(base.glob("*.eml")) + list(base.glob("*.txt"))
        if not files:
            return {"success": True, "message": "No .eml or .txt files found.", "data": {"extracted": 0}}

        extracted, failed = 0, 0
        for f in files[:50]:
            r = self.extract_from_file(str(f))
            if r["success"]:
                extracted += 1
            else:
                failed += 1

        return {
            "success": True,
            "message": f"Scanned {len(files)} files: {extracted} expenses extracted, {failed} skipped.",
            "data": {"extracted": extracted, "failed": failed, "ledger": str(self._ledger)},
        }

    def list_expenses(self, month: Optional[str] = None, limit: int = 20) -> dict:
        """List expenses from the ledger, optionally filtered by month (YYYY-MM)."""
        self._ensure_ledger()
        rows = []
        try:
            with open(self._ledger, newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if month and not row.get("date", "").startswith(month):
                        continue
                    rows.append(row)
        except Exception as e:
            return {"success": False, "message": f"Could not read ledger: {e}"}

        rows = rows[-limit:]
        if not rows:
            return {"success": True, "message": "No expenses recorded yet.", "data": {"expenses": []}}

        total = sum(float(r.get("amount", 0)) for r in rows)
        lines = [f"  {r['date']} | {r['vendor'][:20]:<20} | {r['currency']} {float(r.get('amount',0)):.2f}" for r in rows]
        msg = f"{len(rows)} expense(s), total ≈ {total:.2f}:\n" + "\n".join(lines)
        return {"success": True, "message": msg, "data": {"expenses": rows, "total": total}}

    def monthly_summary(self) -> dict:
        """Summarize expenses by month and category."""
        self._ensure_ledger()
        by_month: dict = {}
        try:
            with open(self._ledger, newline="", encoding="utf-8") as f:
                for row in csv.DictReader(f):
                    month = row.get("date", "")[:7]
                    cat = row.get("category", "Other")
                    amt = float(row.get("amount", 0))
                    by_month.setdefault(month, {}).setdefault(cat, 0)
                    by_month[month][cat] += amt
        except Exception as e:
            return {"success": False, "message": f"Could not read ledger: {e}"}

        if not by_month:
            return {"success": True, "message": "No expenses recorded.", "data": {}}

        lines = []
        for month in sorted(by_month, reverse=True)[:6]:
            total = sum(by_month[month].values())
            lines.append(f"  {month}: {total:.2f}")
            for cat, amt in sorted(by_month[month].items(), key=lambda x: -x[1])[:5]:
                lines.append(f"    └ {cat}: {amt:.2f}")

        return {"success": True, "message": "Monthly expense summary:\n" + "\n".join(lines), "data": by_month}

    def get_ledger_path(self) -> dict:
        return {"success": True, "message": f"Expense ledger: {self._ledger}", "data": {"path": str(self._ledger)}}
