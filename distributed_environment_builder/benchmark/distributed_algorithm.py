from typing import Dict, Callable

from distributed_environment_builder.benchmark.abstract_algorithm import Algorithm


class DistributedAlgorithm:

    def __init__(self):
        self._algorithms: Dict[str, Callable[[], Algorithm]] = dict()

    def add_algorithm(self, key: str, algorithm: Callable[[], Algorithm]):
        self._algorithms[key] = algorithm
        return self

    def create_algorithm_of_key(self, key: str):
        return self._algorithms[key]()