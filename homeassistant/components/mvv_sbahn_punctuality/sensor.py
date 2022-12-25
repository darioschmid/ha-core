"""Platform for sensor integration."""
from __future__ import annotations

from datetime import timedelta

import voluptuous as vol

from homeassistant.components.sensor import (
    PLATFORM_SCHEMA,
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.const import CONF_NAME, PERCENTAGE
from homeassistant.core import HomeAssistant
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

CONF_PUNCTUALITY = "punctuality"

CONF_LINE = "line"

ICON = "mdi:train"

ATTRIBUTION = "Data provided by mvv.de"

SCAN_INTERVAL = timedelta(seconds=30)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_PUNCTUALITY): [
            {
                vol.Required(CONF_LINE): cv.string,
                vol.Optional(CONF_NAME): cv.string,
            }
        ]
    }
)


def setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None,
) -> None:
    """Set up the sensor platform."""
    sensors = []
    for punctuality in config[CONF_PUNCTUALITY]:
        sensors.append(
            MvvSbahnSensor(
                punctuality.get(CONF_LINE),
                punctuality.get(CONF_NAME),
            )
        )
    add_entities(sensors, True)


class MvvSbahnSensor(SensorEntity):
    """Representation of a Sensor."""

    _attr_attribution = ATTRIBUTION

    def __init__(
        self,
        line,
        name,
    ):
        """Initialize the sensor."""
        self._line = line
        self._name = name
        self._state = None
        self._icon = ICON

    _attr_name = "S-Bahn Example"
    _attr_native_unit_of_measurement = PERCENTAGE
    _attr_device_class = SensorDeviceClass.HUMIDITY
    _attr_state_class = SensorStateClass.MEASUREMENT

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def icon(self):
        """Icon to use in the frontend, if any."""
        return self._icon

    @property
    def native_unit_of_measurement(self):
        """Return the unit this state is expressed in."""
        return PERCENTAGE

    def update(self) -> None:
        """Fetch new state data for the sensor.

        This is the only method that should fetch new data for Home Assistant.
        """
        self._attr_native_value = 17
