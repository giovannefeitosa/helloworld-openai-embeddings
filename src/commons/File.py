import json
import os


class File:
    def readFile(self, file):
        with open(file, 'r') as f:
            return f.read()

    def readJsonFile(self, file):
        with open(file, 'r') as f:
            return json.load(f)

    def writeFile(self, outputFilePath, data):
        with open(outputFilePath, 'w') as f:
            f.write(json.dumps(data))

    def exists(self, filePath):
        return os.path.exists(filePath)


file = File()
