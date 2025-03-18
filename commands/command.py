from abc import ABC, abstractmethod

class Command(ABC):
    @abstractmethod
    def send(self, comm):
        pass

    @abstractmethod
    def on_validate(self, message_received) -> bool:
        pass

    @abstractmethod
    def on_receive(self, comm, message_received):
        pass
