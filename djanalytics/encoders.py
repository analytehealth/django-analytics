import decimal
import json


class JSONEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return str(obj)
        return json.JSONEncoder.default(self, obj)

jsonencoder = JSONEncoder()
