# 🔎 Vision - AI Learning Buddy

**Vision** is an AI tutor built for one specific topic - **Open-Vocabulary Object
Detection (OVOD)** - that explains concepts, gives real-world examples, quizzes
you, and grades your answers honestly. It was built as a capstone project for
Infosys Springboard's **AI EMPOW(H)ER** program.

---

## Features

| Mode | What it does |
|---|---|
| 💬 **Explain Simply** | Breaks down an OVOD concept in plain language, using a real-world analogy before any jargon |
| 🌍 **Real Example** | Gives one concrete, visualizable use-case |
| 📝 **Quiz Me** | Generates N mixed-difficulty questions (easy → research-level) with answers |
| ✅ **Check My Answer** | Paste a question + your own answer, get direct, honest feedback — no sugar-coating |
| 🎓 **Full Session** | Runs explain → example → quiz → feedback as one guided flow |

The tutor's persona ("Vision") is a mix of three things: a patient beginner
tutor, a research companion that can go into actual paper-level depth (ViLD,
CLIP, LVIS, base vs. novel categories), and a quiz-master that tests
understanding instead of just being encouraging.

---

## Tech Stack

- **Frontend / App framework:** [Streamlit](https://streamlit.io)
- **LLM backend:** [Gemini API](https://ai.google.dev/) via the official
  [`google-genai`](https://pypi.org/project/google-genai/) Python SDK
- **Language:** Python 3.9+

---

## Getting Started

### 1. Clone this repo
```bash
git clone <your-repo-url>
cd vision_project
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Get a Gemini API key
Get a free key from **[aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)**.

### 4. Run the app
```bash
streamlit run app.py
```
The app opens at `http://localhost:8501`. Paste your API key into the sidebar
field when prompted (no key is stored anywhere in the code).

---

## Deploying Your Own Copy

1. Push this repo to GitHub.
2. Go to **[share.streamlit.io](https://share.streamlit.io)** → **New app** →
   point it at `app.py` in your repo.
3. In the app's **Settings → Secrets**, add:
   ```toml
   GEMINI_API_KEY = "your_key_here"
   ```
4. Deploy. You'll get a public URL that runs this app for anyone who visits it.

---

## Project Structure

```
vision_project/
├── app.py                          # Main Streamlit application
├── requirements.txt                # Python dependencies
└── README.md                       # This file
```

---

## How It Works (Under the Hood)

`app.py` defines a fixed system prompt (the "Vision" persona) and five reusable
prompt templates — one per mode. Each template takes the topic (locked to OVOD
here, but written so `[TOPIC]` could be swapped for anything) and sends it to
Gemini via `client.models.generate_content()`. Responses are rendered in a
Streamlit chat interface with a custom dark theme.

If you want to reuse this for a different subject, everything you need to
change is the `TOPIC` constant and the persona description near the top of
`app.py` — the five prompt template functions don't need to change.

---

## Known Limitations

- No retrieval grounding — answers come from the model's own knowledge, not a
  live lookup of the source papers, so double-check anything highly specific.
- No memory across sessions — each session starts fresh and doesn't track
  what a learner previously got wrong.
- Requires a valid Gemini API key with quota; the free tier is sufficient for
  normal use but can rate-limit under heavy testing.

---

## Troubleshooting

**"404 model not found" error** — Google periodically retires older Gemini
models. This app calls `gemini-flash-latest` (an alias that always points to
the current GA flash model) with `gemini-3.5-flash` as a fallback. If both
ever fail, list what your key currently has access to:
```python
from google import genai
client = genai.Client(api_key="YOUR_KEY")
for m in client.models.list():
    print(m.name)
```
Then update the model name(s) in `app.py` accordingly.

**Make sure you're on the current SDK** — this project uses `google-genai`,
not the older, now-deprecated `google-generativeai` package. If you see
import errors, check `requirements.txt` matches what's installed:
```bash
pip uninstall google-generativeai -y
pip install -r requirements.txt
```

---

## Credits

Built by Ananya as part of the Infosys Springboard AI EMPOW(H)ER capstone,
topic: Open-Vocabulary Object Detection.
