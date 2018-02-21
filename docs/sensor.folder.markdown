---
layout: page
title: "folder sensor"
description: "Sensor for monitoring the contents of a folder."
date: 2018-02-21 14:00
sidebar: true
comments: false
sharing: true
footer: true
logo: file.png
ha_category: Sensor
ha_iot_class: "Local Polling"
ha_release: 0.64
---

Sensor for monitoring the contents of a folder. Note that folder paths must be added to [whitelist_external_dirs](https://home-assistant.io/docs/configuration/basic/). Optionally a [wildcard filter]((http://tldp.org/LDP/GNU-Linux-Tools-Summary/html/x11655.htm)) can be applied to the files considered within the folder. The state of the sensor is the size in MB of files within the folder that meet the filter criteria. The number of filtered files in the folder and total size in bytes of those files are exposed as attributes.

```yaml
sensor:
  - platform: folder
    folder: /config
```

{% configuration %}
folder:
  description: The folder path
  required: true
  type: string
filter:
  description: Filter to apply
  required: false
  default: `*`
  type: string
{% endconfiguration %}
