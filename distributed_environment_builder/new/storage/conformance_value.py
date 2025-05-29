class ConformanceValues:

    def __init__(self, case_id, last_activity, conformance):
        self.case_id = case_id
        self.last_activity= last_activity
        self.conformance = conformance

    def __str__(self):
        return str(self.__dict__)

    def __dict__(self):
        result = dict()
        result["case_id"] = self.case_id
        result["last_activity"] = self.last_activity
        result["conformance"] = self.conformance
        return result