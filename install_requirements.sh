#!/bin/bash
set -e
source venv/bin/activate
pip install -r api/requirements.txt --no-cache-dir
deactivate
