#!/bin/bash

# Activa el entorno virtual y levanta el servidor con autoreload
poetry run uvicorn app.main:app --reload --app-dir src