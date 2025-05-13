class TimestampActivityTuple:

    def __init__(self, timestamp, activity):
        self.timestamp = timestamp
        self.activity = activity

    def __str__(self):
        return str(self.__dict__)
