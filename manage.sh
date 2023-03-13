#!/bin/bash

# This script is used to manage the application

function main() {
    # load environment
    local HERE=$(cd $(dirname "$BASH_SOURCE"); pwd)
    source "$HERE/etc/bash-scripts/lib.sh"
    load_environment_variables
    
    # parse arguments
    local action="$1"
    shift

    case "$action" in
        "install")
            echo "Creating venv..."
            "$PYTHON_ALIAS" -m venv "$VENV_FOLDER"
            echo "Installing dependencies from etc/requirements.txt..."
            "$VENV_FOLDER/bin/pip" install -r "$PROJECT_ROOT/etc/requirements.txt"
            echo "Done."
            ;;
        "*")
            echo "Unknown action: $action"
            exit 1
            ;;
    esac
}

( main "$@" )