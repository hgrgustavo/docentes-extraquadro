from django.core.files import storage
from googleapiclient import discovery, http
from google.oauth2.service_account import Credentials
from django.conf import settings


class GoogleDriveStorage(storage.Storage):
    def __init__(self):
        self.credentials = Credentials.from_service_account_file(
            settings.GOOGLE_DRIVE_CREDENTIALS)

        self.service = discovery.build(
            "drive", "v3", credentials=self.credentials)

    def _save(self, name, content):
        file_metadata = {"name": name}
        media = http.MediaIoBaseUpload(
            filename=name, mimetype="application/pdf")
        file = (
            self.service.files()
            .create(body=file_metadata, media_body=media, fields="id")
            .execute()
        )

        return file.get("id")

    def url(self, name):
        # Retorna a URL pública ou o ID do arquivo no Google Drive
        return f'https://drive.google.com/file/d/{name}/view'
