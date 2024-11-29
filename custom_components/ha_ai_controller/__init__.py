"""The Home Assistant AI Controller integration."""
from __future__ import annotations

import os
import logging
from typing import Any

import voluptuous as vol

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform

from .const import DOMAIN
from .panel import async_register_panel
from .ai_controller import HAClaudeController

_LOGGER = logging.getLogger(__name__)
PLATFORMS: list[Platform] = [Platform.SENSOR]

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Home Assistant AI Controller from a config entry."""
    hass.data.setdefault(DOMAIN, {})
    
    # Initialize the AI controller
    controller = HAClaudeController(hass, entry.data["api_key"])
    hass.data[DOMAIN][entry.entry_id] = controller
    
    # Register frontend panel
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
