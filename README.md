# Homework Helper (NLP based)📚

A multi-agent AI app that helps you solve homework questions. Ask anything — it figures out what you're asking, solves it step by step, checks its own answer, then gives you a clean summary.

🔗 **Live Demo → [homeworkassistant.streamlit.app](https://homeworkassistant.streamlit.app/)**

---

## Demo

<!-- Save a screenshot of your app as 'demo.png' in the repo root folder -->
<img width="1381" height="674" alt="Screenshot 2026-04-17 005107" src="https://github.com/user-attachments/assets/52fdf372-114e-49df-ad60-f1acba49370d" />

---

## 🛠️ Tech Stack

| Layer          |            Technology |
| -------------- | --------------------: |
| Frontend       |             Streamlit |
| Backend Agents | Python (custom logic) |
| NLP Engine     |  spaCy / Transformers |
| Deployment     |       Streamlit Cloud |

---

## ⚙️ How It Works

1. **User Input** via Streamlit UI

2. **Query Analysis** (NLP/custom rules) detects intent, difficulty, and key topics

3. Query is passed through a **multi-agent pipeline**:

   * **Clarification Agent** — checks if the question is clear
   * **Solution Agent** — solves it step-by-step
   * **QA Agent** — reviews for mistakes and improvements
   * **Concise Answer Agent** — gives the final short answer

4. **Output** is displayed in the UI with the structured response and optional explanation steps.

---

## 💡 Tips & Extensions

* Add a **solution-checker agent** to verify student answers.
* Integrate a **knowledge base** (local files or vector DB) for subject-specific resources.
* Add **assistant personas** (concise tutor, detailed explainer, hint-giver).
* Add unit tests for agents to ensure stable behavior.

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
