class ListStorage:

    def __init__(self):
        self.storage = []

    def store_item(self, item):
        self.storage.append(item)

    def get_list(self):
        return self.storage