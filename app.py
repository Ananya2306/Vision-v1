"""
Vision - AI Learning Buddy for Open-Vocabulary Object Detection
Infosys Springboard AI EMPOW(H)ER Capstone

Run locally:   streamlit run app.py
Deploy:        push to GitHub -> share.streamlit.io -> add GEMINI_API_KEY in Secrets
"""

import streamlit as st
import streamlit.components.v1 as components
from google import genai
from google.genai import types

 
# CONFIG
 
st.set_page_config(page_title="Vision  - AI Learning Buddy", page_icon="🔎", layout="wide")

 
# THEME  - aggressive reskin, robust selectors, glow everywhere
 
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=Inter:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap');

:root{
  --ink:#F3F1FA; --dim:#948FB0; --purple:#6C3CE9; --blue:#2653EB;
  --mint:#29E0C4; --dark-1:#0B0A14; --dark-2:#120F1E; --line:rgba(255,255,255,0.16);
}

html, body, [class^="css"], [class*=" css"], .stApp, .main, .block-container{
  font-family:'Inter', sans-serif !important; color: var(--ink) !important;
}

.stApp{
  background: radial-gradient(ellipse at 15% 0%, #1c1533 0%, transparent 45%),
              radial-gradient(ellipse at 85% 100%, #0f2a4a 0%, transparent 45%),
              var(--dark-1) !important;
}

.block-container{ padding-top: 1.2rem !important; max-width: 900px; }

h1, h2, h3, h4{ font-family:'Space Grotesk', sans-serif !important; color: var(--ink) !important; }
p, span, label, li, div{ color: var(--ink); }

/* Sidebar */
section[data-testid="stSidebar"]{
  background: linear-gradient(180deg, var(--dark-2), #0d0a18) !important;
  border-right: 1px solid var(--line);
}
section[data-testid="stSidebar"] *{ color: var(--ink) !important; }

/* Buttons  - gradient + glow pulse on hover */
.stButton>button, div[data-testid="stFormSubmitButton"] button{
  border: none !important; border-radius: 10px !important;
  font-weight: 600 !important; padding: 0.6rem 1rem !important;
  transition: transform .18s ease, box-shadow .3s ease !important;
}
button[kind="primary"]{
  background: linear-gradient(120deg, var(--purple), var(--blue)) !important;
  color: #fff !important;
  box-shadow: 0 4px 18px -6px rgba(108,60,233,0.55) !important;
}
button[kind="secondary"]{
  background: rgba(255,255,255,0.04) !important;
  color: var(--dim) !important;
  border: 1px solid var(--line) !important;
}
button[kind="secondary"]:hover{
  border-color: var(--mint) !important; color: var(--ink) !important;
  background: rgba(41,224,196,0.06) !important;
}
.stButton>button:hover{
  transform: translateY(-3px) scale(1.01);
  box-shadow: 0 10px 30px -6px rgba(108,60,233,0.65), 0 0 0 4px rgba(41,224,196,0.12) !important;
}
.stButton>button:active{ transform: translateY(-1px) scale(0.99); }

/* Inputs  - Streamlit's own CSS-in-JS (Emotion) may also use !important, so we
   win on specificity by chaining the full known DOM path, not just the class. */
html body div[data-testid="stTextArea"] div[data-testid="stTextAreaRootElement"] textarea,
html body div[data-testid="stTextInput"] div[data-testid="stTextInputRootElement"] input,
html body div[data-testid="stChatInput"] textarea[data-testid="stChatInputTextArea"],
html body textarea[class*="st-emotion-cache"],
html body input[class*="st-emotion-cache"]{
  background-color: rgba(255,255,255,0.09) !important;
  color: #F3F1FA !important;
  -webkit-text-fill-color: #F3F1FA !important;
  caret-color: #F3F1FA !important;
  border: 1px solid rgba(255,255,255,0.3) !important;
  border-radius: 10px !important;
}
html body div[data-testid="stTextArea"] div[data-testid="stTextAreaRootElement"] textarea:focus,
html body div[data-testid="stTextInput"] div[data-testid="stTextInputRootElement"] input:focus,
html body textarea[class*="st-emotion-cache"]:focus,
html body input[class*="st-emotion-cache"]:focus{
  border-color: var(--mint) !important;
  box-shadow: 0 0 0 2px rgba(41,224,196,0.25) !important;
}
html body textarea[class*="st-emotion-cache"]::placeholder,
html body input[class*="st-emotion-cache"]::placeholder{
  color: #d8d5e8 !important;
  -webkit-text-fill-color: #d8d5e8 !important;
  opacity: 1 !important;
}

/* Sliders */
div[data-testid="stSlider"] div[role="slider"]{ background: var(--mint) !important; }
div[data-testid="stSlider"] > div > div > div{ background: linear-gradient(90deg, var(--purple), var(--mint)) !important; }

/* Chat bubbles */
div[data-testid="stChatMessage"]{
  background: rgba(255,255,255,0.05) !important; border: 1px solid var(--line) !important;
  border-radius: 14px !important; padding: 4px !important;
  box-shadow: 0 4px 18px -8px rgba(0,0,0,0.4);
}

/* Captions, dividers, misc */
[data-testid="stCaptionContainer"], .stCaption{ color: var(--dim) !important; }
hr{ border-color: var(--line) !important; }
div[data-testid="stAlert"]{ background: rgba(41,224,196,0.08) !important; border: 1px solid var(--mint) !important; border-radius: 10px !important; }

/* Custom mode-nav pills */
.mode-pill{
  display:flex; align-items:center; gap:8px; padding:10px 14px; border-radius:10px;
  border:1px solid var(--line); background: rgba(255,255,255,0.03); margin-bottom:8px;
  font-size: 14px; font-weight: 500;
}
.mode-pill.active{
  background: linear-gradient(120deg, rgba(108,60,233,0.25), rgba(41,224,196,0.15));
  border-color: var(--mint);
}

/* BaseWeb is the underlying component library Streamlit itself is built on  -
   this is the actual element carrying the white background in most versions */
div[data-baseweb="base-input"], div[data-baseweb="input"], div[data-baseweb="textarea"]{
  background: rgba(255,255,255,0.07) !important;
  border-color: var(--line) !important;
}
div[data-baseweb="base-input"] input,
div[data-baseweb="input"] input,
div[data-baseweb="textarea"] textarea,
div[data-baseweb="base-input"] textarea{
  background: transparent !important;
  color: #F3F1FA !important;
  -webkit-text-fill-color: #F3F1FA !important;
  caret-color: #F3F1FA !important;
}

/* Chat input  - force dark bg + visible text, covering all known Streamlit selectors */
div[data-testid="stBottomBlockContainer"],
div[data-testid="stBottom"],
div[data-testid="stChatInputContainer"],
.stChatFloatingInputContainer,
section[data-testid="stMain"] > div:last-child,
footer{
  background: var(--dark-1) !important;
}
div[data-testid="stChatInput"]{
  background: rgba(255,255,255,0.05) !important;
  border: 1px solid var(--line) !important;
  border-radius: 12px !important;
}
div[data-testid="stChatInput"] textarea,
div[data-testid="stChatInput"] [contenteditable="true"]{
  background: transparent !important;
  color: #F3F1FA !important;
  -webkit-text-fill-color: #F3F1FA !important;
  caret-color: #F3F1FA !important;
}
div[data-testid="stChatInput"] textarea::placeholder{
  color: #948FB0 !important;
  -webkit-text-fill-color: #948FB0 !important;
  opacity: 1 !important;
}

/* Scrollbar */
::-webkit-scrollbar{ width:8px; }
::-webkit-scrollbar-thumb{ background: var(--purple); border-radius:8px; }
</style>
""", unsafe_allow_html=True)

 
# BULLETPROOF INPUT FIX  - JS forces inline styles (always wins over any CSS)
 
components.html("""
<script>
function fixEl(el){
  el.style.setProperty('background-color', 'rgba(30,25,50,0.9)', 'important');
  el.style.setProperty('color', '#F3F1FA', 'important');
  el.style.setProperty('-webkit-text-fill-color', '#F3F1FA', 'important');
  el.style.setProperty('caret-color', '#F3F1FA', 'important');
  el.style.setProperty('border', '1px solid rgba(255,255,255,0.35)', 'important');
  el.style.setProperty('border-radius', '10px', 'important');
}
function fixInputs(root){
  try{
    root.querySelectorAll('textarea, input[type="text"], input[type="password"]').forEach(fixEl);
    root.querySelectorAll('*').forEach(el=>{
      if(el.shadowRoot) fixInputs(el.shadowRoot);
    });
  } catch(e) { /* ignore cross-origin or detached nodes */ }
}
function run(){
  try{ fixInputs(window.parent.document); }catch(e){}
  try{ fixInputs(document); }catch(e){}
}
run();
setInterval(run, 400);
try{
  const obs = new MutationObserver(run);
  obs.observe(window.parent.document.body, {childList:true, subtree:true});
}catch(e){}
</script>
""", height=0)

 
# HERO BANNER  - decorative, matches the design concept
 
HERO_HTML = """
<div style="position:relative;height:260px;border-radius:16px;overflow:hidden;
  background:radial-gradient(ellipse at 30% 20%,#1c1533 0%,#0B0A14 55%),#120F1E;
  font-family:'Inter',sans-serif; border:1px solid rgba(255,255,255,0.1);">
  <canvas id="net" style="position:absolute;inset:0;width:100%;height:100%;"></canvas>
  <div id="bot" style="position:absolute;width:38px;height:38px;border-radius:50%;
    background:radial-gradient(circle at 35% 30%,#4be3cf,#6C3CE9 70%);
    box-shadow:0 0 24px 6px rgba(41,224,196,0.4); z-index:3; pointer-events:none;
    animation:breathe 2.6s ease-in-out infinite;"></div>
  <style>@keyframes breathe{0%,100%{transform:scale(1)}50%{transform:scale(1.1)}}</style>
  <div style="position:relative;z-index:2;height:100%;display:flex;flex-direction:column;
    justify-content:center;padding:0 40px;">
    <div style="font-family:'IBM Plex Mono',monospace;font-size:12px;letter-spacing:.14em;
      text-transform:uppercase;color:#29E0C4;margin-bottom:12px;">◆ Vision · AI Learning Buddy</div>
    <div id="type" style="font-family:'Space Grotesk',sans-serif;font-weight:700;
      font-size:32px;color:#F3F1FA;min-height:40px;"></div>
    <div style="font-size:14px;color:#948FB0;margin-top:10px;max-width:520px;line-height:1.5;">
      Open-Vocabulary Object Detection  - explained, quizzed, and graded, one session at a time.
    </div>
  </div>
</div>
<script>
  const canvas = document.getElementById('net');
  const ctx = canvas.getContext('2d');
  function resize(){ canvas.width = canvas.offsetWidth; canvas.height = canvas.offsetHeight; }
  resize(); window.addEventListener('resize', resize);
  const nodes = Array.from({length:60}, ()=>({
    x: Math.random()*canvas.width, y: Math.random()*canvas.height,
    vx:(Math.random()-0.5)*0.35, vy:(Math.random()-0.5)*0.35
  }));
  const mouse = {x:-999,y:-999};
  const wrap = canvas.parentElement;
  wrap.addEventListener('mousemove', e=>{
    const r = canvas.getBoundingClientRect();
    mouse.x = e.clientX - r.left; mouse.y = e.clientY - r.top;
    const bot = document.getElementById('bot');
    bot.style.left = (mouse.x-19)+'px'; bot.style.top = (mouse.y-19)+'px';
    bot.style.opacity = 1;
  });
  wrap.addEventListener('mouseleave', ()=>{
    mouse.x=-999; mouse.y=-999;
    document.getElementById('bot').style.opacity = 0;
  });
  function draw(){
    ctx.clearRect(0,0,canvas.width,canvas.height);
    nodes.forEach(n=>{
      n.x+=n.vx; n.y+=n.vy;
      if(n.x<0||n.x>canvas.width) n.vx*=-1;
      if(n.y<0||n.y>canvas.height) n.vy*=-1;
      const dx=n.x-mouse.x, dy=n.y-mouse.y, d=Math.sqrt(dx*dx+dy*dy);
      if(d<110){ const f=(110-d)/110; n.x+=(dx/d)*f*3; n.y+=(dy/d)*f*3; }
    });
    for(let i=0;i<nodes.length;i++){
      for(let j=i+1;j<nodes.length;j++){
        const dx=nodes[i].x-nodes[j].x, dy=nodes[i].y-nodes[j].y, d=Math.sqrt(dx*dx+dy*dy);
        if(d<115){ ctx.strokeStyle=`rgba(41,224,196,${0.18*(1-d/115)})`; ctx.beginPath();
          ctx.moveTo(nodes[i].x,nodes[i].y); ctx.lineTo(nodes[j].x,nodes[j].y); ctx.stroke(); }
      }
    }
    nodes.forEach(n=>{ ctx.beginPath(); ctx.arc(n.x,n.y,1.5,0,7); ctx.fillStyle='rgba(243,241,250,0.55)'; ctx.fill(); });
    requestAnimationFrame(draw);
  }
  draw();

  const text = "Teach it to see what it's never seen.";
  const el = document.getElementById('type'); let i=0;
  function type(){ if(i<text.length){ el.textContent += text[i]; i++; setTimeout(type,38); } }
  type();
</script>
"""
components.html(HERO_HTML, height=270)

TOPIC = "Open-Vocabulary Object Detection (OVOD)"

PERSONA = f"""You are Vision, an AI Learning Buddy for {TOPIC}.

You are patient and encouraging like a good beginner tutor - you break down complex
ideas (zero-shot detection, embedding spaces) into simple, relatable language first,
using real-world analogies before any jargon.

When the learner is ready to go deeper, you shift into research-companion mode  -
you bring in papers like ViLD, discuss base vs. novel categories, and connect ideas
to benchmarks like LVIS with proper technical nuance.

You also act as a quiz-master: you ask sharp, exam-style questions to make sure
learning actually sticks, and you give direct, honest feedback on answers  -
you point out exactly what's wrong or missing, no sugar-coating.

Always stay focused on {TOPIC} unless the learner explicitly asks about something else.
Keep responses focused and not overly long."""

 
# GEMINI SETUP
 
def get_api_key():
    try:
        if "GEMINI_API_KEY" in st.secrets:
            return st.secrets["GEMINI_API_KEY"]
    except Exception:
        pass
    return st.session_state.get("api_key_input", "")

def call_vision(prompt):
    """Send a prompt to Gemini (new google-genai SDK) with the Vision persona as system instruction."""
    api_key = get_api_key()
    if not api_key:
        return "⚠️ No API key found. Add GEMINI_API_KEY in Streamlit Secrets, or paste one in the sidebar."
    last_error = None
    for model_name in ["gemini-flash-latest", "gemini-3.5-flash"]:
        try:
            client = genai.Client(api_key=api_key)
            response = client.models.generate_content(
                model=model_name,
                contents=prompt,
                config=types.GenerateContentConfig(system_instruction=PERSONA)
            )
            return response.text
        except Exception as e:
            last_error = e
            continue
    return f"⚠️ Error calling Gemini: {last_error}"

 
# PROMPT TEMPLATES (reusable  - swap [TOPIC] for any subject)
 
def prompt_explain(topic):
    return f"Explain {topic} in simple, beginner-friendly language. Use a real-world analogy to make it relatable. Avoid jargon unless you explain it immediately."

def prompt_example(topic):
    return f"Give one clear, real-life example of {topic} in action - something a beginner can visualize or relate to from everyday life or a common industry use-case."

def prompt_quiz(topic, n=3):
    return f"Generate {n} quiz questions on {topic} to test understanding. Mix difficulty levels (easy to advanced), and include the correct answer with a brief explanation for each. Number them clearly."

def prompt_feedback(topic, question, answer):
    return f'Here is a question on {topic}: "{question}"\n\nMy answer: "{answer}"\n\nEvaluate it  - tell me if it\'s correct, what\'s missing or wrong, and how I can improve. Be direct and honest, do not sugarcoat.'

def prompt_full_session(topic):
    return f"You are an AI Learning Buddy for {topic}. Start by briefly explaining the topic simply with an analogy, then give one real-life example, then ask me 2-3 quiz questions one at a time."

 
# SIDEBAR
 
with st.sidebar:
    st.markdown("## 🔎 Vision")
    st.caption("AI Learning Buddy for OVOD")
    has_secret = False
    try:
        has_secret = "GEMINI_API_KEY" in st.secrets
    except Exception:
        has_secret = False
    if not has_secret:
        st.text_input("Gemini API Key", type="password", key="api_key_input",
                       help="Get one free at aistudio.google.com/app/apikey")
    st.divider()

    st.markdown("**Choose a mode**")
    modes = ["💬 Explain Simply", "🌍 Real Example", "📝 Quiz Me", "✅ Check My Answer", "🎓 Full Session"]
    if "mode" not in st.session_state:
        st.session_state.mode = modes[0]
    for m in modes:
        is_active = (st.session_state.mode == m)
        if st.button(m, key=f"navbtn_{m}", use_container_width=True,
                     type="primary" if is_active else "secondary"):
            st.session_state.mode = m
            st.rerun()
    mode = st.session_state.mode

    st.divider()
    st.caption(f"Topic locked to: **{TOPIC}**")

if "chat_log" not in st.session_state:
    st.session_state.chat_log = []

def show_log():
    for role, msg in st.session_state.chat_log:
        with st.chat_message(role):
            st.markdown(msg)

 
# MODE: EXPLAIN SIMPLY
 
if mode == "💬 Explain Simply":
    show_log()
    if st.button("Explain OVOD to me simply", use_container_width=True):
        with st.spinner("Vision is thinking..."):
            reply = call_vision(prompt_explain(TOPIC))
        st.session_state.chat_log.append(("user", "Explain it to me simply."))
        st.session_state.chat_log.append(("assistant", reply))
        st.rerun()

 
# MODE: REAL EXAMPLE
elif mode == "🌍 Real Example":
    show_log()
    if st.button("Give me a real-world example", use_container_width=True):
        with st.spinner("Vision is thinking..."):
            reply = call_vision(prompt_example(TOPIC))
        st.session_state.chat_log.append(("user", "Give me a real-life example."))
        st.session_state.chat_log.append(("assistant", reply))
        st.rerun()

# MODE: QUIZ ME
elif mode == "📝 Quiz Me":
    show_log()
    n = st.slider("How many questions?", 1, 5, 3)
    if st.button("Generate quiz", use_container_width=True):
        with st.spinner("Vision is writing your quiz..."):
            reply = call_vision(prompt_quiz(TOPIC, n))
        st.session_state.chat_log.append(("user", f"Give me {n} quiz questions."))
        st.session_state.chat_log.append(("assistant", reply))
        st.rerun()

 
# MODE: CHECK MY ANSWER (feedback)
 
elif mode == "✅ Check My Answer":
    show_log()
    st.markdown("Paste a question Vision gave you, and your answer, to get honest feedback.")
    q = st.text_area("Question", placeholder="e.g. What is zero-shot detection?")
    a = st.text_area("Your answer", placeholder="Type your answer here...")
    if st.button("Check my answer", use_container_width=True):
        if q.strip() and a.strip():
            with st.spinner("Vision is grading..."):
                reply = call_vision(prompt_feedback(TOPIC, q, a))
            st.session_state.chat_log.append(("user", f"Q: {q}\nMy answer: {a}"))
            st.session_state.chat_log.append(("assistant", reply))
            st.rerun()
        else:
            st.warning("Fill in both the question and your answer first.")

 
# MODE: FULL SESSION
 
elif mode == "🎓 Full Session":
    show_log()
    if st.button("Start full guided session", use_container_width=True):
        with st.spinner("Vision is preparing your session..."):
            reply = call_vision(prompt_full_session(TOPIC))
        st.session_state.chat_log.append(("user", "Start a full session with me."))
        st.session_state.chat_log.append(("assistant", reply))
        st.rerun()

    user_reply = st.chat_input("Reply to Vision (e.g. your quiz answer)...")
    if user_reply:
        with st.spinner("Vision is responding..."):
            reply = call_vision(user_reply)
        st.session_state.chat_log.append(("user", user_reply))
        st.session_state.chat_log.append(("assistant", reply))
        st.rerun()

st.divider()
if st.button("🗑️ Clear conversation"):
    st.session_state.chat_log = []
    st.rerun()
