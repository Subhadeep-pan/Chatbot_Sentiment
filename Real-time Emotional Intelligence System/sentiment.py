from textblob import TextBlob


class SentimentAnalyzer:
    def __init__(self):
        self.negative_keywords = [
            "disappoint", "disappointed", "disappoints",
            "bad", "terrible", "awful", "worst",
            "angry", "upset", "hate", "poor service"
        ]

        self.negation_words = ["not", "never", "no", "hardly", "barely"]

        self.emotion_keywords = {
            "joy": ["happy", "great", "awesome", "love", "fantastic", "amazing"],
            "anger": ["angry", "furious", "hate", "worst", "annoyed", "irritated"],
            "sadness": ["sad", "upset", "disappointed", "depressed", "unhappy"],
            "fear": ["scared", "worried", "nervous", "afraid", "anxious"],
        }

    def detect_emotion(self, text):
        scores = {emotion: 0 for emotion in self.emotion_keywords}
        lower = text.lower()

        for emotion, words in self.emotion_keywords.items():
            for word in words:
                if word in lower:
                    scores[emotion] += 1

        emotion = max(scores, key=scores.get)
        intensity = scores[emotion]

        if intensity == 0:
            emotion = "neutral"

        return emotion, intensity

    def detect_sarcasm(self, text, polarity):
        lower = text.lower()
        if "yeah right" in lower or ("great" in lower and polarity < 0):
            return True
        return False

    def analyze_message(self, text):
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        lower = text.lower()

        has_negation = any(neg + " " + word in lower
                           for neg in self.negation_words
                           for word in self.negative_keywords)

        if any(word in lower for word in self.negative_keywords):
            if not has_negation:
                polarity -= 0.3

        emotion, intensity = self.detect_emotion(text)
        sarcasm = self.detect_sarcasm(text, polarity)

        if sarcasm:
            polarity -= 0.4
            emotion = "anger"

        polarity = max(-1.0, min(1.0, polarity))

        if polarity > 0.1:
            label = "Positive"
        elif polarity < -0.1:
            label = "Negative"
        else:
            label = "Neutral"

        return {
            "polarity": polarity,
            "label": label,
            "emotion": emotion,
            "intensity": intensity,
            "sarcasm": sarcasm
        }

    def analyze_conversation(self, user_messages):
        polarities = [self.analyze_message(m)["polarity"] for m in user_messages]
        avg = sum(polarities) / len(polarities)

        if avg > 0.1:
            label = "Positive"
        elif avg < -0.1:
            label = "Negative"
        else:
            label = "Neutral"

        return avg, label

    def analyze_trend(self, user_messages):
        if len(user_messages) < 4:
            return "Mood trend: Not enough data."

        polarities = [self.analyze_message(m)["polarity"] for m in user_messages]
        weights = [1, 2, 3, 4, 5]
        recent = polarities[-5:]

        weighted_avg = sum(p * w for p, w in zip(recent, weights[-len(recent):])) / sum(weights[-len(recent):])

        if weighted_avg > 0.2:
            return "Mood trend: Strong positive improvement."
        elif weighted_avg < -0.2:
            return "Mood trend: Strong negative deterioration."
        else:
            return "Mood trend: Emotionally stable."


class EmotionalChatBot:
    def generate_response(self, sentiment):
        emotion = sentiment["emotion"]
        intensity = sentiment["intensity"]

        if emotion == "anger":
            return "That sounds seriously frustrating. Walk me through what went wrong."
        if emotion == "sadness":
            return "That’s heavy. I’m here — want to talk about it?"
        if emotion == "joy":
            return "Love that vibe! What made your day so good?"
        if sentiment["sarcasm"]:
            return "I’m sensing sarcasm — sounds like something’s really off."

        return "I’m listening. Tell me more."


def run_chat():
    analyzer = SentimentAnalyzer()
    bot = EmotionalChatBot()
    history = []

    print("=== Emotional Intelligence ChatBot ===")
    print("Type 'quit' to exit.\n")

    while True:
        user = input("User: ")

        if user.lower() in ["quit", "exit"]:
            break

        result = analyzer.analyze_message(user)
        reply = bot.generate_response(result)

        print(f"→ Sentiment: {result['label']} | Emotion: {result['emotion']} | Score: {result['polarity']:.2f}")
        print(f"Bot: {reply}\n")

        history.append(user)

    avg, label = analyzer.analyze_conversation(history)
    trend = analyzer.analyze_trend(history)

    print("\n===== FINAL REPORT =====")
    print(f"Overall sentiment: {label}")
    print(f"Average polarity: {avg:.2f}")
    print(trend)
    print("========================")


if __name__ == "__main__":
    run_chat()
 