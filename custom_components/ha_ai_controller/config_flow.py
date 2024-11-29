"""Config flow for Home Assistant AI Controller integration."""
from typing import Any, Dict, Optional
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
import homeassistant.helpers.config_validation as cv
from .const import DOMAIN, CONF_MODEL, DEFAULT_MODEL
from homeassistant.const import CONF_API_KEY

class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Home Assistant AI Controller."""

    VERSION = 1

    async def async_step_user(
        self, user_input: Optional[Dict[str, Any]] = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors: Dict[str, str] = {}

        if user_input is not None:
            try:
                # Validate the API key here if possible
                return self.async_create_entry(
                    title="Home Assistant AI Controller",
                    data={
                        CONF_API_KEY: user_input[CONF_API_KEY],
                        CONF_MODEL: user_input.get(CONF_MODEL, DEFAULT_MODEL),
                    },
                )
            except Exception:  # pylint: disable=broad-except
                errors["base"] = "unknown"

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_API_KEY): str,
                    vol.Optional(CONF_MODEL, default=DEFAULT_MODEL): str,
                }
            ),
            errors=errors,
        )
