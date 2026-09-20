#!/usr/bin/env python3
"""
Health check script for Flask application
Verifies that the Flask app is running and database is accessible
"""

import sys
import urllib.request
import urllib.error

def check_health():
    """Check application health by making a request to /"""
    try:
        response = urllib.request.urlopen('http://localhost:5004/', timeout=5)
        if response.status == 200:
            return 0  # Healthy
        else:
            print(f"Unexpected status code: {response.status}")
            return 1  # Unhealthy
    except urllib.error.HTTPError as e:
        # HTTPError doesn't return a value, it raises an exception
        print(f"HTTP Error: {e.code}")
        return 1  # Unhealthy
    except urllib.error.URLError as e:
        print(f"URL Error: {e.reason}")
        return 1  # Unhealthy
    except Exception as e:
        print(f"Health check failed: {type(e).__name__}: {e}")
        return 1  # Unhealthy

if __name__ == '__main__':
    sys.exit(check_health())
