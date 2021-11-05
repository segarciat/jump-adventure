import abc


class IState(metaclass=abc.ABCMeta):
    """State interface for modeling class behavior with a state machine."""
    def exit(self) -> None:
        """Cleanup performed by a state before transitioning out of this state."""
        pass

    @abc.abstractmethod
    def enter(self) -> None:
        """Performs necessary setup for transitioning into this state."""
        pass


class StatefulMixin:
    """Mixin meant to be used with classes that rely on the State Pattern for behavior."""
    def __init__(self):
        self._state = None

    @property
    def state(self) -> IState:
        return self._state

    @state.setter
    def state(self, new_state: IState) -> None:
        """Transitions out of the current state and into a new one."""
        self._state.exit()
        self._state = new_state
        self._state.enter()
