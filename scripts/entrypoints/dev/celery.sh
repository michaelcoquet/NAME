#!/bin/sh
celery -A NAME worker --concurrency=20 --loglevel=info