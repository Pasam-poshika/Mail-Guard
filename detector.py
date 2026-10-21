import re

def analyze_email(email):

    score = 0
    reasons = []

    email_lower = email.lower()

    keyword_rules = {
        "urgent": (15, "Urgent language detected"),
        "verify": (15, "Requests verification"),
        "password": (20, "Requests password"),
        "otp": (20, "Requests OTP"),
        "click here": (15, "Encourages clicking a link"),
        "bank": (10, "Mentions bank account"),
        "account": (10, "Mentions account"),
        "payment": (10, "Mentions payment"),
        "gift card": (20, "Requests gift cards"),
        "winner": (20, "Claims you won a prize"),
        "claim": (10, "Asks you to claim a reward"),
        "login": (15, "Requests login"),
        "limited time": (15, "Creates urgency"),
        "suspended": (20, "Threatens account suspension"),
        "bitcoin": (20, "Mentions cryptocurrency"),
        "crypto": (20, "Mentions cryptocurrency"),
        "wallet": (15, "Requests wallet details"),
        "cvv": (25, "Requests CVV"),
        "pin": (20, "Requests PIN")
    }

    for word, (points, message) in keyword_rules.items():
        if word in email_lower:
            score += points
            reasons.append(message)

    # Detect links
    if "http://" in email_lower or "https://" in email_lower:
        score += 20
        reasons.append("Contains website link")

    urls = re.findall(r'https?://\\S+', email)

    shorteners = [
        "bit.ly",
        "tinyurl",
        "goo.gl",
        "t.co",
        "is.gd",
        "ow.ly"
    ]

    for url in urls:
        if any(short in url.lower() for short in shorteners):
            score += 20
            reasons.append("Uses URL shortener")
            break

    # Too many exclamation marks
    if email.count("!") >= 3:
        score += 10
        reasons.append("Uses excessive exclamation marks")

    # Too many CAPITAL letters
    letters = [c for c in email if c.isalpha()]

    if letters:
        upper_ratio = sum(1 for c in letters if c.isupper()) / len(letters)

        if upper_ratio > 0.5:
            score += 10
            reasons.append("Uses excessive capital letters")

    score = min(score, 100)

    if score >= 60:
        result = "🔴 PHISHING"

    elif score >= 30:
        result = "🟡 SUSPICIOUS"

    else:
        result = "🟢 SAFE"

    if not reasons:
        reasons.append("No major phishing indicators found.")

    return result, score, reasons