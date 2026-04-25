#!/bin/bash
# Direct wizard runner (assumes setup already done)
cd "$(dirname "$0")/_core"
python3 .sdd-wizard/src/wizard.py "$@"
