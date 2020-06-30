#!/bin/sh


set -o errexit
set -o nounset



while python check_db.py; do echo 'connecting to database...'; sleep 2; done;

echo ". . . . . Database Connection Is Done! . . . . ."




echo ". . . . . Web Boot Up Is Done! . . . "

uvicorn run_app:app --host "0.0.0.0" --port 80 --reload --ws 'auto' \
--loop 'auto' --workers 8