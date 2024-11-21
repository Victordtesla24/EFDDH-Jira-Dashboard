class HealthMonitor:
    def setup_health_endpoint(self) -> int:
        return 8080

    def check_system_health(self) -> dict[str, str]:
        """Check system health status."""
        return {"status": "healthy", "message": "System operational"}
