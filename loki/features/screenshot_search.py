"""
ScreenshotSearch — capture screen / region, extract text via OCR,
and optionally perform visual search using a multimodal LLM.

Dependencies:
  - Pillow (PIL.ImageGrab) — screen capture, ships with most setups
  - pytesseract (optional) — better OCR quality; requires Tesseract binary
  - mss (optional) — faster multi-monitor capture
"""

import base64
import io
import logging
import subprocess
import tempfile
from pathlib import Path
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from loki.core.brain import LokiBrain

logger = logging.getLogger(__name__)


def _capture_screen(region: Optional[tuple] = None) -> Optional[bytes]:
    """Capture screen as PNG bytes. Returns None on failure."""
    # Try PIL ImageGrab first (Windows built-in)
    try:
        from PIL import ImageGrab
        img = ImageGrab.grab(bbox=region)
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        return buf.getvalue()
    except Exception:
        pass

    # Try mss (multi-monitor, lightweight)
    try:
        import mss
        with mss.mss() as sct:
            monitor = sct.monitors[1]  # primary monitor
            if region:
                l, t, r, b = region
                monitor = {"left": l, "top": t, "width": r - l, "height": b - t}
            img = sct.grab(monitor)
            buf = io.BytesIO()
            from PIL import Image
            Image.frombytes("RGB", img.size, img.bgra, "raw", "BGRX").save(buf, format="PNG")
            return buf.getvalue()
    except Exception:
        pass

    return None


def _ocr_windows(png_bytes: bytes) -> str:
    """Use Windows built-in OCR via PowerShell WinRT (Windows 10+)."""
    try:
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
            f.write(png_bytes)
            tmp_path = f.name

        ps_script = f"""
Add-Type -AssemblyName System.Runtime.WindowsRuntime
$null = [Windows.Media.Ocr.OcrEngine, Windows.Foundation, ContentType=WindowsRuntime]
$null = [Windows.Storage.StorageFile, Windows.Foundation, ContentType=WindowsRuntime]

function Await($WinRTTask) {{
    $netTask = [System.WindowsRuntimeSystemExtensions]::AsTask($WinRTTask)
    $netTask.Wait() | Out-Null
    $netTask.Result
}}

$engine = [Windows.Media.Ocr.OcrEngine]::TryCreateFromUserProfileLanguages()
$file = Await([Windows.Storage.StorageFile]::GetFileFromPathAsync('{tmp_path.replace(chr(92), "/")}'))
$stream = Await($file.OpenReadAsync())
$decoder = Await([Windows.Graphics.Imaging.BitmapDecoder]::CreateAsync($stream))
$bitmap = Await($decoder.GetSoftwareBitmapAsync())
$result = Await($engine.RecognizeAsync($bitmap))
$result.Text
"""
        result = subprocess.run(
            ["powershell", "-NoProfile", "-Command", ps_script],
            capture_output=True, text=True, timeout=15, encoding="utf-8", errors="replace",
        )
        Path(tmp_path).unlink(missing_ok=True)
        return result.stdout.strip()
    except Exception as e:
        logger.debug("Windows OCR failed: %s", e)
        return ""


def _ocr_tesseract(png_bytes: bytes) -> str:
    """Use pytesseract if available."""
    try:
        import pytesseract
        from PIL import Image
        img = Image.open(io.BytesIO(png_bytes))
        return pytesseract.image_to_string(img).strip()
    except Exception:
        return ""


