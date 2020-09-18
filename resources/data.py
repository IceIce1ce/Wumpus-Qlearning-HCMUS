import json

class Data:
    def __init__(self):
        self.data = json.load(open("dataLogic.json"))

    def get_all_types(self):
        return self.data["types"]

    def get_type(self, type):
        return self.get_all_types()[type]

    def get_rows(self):
        return self.data["rows"]

    def get_cols(self):
        return self.data["cols"]

gamedata = Data()