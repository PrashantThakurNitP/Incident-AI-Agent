from mcp.server import MCPServer

# actual MCP server.
# exposes operational tools:

# get_service_metrics
# get_service_logs
# get_deployment_status
# get_database_stats

mcp = MCPServer("Incident Operations Server")


@mcp.tool()
def get_service_metrics(service_name: str) -> dict:
    """
    Get current operational metrics for a service.
    """

    if service_name == "payment-service":
        return {
            "service": "payment-service",
            "p95_latency_ms": 2800,
            "error_rate_percent": 4.2,
            "cpu_percent": 72,
            "redis_connections": 19,
            "redis_pool_size": 20,
        }

    return {
        "service": service_name,
        "p95_latency_ms": 320,
        "error_rate_percent": 0.2,
        "cpu_percent": 40,
    }


@mcp.tool()
def get_service_logs(service_name: str) -> dict:
    """
    Get recent logs for a service.
    """

    if service_name == "payment-service":
        return {
            "service": "payment-service",
            "logs": [
                "Redis connection pool exhausted",
                "Redis timeout while acquiring connection",
                "Request waiting for Redis connection",
                "Payment request latency exceeded 2 seconds",
            ],
        }

    return {
        "service": service_name,
        "logs": [
            "No significant errors found",
        ],
    }
    
@mcp.tool()
def get_deployment_status(service_name: str) -> dict:
    """
    Get the current deployment status and version of a service.
    """

    if service_name == "payment-service":
        return {
            "service": "payment-service",
            "version": "v2.4.1",
            "status": "healthy",
            "deployed_at": "2026-09-17T08:30:00",
            "previous_version": "v2.4.0",
            "deployment_change": "Updated payment processing configuration",
        }

    return {
        "service": service_name,
        "version": "unknown",
        "status": "healthy",
    }
@mcp.tool()
def get_database_stats(service_name: str) -> dict:
    """
    Get current database health and performance statistics.
    """

    if service_name == "payment-service":
        return {
            "service": "payment-service",
            "database": "postgresql",
            "connection_pool_active": 18,
            "connection_pool_max": 50,
            "slow_queries": 0,
            "average_query_latency_ms": 45,
            "status": "healthy",
        }

    return {
        "service": service_name,
        "database": "postgresql",
        "status": "healthy",
    }


if __name__ == "__main__":
    mcp.run()