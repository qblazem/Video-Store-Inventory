import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from supabase import create_client

if getattr(sys, "frozen", False):
    base_path = Path(sys.executable).parent
else:
    base_path = Path(__file__).resolve().parent.parent

load_dotenv(base_path / ".env")

url = os.environ["SUPABASE_URL"]
key = os.environ["SUPABASE_KEY"]

supabase = create_client(url, key)