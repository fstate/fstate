#!/bin/bash
#cd parrticleparser
#python parse_particle.py
#cd ../decaydecparser
#python parser.py
#cd ../createdatabase
#python make_fstates.py
#cd ../web

# Prepare log files and start outputting logs to stdout
touch gunicorn.log
touch access.log
tail -n 0 -f *.log &

# Start Gunicorn processes
echo Starting Gunicorn.
exec gunicorn web.server:app \
    --name app \
    --bind 0.0.0.0:5000 \
    --workers 3 \
    --log-level=info \
    --log-file=gunicorn.log \
    --access-logfile=access.log \
    "$@"