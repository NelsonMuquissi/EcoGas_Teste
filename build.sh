#!/usr/bin/env bash
echo "� Building EcoGás Admin..."
pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate --noinput
echo "✅ Build completed!"
