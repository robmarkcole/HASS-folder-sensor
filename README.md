# HASS-folder-sensor
Home-assistant custom component for monitoring the contents of a folder.

To use this custom component, add the custom_components folder to your root config folder [following the docs](https://home-assistant.io/developers/platform_example_sensor/). Note that folder paths must be added to [whitelist_external_dirs](https://home-assistant.io/docs/configuration/basic/).Then add to your config:

```yaml
homeassistant:
  whitelist_external_dirs:
    - /share/

sensor:
  - platform: folder
    folder: /share/motion
    filter: '*capture.jpg'
  - platform: folder
    folder: /config
```

Configuration variables:

- **folder** (*Required*): The folder path
- **filter** (*Optional*): Optional filter

#### Command line equivalent
Note that the basic functionality is identical to a command line sensor with the following config:
```yaml
sensor:
  - platform: command_line
    name: new_image
    command: "ls /share/motion -Art | tail -n -3 | grep 'capture.jpg'"
```

Adding file watching will require watchdog as per https://github.com/home-assistant/home-assistant/pull/12866#pullrequestreview-100987902
