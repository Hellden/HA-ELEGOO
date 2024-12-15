from datetime import datetime
import logging

from homeassistant.core import HomeAssistant, callback
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.components.sensor import SensorEntity
from homeassistant.const import UnitOfTime
from homeassistant.components.sensor import (
    SensorEntity,
    SensorDeviceClass,
    SensorStateClass,
)
from homeassistant.helpers.event import async_track_time_interval

_LOGGER = logging.getLogger(__name__)


async def async_setup_platform(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
    discovery_info=None,  # pylint: disable=unused-argument
):

    _LOGGER.debug("Calling async_setup_entry entry=%s", entry)

    entity = TutoHacsElapsedSecondEntity(hass, entry)
    async_add_entities([entity], True)


class TutoHacsElapsedSecondEntity(SensorEntity):
    _hass = HomeAssistant

    def __init__(
        self,
        hass: HomeAssistant,  # pylint: disable=unused-argument
        entry_infos,  # pylint: disable=unused-argument
    ) -> None:
        """Initisalisation de notre entité"""
        self._hass = hass
        self._attr_name = entry_infos.get("name")
        self._attr_unique_id = entry_infos.get("entity_id")
        self._attr_has_entity_name = True
        self._attr_native_value = 12

        @property
        def icon(self) -> str | None:
            return "mdi:timerplay"

        @property
        def device_class(self) -> SensorDeviceClass | None:
            return SensorDeviceClass.DURATION

        @property
        def state_class(self) -> SensorStateClass | None:
            return SensorStateClass.MEASUREMENT

        @property
        def native_unif_of_measurement(self) -> str | None:
            return UnitOfTime.SECONDS

        @property
        def shoud_poll(self) -> bool:
            return False

    @callback
    async def async_added_to_hass(self) -> None:
        # Arme le timer
        timer_cancel = async_track_time_interval(
            self._hass,
            self.incremente_secondes,  # la méthode qui sera appelée toutes les secondes
            interval=timedelta(seconds=1),
        )
        # desarme le timer lors de la destruction de l'entité
        self.async_on_remove(timer_cancel)

    @callback
    async def incremente_secondes(self, _):
        """Cette méthode va être appelée toutes les secondes"""
        _LOGGER.info("Appel de incremente_secondes à %s", datetime.now())
