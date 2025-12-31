import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

supabase = create_client(
    os.getenv("https://nxrrlpkpfdflwfckpqzj.supabase.co"),
    os.getenv("sb_publishable_U3PmmcPuxzgl7MfzhXrKKw_MHM_g_UB")
)
