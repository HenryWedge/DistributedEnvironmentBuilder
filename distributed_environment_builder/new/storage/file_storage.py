import threading
import time
from typing import Dict
import json
import os

from node_monitor import NodeMonitor


class DictFileStorage(Dict):

    def __init__(self, filepath, monitor):
        self.lock = threading.Semaphore()
        self.monitor: NodeMonitor = monitor
        self.filepath = filepath
        self._data = {}
        if not os.path.exists(self.filepath):
            with open(self.filepath, 'w+'): pass
        else:
            self._load_data()

    def _load_data(self):
        start = time.time()
        self.lock.acquire()
        if os.path.exists(self.filepath) and os.path.getsize(self.filepath) > 0:
            try:
                with open(self.filepath, 'r') as f:
                    result = json.load(f)
                    end = time.time()
                    self.monitor.add_value("read_time_metrics", end - start)
                    self._data=result
            except json.JSONDecodeError:
                print(f"Warning: Could not decode JSON from {self.filepath}. Starting with empty dictionary.")
                self._data = {}
        self.lock.release()

    def _save_data(self):
        self.lock.acquire()
        start = time.time()
        with open(self.filepath, 'w+') as f:
           f.write(json.dumps(self._data))
        end = time.time()

        self.monitor.add_value("write_time_metrics", end - start)
        self.lock.release()

    def __getitem__(self, key):
        self._load_data()
        if key in self._data:
            return self._data[key]
        return None

    def get_item(self, key, clazz):
        return clazz.model_validate_json(self.__getitem__(key))

    def __setitem__(self, key, value):
        if hasattr(value, "model_dump_json"):
            self._data[key] = value.model_dump_json()
        else:
            self._data[key] = value
        self._save_data()  # Save data after modification

    def __delitem__(self, key):
        del self._data[key]
        self._save_data()  # Save data after modification

    def __len__(self):
        return len(self._data)

    def __iter__(self):
        return iter(self._data)

    def __contains__(self, key):
        self._load_data()
        return key in self._data

    def keys(self):
        return self._data.keys()

    def values(self):
        return self._data.values()

    def items(self):
        return self._data.items()

    def get(self, key, default=None):
        return self._data.get(key, default)

    def clear(self):
        self._data.clear()
        self._save_data()

    def __str__(self):
        return str(self._data)

    def __repr__(self):
        return f"FileBackedDict(filepath='{self.filepath}', data={self._data})"
