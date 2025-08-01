# card/EditCard.py
from supabase import create_client, Client
from werkzeug.utils import secure_filename
import os

#Definitly not secure storing these api keys here but for this project It might not matter 
SUPABASE_URL = 'https://nuivtmqkqxmritchchxj.supabase.co'
SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im51aXZ0bXFrcXhtcml0Y2hjaHhqIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTA4OTY1MjMsImV4cCI6MjA2NjQ3MjUyM30.cTgFkrqoJeNzmyggNZ8mf-gXcZu7xl-J8rYGXPyDGoA'
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def get_card(card_id: int):
    """Fetch a card by its ID from the supabase db."""
    response = supabase.table('cards').select('*').eq('card_id', card_id).single().execute()
    return response.data if response.data else None

def update_card(card_id: int, updated_data: dict):
    """Update a card by its ID with given updated_data dictionary."""
    response = supabase.table('cards').update(updated_data).eq('card_id', card_id).execute()
    return response

def upload_image_to_supabase(file_storage):
    """Upload image file to Supabase storage and return public URL."""
    file_name = secure_filename(file_storage.filename)
    file_path = f"cards/{file_name}"

    # Upload to storage bucket
    supabase.storage.from_('images').upload(file_path, file_storage.stream, {"content-type": file_storage.content_type})
    public_url = supabase.storage.from_('images').get_public_url(file_path)
    return public_url

