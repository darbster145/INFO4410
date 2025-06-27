from supabase import create_client, Client
# card/addCard.py

#Probably need to store they keys somewhere eles
SUPABASE_URL = 'https://nuivtmqkqxmritchchxj.supabase.co'
SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im51aXZ0bXFrcXhtcml0Y2hjaHhqIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTA4OTY1MjMsImV4cCI6MjA2NjQ3MjUyM30.cTgFkrqoJeNzmyggNZ8mf-gXcZu7xl-J8rYGXPyDGoA'
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def add_card(card_data):
    return supabase.table('cards').insert(card_data).execute()




