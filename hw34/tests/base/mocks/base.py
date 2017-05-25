class BaseMock:
    def __init__(self):
        self._mocks = []
        self._create_mocks()

    def start(self):
        for mok in self._mocks:
            mok.start()

    def stop(self):
        for mok in self._mocks:
            mok.stop()

    def clear(self):
        pass

    def _create_mocks(self):
        raise NotImplementedError
