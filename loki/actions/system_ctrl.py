"""
System controls — volume, brightness, WiFi, Bluetooth.
"""

import subprocess
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

try:
    from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
    from comtypes import CLSCTX_ALL
    PYCAW_AVAILABLE = True
except ImportError:
    PYCAW_AVAILABLE = False

try:
    import screen_brightness_control as sbc
    SBC_AVAILABLE = True
except ImportError:
    SBC_AVAILABLE = False


class SystemCtrl:
    """Windows system controls with undo support."""

    def __init__(self, undo_stack):
        self._undo = undo_stack
        self._vol_iface: Optional[Any] = None

        if PYCAW_AVAILABLE:
            try:
                devices = AudioUtilities.GetSpeakers()
                interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
                self._vol_iface = interface.QueryInterface(IAudioEndpointVolume)
            except Exception as e:
                logger.error(f"Volume init failed: {e}")

    def set_volume(self, percent: int) -> Dict[str, Any]:
        if not 0 <= percent <= 100:
            return {"success": False, "message": "Volume must be 0–100."}
        if not self._vol_iface:
            return {"success": False, "message": "Volume control unavailable."}
        try:
            current = int(self._vol_iface.GetMasterVolumeLevelScalar() * 100)
            self._undo.push("volume_change", {"previous": current}, f"Volume {current}%→{percent}%")
            self._vol_iface.SetMasterVolumeLevelScalar(percent / 100.0, None)
            return {"success": True, "message": f"Volume set to {percent}%."}
        except Exception as e:
            logger.error(f"set_volume error: {e}")
            return {"success": False, "message": "Volume change failed."}

    def get_volume(self) -> Dict[str, Any]:
        if not self._vol_iface:
            return {"success": False, "message": "Volume control unavailable."}
        try:
            vol = int(self._vol_iface.GetMasterVolumeLevelScalar() * 100)
            return {"success": True, "volume": vol, "message": f"Volume is at {vol}%."}
        except Exception as e:
            return {"success": False, "message": f"Cannot read volume: {e}"}

    def set_brightness(self, percent: int) -> Dict[str, Any]:
        if not SBC_AVAILABLE:
            return {"success": False, "message": "Brightness control unavailable."}
        if not 0 <= percent <= 100:
            return {"success": False, "message": "Brightness must be 0–100."}
        try:
            current = sbc.get_brightness()[0]
            self._undo.push("brightness_change", {"previous": current}, f"Brightness {current}%→{percent}%")
            sbc.set_brightness(percent)
            return {"success": True, "message": f"Brightness set to {percent}%."}
        except Exception as e:
            return {"success": False, "message": f"Brightness change failed: {e}"}

    def get_brightness(self) -> Dict[str, Any]:
        if not SBC_AVAILABLE:
            return {"success": False, "message": "Brightness control unavailable."}
        try:
            b = sbc.get_brightness()[0]
            return {"success": True, "brightness": b, "message": f"Brightness is at {b}%."}
        except Exception as e:
            return {"success": False, "message": f"Cannot read brightness: {e}"}

    def toggle_wifi(self) -> Dict[str, Any]:
        try:
            result = subprocess.run(
                ["netsh", "interface", "show", "interface"],
                capture_output=True, text=True, timeout=10
            )
            lines = result.stdout.lower()
            wifi_enabled = "wi-fi" in lines and "connected" in lines

            if wifi_enabled:
                cmd = ["netsh", "interface", "set", "interface", "Wi-Fi", "disabled"]
                action = "disabled"
            else:
                cmd = ["netsh", "interface", "set", "interface", "Wi-Fi", "enabled"]
                action = "enabled"

            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                return {"success": True, "message": f"Wi-Fi {action}."}
            return {"success": False, "message": f"Wi-Fi toggle failed: {result.stderr[:100]}"}
        except PermissionError:
            return {"success": False, "message": "Requires administrator privileges."}
        except Exception as e:
            return {"success": False, "message": f"Wi-Fi control failed: {e}"}

    def toggle_bluetooth(self) -> Dict[str, Any]:
        try:
            ps_cmd = (
                "Add-Type -AssemblyName System.Runtime.WindowsRuntime; "
                "$radio = [Windows.Devices.Radios.Radio,Windows.System.Devices,ContentType=WindowsRuntime]; "
                "[void][Windows.Devices.Radios.RadioAccessStatus,Windows.System.Devices,ContentType=WindowsRuntime]; "
                "$radios = ($radio::GetRadiosAsync()).GetAwaiter().GetResult(); "
                "$bt = $radios | Where-Object { $_.Kind -eq 'Bluetooth' }; "
                "if ($bt) { if ($bt.State -eq 'On') { ($bt.SetStateAsync('Off')).Wait() } "
                "else { ($bt.SetStateAsync('On')).Wait() } }"
            )
            result = subprocess.run(
                ["powershell", "-NonInteractive", "-Command", ps_cmd],
                capture_output=True, text=True, timeout=15
            )
            if result.returncode == 0:
                return {"success": True, "message": "Bluetooth toggled."}
            return {"success": False, "message": "Bluetooth toggle requires Windows 10+ and admin rights."}
        except Exception as e:
            return {"success": False, "message": f"Bluetooth control failed: {e}"}
