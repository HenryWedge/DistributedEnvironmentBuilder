from typing import Dict

class DictStorage(Dict):

    def __init__(self, dictionary):
        super().__init__()
        dict()

    def __setitem__(self, __key, __value):
        super().__setitem__(__key, __value)
        #print(f"Stored=[key: {__key}, value: {__value}]")
