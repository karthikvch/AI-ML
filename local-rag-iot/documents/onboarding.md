# Device Onboarding

A new edge device must be securely registered before it can communicate with the platform.

The onboarding process consists of:

1. Device registration
2. Claim code validation
3. Device identity creation
4. Certificate generation
5. Secure MQTT connection
6. Initial heartbeat

After successful onboarding, the platform should mark the device as online after receiving its heartbeat.