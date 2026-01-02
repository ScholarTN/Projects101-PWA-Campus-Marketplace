from supabase_client import supabase
import uuid

def upload_file(file, folder):
    file_ext = file.name.split(".")[-1].lower()
    file_name = f"{folder}/{uuid.uuid4()}.{file_ext}"

    supabase.storage.from_("media").upload(
        path=file_name,
        file=file.read(),
        file_options={"content-type": file.type}
    )

    public_url = supabase.storage.from_("media").get_public_url(file_name)

    return public_url
#We need a try except block to handle exceptions