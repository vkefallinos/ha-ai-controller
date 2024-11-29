"""Home Assistant AI Controller using Anthropic's Claude."""
import logging
import json
from typing import Any, Dict, List, Optional
import anthropic
from homeassistant.core import HomeAssistant, callback
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.typing import ConfigType
from homeassistant.const import CONF_API_KEY
from .const import DOMAIN, EVENT_AI_ACTION, EVENT_AI_ERROR
from .tools import (
    get_entity_state,
    set_entity_state,
    create_automation,
    create_scene,
    get_zigbee_info,
    list_entities,
)

_LOGGER = logging.getLogger(__name__)

class HAClaudeController:
    """Class to handle Claude AI interactions."""

    def __init__(self, hass: HomeAssistant, api_key: str):
        """Initialize the controller."""
        self.hass = hass
        self.client = anthropic.Anthropic(api_key=api_key)
        self.available_tools = [
            {
                "name": "get_entity_state",
                "description": "Get the current state of a Home Assistant entity",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "entity_id": {
                            "type": "string",
                            "description": "The entity ID to query"
                        }
                    },
                    "required": ["entity_id"]
                }
            },
            {
                "name": "set_entity_state",
                "description": "Set the state of a Home Assistant entity",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "entity_id": {"type": "string"},
                        "state": {"type": "string"},
                        "attributes": {"type": "object"}
                    },
                    "required": ["entity_id", "state"]
                }
            },
            {
                "name": "create_automation",
                "description": "Create a new Home Assistant automation",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "trigger": {"type": "object"},
                        "condition": {"type": "object"},
                        "action": {"type": "object"},
                        "description": {"type": "string"}
                    },
                    "required": ["trigger", "action", "description"]
                }
            },
            {
                "name": "create_scene",
                "description": "Create a new scene in Home Assistant",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "entities": {"type": "object"}
                    },
                    "required": ["name", "entities"]
                }
            },
            {
                "name": "get_zigbee_info",
                "description": "Get information about Zigbee devices",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "device_id": {
                            "type": "string",
                            "description": "Optional device ID to get specific device info"
                        }
                    }
                }
            },
            {
                "name": "list_entities",
                "description": "List all entities or entities of a specific domain",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "domain": {
                            "type": "string",
                            "description": "Optional domain to filter entities"
                        }
                    }
                }
            }
        ]

    async def process_request(self, user_input: str) -> Dict[str, Any]:
        """Process a user request through Claude."""
        try:
            message = await self.client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=1024,
                temperature=0,
                tools=self.available_tools,
                messages=[{"role": "user", "content": user_input}]
            )

            # Process tool calls if any
            if message.tool_calls:
                for tool_call in message.tool_calls:
                    tool_result = await self._execute_tool(tool_call)
                    # Fire event for UI updates
                    self.hass.bus.fire(EVENT_AI_ACTION, {
                        "tool": tool_call.name,
                        "input": tool_call.parameters,
                        "result": tool_result
                    })

            return {"success": True, "response": message.content}

        except Exception as e:
            _LOGGER.error("Error processing AI request: %s", str(e))
            self.hass.bus.fire(EVENT_AI_ERROR, {"error": str(e)})
            return {"success": False, "error": str(e)}

    async def _execute_tool(self, tool_call: Any) -> Any:
        """Execute a tool call from Claude."""
        tool_name = tool_call.name
        parameters = json.loads(tool_call.parameters)

        tool_mapping = {
            "get_entity_state": get_entity_state,
            "set_entity_state": set_entity_state,
            "create_automation": create_automation,
            "create_scene": create_scene,
            "get_zigbee_info": get_zigbee_info,
            "list_entities": list_entities,
        }

        if tool_name in tool_mapping:
            return await tool_mapping[tool_name](self.hass, **parameters)
        else:
            raise ValueError(f"Unknown tool: {tool_name}")

async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the AI Controller component."""
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up AI Controller from a config entry."""
    api_key = entry.data[CONF_API_KEY]
    
    controller = HAClaudeController(hass, api_key)
    hass.data[DOMAIN] = controller

    # Register the WebSocket API
    hass.components.websocket_api.async_register_command(
        "ai_controller/process_request",
        handle_process_request,
        {
            "type": "object",
            "properties": {
                "input": {"type": "string"}
            },
            "required": ["input"]
        }
    )

    return True

@callback
async def handle_process_request(hass, connection, msg):
    """Handle WebSocket API requests."""
    controller: HAClaudeController = hass.data[DOMAIN]
    result = await controller.process_request(msg["input"])
    connection.send_result(msg["id"], result)
