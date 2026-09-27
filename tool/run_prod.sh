#!/usr/bin/env bash
# Runs the app against the prod backend. Usage: tool/run_prod.sh -d macos
exec "$(dirname "$0")/run_with_env.sh" prod "$@"
