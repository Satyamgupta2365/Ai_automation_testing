# 🧠 AI-Powered Web Testing Automation

This repository demonstrates an **AI-driven testing automation tool** that intelligently validates user queries by combining:

- **LLaMA3 via Groq** for concise, LLM-generated answers
- **Google Search** scraping for real-time answer verification
- **Selenium with undetected_chromedriver** for browser automation
- **Visual debugging via screenshots** to track any issues during the test flow

---

## 📉 Architecture Overview

```
                            ┌────────────────────────────┐
                            │     User Query      │
                            └────────────────────────────┘
                                     │
                  ┌───────────────────────────────┐
                  │     LLM (via Groq / LLaMA3)        │
                  │  → Provides concise first-sentence │
                  └────────────────────────────┘
                                     │
         ┌─────────────────────────────────────────┐
         │     Web Scraper (Selenium + undetected_chromedriver)   │
         │  → Launches Chrome, handles cookies, queries Google     │
         │  → Captures top answers, fallback to various selectors │
         └─────────────────────────────────────────┘
                                     │
                    ┌─────────────────────────┐
                    │ Screenshot & Logging Engine       │
                    │ → Saves screenshots on errors     │
                    └─────────────────────────┘
                                     │
                ┌───────────────────────────────┐
                │ Compare LLM vs Google & Validate Output │
                └───────────────────────────────┘
```

---

## ✅ Features

- **LLM-generated test case** from natural language query
- **Web scraping for external validation** using real-time Google results
- **Multiple fallback selectors** for answer extraction
- **Screenshot logging** for easier debugging
- **Robust error handling** at every step

---

## 🚀 How to Run

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Add your Groq API Key
Create a `.env` file:
```env
GROQ_API_KEY=your_groq_api_key_here
```

### 3. Run the script
```bash
python main.py
```

Or run directly with a query:
```bash
python main.py "What is the capital of Japan?"
```

---

## 🚧 Technologies Used
- Python
- Groq API (LLaMA3)
- Selenium + undetected_chromedriver
- dotenv

---

## 🔮 Example Output
```
Ask a question: Who is the CEO of OpenAI?

🔄 Getting concise LLM response...
🔎 Searching Google...
🧠 LLM Answer: Sam Altman is the CEO of OpenAI.
🌍 Google Answer: Sam Altman
```

Screenshot saved as `search_results.png` for inspection if needed.

---

## 🚫 Limitations
- Google may block or throttle if scraping too frequently
- LLM may hallucinate or provide outdated answers
- Regional Google results may vary

---

## 🔧 Roadmap / Next Steps
- [ ] Add fuzzy similarity matching between LLM & Google answers
- [ ] Extend test suite with predefined assertions
- [ ] Deploy UI for non-technical testers (Streamlit or Flask)
- [ ] Add Google SERP API fallback

---

## 📊 License
MIT License. Feel free to fork and build on top of it.

---

## ✨ Contributions
Pull requests and issue discussions are welcome! Let’s build smarter test frameworks together.

