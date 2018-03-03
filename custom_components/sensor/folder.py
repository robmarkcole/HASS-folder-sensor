"""
Sensor for monitoring the contents of a folder.

For more details about this platform, refer to the documentation at
https://home-assistant.io/components/sensor.folder/
"""
import datetime
from datetime import timedelta
import glob
import logging
import os

import voluptuous as vol

from homeassistant.helpers.entity import Entity
import homeassistant.helpers.config_validation as cv
from homeassistant.components.sensor import PLATFORM_SCHEMA

_LOGGER = logging.getLogger(__name__)

CONF_FOLDER_PATHS = 'folder'
CONF_FILTER = 'filter'
DEFAULT_FILTER = '*'

SCAN_INTERVAL = timedelta(seconds=1)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_FOLDER_PATHS): cv.isdir,
    vol.Optional(CONF_FILTER, default=DEFAULT_FILTER): cv.string,
})


def get_timestamp(file_path):
    """Return the timestamp of file."""
    mtime = os.stat(file_path).st_mtime
    return datetime.datetime.fromtimestamp(mtime).isoformat()


def get_files_list(folder_path, filter_term):
    """Return the list of file paths, applying filter."""
    query = folder_path + filter_term
    files_list = glob.glob(query)
    files_list = [f for f in files_list if os.path.isfile(f)]
    return files_list


def get_size(files_list):
    """Return the sum of the size in bytes of files in the list."""
    size_list = [os.stat(f).st_size for f in files_list]
    return sum(size_list)


def setup_platform(hass, config, add_devices, discovery_info=None):
    """Set up the folder sensor."""
    path = config.get(CONF_FOLDER_PATHS)

    if not hass.config.is_allowed_path(path):
        _LOGGER.error("folder %s is not valid or allowed", path)
    else:
        folder = Folder(path, config.get(CONF_FILTER), hass)
        add_devices([folder], True)


class Folder(Entity):
    """Representation of a folder."""

    ICON = 'mdi:folder'

    def __init__(self, folder_path, filter_term, hass):
        """Initialize the data object."""
        folder_path = os.path.join(folder_path, '')  # If no trailing / add it
        self._folder_path = folder_path   # Need to check its a valid path
        self._filter_term = filter_term
        self._hass = hass
        self._number_of_files = None
        self._files_dict = {}
        self._size = None
        self._name = os.path.split(os.path.split(folder_path)[0])[1]
        self._unit_of_measurement = 'MB'

    def update(self):
        """Update the sensor."""
        current_files = get_files_list(self._folder_path, self._filter_term)
        self._number_of_files = len(current_files)
        self._size = get_size(current_files)

        deleted_files = []
        added_files = []
        modified_files = []
        previous_files = list(self._files_dict.keys())

        for file_path in current_files:
            file_name = os.path.split(file_path)[-1]
            file_mtime = get_timestamp(file_path)

            if file_path not in self._files_dict:
                added_files.append(file_name)
                self._hass.bus.fire('file_added', {'file': file_name})
                self._files_dict[file_path] = file_mtime  # Add the entry

            elif (file_path in self._files_dict and  # If exists and modified
                    self._files_dict[file_path] != file_mtime):
                        modified_files.append(file_name)
                        self._hass.bus.fire(
                            'file_modified', {'file': file_name})
                        self._files_dict[file_path] = file_mtime  # Reassign

        # Check if any files deleted
        deleted_files = list(set(previous_files) - set(current_files))
        for file_path in deleted_files:
            file_name = os.path.split(file_path)[-1]
            self._hass.bus.fire('file_deleted', {'file': file_name})
            self._files_dict.pop(file_path, None)

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self):
        """Return the state of the sensor."""
        decimals = 2
        size_mb = round(self._size/1e6, decimals)
        return size_mb

    @property
    def icon(self):
        """Icon to use in the frontend, if any."""
        return self.ICON

    @property
    def device_state_attributes(self):
        """Return other details about the sensor state."""
        attr = {
            'path': self._folder_path,
            'filter': self._filter_term,
            'number_of_files': self._number_of_files,
            'bytes': self._size,
            }
        return attr

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement of this entity, if any."""
        return self._unit_of_measurement
