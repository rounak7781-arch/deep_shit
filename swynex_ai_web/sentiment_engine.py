import re

POSITIVE_WORDS = {
    "good", "great", "excellent", "amazing", "helpful",
    "easy", "love", "like", "satisfied", "best",
    "awesome", "nice", "clear", "interesting"
}

NEGATIVE_WORDS = {
    "bad", "poor", "terrible", "worst", "hate",
    "difficult", "hard", "slow", "confusing", "boring",
    "unsatisfied", "problem", "issue", "waste",
    "quitting", "useless", "disappointing"
}

NEGATIONS = {"not", "no", "never", "neither", "nor", "isn't", "wasn't", "don't", "doesn't", "didn't"}

def analyze_sentiment(text):
    words = re.findall(r"\b[a-zA-Z']+\b", text.lower())

    positive = 0
    negative = 0

    for i, word in enumerate(words):
        previous = words[max(0, i-3):i]
        negated = any(w in NEGATIONS for w in previous)

        if word in POSITIVE_WORDS:
            if negated:
                negative += 1
            else:
                positive += 1

        elif word in NEGATIVE_WORDS:
            if negated:
                positive += 1
            else:
                negative += 1

    phrase = " ".join(words)

    # Context-aware phrases
    if "feel like quitting" in phrase or "want to quit" in phrase:
        negative += 2

    if "not good" in phrase or "not helpful" in phrase or "not easy" in phrase:
        negative += 2

    if positive > negative:
        return "Positive"
    if negative > positive:
        return "Negative"
    return "Neutral"
