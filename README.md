# Vision  - AI Learning Buddy
Infosys Springboard · AI EMPOW(H)ER Capstone
Topic: **Open-Vocabulary Object Detection (OVOD)**

## Project Structure

```
vision_project/
├── app.py                          # Deliverable 7  - working Streamlit app (mandatory)
├── requirements.txt                # Python dependencies for deployment
├── docs/
│   ├── 02_persona.md                # Deliverable 2  - persona + system prompt
│   ├── 03_prompt_templates.md       # Deliverable 3  - 5 reusable templates
│   ├── 04_sample_conversation.md    # Deliverable 4  - sample chat transcript
│   ├── 05_quiz_and_answers.md       # Deliverable 5  - 5-question quiz + answers
│   └── 06_reflection_template.md    # Deliverable 6  - scaffold, fill in your own words
└── assets/
    └── landing_preview.html         # optional  - visual concept, not required by rubric
```

**Deliverable 1 (Topic Selected)** = Open-Vocabulary Object Detection  - stated at
the top of this file and inside `docs/02_persona.md`.

## How to run locally
```bash
pip install -r requirements.txt
streamlit run app.py
```
You'll need a free Gemini API key from https://aistudio.google.com/app/apikey  -
paste it into the sidebar when the app opens locally.

## How to deploy (for the mandatory Streamlit link)
1. Push this whole folder to a GitHub repo.
2. Go to https://share.streamlit.io → New app → point it at `app.py`.
3. In the app's Settings → Secrets, add:
   ```
   GEMINI_API_KEY = "your_key_here"
   ```
4. Deploy → copy the public URL → submit it in the capstone form.

## Submission checklist
- [ ] Topic selected  - OVOD ✅ (done)
- [ ] Persona written  - ✅ (`docs/02_persona.md`)
- [ ] 5 prompt templates  - ✅ (`docs/03_prompt_templates.md`)
- [ ] Sample conversation  - ✅ draft ready, consider re-running live for real screenshots
- [ ] 5-question quiz + answers  - ✅ draft ready, add screenshots from the live app
- [ ] Reflection (300–400 words)  - ⚠️ needs your own words (`docs/06_reflection_template.md`)
- [ ] Streamlit app deployed + link  - ⚠️ deploy using steps above, then submit link
