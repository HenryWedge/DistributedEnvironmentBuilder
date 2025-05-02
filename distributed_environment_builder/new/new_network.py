class NewNetwork:

    def __init__(self):
        self.network_functions = dict()

    def add_network_function(self, name, network_function):
        self.network_functions[name] = network_function

    def get(self, name):
        return self.network_functions[name]
