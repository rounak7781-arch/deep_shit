from flask import Flask, render_template, request, jsonify
import csv
import io
from sentiment_engine import analyze_sentiment

app = Flask(__name__)

SAMPLE_DATA = [
    {"feedback": "The system is very easy and helpful", "sentiment": "Positive"},
    {"feedback": "The teacher is poor", "sentiment": "Negative"},
    {"feedback": "The classroom is okay", "sentiment": "Neutral"},
]

def analyze_rows(rows):
    results = []
    for row in rows:
        feedback = row.get("feedback", "").strip()
        if feedback:
            results.append({
                "feedback": feedback,
                "sentiment": analyze_sentiment(feedback)
            })
    return results

@app.route("/")
def index():
    results = analyze_rows(SAMPLE_DATA)
    return render_template("index.html", results=results)

@app.post("/analyze")
def analyze():
    data = request.get_json(silent=True) or {}
    feedback = data.get("feedback", "").strip()
    if not feedback:
        return jsonify({"error": "Please enter feedback."}), 400

    return jsonify({
        "feedback": feedback,
        "sentiment": analyze_sentiment(feedback)
    })

@app.post("/upload")
def upload():
    uploaded = request.files.get("file")
    if not uploaded or uploaded.filename == "":
        return jsonify({"error": "Please choose a CSV file."}), 400

    try:
        text = uploaded.read().decode("utf-8-sig")
        reader = csv.DictReader(io.StringIO(text))

        if not reader.fieldnames or "feedback" not in reader.fieldnames:
            return jsonify({"error": "CSV must contain a column named 'feedback'."}), 400

        results = analyze_rows(reader)
        counts = {
            "Positive": sum(r["sentiment"] == "Positive" for r in results),
            "Negative": sum(r["sentiment"] == "Negative" for r in results),
            "Neutral": sum(r["sentiment"] == "Neutral" for r in results),
        }

        return jsonify({"results": results, "counts": counts})
    except Exception as exc:
        return jsonify({"error": f"Could not read CSV: {exc}"}), 400

if __name__ == "__main__":
    app.run(debug=True)
