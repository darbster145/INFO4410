# app.py
from flask import Flask, request, render_template, redirect, flash, url_for
from card.addCard import add_card  # now a plain function
from card.EditCard import update_card  # same here
from supabase import create_client

SUPABASE_URL = 'https://nuivtmqkqxmritchchxj.supabase.co'
SUPABASE_KEY ='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im51aXZ0bXFrcXhtcml0Y2hjaHhqIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTA4OTY1MjMsImV4cCI6MjA2NjQ3MjUyM30.cTgFkrqoJeNzmyggNZ8mf-gXcZu7xl-J8rYGXPyDGoA'

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

app = Flask(__name__)
app.secret_key = 'we have never met'

#route to add a card (uses post) referecessn addCard.py
@app.route('/addcard', methods=['GET', 'POST'])
def add_card_form():
    if request.method == 'POST':
        card_data = {
            'card_name': request.form['cardName'],
            'description': request.form['description'],
            'rarity': request.form['rarity'],
            'card_price': float(request.form['cardPrice']),
            'set_name': request.form['setName']
        }

        result = add_card(card_data)

        # Inspect .data for error handling
        if not result.data:
            flash("Error adding card. No data returned.", "error")
        else:
            flash("Card added successfully!", "success")

        return redirect('/addcard')

    return render_template('AddForm.html')

#route to show list to edit a card uses EditCard.py
@app.route('/edit')
def edit_card_list_route():
    response = supabase.table('cards').select('*').execute()
    cards = response.data if response.data else []
    return render_template('edit_list.html', cards=cards)

#route to edit a card references EditCard.py
@app.route('/edit/<int:card_id>', methods=['GET', 'POST'])
def edit_card_route(card_id):
    # Fetch the card by ID
    response = supabase.table('cards').select('*').eq('card_id', card_id).execute()
    card = response.data[0] if response.data else None

    if not card:
        flash('Card not found.', 'error')
        return redirect(url_for('edit_card_list_route'))

    if request.method == 'POST':
        if 'cancel' in request.form:
            return redirect(url_for('edit_card_list_route'))

        # Collect updated values from the form
        updated_card = {
            'card_name': request.form['card_name'],
            'description': request.form['description'],
            'rarity': request.form['rarity'],
            'card_price': float(request.form['card_price']),
            'set_name': request.form['set_name'],
            'img_url': request.form['img_url']
        }

        # Update the card in Supabase
        update_response = supabase.table('cards').update(updated_card).eq('card_id', card_id).execute()

        print(update_response)  # debug output

        if not update_response.data:
            flash("Error updating card: No data returned", "error")
        else:
            flash("Card updated successfully!", "success")

        return redirect(url_for('edit_card_list_route'))

    return render_template('edit_form.html', card=card)


@app.route('/')
def index():
    cards_response = supabase.table('cards').select('*').execute()
    cards = cards_response.data if cards_response.data else []
    return render_template('index.html', cards=cards)


if __name__ == "__main__":
    app.run(debug=True)

