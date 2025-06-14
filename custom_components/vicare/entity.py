"""Entities for the ViCare integration."""

from PyViCare2.PyViCareDevice import Device as PyViCareDevice
from PyViCare2.PyViCareDeviceConfig import PyViCareDeviceConfig
from PyViCare2.PyViCareHeatingDevice import (
    HeatingDeviceWithComponent as PyViCareHeatingDeviceComponent,
)

from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity import Entity

from .const import DOMAIN


class ViCareEntity(Entity):
    """Base class for ViCare entities."""

    _attr_has_entity_name = True

    def __init__(
        self,
        unique_id_suffix: str,
        device_serial: str | None,
        device_config: PyViCareDeviceConfig,
        device: PyViCareDevice,
        component: PyViCareHeatingDeviceComponent | None = None,
    ) -> None:
        """Initialize the entity."""
        gateway_serial = device_config.getConfig().serial
        device_id = device_config.getId()
        model = device_config.getModel().replace("_", " ")

        identifier = (
            f"{gateway_serial}_{device_serial.replace('zigbee-', 'zigbee_')}"
            if device_serial is not None
            else f"{gateway_serial}_{device_id}"
        )

        self._api: PyViCareDevice | PyViCareHeatingDeviceComponent = (
            component if component else device
        )
        self._attr_unique_id = f"{identifier}-{unique_id_suffix}"
        if component:
            self._attr_unique_id += f"-{component.id}"

        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, identifier)},
            serial_number=device_serial,
            name=model,
            manufacturer="Viessmann",
            model=model,
            configuration_url="https://developer.viessmann.com/",
        )
