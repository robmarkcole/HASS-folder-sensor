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


#### Hassio
In my testing of this custom component with Hassio, I ran into an issue related to permissions. It appears you may need to add folders (other than **config**) to the whitelist_external_dirs. As per [this thread](https://community.home-assistant.io/t/hassio-share-directory-access/41617/11), a reboot of the hardware (not just restart of HA) is required for the following to take effect:
```yaml
homeassistant:
  whitelist_external_dirs:
    - /share
```
After reboot, the component should just work without permissions errors.

**UPDATE**: this wasn't required on my last Hassio install at HA 0.62.1.
