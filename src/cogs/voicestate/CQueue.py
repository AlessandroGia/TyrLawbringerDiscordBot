from asyncio import Queue


class CQueue(Queue):
    def __init__(self):
        super().__init__()

    def add(self, element: dict):
        if not self.__check_same(element):
            self.put_nowait(element)

    def __check_same(self, element: dict):
        return (element['state'].channel, element['event']) in [(e['state'].channel, e['event']) for e in self._queue]

