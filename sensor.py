from homeassistant.helpers.entity import Entity
from .schedule_generator import get_average_on_time

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    async_add_entities([LoggingScheduleSensor(hass)])

class LoggingScheduleSensor(Entity):
    def __init__(self, hass):
        self._hass = hass
        self._state = None

    @property
    def name(self):
        return "Suggested Keukenlamp Tijd"

    @property
    def state(self):
        return self._state

    async def async_update(self):
        time = await self._hass.async_add_executor_job(
            get_average_on_time,
            self._hass,
            "light.keuken",  # <- pas deze entiteit aan voor tests
            18,
            23
        )
        self._state = time or "geen data"
