"""Platform for sensor integration."""
from __future__ import annotations

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN

async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the AI Controller sensor."""
    async_add_entities([AIControllerSensor(config_entry)])

class AIControllerSensor(SensorEntity):
    """Representation of an AI Controller Sensor."""

    def __init__(self, config_entry: ConfigEntry) -> None:
        """Initialize the sensor."""
        self._attr_unique_id = f"{config_entry.entry_id}_status"
        self._attr_name = "AI Controller Status"
        self._attr_native_value = "Ready"

    @property
    def icon(self) -> str:
        """Return the icon of the sensor."""
        return "mdi:robot"
