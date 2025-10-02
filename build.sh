#!/usr/bin/env bash
echo "íº€ Building EcoGÃ¡s Admin..."
pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate --noinput
echo "âœ… Build completed!"
