from flask import Flask, render_template_string, request, redirect, url_for

app = Flask(__name__)

# Magic: The Gathering card data
cards = [
    [1, "Black Lotus", "Adds three mana of any one color.", "Mythic", 29999.99, "Alpha", "black_lotus.png", "MTG-0001", "Mint", "Vault Drawer 1"],
    [2, "Lightning Bolt", "Deals 3 damage to any target.", "Common", 2.49, "Revised Edition", "lightning_bolt.png", "MTG-0002", "Near Mint", "Binder A Page 1"],
    [3, "Tarmogoyf", "Power and toughness equal to cards in graveyards.", "Rare", 45.00, "Modern Masters", "tarmogoyf.png", "MTG-0003", "Good", "Deck Box Red"],
    [4, "Jace, the Mind Sculptor", "Legendary Planeswalker with four powerful abilities.", "Mythic", 69.99, "Worldwake", "jace_mind_sculptor.png", "MTG-0004", "Near Mint", "Binder B Page 6"],
    [5, "Counterspell", "Counter target spell.", "Uncommon", 1.25, "Ice Age", "counterspell.png", "MTG-0005", "Fair", "Binder A Page 3"]
]

# HTML template
template = '''
<!doctype html>
<title>Trading Cards</title>
<h1>All Trading Cards</h1>
<table border=1>
  <tr>
    <th>Name</th><th>Description</th><th>Rarity</th><th>Price</th>
    <th>Set Name</th><th>UID</th><th>Quality</th><th>Locator</th>
    <th>Image</th><th>Action</th>
  </tr>
  {% for card in cards %}
  <tr>
    <td>{{ card[1] }}</td>
    <td>{{ card[2] }}</td>
    <td>{{ card[3] }}</td>
    <td>${{ '%.2f'|format(card[4]) }}</td>
    <td>{{ card[5] }}</td>
    <td>{{ card[7] }}</td>
    <td>{{ card[8] }}</td>
    <td>{{ card[9] }}</td>
    <td><img src="/static/{{ card[6] }}" width="50"></td>
    <td><a href="/edit/{{ card[0] }}">Edit</a></td>
  </tr>
  {% endfor %}
</table>

{% if card_to_edit %}
<h2>Edit Card</h2>
<form method="post">
  <label>Card Name:</label><br>
  <input type="text" name="name" value="{{ card_to_edit[1] }}" required><br>

  <label>Description:</label><br>
  <textarea name="description">{{ card_to_edit[2] }}</textarea><br>

  <label>Rarity:</label><br>
  <select name="rarity">
    {% for r in ['Common', 'Uncommon', 'Rare', 'Mythic'] %}
      <option value="{{ r }}" {% if r == card_to_edit[3] %}selected{% endif %}>{{ r }}</option>
    {% endfor %}
  </select><br>

  <label>Price ($):</label><br>
  <input type="text" name="price" value="{{ card_to_edit[4] }}"><br>

  <label>Set Name:</label><br>
  <input type="text" name="set_name" value="{{ card_to_edit[5] }}"><br>

  <label>Image Filename:</label><br>
    <input type="text" name="image" value="{{ card_to_edit[6] }}"><br>

  <label>UID:</label><br>
  <input type="text" name="uid" value="{{ card_to_edit[7] }}"><br>

  <label>Quality:</label><br>
  <select name="quality">
    {% for q in ['Mint', 'Near Mint', 'Good', 'Fair', 'Poor'] %}
      <option value="{{ q }}" {% if q == card_to_edit[8] %}selected{% endif %}>{{ q }}</option>
    {% endfor %}
  </select><br>

  <label>Locator:</label><br>
  <input type="text" name="locator" value="{{ card_to_edit[9] }}"><br><br>

  <input type="submit" value="Update Card">
</form>
{% endif %}
'''

@app.route('/')
def index():
    return render_template_string(template, cards=cards, card_to_edit=None)

@app.route('/edit/<int:card_id>', methods=['GET', 'POST'])
def edit_card(card_id):
    card = next((c for c in cards if c[0] == card_id), None)
    if not card:
        return redirect(url_for('index'))

    if request.method == 'POST':
        card[1] = request.form['name']
        card[2] = request.form['description']
        card[3] = request.form['rarity']
        card[4] = float(request.form['price'])
        card[5] = request.form['set_name']
        card[6] = request.form['image']
        card[7] = request.form['uid']
        card[8] = request.form['quality']
        card[9] = request.form['locator']
        return redirect(url_for('index'))

    return render_template_string(template, cards=cards, card_to_edit=card)

if __name__ == '__main__':
    app.run(debug=True, port=5000)