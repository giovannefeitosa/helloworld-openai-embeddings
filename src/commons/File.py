import json


class File:
    def readFile(self, file):
        with open(file, 'r') as f:
            return f.read()

    def writeFile(self, outputFilePath, data):
        with open(outputFilePath, 'w') as f:
            f.write(json.dumps(data))

    def exists(self, filePath):
        try:
            with open(filePath, 'r') as f:
                return True
        except FileNotFoundError:
            return False


file = File()
