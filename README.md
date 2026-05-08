# AI Market Analyzer & Portfolio

## About Me

I am currently juggling two diverse fields of study: **Computer Science** and **Chemistry**. This unique combination allows me to approach problems with both analytical precision and creative logic. My passion lies in **Cyber Security**, where I enjoy understanding how systems break to make them stronger. I'm also deeply interested in web development, creating user interfaces that are intuitive and beautiful.

## AI Market Analyzer

This repository contains an automated script (`ai_market_analyzer.py`) that identifies new problem statements in the market and generates business analyses for them using the Gemini AI API.

### How it works:
1. It fetches the latest news about technology and startups from Google News via RSS.
2. It uses Google's Gemini AI to analyze these trends and extract new problem statements.
3. For each problem statement, the AI suggests a potential business solution, target market, and business model.
4. The insights are automatically saved to `market_insights.json` with a timestamp.
5. A built-in scheduler allows the script to run periodically (e.g., every 24 hours).

### Setup Instructions

1. **Clone the repository and create a virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. **Install the dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure your API Key (100% Free)**:
   This tool is completely free to use! Google offers a free tier for the Gemini API. Here is how to get it without a credit card:

   - Go to [Google AI Studio](https://aistudio.google.com/).
   - Sign in with your Google account.
   - Click on **"Get API key"** in the left menu.
   - Click the **"Create API key"** button.
   - Copy the generated key.

   Create a `.env` file in the root directory and add your free Google Gemini API key:
   ```env
   GEMINI_API_KEY="your_api_key_here"
   ```

### Running the Script

To run the analyzer once and start the daily schedule, simply run:
```bash
python ai_market_analyzer.py
```

The script will fetch news, generate the first set of insights, and then wait 24 hours before running again.