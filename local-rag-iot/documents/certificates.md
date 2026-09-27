# Device Certificate Troubleshooting

Edge devices use certificates to establish secure communication with the MQTT broker.

## Certificate problems

If the device cannot establish an MQTT TLS connection:

1. Check certificate expiration.
2. Verify the certificate chain.
3. Verify the certificate subject.
4. Verify the private key.
5. Verify that the CA certificate is trusted.
6. Check system time on the device.

An incorrect system clock can cause a valid certificate to appear invalid.

## Certificate renewal

Devices should renew certificates before expiration.

Certificate renewal should not interrupt device communication unnecessarily.