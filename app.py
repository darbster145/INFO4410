from flask import Flask, request, render_template, redirect, flash, url_for
from card.addCard import add_card
from card.EditCard import update_card
from supabase import create_client
from werkzeug.utils import secure_filename
import uuid
import os

SUPABASE_URL = 'https://nuivtmqkqxmritchchxj.supabase.co'
SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im51aXZ0bXFrcXhtcml0Y2hjaHhqIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1MDg5NjUyMywiZXhwIjoyMDY2NDcyNTIzfQ.UOlnC5E0AYawtwlc6bPanVPTD96A9v5AT9XrbJJCZwc'  # (hide this in production)
STORAGE_BUCKET = 'card-images'

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

app = Flask(__name__)
app.secret_key = 'we have never met'

@app.route('/addcard', methods=['GET', 'POST'])
def add_card_form():
    if request.method == 'POST':
        image = request.files.get('image')
        image_url = ""

        if image:
            original_filename = secure_filename(image.filename)
            ext = original_filename.rsplit('.', 1)[-1] if '.' in original_filename else ''
            unique_filename = f"{uuid.uuid4()}.{ext}" if ext else str(uuid.uuid4())
            path_on_storage = unique_filename

            file_bytes = image.read()

            try:
                res = supabase.storage.from_(STORAGE_BUCKET).upload(
                    path_on_storage,
                    file_bytes,
                    {"content-type": image.content_type}
                )
                image_url = f"{SUPABASE_URL}/storage/v1/object/public/{STORAGE_BUCKET}/{path_on_storage}"
            except Exception as e:
                flash(f"Image upload failed: {e}", "error")
                image_url = ""

        card_data = {
            'card_name': request.form['cardName'],
            'description': request.form['description'],
            'rarity': request.form['rarity'],
            'card_price': float(request.form['cardPrice']),
            'set_name': request.form['setName'],
            'img_url': image_url
        }

        result = add_card(card_data)

        if not result.data:
            flash("Error adding card. No data returned.", "error")
        else:
            flash("Card added successfully!", "success")

        return redirect('/addcard')

    return render_template('AddForm.html')



@app.route('/edit')
def edit_card_list_route():
    response = supabase.table('cards').select('*').execute()
    cards = response.data if response.data else []
    return render_template('edit_list.html', cards=cards)


@app.route('/edit/<int:card_id>', methods=['GET', 'POST'])
def edit_card_route(card_id):
    response = supabase.table('cards').select('*').eq('card_id', card_id).execute()
    card = response.data[0] if response.data else None

    if not card:
        flash('Card not found.', 'error')
        return redirect(url_for('edit_card_list_route'))

    if request.method == 'POST':
        if 'cancel' in request.form:
            return redirect(url_for('edit_card_list_route'))

        updated_card = {
            'card_name': request.form['card_name'],
            'description': request.form['description'],
            'rarity': request.form['rarity'],
            'card_price': float(request.form['card_price']),
            'set_name': request.form['set_name'],
            'img_url': request.form['img_url']  # Assuming this is still a manual field
        }

        update_response = supabase.table('cards').update(updated_card).eq('card_id', card_id).execute()

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

    rarity_map = {
        "CM": "Common",
        "UC": "Uncommon",
        "RR": "Rare",
        "HR": "Holo Rare",
        "UR": "Ultra Rare",
        "SR": "Secret Rare"
    }

    for card in cards:
        if "rarity" in card and card["rarity"] in rarity_map:
            card["rarity"] = rarity_map[card["rarity"]]
    return render_template('index.html', cards=cards)


if __name__ == "__main__":
    app.run(debug=True)
