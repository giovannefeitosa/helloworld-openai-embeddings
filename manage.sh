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
        # Install the dependencies into a .venv folder
        "install")
            echo "Creating venv..."
            "$PYTHON_ALIAS" -m venv "$VENV_FOLDER"
            echo "Installing dependencies from etc/requirements.txt..."
            "$VENV_FOLDER/bin/pip" install -r "$PROJECT_ROOT/etc/requirements.txt"
            echo "Installing spacy language model..."
            "$PYTHON_ALIAS" -m spacy download en_core_web_sm
            echo "Done."
            ;;
        # generate dataset and embeddings
        "prepare")
            source "$VENV_FOLDER/bin/activate"
            "$PYTHON_ALIAS" "$PROJECT_ROOT/src/generateDataset.py" "$@" || exit 1
            "$PYTHON_ALIAS" "$PROJECT_ROOT/src/generateEmbeddings.py" "$@" || exit 1
            ;;
        # ask a question
        "ask")
            source "$VENV_FOLDER/bin/activate"
            "$PYTHON_ALIAS" "$PROJECT_ROOT/src/ask.py" "$@"
            ;;
        # train the model
        "train")
            source "$VENV_FOLDER/bin/activate"
            "$PYTHON_ALIAS" "$PROJECT_ROOT/src/train.py" "$@"
            ;;
        # starts a demo webserver
        "serve")
            source "$VENV_FOLDER/bin/activate"
            "$PYTHON_ALIAS" "$PROJECT_ROOT/src/serve.py" "$@"
            ;;
        # runs a prompt in Chat completion api
        "prompt")
            source "$VENV_FOLDER/bin/activate"
            "$PYTHON_ALIAS" "$PROJECT_ROOT/src/run-prompt.py" "$@"
            ;;
        "ci")
            # rm -f "$PROJECT_ROOT/io/generated/dataset.json" "$PROJECT_ROOT/io/generated/embeddings.json" "$PROJECT_ROOT/io/generated/model.sklearn"
            rm -f "$PROJECT_ROOT/io/generated/embeddings.json" "$PROJECT_ROOT/io/generated/model.sklearn"
            bash manage.sh prepare io/data/original-sample.txt || exit 1
            bash manage.sh train || exit 1
            echo "------------------------"
            echo "How many goals did Pelé score in his career?"
            bash manage.sh ask "How many goals did Pelé score in his career?" # expect like 1,279 goals in 1,363 games
            echo "What is the opposite of Pelé?"
            bash manage.sh ask "What is the opposite of Pelé?" # expect i don't know

            ;;
        *)
            echo "Unknown action: $action"
            exit 1
            ;;
    esac
}

( main "$@" )
