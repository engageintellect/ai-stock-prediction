#!/usr/bin/env bash


deactivate
source venv/bin/activate
uvicorn main_v2:app --reload