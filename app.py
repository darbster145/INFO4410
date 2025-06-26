# app.py
from flask import Flask, request, render_template, redirect, flash
from card.addCard import add_card
from card.EditCard import edit_card

app = Flask(__name__)
app.secret_key = 'something-secure'

@app.route('/addcard')
def add_card_form():
    return render_template('AddForm.html')

@app.route("/", methods=["GET", "POST"])
def form():
    if request.method == "POST":
        card_data = {
            "card_name": request.form["cardName"],
            "description": request.form["description"],
            "rarity": request.form["rarity"],
            "card_price": float(request.form["cardPrice"]),
            "set_name": request.form["setName"]
        }

        result = add_card(card_data)

        if result.get("error"):
            flash("Error: " + result["error"]["message"], "error")
        else:
            flash("Card added successfully!", "success")

        return redirect("/")

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
