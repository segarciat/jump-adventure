import abc


class Item(metaclass=abc.ABCMeta):
    GROUP_NAME = "items"

    def __init__(self, groups):
        groups[Item.GROUP_NAME].add(self)

    @abc.abstractmethod
    def affect(self, player):
        pass
