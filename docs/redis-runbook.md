# Redis Troubleshooting Runbook

## Symptoms

Common Redis-related symptoms include:

- Increased API latency
- Redis timeout errors
- Connection pool exhaustion
- Increased request failures

## Investigation

When Redis timeout errors occur:

1. Check Redis latency.
2. Check active connections.
3. Check connection pool utilization.
4. Check application logs.
5. Check whether a recent deployment changed Redis configuration.

## Connection Pool

If the Redis connection pool is exhausted, requests may wait
for an available connection.

This can significantly increase API latency.

The normal Payment Service Redis connection pool size is 50.

## Known Failure Pattern

A Redis connection pool that is too small can cause:

- Connection timeout
- Increased API latency
- Request failures
- Thread/request queue buildup