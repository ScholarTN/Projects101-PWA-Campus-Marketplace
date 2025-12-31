from supabase_client import supabase
import uuid

def upload_file(file, folder):
    file_ext = file.name.split(".")[-1]
    file_name = f"{folder}/{uuid.uuid4()}.{file_ext}"

    supabase.storage.from_("media").upload(
        file_name,
        file.read()
    )

    return supabase.storage.from_("media").get_public_url(file_name)