class ScreenshotSearch:
    def __init__(self, brain: Optional["LokiBrain"] = None):
        self._brain = brain

    def _llm(self, prompt: str) -> str:
        if not self._brain:
            return ""
        return "".join(self._brain.ask(prompt))

    def _ocr(self, png_bytes: bytes) -> str:
        # Try Windows built-in OCR first (no extra deps)
        text = _ocr_windows(png_bytes)
        if text:
            return text
        # Fallback to pytesseract
        return _ocr_tesseract(png_bytes)

    def capture_and_read(self, region: Optional[str] = None) -> dict:
        """Capture the screen (or a region) and extract all visible text via OCR."""
        bbox = None
        if region:
            try:
                parts = [int(x.strip()) for x in region.split(",")]
                if len(parts) == 4:
                    bbox = tuple(parts)
            except ValueError:
                pass

        png = _capture_screen(bbox)
        if not png:
            return {"success": False, "message": "Could not capture screen. Ensure Pillow is installed: pip install Pillow"}

        text = self._ocr(png)
        if not text:
            return {
                "success": True,
                "message": "Screen captured but no text detected (OCR found nothing).",
                "data": {"text": "", "png_size_kb": round(len(png) / 1024, 1)},
            }

        return {
            "success": True,
            "message": f"Extracted {len(text)} characters from screen:\n\n{text[:1000]}",
            "data": {"text": text, "png_size_kb": round(len(png) / 1024, 1)},
        }

    def search_screen(self, query: str) -> dict:
        """Capture screen, OCR it, then search for query text."""
        result = self.capture_and_read()
        if not result["success"]:
            return result

        text = result["data"]["text"]
        query_lower = query.lower()
        matches = [line for line in text.splitlines() if query_lower in line.lower()]

        if not matches:
            return {
                "success": True,
                "message": f"'{query}' not found in visible screen text.",
                "data": {"matches": [], "total_text": len(text)},
            }

        return {
            "success": True,
            "message": f"Found '{query}' in {len(matches)} line(s):\n" + "\n".join(f"  • {m}" for m in matches[:10]),
            "data": {"matches": matches},
        }

    def describe_screen(self) -> dict:
        """Capture the screen and ask LLM to describe what's on it (vision model)."""
        png = _capture_screen()
        if not png:
            return {"success": False, "message": "Could not capture screen."}

        # First try OCR so we have text context
        text = self._ocr(png)

        if not self._brain:
            return {
                "success": True,
                "message": f"Screen captured. OCR text ({len(text)} chars):\n{text[:500]}",
                "data": {"text": text},
            }

        # If text was found, give LLM the text to describe context
        if text:
            prompt = (
                f"Based on this text extracted from a screenshot, describe what the user is currently doing "
                f"and what is visible on their screen:\n\n{text[:2000]}"
            )
            description = self._llm(prompt)
        else:
            # Try base64 vision if LLM supports it (best-effort)
            b64 = base64.b64encode(png).decode()
            prompt = (
                f"This is a base64 PNG screenshot: data:image/png;base64,{b64[:100]}... "
                f"(image too large for text prompt). Based on context, describe what might be on screen."
            )
            description = "Could not extract text from screen — no OCR text found and vision model not configured."

        return {
            "success": True,
            "message": description or "Screen captured successfully.",
            "data": {"text": text, "description": description},
        }

    def translate_screen(self, target_language: str = "English") -> dict:
        """Capture screen, OCR it, and translate all text to target language."""
        result = self.capture_and_read()
        if not result["success"]:
            return result

        text = result["data"]["text"]
        if not text:
            return {"success": False, "message": "No text found on screen to translate."}

        if not self._brain:
            return {"success": False, "message": "LLM required for translation."}

        prompt = (
            f"Translate the following screen text to {target_language}. "
            f"Preserve the layout as much as possible.\n\nORIGINAL:\n{text[:3000]}"
        )
        translated = self._llm(prompt)
        return {
            "success": True,
            "message": translated or "Translation failed.",
            "data": {"original": text, "translated": translated, "language": target_language},
        }

    def save_screenshot(self, output_path: Optional[str] = None) -> dict:
        """Capture and save screenshot to disk."""
        from datetime import datetime
        png = _capture_screen()
        if not png:
            return {"success": False, "message": "Could not capture screen."}

        if output_path:
            out = Path(output_path).expanduser().resolve()
        else:
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            out = Path.home() / "Pictures" / f"loki_screenshot_{ts}.png"

        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_bytes(png)
        return {
            "success": True,
            "message": f"Screenshot saved to {out} ({round(len(png)/1024, 1)} KB).",
            "data": {"path": str(out)},
        }
