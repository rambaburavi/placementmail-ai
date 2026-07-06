from app.agents.analyzer.prompt_builder import PromptBuilder
from app.agents.analyzer.response_parser import ResponseParser

from app.services.ai.ai_factory import AIFactory
from app.services.ai.keyword_analyzer import KeywordAnalyzer


class AnalyzerAgent:

    def __init__(self):

        self.prompt = PromptBuilder()

        self.parser = ResponseParser()

        self.keyword = KeywordAnalyzer()

    def analyze(self, email):

        prompt = self.prompt.build(email)

        providers = [
            "gemini",
            "groq",
        ]

        for provider in providers:

            try:

                ai = AIFactory.create(provider)

                response = ai.generate(prompt)

                result = self.parser.parse(response)

                result["ai_provider"] = provider.capitalize()

                result["analysis_status"] = "SUCCESS"

                print(f"✅ AI Provider: {provider}")

                return result

            except Exception:

                print(f"❌ {provider} failed")

        print("⚠ Keyword Analyzer Activated")

        return self.keyword.analyze(email)