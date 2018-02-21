#!/usr/bin/env python3

"""
    Python script to run a test server.
"""
from app import app

app.run(host='0.0.0.0', port=8000)
