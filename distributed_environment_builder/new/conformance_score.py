class ConformanceScore:

    def __init__(self, path_length=0, conformance_violations=0):
        self.path_length = path_length
        self.conformance_violations = conformance_violations

    def increment_violations(self, count=1):
        if count < 1:
            print("help")
        self.conformance_violations = self.conformance_violations + count

    def increase_path_length(self, count=1):
        self.path_length = self.path_length + count

    def get_score(self):
        if self.path_length:
            return 1 - (self.conformance_violations / self.path_length)
        return 0.0

    def __str__(self):
        return str(self.__dict__)

    def __add__(self, other):
        return ConformanceScore(self.path_length + other.path_length, self.conformance_violations + other.conformance_violations)