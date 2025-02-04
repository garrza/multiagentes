#!/bin/bash
cd "$(dirname "$0")"
PYTHONPATH=.:$(dirname "$0")/.. python3 main.py
