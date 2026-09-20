# Coach — Fitness RAG Chatbot (Streamlit, no API key)

A retrieval-based fitness chatbot: it matches your question against a curated
knowledge base (workout splits, exercise form, nutrition, recovery, common
aches) using TF-IDF + cosine similarity, and returns the best-matching
answer. No LLM API, no API key, no external network calls at all — it runs
entirely offline once installed.

## ⚠️ About deploying this on Vercel

Vercel does not run Streamlit apps — Streamlit needs a persistent Python
server with websocket support, which Vercel's serverless/static hosting
doesn't provide. The free host built for this is **Streamlit Community
Cloud**, and it uses the exact same "connect your GitHub repo" flow you'd
get on Vercel. Render and Hugging Face Spaces also work if you want
alternatives. Steps for all three are below.

## Optional: enable LLM-generated answers (Llama-3.1-8B-Instruct via Hugging Face)

By default this app works with zero API keys (plain retrieval). If you have
a Hugging Face token, it'll use Llama-3.1-8B-Instruct to write a better-
phrased answer from the same retrieved knowledge base instead of returning
the canned text.

**One-time step:** Llama-3.1-8B-Instruct is a gated model. Visit
https://huggingface.co/meta-llama/Llama-3.1-8B-Instruct while logged in and
click "Agree and access repository" — otherwise your token gets a 403 error
no matter how correct the code is.

**Get a token:** huggingface.co → Settings → Access Tokens → create a
fine-grained token with the "Make calls to Inference Providers" permission.

**Locally:** create `.streamlit/secrets.toml` (already gitignored — never
commit this file) with:
```toml
HF_TOKEN = "hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

**On Streamlit Community Cloud:** open your app → Settings → Secrets, and
paste the same line there instead. No code changes, no redeploy needed to
add/remove it.

If the token is missing, invalid, ungated, or the call fails for any
reason, the app automatically falls back to the plain retrieval answer —
it never crashes or blocks you out.

## 1. Run it locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

Opens automatically at http://localhost:8501. No `.env` file, no keys —
just run it.

## 2. Push to your GitHub

```bash
git init
git add .
git commit -m "Initial commit: fitness RAG chatbot"
git branch -M main
git remote add origin https://github.com/<your-username>/<your-repo-name>.git
git push -u origin main
```

Create the empty repo on GitHub first (github.com/new), without adding a
README there, so it doesn't conflict with this push.

## 3. Deploy for free — Streamlit Community Cloud (recommended)

1. Go to https://share.streamlit.io and sign in with GitHub.
2. Click **New app**, pick your repo, branch `main`, main file `app.py`.
3. Click **Deploy**. You'll get a live `https://<name>.streamlit.app` URL
   in about a minute. No environment variables needed.
4. Every future `git push` to `main` auto-redeploys.

## Alternative hosts (also support Streamlit, unlike Vercel)

- **Hugging Face Spaces**: create a Space, choose "Streamlit" as the SDK,
  push this repo to it (or link your GitHub repo). Free tier available.
- **Render**: New → Web Service → connect the GitHub repo → start command
  `streamlit run app.py --server.port $PORT --server.address 0.0.0.0`.

## Project structure

```
app.py             Streamlit UI (chat interface)
rag.py              TF-IDF retrieval engine
knowledge_base.py    The fitness Q&A knowledge base — edit/extend this
                      to teach Coach new topics, no retraining needed
requirements.txt
```

## Extending the knowledge base

Add new entries to the `KB` list in `knowledge_base.py`:

```python
{
    "topic": "Your topic name",
    "q": "keywords and phrasings someone might type",
    "a": "The answer text.",
},
```

No embeddings model or GPU needed — TF-IDF rebuilds instantly on each app
restart.
