import heapq


class Heap:
    class Wrapper:
        def __init__(self, value, obj) -> None:
            self.value = value
            self.obj = obj

        def __lt__(self, __obj):
            return self.value < __obj.value

    def __init__(self, eval_fnc) -> None:
        self.__internal_heap = []
        self.__eval_fnc = eval_fnc

    def insert(self, item):
        heapq.heappush(self.__internal_heap, Heap.Wrapper(self.__eval_fnc(item), item))

    def insert_with_custom_value(self, value, item):
        heapq.heappush(self.__internal_heap, Heap.Wrapper(value, item))

    def pop(self):
        return heapq.heappop(self.__internal_heap).obj

    def empty(self):
        return not bool(self.__internal_heap)
