# SWYNEX AI — Student Feedback Sentiment Analyzer

## Run
1. Open this folder in VS Code.
2. Open Terminal.
3. Install Flask:
   `pip install -r requirements.txt`
4. Start:
   `python app.py`
5. Open the local address shown by Flask, usually:
   `http://127.0.0.1:5000`

## CSV format
Your CSV should have a column named:
`feedback`

## Demo flow
- Show dashboard
- Upload `data/student_feedback.csv`
- Show Positive / Negative / Neutral counts
- Enter: `The teaching method is not good`
- Enter: `I feel like quitting`
- Explain that the engine handles basic negation/context rules
