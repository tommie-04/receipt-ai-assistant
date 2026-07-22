# 🧾 AI Receipt Assistant

An AI-powered expense tracker that automatically reads receipts, bank statements, and handwritten notes — no manual entry needed.

## What it does

Upload a photo of a receipt, statement screenshot, or handwritten expense note. The app uses Google's Gemini AI to extract the merchant, amount, date, category, and individual items, then saves everything to your personal history.

## Tech Stack

- **Frontend:** Streamlit
- **AI:** Google Gemini API (`gemini-3.5-flash`)
- **Database:** SQLite
- **Language:** Python

## Setup

```bash
git clone https://github.com/tommie-04/receipt-ai-assistant.git
cd receipt-ai-assistant

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt
```

Create a `.env` file in the project root:

Run the app:

```bash
streamlit run app.py
```

## Features

- AI-powered receipt/statement/handwriting recognition
- Automatic spending categorization
- Line-item level detail extraction
- Detects and rejects irrelevant (non-financial) images
- Simple username login
- Persistent transaction history

## Roadmap

- [ ] Spending analytics by day/week/month
- [ ] Charts and visualizations
- [ ] AI-generated spending insights

## License

MIT
