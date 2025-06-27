# card/EditCard.py
from supabase import create_client, Client

SUPABASE_URL = 'https://nuivtmqkqxmritchchxj.supabase.co'
SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im51aXZ0bXFrcXhtcml0Y2hjaHhqIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTA4OTY1MjMsImV4cCI6MjA2NjQ3MjUyM30.cTgFkrqoJeNzmyggNZ8mf-gXcZu7xl-J8rYGXPyDGoA'
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def get_card(card_id: int):
    """Fetch a card by its ID from supabase."""
    response = supabase.table('cards').select('*').eq('id', card_id).single().execute()
    if response.data:
        return response.data
    return None

def update_card(card_id: int, updated_data: dict):
    """Update a card by its ID with given updated_data dict."""
    response = supabase.table('cards').update(updated_data).eq('id', card_id).execute()
    return response
