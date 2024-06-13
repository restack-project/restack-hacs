"""Platform for switch integration."""

from __future__ import annotations

import typing

from homeassistant.components.switch import SwitchEntity, SwitchEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfTemperature
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import EntityCategory, EntityDescription
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

from .const import DOMAIN
from . import ReStackDataUpdateCoordinator
from .entity import ReStackEntity
from .utils import format_entity_name

JsonDictType = typing.Dict[str, typing.Any]


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the ReStack switches."""
    coordinator: ReStackDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(
        ReStackSwitch(
            coordinator,
            SwitchEntityDescription(
                key=str(stack["name"]),
                name=stack["name"],
                entity_category=EntityCategory.DIAGNOSTIC,
                device_class="restack__stacks",
            ),
            stack=stack,
        )
        for stack in coordinator.data
    )


class ReStackSwitch(ReStackEntity, SwitchEntity):
    """Representation of a ReStack switch."""

    def __init__(
        self,
        coordinator: ReStackDataUpdateCoordinator,
        description: EntityDescription,
        stack: JsonDictType,
    ) -> None:
        """Set entity ID."""
        super().__init__(coordinator, description, stack)
        self.entity_id = f"switch.restack_{format_entity_name(self.stack['name'])}"

    @property
    def is_on(self):
        """If the switch is currently on or off."""
        if self.stack["lastJob"]:
            return self.stack["lastJob"]["state"] == "Running"

        return False

    async def async_turn_on(self, **kwargs):
        """Turn the switch on."""
        await self.coordinator.api.execute(self.stack["id"])

    # def turn_off(self, **kwargs):
    #     """Turn the switch off."""
    #     self._is_on = False
