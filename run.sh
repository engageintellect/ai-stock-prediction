#!/usr/bin/env bash

source venv/bin/activate
uvicorn main_v3:app --reload
