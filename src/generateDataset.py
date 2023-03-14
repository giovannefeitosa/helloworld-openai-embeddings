# Command:
#   bash manage.sh prepare <txt_file>
#
# This command will create a dataset.json file containing a list of questions and answers
# in json format. This file will be used to generate embeddings.
#
#   io/generated/dataset.json
#
import sys
import os
import spacy
import json
from commons.Configs import configs
from commons.OpenAIClient import openaiClient
from commons.File import file
from prepareutils.Dataset import dataset
import openai
from tqdm import tqdm


def main(inputFilePath):
    """
        Command:
            bash manage.sh prepare <txt_file> <output_file>

        Transforms the input file into a dataset file
    """
    # Generating io/generated/dataset.json
    if not file.exists(configs.generatedDatasetPath):
        dataset.generateDatasetFromFile(
            inputFile=inputFilePath,
            outputFile=configs.generatedDatasetPath,
        )


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Error: missing arguments")
        print("Usage: bash manage.py prepare <input_file_path>\n")
        sys.exit(1)
    # read arguments
    inputFilePath = sys.argv[1]
    # process
    main(inputFilePath)
