"""The Home Assistant AI Controller integration."""
from __future__ import annotations

import os
import logging
from typing import Any

from aiohttp import web
import voluptuous as vol

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.components.http import HomeAssistantView

from .const import DOMAIN
from .panel import async_register_panel

_LOGGER = logging.getLogger(__name__)
PLATFORMS: list[Platform] = [Platform.SENSOR]

class AIPanelView(HomeAssistantView):
    """View to serve AI Controller Panel."""

    requires_auth = True
    name = "api:ha_ai_controller:panel"
    url = "/api/ha_ai_controller/panel/{path:.*}"

    def __init__(self, frontend_path: str) -> None:
        """Initialize the view with frontend path."""
        self.frontend_path = frontend_path

    async def get(self, request: web.Request, path: str) -> web.Response:
        """Serve frontend files."""
        if not path:
            path = "index.html"

        frontend_path = os.path.join(self.frontend_path, "build", path)

        if not os.path.isfile(frontend_path):
            _LOGGER.error("File not found: %s", frontend_path)
            return web.Response(status=404)

        return web.FileResponse(frontend_path)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Home Assistant AI Controller from a config entry."""
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = entry.data
    
    # Register frontend panel
    frontend_path = os.path.join(os.path.dirname(__file__), "frontend")
    hass.http.register_view(AIPanelView(frontend_path))
    await async_register_panel(hass)
    
    # Forward the setup to the sensor platform
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
