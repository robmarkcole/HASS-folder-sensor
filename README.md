# HASS-folder-sensor
Home-assistant custom component for monitoring the contents of a folder.
The state of the sensor is the time that the most recently modified file in a folder was modified.
The use case is detecting when a file in a folder is created or updated. For example, I have a USB camera attached to my
HA instance that saves a timestamped photo when [motion](https://github.com/HerrHofrat/hassio-addons/tree/master/motion) is detected. This sensor allows me to detect when another image is saved, and
exposes the name of that new image file. The number of files in the folder and the names of those files are exposed as attributes.

To use this custom component, add the custom_components folder to your root config folder [following the docs](https://home-assistant.io/developers/platform_example_sensor/). Then add to your config:

```yaml
sensor:
  - platform: folder
    folder: /Users/robincole/Pictures/
    filter: '*.jpg'
  - platform: folder
    folder: /Users/robincole/Google Drive
    filter: '*.txt'
```

Configuration variables:

- **folder** (*Required*): The folder path
- **filter** (*Optional*): Optional filter
