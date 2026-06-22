import logging

from langchain_ollama import ChatOllama

logger = logging.getLogger(__name__)


class LLMHandler:
    """
    Handles interaction with the LLM.
    Supports Ollama-based local models.
    """

    def __init__(
        self,
        model_name: str = "llama3.2",
        temperature: float = 0.0
    ):

        self.model_name = model_name

        try:
            logger.info(
                f"Loading LLM: {model_name}"
            )

            self.llm = ChatOllama(
                model=model_name,
                temperature=temperature
            )

            logger.info(
                f"LLM loaded successfully: {model_name}"
            )

        except Exception as e:
            logger.error(
                f"Failed to initialize LLM: {str(e)}"
            )
            raise

    def generate_answer(
        self,
        question: str,
        context: str,
        chat_history: str = ""
    ) -> str:
        """
        Generate answer using retrieved context
        and conversation history.
        """

        prompt = f"""
You are an Enterprise Knowledge Assistant.

Your responsibilities:

1. Answer ONLY using the provided context.
2. Use chat history when relevant.
3. Do not make up facts.
4. If information is missing, clearly say so.
5. Be concise and professional.
6. Format answers clearly using bullet points when appropriate.

Chat History:
{chat_history}

Retrieved Context:
{context}

User Question:
{question}

If the answer cannot be found in the context, reply exactly:

"I could not find the answer in the uploaded documents."

Answer:
"""

        try:

            logger.info(
                f"Generating answer for query: {question}"
            )

            response = self.llm.invoke(
                prompt
            )

            logger.info(
                "Answer generated successfully."
            )

            return response.content

        except Exception as e:

            logger.error(
                f"LLM generation failed: {str(e)}"
            )

            return (
                "An error occurred while generating "
                "the response."
            )

    def health_check(self) -> bool:
        """
        Verify that the model is responding.
        """

        try:

            response = self.llm.invoke(
                "Respond with only: OK"
            )

            return bool(response.content)

        except Exception as e:

            logger.error(
                f"LLM health check failed: {str(e)}"
            )

            return False