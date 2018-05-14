"""
Family Hub camera for Samsung Refrigerators.

For more details about this platform, please refer to the documentation
https://home-assistant.io/components/camera.familyhub/
"""
import logging
import voluptuous as vol

import homeassistant.helpers.config_validation as cv
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import (CONF_NAME)
from homeassistant.components.camera import Camera
from homeassistant.helpers.aiohttp_client import async_get_clientsession

_LOGGER = logging.getLogger(__name__)

CONF_IP = 'address'

DEFAULT_NAME = 'FamilyHub Camera'

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_IP): cv.string,
    vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
})

async def async_setup_platform(hass, config, async_add_devices, discovery_info=None):
    """Set up the Family Hub Camera."""
    from .pyfamilyhublocal import FamilyHubCam
    address = config.get(CONF_IP)
    name = config.get(CONF_NAME)

    session = async_get_clientsession(hass)
    family_hub_cam = FamilyHubCam(address, hass.loop, session)

    async_add_devices([FamilyHubCamera(name, family_hub_cam)], True)



class FamilyHubCamera(Camera):

    def __init__(self, name, family_hub_cam):
        super().__init__()
        self._name = name
        self.family_hub_cam = family_hub_cam

    async def camera_image(self):
        """Return a still image response."""
        return await self.family_hub_cam.async_get_cam_image()

    @property
    def name(self):
        return self._name

    @property
    def should_poll(self):
        return False
