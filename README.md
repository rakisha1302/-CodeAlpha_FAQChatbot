# 🤖 NovaDesk AI – Smart FAQ Chatbot

NovaDesk AI is an intelligent FAQ chatbot built using **Python, Streamlit, and Natural Language Processing (NLP)**. It helps users find answers to frequently asked questions through a simple and interactive chat interface.

The chatbot uses machine learning techniques to understand user queries and identify the most relevant answers from a predefined FAQ dataset.

## 🌐 Live Demo

https://novadesk-faq-chatbot.streamlit.app/
## ✨ Features

- 💬 Interactive chatbot interface
- 🧠 NLP-based question matching
- 🔍 Finds relevant answers from the FAQ dataset
- 📂 FAQ data managed using a CSV file
- 🎨 Custom Streamlit user interface
- ⚡ Fast and simple responses
- 🧪 Unit testing with Pytest

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Streamlit | Web application interface |
| Scikit-learn | Machine learning and text similarity |
| Pandas | FAQ data handling |
| NLP | Understanding and matching user queries |
| Pytest | Testing |

## 📁 Project Structure

```text
-CodeAlpha_FAQChatbot/
│
├── .streamlit/
│   ├── config.toml
│   └── secrets.toml.example
│
├── assets/
│   └── style.css
│
├── data/
│   └── faqs.csv
│
├── modules/
│   ├── ui.py
│   ├── data_manager.py
│   └── nlp.py
│
├── tests/
│   └── test_chatbot.py
│
├── app.py
├── requirements.txt
├── README.md
└── .gitignore
```

## 🚀 Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/rakisha1302/-CodeAlpha_FAQChatbot.git
```

### 2. Navigate to the project folder

```bash
cd -CodeAlpha_FAQChatbot
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the virtual environment

**Windows:**

```bash
venv\Scripts\activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Run the application

```bash
streamlit run app.py
```

The application will open in your browser at:

`http://localhost:8501`

## 📊 How It Works

1. The user enters a question in the chatbot.
2. The application processes the input using NLP techniques.
3. The chatbot compares the question with the available FAQ data.
4. It identifies the most relevant matching answer.
5. The answer is displayed in the chat interface.

## 🧪 Run Tests

To execute the project tests, run:

```bash
pytest
```

## 🎯 Project Objective

The main objective of NovaDesk AI is to simplify access to frequently requested information by providing an automated, user-friendly chatbot experience.

This project was developed as part of the **CodeAlpha Internship Program**.

## 👩‍💻 Developer

**Rakisha R.**

B.Tech – Artificial Intelligence and Data Science

- GitHub: [rakisha1302](https://github.com/rakisha1302)
- LinkedIn: [Rakisha R.](https://www.linkedin.com/in/rakisha-r-5b02b8392/)

---

⭐ If you find this project interesting, consider giving the repository a star!
