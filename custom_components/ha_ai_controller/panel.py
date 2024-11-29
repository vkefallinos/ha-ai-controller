"""Panel for Home Assistant AI Controller."""
import logging
import os
import voluptuous as vol

from homeassistant.components import panel_custom
from homeassistant.core import HomeAssistant

_LOGGER = logging.getLogger(__name__)
DOMAIN = "ha_ai_controller"
PANEL_URL = f"/api/{DOMAIN}/panel"
PANEL_TITLE = "AI Controller"
PANEL_ICON = "mdi:robot"
PANEL_NAME = "ha-ai-controller-panel"

async def async_register_panel(hass: HomeAssistant) -> None:
    """Register the panel."""
    frontend_path = os.path.join(os.path.dirname(__file__), "frontend")
    
    if not os.path.isdir(frontend_path):
        _LOGGER.error("Frontend directory not found: %s", frontend_path)
        return

    await panel_custom.async_register_panel(
        hass,
        webcomponent_name=PANEL_NAME,
        frontend_url_path=DOMAIN,
        module_url=f"{PANEL_URL}/main.js",
        sidebar_title=PANEL_TITLE,
        sidebar_icon=PANEL_ICON,
        require_admin=False,
    )
