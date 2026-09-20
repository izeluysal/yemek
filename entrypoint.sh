#!/bin/bash
set -e

# Fix ownership for volume mounts
# Container root olarak başlar, volume mount'larının sahipliğini otomatik onarıp
# gosu ile ecedocappuser'a düşer
if [ "$(id -u)" = "0" ]; then
    # Yemekfiles klasörü sahipliğini düzelt
    if [ -d "/app/yemekfiles" ]; then
        chown -R ecedocappuser:ecedocappuser /app/yemekfiles
    fi
    
    # Data klasörü sahipliğini düzelt
    if [ -d "/app/data" ]; then
        chown -R ecedocappuser:ecedocappuser /app/data
    fi
    
    # gosu ile ecedocappuser'a düş
    exec gosu ecedocappuser "$@"
else
    exec "$@"
fi
