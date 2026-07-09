import time
from mistralai.client import Mistral
from orchestrator.providers.base import LLMProvider

class MistralProvider(LLMProvider):
    def __init__(
            self,
            api_key: str,
            max_retries: int = 3,
            initial_backoff: float = 1.0,
    ) -> None:
        self.client = Mistral(api_key=api_key)
        self.max_retries = max_retries
        self.initial_backoff = initial_backoff

    
    def run(self, agent_id: str, prompt: str) -> str:
        for attempt in range(self.max_retries):
            try:
                response = self.client.beta.conversations.start(
                    agent_id=agent_id,
                    agent_version="latest",
                    inputs=prompt,
                    model="mistral-medium-latest",
                    completion_args={
                        "temperature": 0.1,
                        "max_tokens": 4096,
                    }
                )
                return self._extract_text(response)
            except Exception as e:
                if attempt < self.max_retries - 1:
                    backoff_time = self.initial_backoff * (2 ** attempt)
                    time.sleep(backoff_time)
                else:
                    raise e
                
    @staticmethod
    def _extract_text(response) -> str:
        parts: list[str] = []

        for output in response.outputs:
            content = getattr(output, "content", None)

            if isinstance(content, str):
                parts.append(content)
                continue

            if isinstance(content, list):
                for item in content:
                    text = getattr(item, "text", None)
                    if text:
                        parts.append(text)

        return "\n".join(parts)