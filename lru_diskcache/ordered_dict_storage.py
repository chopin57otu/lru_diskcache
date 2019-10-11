import json
from collections import OrderedDict
from pathlib import Path


class OrderedDictStorage(OrderedDict):
    def __init__(self, file: str = ""):
        super().__init__()
        self.file = Path(file)

        if self.file.exists():
            self.load()
        else:
            with self.file.open('w') as f:
                json.dump(OrderedDict(), f)

    def save(self):
        with self.file.open('w') as f:
            json.dump(self, f)

    def load(self):
        self.clear()
        with self.file.open() as f:
            od: OrderedDict = json.load(f, object_pairs_hook=OrderedDict)
            for k, v in od.items():
                self[k] = v
