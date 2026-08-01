from openai import OpenAI

from app.config import get_settings


class GenerationService:
    def __init__(self) -> None:
        self.settings = get_settings()

    def generate_answer(
        self,
        question: str,
        sources: list[dict],
    ) -> tuple[str, str]:
        if not sources:
            return (
                "I could not find relevant information in the uploaded documents.",
                "retrieval-only",
            )

        context = "\n\n".join(
            f"Source {index + 1}:\n{source['content']}"
            for index, source in enumerate(sources)
        )

        if not self.settings.openai_api_key:
            answer = self._fallback_answer(question, sources)
            return answer, "local-fallback"

        client = OpenAI(api_key=self.settings.openai_api_key)

        response = client.chat.completions.create(
            model=self.settings.openai_model,
            temperature=0.2,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a knowledge assistant. "
                        "Answer only from the provided context. "
                        "If the context does not contain the answer, say so."
                    ),
                },
                {
                    "role": "user",
                    "content": (
                        f"Context:\n{context}\n\n"
                        f"Question:\n{question}"
                    ),
                },
            ],
        )

        answer = response.choices[0].message.content or (
            "No answer was generated."
        )

        return answer, "openai"

    @staticmethod
    def _fallback_answer(
        question: str,
        sources: list[dict],
    ) -> str:
        context_preview = "\n\n".join(
            source["content"]
            for source in sources[:2]
        )

        return (
            "OpenAI generation is not configured. "
            "The most relevant retrieved context is shown below.\n\n"
            f"Question: {question}\n\n"
            f"Relevant context:\n{context_preview}"
        )