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
            "1Ykw24XKHNcartBaRbSAvrBf1z-qTKqGd",  # contratos
            "1Tztz11cmKNtLZZY53mxRA2hweK6AawVi",  # professores
            "1KnyEXJfj0VY_TVxCuPw54uPe437vEMwi",  # usuarios
        ]

    def upload(self, fd, filename: str) -> None:
        try:
            match True:
                case _ if "contract_" in filename:
                    file_metadata = {
                        "name": str(filename),
                        "parents": [self.PARENTS_FOLDER[0]],
                    }

                    media = http.MediaIoBaseUpload(
                        fd=fd, mimetype="application/pdf")

                    self.service.files().create(body=file_metadata,
                                                media_body=media, fields="id").execute()

                case _ if "teacher_" in filename:
                    teacher_photo_metadata = {
                        "name": str(filename),
                        "parents": [self.PARENTS_FOLDER[1]]
                    }

                    media = http.MediaIoBaseUpload(
                        fd=fd,
                        mimetype="image/*",
                        resumable=True
                    )

                    self.service.files().create(body=teacher_photo_metadata,
                                                media_body=media).execute()

                case _ if "user_" in filename:
                    user_photo_metadata = {
                        "name": str(filename),
                        "parents": [self.PARENTS_FOLDER[2]]
                    }

                    media = http.MediaIoBaseUpload(
                        fd=fd,
                        mimetype="image/*",
                        resumable=True
                    )

                    self.service.files().create(body=user_photo_metadata,
                                                media_body=media, fields="id").execute()
        except HttpError as e:
            print(f"Error while uploading photo, because {e.reason}")

    def search_drivefile_id(self, filename: str) -> str:
        try:
            match True:
                case _ if "contract_" in filename:
                    query = f"name = '{filename}' and '{
                        self.PARENTS_FOLDER[0]}' in parents"

                    result = (
                        self.service.files().list(
                            q=query,
                            fields="files(id)",
                        ).execute()
                    )

                    file = result.get("files", [])

                    return file[0]["id"] if file else "File not found"

                case _ if "teacher_" in filename:

                    query = f"name = '{filename}' and '{
                        self.PARENTS_FOLDER[1]}' in parents"

                    result = (
                        self.service.files().list(
                            q=query,
                            fields="files(id)"
                        ).execute()
                    )

                    file = result.get("files", [])

                    return file[0]["id"] if file else "File not found"

                case _ if "user_" in filename:

                    query = f"name = '{filename}' and '{
                        self.PARENTS_FOLDER[2]}' in parents"

                    result = (
                        self.service.files().list(
                            q=query,
                            fields="files(id)"
                        ).execute()
                    )

                    file = result.get("files", [])

                    return file[0]["id"] if file else "File not found"

        except HttpError as e:
            return f"Error while searching drive file id, because {e.reason}"

    def get_download_link(self, filename: str) -> str | None:
        try:
            drivefile_id = self.search_drivefile_id(filename)

            if not drivefile_id or drivefile_id == "File not found":
                print(f"File {filename} not found in Drive.")

                return None

            request = self.service.files().get(
                fileId=drivefile_id, fields="webContentLink").execute()

            return request.get("webContentLink", None)

        except HttpError as e:
            print(f"Error fetching download link for {filename}: {e}")

            return None

    def url():
        return None

    def delete(self, filename: str) -> str | None:
        try:
            drivefile_id = self.search_drivefile_id(filename)

            if not drivefile_id or drivefile_id == "File not found":
                print(f"File {filename} not found in Drive.")

                return None

            self.service.files().delete(fileId=drivefile_id).execute()

            return f"File {filename} deleted successfully!"

        except HttpError as e:
            print(f"Error while deleting {filename}: {e.reason}")

            return None

    def get_drivefile_url(self, filename: str) -> str | None:
        try:
            drivefile_id = self.search_drivefile_id(filename)

            if not drivefile_id or drivefile_id == "File not found":
                print(f"File {filename} not found in Drive.")

                return None

            return f"https://lh3.googleusercontent.com/d/{drivefile_id}"

        except HttpError as e:
            print(f"Error fetching Drive file URL: {
                  e.reason}")  # Debug log

            return None
