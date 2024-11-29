"""Panel for Home Assistant AI Controller."""
import logging
import os
import voluptuous as vol

from homeassistant.components import panel_custom, frontend
from homeassistant.core import HomeAssistant

_LOGGER = logging.getLogger(__name__)
DOMAIN = "ha_ai_controller"
PANEL_URL = f"/frontend_es5/ha_ai_controller/"
PANEL_TITLE = "AI Controller"
PANEL_ICON = "mdi:robot"
PANEL_NAME = "ha-ai-controller-panel"  # This matches our custom element name

async def async_register_panel(hass: HomeAssistant) -> None:
    """Register the panel."""
    frontend_path = os.path.join(os.path.dirname(__file__), "frontend", "build")
    
    if not os.path.isdir(frontend_path):
        _LOGGER.error("Frontend build directory not found: %s", frontend_path)
        return

    # Register frontend resources
    hass.http.register_static_path(
        f"{PANEL_URL}static",
        os.path.join(frontend_path, "static"),
        True
    )
    
    # Register the main.js file
    main_js_path = os.path.join(frontend_path, "static/js/main.js")
    if not os.path.isfile(main_js_path):
        _LOGGER.error("Main.js not found: %s", main_js_path)
        return

    # Copy the new main.js file
    import shutil
    new_main_js = os.path.join(frontend_path, "static/js/main.c17750e1.js")
    shutil.copy2(new_main_js, main_js_path)

    await panel_custom.async_register_panel(
        hass,
        webcomponent_name=PANEL_NAME,
        frontend_url_path=DOMAIN,
        module_url=f"{PANEL_URL}static/js/main.js",
        sidebar_title=PANEL_TITLE,
        sidebar_icon=PANEL_ICON,
        require_admin=False,
    )
