"""
prompt_library.py
------------------
Stores reusable prompt templates for the Document Portal project.
"""

# Example prompt template
SUMMARIZE_PROMPT = """
You are a helpful assistant. Summarize the following document concisely:

{document_text}
"""

QA_PROMPT = """
You are a helpful assistant. Answer the question based on the provided context.

Context:
{context}

Question:
{question}

Answer:
"""
