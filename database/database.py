import os
from pathlib import Path
from dotenv import load_dotenv
from supabase import create_client, Client

env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(env_path)

url = os.environ["SUPABASE_URL"]
key = os.environ["SUPABASE_KEY"]

supabase: Client = create_client(url, key)

#Supabase connection, variable "supabase"