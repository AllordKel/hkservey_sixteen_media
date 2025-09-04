from flask import Flask, render_template, request, redirect, url_for, session
import json

app = Flask(__name__)
app.secret_key = "supersecret"


@app.route("/")
def landing():
    return render_template("landing.html")


@app.route("/start_survey", methods=["POST"])
def start_survey():
    # collecting data
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    email = request.form["email"]

    # saving in session
    session["user"] = {"first_name": first_name, "last_name": last_name, "email": email}

    # switching to survey
    return redirect(url_for("survey"))


@app.route("/survey", methods=["GET", "POST"])
def survey():
    if request.method == "POST":
        answers = request.form.to_dict()

        # adding to json
        data = {"user": session.get("user", {}), "answers": answers}

        with open("survey_data.json", "a", encoding="utf-8") as f:
            f.write(json.dumps(data, ensure_ascii=False) + "\n")

        return redirect(url_for("thank_you"))

    return render_template("survey.html")  # questions


@app.route("/thank_you")
def thank_you():
    return render_template("typ.html")


if __name__ == "__main__":
    app.run(debug=True)
