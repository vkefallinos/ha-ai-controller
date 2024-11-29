"""Tools for the Home Assistant AI Controller."""
from typing import Any, Dict, Optional
from homeassistant.core import HomeAssistant
from homeassistant.helpers import entity_registry as er
from homeassistant.helpers import device_registry as dr
from homeassistant.const import ATTR_ENTITY_ID
import voluptuous as vol

async def get_entity_state(hass: HomeAssistant, entity_id: str) -> Dict[str, Any]:
    """Get the current state of an entity."""
    state = hass.states.get(entity_id)
    if state is None:
        raise ValueError(f"Entity {entity_id} not found")
    return {
        "state": state.state,
        "attributes": dict(state.attributes)
    }

async def set_entity_state(
    hass: HomeAssistant,
    entity_id: str,
    state: str,
    attributes: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """Set the state of an entity."""
    attributes = attributes or {}
    await hass.services.async_call(
        domain=entity_id.split(".")[0],
        service="turn_on" if state == "on" else "turn_off",
        target={ATTR_ENTITY_ID: entity_id},
        service_data=attributes
    )
    return {"success": True}

async def create_automation(
    hass: HomeAssistant,
    trigger: Dict[str, Any],
    action: Dict[str, Any],
    description: str,
    condition: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """Create a new automation."""
    automation_data = {
        "description": description,
        "trigger": trigger,
        "action": action
    }
    if condition:
        automation_data["condition"] = condition

    await hass.services.async_call(
        "automation",
        "create",
        service_data=automation_data
    )
    return {"success": True, "automation": automation_data}

async def create_scene(
    hass: HomeAssistant,
    name: str,
    entities: Dict[str, Any]
) -> Dict[str, Any]:
    """Create a new scene."""
    scene_data = {
        "name": name,
        "entities": entities
    }
    await hass.services.async_call(
        "scene",
        "create",
        service_data=scene_data
    )
    return {"success": True, "scene": scene_data}

async def get_zigbee_info(
    hass: HomeAssistant,
    device_id: Optional[str] = None
) -> Dict[str, Any]:
    """Get information about Zigbee devices."""
    device_registry = dr.async_get(hass)
    
    if device_id:
        device = device_registry.async_get(device_id)
        if not device:
            raise ValueError(f"Device {device_id} not found")
        return {
            "id": device.id,
            "name": device.name,
            "model": device.model,
            "manufacturer": device.manufacturer,
            "connections": [list(c) for c in device.connections],
        }
    
    # Get all Zigbee devices
    zigbee_devices = []
    for device in device_registry.devices.values():
        if any(c[0] == "zigbee" for c in device.connections):
            zigbee_devices.append({
                "id": device.id,
                "name": device.name,
                "model": device.model,
                "manufacturer": device.manufacturer,
            })
    
    return {"devices": zigbee_devices}

async def list_entities(
    hass: HomeAssistant,
    domain: Optional[str] = None
) -> Dict[str, Any]:
    """List all entities or entities of a specific domain."""
    entity_registry = er.async_get(hass)
    
    entities = []
    for entity in entity_registry.entities.values():
        if domain and entity.domain != domain:
            continue
        entities.append({
            "entity_id": entity.entity_id,
            "name": entity.name,
            "domain": entity.domain,
            "device_id": entity.device_id,
        })
    
    return {"entities": entities}
