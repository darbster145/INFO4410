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
    'card_name': request.form.get('card_name'),
    'oracle_text': request.form.get('oracle_text'),
    'rarity': request.form.get('rarity'),
    'card_price': float(request.form.get('card_price') or 0),
    'set_name': request.form.get('set_name'),
    'mana_cost': request.form.get('mana_cost'),
    'cmc': float(request.form.get('cmc') or 0),
    'colors': request.form.get('colors'),
    'type_line': request.form.get('type_line'),
    'power': request.form.get('power'),
    'toughness': request.form.get('toughness'),
    'language': request.form.get('language'),
    'img_url': image_url  # or card['img_url'] if no new image uploaded
}

        result = add_card(card_data)

        if not result.data:
            flash("Error adding card. No data returned.", "error")
        else:
            flash("Card added successfully!", "success")
            return redirect(url_for('index'))

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

    # Extract current image filename from URL for display
    current_img_url = card.get('img_url', '')
    current_img_filename = ''
    if current_img_url:
        # Assuming URL format ends with the filename
        current_img_filename = current_img_url.split('/')[-1]

    if request.method == 'POST':
        if 'cancel' in request.form:
            return redirect(url_for('edit_card_list_route'))

        # Handle new image upload
        image = request.files.get('image')
        new_img_url = current_img_url  # default keep old image url

        if image and image.filename != '':
            original_filename = secure_filename(image.filename)
            ext = original_filename.rsplit('.', 1)[-1] if '.' in original_filename else ''
            unique_filename = f"{uuid.uuid4()}.{ext}" if ext else str(uuid.uuid4())
            path_on_storage = unique_filename

            file_bytes = image.read()

            try:
                supabase.storage.from_(STORAGE_BUCKET).upload(
                    path_on_storage,
                    file_bytes,
                    {"content-type": image.content_type}
                )
                new_img_url = f"{SUPABASE_URL}/storage/v1/object/public/{STORAGE_BUCKET}/{path_on_storage}"
            except Exception as e:
                flash(f"Image upload failed: {e}", "error")
                return redirect(url_for('edit_card_route', card_id=card_id))

        updated_card = {
    'card_name': request.form.get('card_name'),
    'oracle_text': request.form.get('oracle_text'),
    'rarity': request.form.get('rarity'),
    'card_price': float(request.form.get('card_price') or 0),
    'set_name': request.form.get('set_name'),
    'mana_cost': request.form.get('mana_cost'),
    'cmc': float(request.form.get('cmc') or 0),
    'colors': request.form.get('colors'),
    'type_line': request.form.get('type_line'),
    'power': request.form.get('power'),
    'toughness': request.form.get('toughness'),
    'language': request.form.get('language'),
    'img_url': new_img_url  # or card['img_url'] if no new image uploaded
}


        update_response = supabase.table('cards').update(updated_card).eq('card_id', card_id).execute()

        if not update_response.data:
            flash("Error updating card: No data returned", "error")
        else:
            flash("Card updated successfully!", "success")

        return redirect(url_for('edit_card_list_route'))

    return render_template('edit_form.html', card=card, current_img_filename=current_img_filename)


@app.route('/')
def index():
    search_query = request.args.get('search', '').lower()
    sort_by = request.args.get('sort_by')

    # Get all cards from Supabase
    cards_response = supabase.table('cards').select('*').execute()
    cards = cards_response.data if cards_response.data else []

    # 🔍 Filter by search query (name, description, set)
    if search_query:
        cards = [
            card for card in cards
            if search_query in card.get('card_name', '').lower()
            or search_query in card.get('oracle_text', '').lower()
            or search_query in card.get('set_name', '').lower()
        ]

    # 💸 Sort by price
    if sort_by == 'price_asc':
        cards.sort(key=lambda x: x.get('card_price', 0))
    elif sort_by == 'price_desc':
        cards.sort(key=lambda x: x.get('card_price', 0), reverse=True)

    # (Optional: Convert rarity codes for display)
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

