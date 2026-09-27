# Device Heartbeat

The heartbeat indicates that an edge device is alive and communicating with the platform.

A healthy device periodically publishes heartbeat messages.

If the platform stops receiving heartbeats:

1. Check MQTT connectivity.
2. Check network connectivity.
3. Check whether the edge agent is running.
4. Check CPU and memory usage.
5. Check device logs.
6. Check whether an OTA update occurred immediately before the heartbeat stopped.

A device should not be considered healthy only because it was previously connected. The platform should use the latest heartbeat to determine device availability.