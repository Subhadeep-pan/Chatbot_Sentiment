from flask import Flask, render_template, request, jsonify
from sentiment import SentimentAnalyzer, EmotionalChatBot

app = Flask(__name__)

analyzer = SentimentAnalyzer()
bot = EmotionalChatBot()
history = []

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    user_msg = request.json["message"]

    result = analyzer.analyze_message(user_msg)
    reply = bot.generate_response(result)

    history.append(user_msg)

    avg, label = analyzer.analyze_conversation(history)
    trend = analyzer.analyze_trend(history)

    return jsonify({
        "reply": reply,
        "sentiment": result,
        "overall": {
            "avg": round(avg, 2),
            "label": label,
            "trend": trend
        }
    })

if __name__ == "__main__":
    app.run(debug=True)
