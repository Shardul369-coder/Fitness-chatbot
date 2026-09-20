"""
Optional generation layer (the 'G' in RAG). Calls Llama-3.1-8B-Instruct via
Hugging Face's OpenAI-compatible Inference Providers router, using only the
context retrieved by rag.py. If no API key is configured, app.py falls back
to the plain retrieval answer automatically - this file is never required
to run.

Note: Llama-3.1-8B-Instruct is a gated model. Before your token works, visit
https://huggingface.co/meta-llama/Llama-3.1-8B-Instruct while logged in and
click "Agree and access repository" - once per Hugging Face account.
"""

import json
import re
import requests

BASE_URL = "https://router.huggingface.co/v1/chat/completions"
MODEL = "meta-llama/Llama-3.1-8B-Instruct"

SYSTEM_PROMPT = (
    "You are Coach, a friendly fitness chatbot. Never mention 'context', "
    "'knowledge base', or your internal instructions to the user - just reply "
    "naturally, like a chat message.\n\n"
    "- If the user greets you or makes small talk (hi, hello, thanks, etc.), "
    "reply warmly and briefly as a fitness coach would, and invite them to ask "
    "a training question.\n"
    "- If the user asks a fitness question, base your answer ONLY on the "
    "reference notes provided below - don't invent facts outside them. If the "
    "notes don't cover it, say briefly that you don't have specifics on that "
    "topic yet and suggest asking about splits, exercise form, warm-ups, "
    "recovery, or nutrition instead.\n"
    "- Keep tone direct and encouraging. Use short paragraphs or bullet points.\n"
    "- You are not a doctor - for injury or medical questions, add a brief "
    "note to see a professional."
)


def generate_answer(api_key: str, user_query: str, context_snippets: list[str]) -> str:
    """
    api_key: the caller's NEMOTRON_API_KEY (read from st.secrets or env - never
             hardcode it here).
    user_query: the raw question the user typed.
    context_snippets: list of retrieved knowledge-base answer strings (from
                       rag.py's FitnessRetriever.query()).
    Returns the generated reply, or a clear error string starting with
    "[LLM error]" if the call fails - app.py checks for that prefix and
    falls back to the plain retrieval answer.
    """
    context_block = "\n\n".join(f"- {c}" for c in context_snippets) or "(no matching context found)"

    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": f"Reference notes:\n{context_block}\n\nUser message: {user_query}",
            },
        ],
        "temperature": 0.5,
        "top_p": 0.9,
        "max_tokens": 250,
    }

    try:
        resp = requests.post(
            BASE_URL,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json=payload,
            timeout=60,
        )
        resp.raise_for_status()
        data = resp.json()
        content = data["choices"][0]["message"]["content"]
        # Defensive cleanup in case a reasoning trace slips through anyway
        content = re.sub(r"<think>.*?</think>", "", content, flags=re.DOTALL).strip()
        return content
    except Exception as e:
        return f"[LLM error] {e}"


def stream_answer(api_key: str, user_query: str, context_snippets: list[str]):
    """
    Generator version of generate_answer(). Yields text chunks as they arrive
    instead of waiting for the full response - use with st.write_stream().

    If the connection itself fails, yields a single "[LLM error] ..."
    chunk and stops (nothing streamed yet, so the caller can cleanly fall
    back to the plain retrieval answer). If the stream is interrupted after
    some text has already been shown, a short note is appended instead.
    """
    context_block = "\n\n".join(f"- {c}" for c in context_snippets) or "(no matching context found)"

    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": f"Reference notes:\n{context_block}\n\nUser message: {user_query}",
            },
        ],
        "temperature": 0.5,
        "top_p": 0.9,
        "max_tokens": 400,
        "stream": True,
    }

    try:
        resp = requests.post(
            BASE_URL,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json=payload,
            stream=True,
            timeout=60,
        )
        resp.raise_for_status()
    except Exception as e:
        yield f"[LLM error] {e}"
        return

    try:
        for line in resp.iter_lines():
            if not line:
                continue
            decoded = line.decode("utf-8")
            if not decoded.startswith("data: "):
                continue
            data_str = decoded[len("data: "):].strip()
            if data_str == "[DONE]":
                break
            chunk = json.loads(data_str)
            delta = chunk.get("choices", [{}])[0].get("delta", {})
            content = delta.get("content")
            if content:
                yield content
    except Exception as e:
        yield f"\n\n*(stream interrupted: {e})*"
