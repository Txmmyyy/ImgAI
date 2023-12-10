from flask import Flask, request, jsonify
from transformers import pipeline

summarizer = pipeline("summarization", model="Falconsai/text_summarization")

app = Flask(__name__)

@app.route("/summarize", methods=["POST"])
def summarize_text():
    data = request.get_json()

    text = data.get("text")

    if not text:
        return jsonify({"error": "Missing text field in request body"}), 400

    try:
        summary = summarizer(text, max_length=3000, min_length=30, do_sample=False)
    except Exception as e:
        return jsonify({"error": f"Error summarizing text: {e}"}), 500

    return jsonify({"summary": summary[0]["summary_text"]}), 200

if __name__ == "__main__":
    app.run(debug=False)
