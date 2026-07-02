from abc import ABC, abstractmethod

class LLMProvider(ABC):
    @abstractmethod
    def run(self, agent_id: str, prompt: str) -> str:
        pass