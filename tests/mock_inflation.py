from datetime import datetime

class MockInflation:
    def __init__(self, constant_inflation):
        self._constant_inflation = constant_inflation

    def inflation_to(self, when: datetime):
        return self._constant_inflation
