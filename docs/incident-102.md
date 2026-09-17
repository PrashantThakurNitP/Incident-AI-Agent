# Incident 102

## Service

payment-service

## Symptoms

The Payment Service experienced:

- CPU utilization above 90%
- Increased API latency
- Database query timeouts
- Increased request failures

## Investigation

A recent deployment introduced a new database query.

The query performed a full table scan on the payment transactions table.

## Root Cause

The database query was missing an index.

This caused high database CPU utilization and increased API latency.

## Resolution

An index was added to the payment transaction table.

The query was optimized.

After deployment:

- Database CPU decreased
- API latency returned to normal
- Query execution time decreased significantly