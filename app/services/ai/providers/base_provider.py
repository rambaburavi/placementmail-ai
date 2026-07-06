from abc import ABC, abstractmethod


class AIProvider(ABC):

    @abstractmethod
    def generate(self, prompt: str) -> str:
        pass

    @abstractmethod
    def generate_json(self, prompt: str) -> str:
        pass