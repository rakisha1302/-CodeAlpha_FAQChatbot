# 💬 FAQ Chatbot – Smart AI-Powered FAQ Assistant
CodeAlpha AI Internship · Task 2

An NLP-based FAQ chatbot (not if-else rules). It cleans the user's question, converts it to a **TF-IDF** vector,
compares it with every FAQ using **cosine similarity**, and returns the best answer. Premium dark-purple Streamlit UI.
Runs fully offline: **no paid APIs, no API keys.**

## Features
- Chat bubbles, welcome message, typing indicator, clickable suggested and related questions, clear-chat button
- 45 FAQs in 7 categories stored in `data/faqs.csv`
- Preprocessing: lowercase, punctuation and space cleanup, tokenising, synonyms, stop words, light stemming
- Configurable similarity threshold (sidebar) with friendly fallback
- Dashboard: total FAQs, questions asked, matched, unanswered, success rate, average score, category chart
- Admin page: add and delete FAQs (validated), model retrains instantly, search, CSV download, optional password
- Error handling for empty input, missing or invalid FAQ files, and unmatched questions

## Project structure
```
faq-chatbot/
├── app.py                  # Streamlit UI and pages
├── modules/
│   ├── nlp.py              # preprocessing, TF-IDF, cosine similarity
│   ├── data_manager.py     # load / validate / add / delete FAQs
│   └── ui.py               # HTML components
├── data/faqs.csv           # knowledge base (edit freely)
├── assets/style.css        # purple glassmorphism theme
├── tests/test_chatbot.py   # pytest suite
├── .streamlit/config.toml  # theme
├── requirements.txt  .gitignore  README.md
```

## Run on Windows (PowerShell)
```powershell
cd faq-chatbot
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app.py
```
If activation is blocked: `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`, then activate again.

## Run the tests
```powershell
python -m pytest -v
```
Covers: exact question, different wording, uppercase, extra spaces, unrelated question, empty input,
threshold, related questions, FAQ add/delete updates, validation, missing and invalid files.

## Manage FAQs
Edit `data/faqs.csv` (columns `category,question,answer`) or use the **Admin** page.
To protect Admin, set `ADMIN_PASSWORD` in `.streamlit/secrets.toml` (see `secrets.toml.example`) or as an environment variable.

## Upload to GitHub
```powershell
git init
git add .
git commit -m "FAQ Chatbot - CodeAlpha Task 2"
git branch -M main
git remote add origin https://github.com/<your-username>/faq-chatbot.git
git push -u origin main
```
Create the empty repository `faq-chatbot` on github.com first (no README).

## Deploy on Streamlit Community Cloud
1. Go to https://share.streamlit.io and sign in with GitHub.
2. Click **Create app**, choose your repository, branch `main`, main file `app.py`.
3. Optional: **Advanced settings → Secrets** → `ADMIN_PASSWORD = "your-password"`.
4. Click **Deploy**. Admin changes on Cloud reset on restart; commit `faqs.csv` to keep them.

## LinkedIn description
🚀 Excited to share my CodeAlpha AI Internship project: **FAQ Chatbot – Smart AI-Powered FAQ Assistant**!
It uses NLP preprocessing, TF-IDF vectorization and cosine similarity (scikit-learn) to match user questions to the
most relevant answer from a 45-entry knowledge base, even when the wording is different. Built with Python and Streamlit,
featuring a premium dark-purple chat UI, a live analytics dashboard and an admin panel that retrains the model instantly.
🔗 Live demo: <link> · 💻 Code: <github link>
#AI #NLP #Python #Streamlit #MachineLearning #CodeAlpha #Internship

## Video demo script (about 2 minutes)
1. **0:00** Introduce yourself and the project: "An FAQ chatbot that understands meaning, not keywords."
2. **0:15** Show the Chat page: welcome message, click a suggested question, point out the category and match-score chips.
3. **0:40** Type a differently worded question ("I forgot my password, how can I change it?") and an UPPERCASE one with extra spaces.
4. **1:00** Ask an unrelated question to show the fallback and related questions. Move the threshold slider and repeat.
5. **1:15** Open Dashboard: metrics, success rate, unanswered questions.
6. **1:30** Open Admin: add a new FAQ, then ask it in chat to show the model updating instantly.
7. **1:50** Explain the pipeline (preprocessing → TF-IDF → cosine similarity) and close with the GitHub and live links.
