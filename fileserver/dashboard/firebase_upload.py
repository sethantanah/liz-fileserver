import json
import os

from firebase_admin import credentials, initialize_app, storage
from django.core.files.storage import FileSystemStorage

service_account_info = json.loads(os.environ.get('FIREBASE_SERVICE_ACCOUNT_KEY'))
cred = credentials.Certificate(service_account_info)
initialize_app(cred, {'storageBucket': 'home-status-c4316.appspot.com'})


def uploadfile(file):
    # Put your local file path
    fileName = file_path(file)
    bucket = storage.bucket()
    blob = bucket.blob(fileName)
    blob.upload_from_filename(fileName)
    blob.make_public()
    fs = FileSystemStorage()
    fs.delete(file.name)
    return blob.public_url


def delete_firebase_file(file):
    storage.bucket()
    blob = storage.bucket()
    blob.delete_blob(f'/opt/render/project/src/fileserver/songdir/{file}')


def file_path(file):
    fs = FileSystemStorage()
    filename = fs.save(file.name, file)
    uploaded_file_path = fs.path(filename)
    return uploaded_file_path
