from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    memo = None

    if request.method == "POST":
        memo = request.form.get("memo")

    return render_template("index.html", memo=memo)

if __name__ == "__main__":
    app.run(debug=True)