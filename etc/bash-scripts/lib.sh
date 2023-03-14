#!#####################################################################
#! THIS FILE SHOULD BE SOURCED BY OTHER SCRIPTS, NOT EXECUTED DIRECTLY
#!#####################################################################

function load_environment_variables() {
    local HERE=$(cd $(dirname "$BASH_SOURCE"); pwd)

    # default environment variables
    export PROJECT_ROOT=$(cd "$HERE/../.."; pwd)
    export VENV_FOLDER="$PROJECT_ROOT/.venv"
    if [ -d "$VENV_FOLDER" ]; then
        # if we have venv folder, use python and pip from there
        export PYTHON_ALIAS="$VENV_FOLDER/bin/python"
        export PIP_ALIAS="$VENV_FOLDER/bin/pip"
    else
        # if not, we check if we have to use python3/pip3 or python/pip command aliases
        if [ -z "$(which python3)" ]; then
            export PYTHON_ALIAS="python"
            export PIP_ALIAS="pip"
        else
            export PYTHON_ALIAS="python3"
            export PIP_ALIAS="pip3"
        fi
    fi
    
    # requires the .env file to exist
    if [ ! -f "$PROJECT_ROOT/.env" ]; then
        echo "ERROR: Missing environment file: $PROJECT_ROOT/.env"
        exit 1
    fi

    # load env file
    set -a
    source "$PROJECT_ROOT/.env"
    set +a
}
