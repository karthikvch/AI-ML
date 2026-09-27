# MQTT Troubleshooting

MQTT is used by edge devices to communicate with the MQTT broker.

## Device cannot connect

If an edge device cannot connect to MQTT, check the following:

1. Verify that the device has network connectivity.
2. Verify that the MQTT broker is reachable.
3. Verify the MQTT port.
4. Check the device certificate.
5. Check whether the certificate has expired.
6. Verify the device private key.
7. Check TLS configuration.
8. Review MQTT client logs.

## Device disconnects frequently

Frequent MQTT disconnections may be caused by:

- Network instability
- Broker availability problems
- TLS certificate issues
- Incorrect keepalive configuration
- Client connection timeout
- Resource constraints on the edge device

## Heartbeat

The device should periodically publish a heartbeat message.

If heartbeat messages stop, check:

- MQTT connection
- Device network
- Edge agent status
- Device CPU and memory