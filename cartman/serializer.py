import json


class Serializer(object):

    """docstring for Serializer"""

    @staticmethod
    def dumps(data_obj):
        return json.dumps(data_obj)

    @staticmethod
    def loads(data_string):
        return json.loads(data_string)
