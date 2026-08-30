# Dev-Review Cycle Monitor

This microservice monitors and enforces the 120-minute cycle timeboxes for Developer Agent iterations.

- **Cycle Duration**: 120 minutes
- **Warning Threshold**: 90 minutes (alerts sent to `orca.alerts.ops`)
- **Action on Breach**: Requires Developer to post a WIP PR and request Manager directive.
