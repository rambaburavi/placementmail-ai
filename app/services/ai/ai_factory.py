from app.services.ai.providers.gemini_provider import GeminiProvider
from app.services.ai.providers.groq_provider import GroqProvider


class AIFactory:

    PROVIDERS = {
        "gemini": GeminiProvider,
        "groq": GroqProvider,
    }

    @staticmethod
    def create(provider: str = "gemini"):

        provider = provider.lower()

        provider_class = AIFactory.PROVIDERS.get(provider)

        if provider_class is None:
            raise ValueError(
                f"Unsupported AI provider: {provider}"
            )

        return provider_class()

    @staticmethod
    def available_providers():

        return list(AIFactory.PROVIDERS.keys())