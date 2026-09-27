#!/usr/bin/env bash
# Runs the app against the dev backend. Usage: tool/run_dev.sh -d macos
exec "$(dirname "$0")/run_with_env.sh" dev "$@"
