class ConformanceValues:

    def __init__(self, case_id, last_activity, conformance):
        self.case_id = case_id
        self.last_activity= last_activity
        self.conformance = conformance

    def __str__(self):
        return str(self.__dict__)