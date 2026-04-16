# Homework Helper (NLP based)📚

A multi-agent AI app that helps you solve homework questions. Ask anything — it figures out what you're asking, solves it step by step, checks its own answer, then gives you a clean summary.

🔗 **Live Demo → [homeworkassistant.streamlit.app](https://homeworkassistant.streamlit.app/)**

---

## Demo

<!-- Save a screenshot of your app as 'demo.png' in the repo root folder -->
<img width="1381" height="674" alt="Screenshot 2026-04-17 005107" src="https://github.com/user-attachments/assets/52fdf372-114e-49df-ad60-f1acba49370d" />


---

## How it works

4 agents run one after another:

1. **Clarification** — makes sure the question is clear enough to answer
2. **Solution** — breaks it down step by step
3. **QA** — checks the solution for any mistakes
4. **Concise Answer** — gives you the short version

The sidebar also does a quick analysis of your question — detects the type, complexity, and key topics using basic NLP.

---

## Built with

- **Groq** — LLaMA 3.3 70B Versatile
- **Streamlit** — UI
- **streamlit-shadcn-ui** — copy button
- **python-dotenv** — local API key management

---

## Run locally

**1. Clone the repo**
```bash
git clone https://github.com/krishparmar003/Homework-Helper-using-NLP.git
cd Homework-Helper-using-NLP
```

**2. Create a virtual environment**
```bash
python -m venv myenv
```

**3. Activate it**
```bash
# Windows
myenv\Scripts\activate

# Mac/Linux
source myenv/bin/activate
```

**4. Install dependencies**
```bash
pip install -r requirements.txt
```

**5. Add your API key**

Create a `.env` file in the root folder:
```
GROQ_API_KEY=your_key_here
```

Get a free key at [console.groq.com](https://console.groq.com)

**6. Run the app**
```bash
streamlit run streamlit_app.py
```

---

## Structure

```
├── agent.py            # Groq client + 4 agent functions
├── streamlit_app.py    # UI + NLP analysis
├── requirements.txt
├── .gitignore
└── README.md
```

---

## License

MIT
