from textblob import TextBlob


class SentimentAnalyzer:
    def analyze_message(self, text):
        """
        Handles sentiment analysis for single messages.
        Returns polarity (-1 to 1) and label (Positive/Negative/Neutral).
        """
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity

        lower_text = text.lower()

        negative_keywords = [
            "disappoint", "disappointed", "disappoints",
            "bad", "terrible", "awful", "worst",
            "angry", "upset", "hate", "poor service"
        ]

        if any(word in lower_text for word in negative_keywords) and polarity > -0.4:
            polarity -= 0.4 
        if polarity > 0.1:
            label = "Positive"
        elif polarity < -0.1:
            label = "Negative"
        else:
            label = "Neutral"

        return {
            "polarity": polarity,
            "label": label,
        }

    def analyze_conversation(self, user_messages):
        if not user_messages:
            return {
                "average_polarity": 0.0,
                "label": "Neutral",
                "description": "No messages to analyze.",
            }

        polarities = []
        for msg in user_messages:
            result = self.analyze_message(msg)
            polarities.append(result["polarity"])

        avg_polarity = sum(polarities) / len(polarities)

        if avg_polarity > 0.1:
            label = "Positive"
            description = "Overall conversation sentiment: Positive – generally satisfied or optimistic."
        elif avg_polarity < -0.1:
            label = "Negative"
            description = "Overall conversation sentiment: Negative – general dissatisfaction or concern."
        else:
            label = "Neutral"
            description = "Overall conversation sentiment: Neutral – mixed or balanced emotions."

        return {
            "average_polarity": avg_polarity,
            "label": label,
            "description": description,
        }

    def analyze_trend(self, user_messages):
        if len(user_messages) < 3:
            return "Mood trend: Not enough data to identify a clear trend."

        polarities = [self.analyze_message(msg)["polarity"] for msg in user_messages]

        mid = len(polarities) // 2
        early = polarities[:mid]
        late = polarities[mid:]

        if len(early) == 0 or len(late) == 0:
            return "Mood trend: Not enough data to identify a clear trend."

        early_avg = sum(early) / len(early)
        late_avg = sum(late) / len(late)

        diff = late_avg - early_avg

        if diff > 0.1:
            return "Mood trend: Improving – the conversation became more positive over time."
        elif diff < -0.1:
            return "Mood trend: Worsening – the conversation became more negative over time."
        else:
            return "Mood trend: Stable – no major shift in emotional tone."


class SimpleChatBot:
    def generate_response(self, user_message):
        text = user_message.lower().strip()

        if any(greet in text for greet in ["hi", "hello", "hey"]):
            return "Hello! How are you feeling today?"
        if "bye" in text or "exit" in text or "quit" in text:
            return "Goodbye! Thanks for chatting with me."
        if "sad" in text or "upset" in text or "angry" in text:
            return "I'm sorry you're feeling that way. Do you want to talk about it more?"
        if "happy" in text or "great" in text or "awesome" in text:
            return "That’s good to hear! Tell me more about what’s going well."
        if "service" in text or "support" in text:
            return "I understand. What specifically about the service bothered you or pleased you?"

        return "I see. Please tell me more."


def run_chat():
    analyzer = SentimentAnalyzer()
    bot = SimpleChatBot()

    conversation_history = []

    print("ChatBot with Sentiment Analysis")
    print("--------------------------------")
    print("Type 'quit' or 'exit' to end the conversation.\n")

    while True:
        user_input = input("User: ")

        if user_input.lower().strip() in ["quit", "exit"]:
            print("ChatBot: Ending conversation. Let me analyze our chat...\n")
            break

        sentiment_result = analyzer.analyze_message(user_input)
        bot_reply = bot.generate_response(user_input)

        print(f"→ Sentiment: {sentiment_result['label']} (score = {sentiment_result['polarity']:.2f})")
        print(f"ChatBot: {bot_reply}\n")

        conversation_history.append({
            "user_message": user_input,
            "bot_reply": bot_reply,
            "sentiment_label": sentiment_result["label"],
            "polarity": sentiment_result["polarity"],
        })

    user_messages_only = [c["user_message"] for c in conversation_history]
    overall = analyzer.analyze_conversation(user_messages_only)
    trend_summary = analyzer.analyze_trend(user_messages_only)

    print("===== FINAL SENTIMENT REPORT =====")
    print(f"Overall conversation sentiment: {overall['label']}")
    print(f"Average sentiment score: {overall['average_polarity']:.2f}")
    print(overall["description"])
    print(trend_summary)
    print("==================================")


if __name__ == "__main__":
    run_chat()
