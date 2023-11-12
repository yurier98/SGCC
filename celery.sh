#!/usr/bin/env sh

celery -A config worker -l INFO
