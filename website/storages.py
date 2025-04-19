from django.core.files import storage
from django.conf import settings

from googleapiclient.errors import HttpError
from google.oauth2.service_account import Credentials
from googleapiclient import discovery, http


class GoogleDriveStorage(storage.Storage):
    def __init__(self):
        self.credentials = Credentials.from_service_account_file(
            settings.GOOGLE_DRIVE_CREDENTIALS)

        self.service = discovery.build(
            "drive", "v3", credentials=self.credentials)

        self.PARENTS_FOLDER = [
            "1Ykw24XKHNcartBaRbSAvrBf1z-qTKqGd",
        ]

    def save(self, fd, filename):
        file_metadata = {
            "name": str(filename),
            "parents": self.PARENTS_FOLDER,
        }
        media = http.MediaIoBaseUpload(
            fd=fd, mimetype="application/pdf")
        file = (
            self.service.files()
            .create(body=file_metadata, media_body=media, fields="id")
            .execute()
        )

        return file.get("id")

    def search_drivefile_id(self, url_id):
        query = f"name contains 'contrato_{url_id}' and '{
            self.PARENTS_FOLDER[0]}' in parents"

        try:
            result = (
                self.service.files().list(
                    q=query,
                    fields="files(id)"
                ).execute()
            )

            files = result.get("files", [])

            return files[0]["id"]

        except HttpError as error:
            return f"Error while fetching file id, because {error}"

    def get_download_link(self, url_id):

        try:
            drivefile_id = self.search_drivefile_id(url_id)

            if not drivefile_id:
                raise ValueError("File not found")

            request = (
                self.service.files().get(
                    fileId=drivefile_id,
                    fields="webContentLink"
                ).execute()
            )

            return request.get("webContentLink")

        except HttpError as error:
            return f"Link not found, because {error}"

    def url():
        return None

    def delete(self, url_id):
        try:
            drivefile_id = self.search_drivefile_id(url_id)

            if not drivefile_id:
                raise ValueError("File not found.")

            self.service.files().delete(
                fileId=drivefile_id
            ).execute()

            return f"contrato_{url_id} deleted successfully!"

        except HttpError as e:
            return f"Error while deleting file, because {e}"
