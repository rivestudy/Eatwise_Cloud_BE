from google.cloud import storage
from werkzeug.utils import secure_filename
import os

def upload_to_bucket(bucket_name, file):
    """Uploads a file to Google Cloud Storage."""
    # Ensure you have the service account credentials set up properly for Google Cloud Storage.
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    
    # Securely name the file
    filename = secure_filename(file.filename)
    
    # Create a blob in the bucket
    blob = bucket.blob(filename)
    
    # Upload the file's content directly from the FileStorage object
    blob.upload_from_file(file)

    # Optionally, return the public URL or path to the file
    return blob.public_url  # Or any other URL/path based on your configuration
