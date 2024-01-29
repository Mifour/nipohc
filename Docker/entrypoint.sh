#!/bin/sh

cd nipohc_app/
pip install -r requirements.txt

exec "$@"
