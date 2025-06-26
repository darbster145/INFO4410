from flask import Flask, request, render_template, redirect, flash
from supabase import create_client, Client
import os

app = Flask(__name__)
app.secret_key = 'your-secret-key'  # Needed for flashing messages

# Supabase setup
SUPABASE_URL = 'https://nuivtmqkqxmritchchxj.supabase.co'
SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im51aXZ0bXFrcXhtcml0Y2hjaHhqIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTA4OTY1MjMsImV4cCI6MjA2NjQ3MjUyM30.cTgFkrqoJeNzmyggNZ8mf-gXcZu7xl-J8rYGXPyDGoA'
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.route('/', methods=['GET', 'POST'])
def add_card():
    if request.method == 'POST':
        card_data = {
            'card_name': request.form['cardName'],
            'description': request.form['description'],
            'rarity': request.form['rarity'],
            'card_price': float(request.form['cardPrice']),
            'set_name': request.form['setName']
        }

        response = supabase.table('cards').insert(card_data).execute()

        if response.get("error"):
            flash("Error adding card: " + response["error"]["message"], "error")
        else:
            flash("Card added successfully!", "success")

        return redirect('/')

    return render_template('AddForm.html')
