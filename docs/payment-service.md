# Payment Service

The Payment Service is responsible for processing payment authorization
requests.

## Architecture

The Payment Service communicates with:

- Redis
- PostgreSQL
- Payment Gateway
- Apache Kafka

## Performance

Normal P95 API latency is below 500ms.

If P95 latency exceeds 2 seconds, engineers should investigate:

1. Redis latency
2. Database connection pool utilization
3. CPU utilization
4. Recent deployments
5. Downstream payment gateway latency

## Retry Policy

Payment requests are retried three times.

Initial retry delay is 500 milliseconds.

Maximum retry delay is 5 seconds.

## Circuit Breaker

The circuit breaker opens after 5 consecutive failures.

## Redis

Redis is used for:

- Payment session data
- Idempotency keys
- Frequently accessed payment metadata

Redis connection pool size is normally configured to 50 connections.