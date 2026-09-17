# Incident 101

## Service

payment-service

## Symptoms

The Payment Service experienced:

- P95 latency of 2.5 seconds
- Increased request failures
- Redis timeout errors
- Increased request queueing

## Investigation

Engineers found that the Redis connection pool was exhausted.

The connection pool was configured with only 20 connections.

The normal configuration is 50 connections.

## Root Cause

A configuration change reduced the Redis connection pool from
50 to 20 connections.

The smaller pool was insufficient during increased traffic.

## Resolution

The Redis connection pool was increased from 20 to 50 connections.

After the change:

- Redis timeouts disappeared
- P95 latency returned below 500ms
- Request failures returned to normal levels