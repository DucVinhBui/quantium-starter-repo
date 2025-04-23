#!/bin/bash

source venv/bin/activate

python -m pytest test_app.py

status=$?

if [ $status -eq 0 ]; then
    echo "✅ All tests passed."
    exit 0
else
    echo "❌ Some tests failed."
    exit 1
fi
