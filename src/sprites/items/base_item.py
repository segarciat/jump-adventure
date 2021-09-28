import abc


class BaseItem:
    @abc.abstractmethod
    def collide(self, player):
        pass
