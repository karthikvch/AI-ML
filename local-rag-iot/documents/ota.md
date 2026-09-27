# OTA Troubleshooting

OTA allows firmware or software packages to be remotely deployed to edge devices.

## OTA update failed

If an OTA update fails:

1. Check whether the device downloaded the package.
2. Verify available disk space.
3. Verify package integrity.
4. Check the OTA agent logs.
5. Verify the device firmware compatibility.
6. Check whether the device restarted after installation.

## Device offline after OTA

If the device becomes offline after an OTA update:

1. Check whether the OTA installation completed.
2. Check the device reboot status.
3. Check the edge agent status.
4. Check MQTT connectivity.
5. Check device certificates.
6. Review logs immediately before and after the OTA update.

An OTA update should not be considered successful only because the package was downloaded. The device should reconnect and report a healthy heartbeat after installation.