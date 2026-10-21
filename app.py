from flask import Flask, render_template, request, redirect
from detector import analyze_email

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyzer")
def analyzer():
    return render_template("analyzer.html")


@app.route("/analyze", methods=["POST"])
def analyze():

    email = request.form["email"]

    result, score, reasons = analyze_email(email)

    return render_template(
        "analyzer.html",
        result=result,
        score=score,
        reasons=reasons
    )


@app.route("/feedback", methods=["POST"])
def feedback():

    rating = request.form["rating"]
    comment = request.form["comment"]

    with open("feedback.txt", "a", encoding="utf-8") as file:
        file.write(f"Rating: {rating}\n")
        file.write(f"Comment: {comment}\n")
        file.write("-" * 40 + "\n")

    return redirect("/analyzer")


if __name__ == "__main__":
    app.run(debug=True)