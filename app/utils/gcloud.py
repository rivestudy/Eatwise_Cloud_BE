from google.cloud import storage
from app.utils.config import Config

def upload_to_bucket(bucket_name, file_path):
    client = storage.Client.from_service_account_json(Config.SERVICE_ACCOUNT_FILE)
    bucket = client.get_bucket(bucket_name or Config.BUCKET_NAME)
    blob = bucket.blob(file_path.filename if hasattr(file_path, 'filename') else file_path)
    blob.upload_from_filename(file_path)
    return blob.public_url
