
from flask import Flask, render_template, request
import random

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    dice = []
    total = 0
    number = 2

    if request.method == "POST":
        try:
            number = int(request.form.get("number", 2))
            number = max(1, min(number, 10))
            dice = [random.randint(1, 6) for _ in range(number)]
            total = sum(dice)
        except (ValueError, TypeError):
            number = 2

    return render_template(
        "index.html",
        dice=dice,
        total=total,
        number=number
    )

if __name__ == "__main__":
    app.run(debug=True)
