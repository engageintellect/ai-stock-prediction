#!/usr/bin/env bash

source venv/bin/activate
uvicorn main_v3:app --host '0.0.0.0' --port '6969' --reload
