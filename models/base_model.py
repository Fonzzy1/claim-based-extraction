from tqdm import tqdm
import dill
import os
from tqdm import tqdm
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.http import MediaIoBaseDownload
import os
import io
from io import BytesIO

# --- Google Drive Auth ---
SCOPES = ["https://www.googleapis.com/auth/drive"]
SERVICE_ACCOUNT_FILE = "/root/client.json"

# Make sure /root/client.json exists
credentials = ServiceAccountCredentials.from_json_keyfile_name(
    SERVICE_ACCOUNT_FILE, SCOPES
)

gauth = GoogleAuth()
gauth.credentials = credentials
drive = GoogleDrive(gauth)

folder_id = "1splKDhcBuy1p_OAJTCTuIbx6t5o6yURi"


class BaseModel:
    def __init__(self) -> None:
        pass

    def save_to_file(self, filepath):
        if os.path.exists(filepath):
            raise FileExistsError("File already exists")
        with open(filepath, 'wb') as f:
            dill.dump(self, f)


    def save_to_drive(self, filename):
        # Serialize current object to bytes
        data_bytes = dill.dumps(self)
        file_size = len(data_bytes)
        file_stream = io.BytesIO(data_bytes)

        # Search for existing file
        file_list = drive.ListFile(
            {
                "q": f"'{folder_id}' in parents and title='{filename}' and trashed=false"
            }
        ).GetList()

        if file_list:
            raise Exception(f"Filename {filename} allready exists")
        else:
            # File does not exist, create new
            file_metadata = {
                "title": filename,
                "parents": [{"id": folder_id}],
            }
            gfile = drive.CreateFile(file_metadata)

            file_stream.seek(0)
            with tqdm.wrapattr(
                file_stream,
                "read",
                desc=f"Upload {filename}",
                total=file_size,
                unit="B",
                unit_scale=True,
                unit_divisor=1024,
            ) as wrapped:
                if file_size:
                    gfile.content = wrapped
                gfile["title"] = filename
                gfile.Upload(param={"supportsAllDrives": True})

            print(f"Created new file: {filename}")

    @classmethod
    def load_from_file(cls, filepath):
        with open(filepath, 'rb') as f:
            obj = dill.load(f)
        if type(obj) != cls:
            raise Exception("Incompatible Object")
        return obj

    @classmethod
    def load_from_drive(cls, filename):

        file_list = drive.ListFile(
            {
                "q": f"'{folder_id}' in parents and title='{filename}' and trashed=false"
            }
        ).GetList()

        if not file_list:
            raise FileNotFoundError(
                f"No backup file '{filename}' found in Drive folder."
            )

        gfile = file_list[0]
        file_size = int(gfile["fileSize"])

        print("Downloading backup from Drive...")
        request = gfile.auth.service.files().get_media(fileId=gfile["id"])
        fh = BytesIO()
        downloader = MediaIoBaseDownload(
            fh, request, chunksize=1024 * 1024 * 10
        )  # 10MB chunks
        done = False
        with tqdm(
            total=file_size, unit="B", unit_scale=True, desc="Download"
        ) as pbar:
            while not done:
                status, done = downloader.next_chunk()
                if status:
                    pbar.update(status.resumable_progress - pbar.n)

        fh.seek(0)
        obj = dill.load(fh)
        return obj

