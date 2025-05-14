import json

class Constants:
    def __init__(self):
        with open("../config.json", "r") as file:
            self.constants = json.load(file)["constants"]

    def saveData(self, data):
        with open("../config.json", "w") as file:
            json.dump(data, file, indent = 2)

    def getConstant(self, path):
        keys = path.split(".")

        value = self.constants

        for key in keys:
            value = value[key]

        return value

    def setConstant(self, path, val):
        data = self.constants
        keys = path.split(".")

        for key in keys[:-1]:
            data = data[key]

        data[keys[-1]] = val

        Constants.saveData(self, data)
