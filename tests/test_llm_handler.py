from llm_handler import LLMHandler

context = """
Retrieval Augmented Generation combines search
with language models.

Artificial Intelligence is transforming industries.
"""

llm = LLMHandler()

answer = llm.generate_answer(
    question="What is Retrieval Augmented Generation?",
    context=context
)

print(answer)