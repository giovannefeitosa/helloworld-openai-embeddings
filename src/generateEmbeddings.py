# Command:
#   bash manage.sh prepare <txt_file>
# --------------------------------------------------
# This command will create a embeddings.json file containing a list of questions and answers
# in json format (arrays of numbers). This file will be used to train the model.
#
#   io/generated/embeddings.json
#
import sys
from commons.Configs import configs
from commons.File import file
from prepareutils.Embeddings import embeddings

if __name__ == "__main__":
    # Generate io/generated/embeddings.json
    if not file.exists(configs.generatedEmbeddingsPath):
        embeddings.generateEmbeddings()
