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
from multiprocessing.dummy import Pool as ThreadPool
from typing import Literal, Optional, List
from pydantic import BaseModel as BaseModelType
from dataclasses import dataclass, field

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
        with open(filepath, "wb") as f:
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
        with open(filepath, "rb") as f:
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


TECH_TAXONOMY = {
    "Renewable Energy": {
        "Solar Power": {
            "Small Scale Solar",
            "Large Scale Solar",
            "Concentrated Solar",
        },
        "Wind Power": {"Offshore Wind", "Onshore Wind"},
        "Hydro Power": {"Small Scale Hydro", "Large Scale Hydro"},
    },
    "Fossil Fuels": {
        "Coal": {"Brown Coal", "Black Coal", "Peat"},
        "Gas": {"Conventional Gas", "Non-Conventional Gas"},
        "Oil": {"Oil"},
    },
    "Non-Viable Alternatives": {
        "Biomass": {"Waste Fermentation", "Farmed Biomass", "BioFuels"},
        "Nuclear": {"Large Scale Fission", "Small Modular Fission", "Fusion"},
        "CCS": {"post-combustion", "pre-combustion", "Direct Air Capture"},
        "Ocean Energy": {"Wave", "Tidal", "Thermal"},
        "Geothermal": {"Geothermal Energy"},
    },
    "Storage and Transportation": {
        "Long-Term Storage": {
            "Gravity Storage",
            "Pumped Hydro Storage",
            "Compressed Air Energy Storage (CAES)",
            "Large-Scale Batteries",
            "Hydrogen Storage",
        },
        "Peaking Supply": {
            "Battery Energy Storage Systems (BESS)",
            "Home Battery",
            "Flywheels",
            "Thermal Storage",
        },
        "Transport": {
            "Electrical Transmission Lines",
            "Gas Pipelines",
            "Hydrogen Pipelines",
            "Oil Pipelines",
        },
    },
}

ISSUE_TAXONOMY = {
    "Economic": {
        "Affordability / Cost",
        "Jobs & Industry",
        "Innovation & Growth",
        "Opportunity Cost",
    },
    "Security": {
        "Reliability",
        "Infrastructure Resilience",
        "Resource Scarcity",
        "Resource Control",
        "Achievability",
    },
    "Green / Environmental Sustainability": {
        "Climate Change",
        "Ecology",
        "Natural Beauty",
    },
    "Justice": {"Fairness", "Consent", "Health Impacts"},
    "National Standing": {
        "International Obligations",
        "Keeping up internationally",
    },
}

# --- Literals

Impact = Literal["Alleviates", "Exacerbates", "Does Not Impact"]
tech_level_1 = []
tech_level_2 = []
tech_level_3 = []
for k, v in TECH_TAXONOMY.items():
    tech_level_1.append(k)
    for k2, v2 in v.items():
        tech_level_2.append(k2)
        for k3 in v2:
            tech_level_3.append(k3)

TechLevel1 = Literal.__getitem__(tuple(tech_level_1))
TechLevel2 = Literal.__getitem__(tuple(tech_level_2))
TechLevel3 = Literal.__getitem__(tuple(tech_level_3))

issue_level_1 = []
issue_level_2 = []
for k, v in ISSUE_TAXONOMY.items():
    issue_level_1.append(k)
    for k2 in v:
        issue_level_2.append(k2)

IssueLevel1 = Literal.__getitem__(tuple(issue_level_1))
IssueLevel2 = Literal.__getitem__(tuple(issue_level_2))

# --- Main Model with validation ---


class Label(BaseModelType):
    tech_level_1: TechLevel1
    tech_level_2: Optional[TechLevel2] = (
        None  # Will validate later as Enum dynamically
    )
    tech_level_3: Optional[TechLevel3] = None

    issue_level_1: IssueLevel1
    issue_level_2: Optional[IssueLevel2] = None

    sentiment: Impact

    # @model_validator(mode="after")
    # @classmethod
    # def check_tech_hierarchy(cls, values):
    #     lvl1 = values.tech_level_1
    #     lvl2 = values.tech_level_2
    #     lvl3 = values.tech_level_3

    #     # Check level 2 is valid under level 1
    #     if lvl2:
    #         if lvl1 not in TECH_TAXONOMY or lvl2 not in TECH_TAXONOMY[lvl1]:
    #             raise ValueError(
    #                 f"tech_level_2 '{lvl2}' is not a valid child of tech_level_1 '{lvl1}'"
    #             )

    #     # Check level 3 is valid under level 2 of level 1
    #     if lvl3:
    #         if (
    #             not lvl2
    #             or lvl1 not in TECH_TAXONOMY
    #             or lvl2 not in TECH_TAXONOMY[lvl1]
    #         ):
    #             raise ValueError(
    #                 f"Cannot validate tech_level_3 '{lvl3}' without a valid tech_level_2 '{lvl2}' under tech_level_1 '{lvl1}'"
    #             )
    #         elif lvl3 not in TECH_TAXONOMY[lvl1][lvl2]:
    #             raise ValueError(
    #                 f"tech_level_3 '{lvl3}' is not a valid child of tech_level_2 '{lvl2}' under tech_level_1 '{lvl1}'"
    #             )

    #     return values

    # @model_validator(mode="after")
    # @classmethod
    # def check_issue_hierarchy(cls, values):
    #     lvl1 = values.issue_level_1
    #     lvl2 = values.issue_level_2

    #     if lvl2:
    #         if lvl1 not in ISSUE_TAXONOMY or lvl2 not in ISSUE_TAXONOMY[lvl1]:
    #             raise ValueError(
    #                 f"issue_level_2 '{lvl2}' is not a valid child of issue_level_1 '{lvl1}'"
    #             )

    #     return values


@dataclass
class Claim:
    text: str
    deconstruction: Optional[Label] = None


@dataclass
class DocumentElement:
    text: str
    context: List[str] = field(default_factory=list)
    claims: Optional[List[Claim]] = None


@dataclass
class Document:
    id: int
    text: str
    elements: Optional[List[DocumentElement]] = None


@dataclass
class Corpus(BaseModel):
    documents: List[Document]


class DocumentLevel(BaseModel):
    """
    Base class for things that run inferance on documents
    """

    def infer_corpus(self, corpus: Corpus):
        with ThreadPool() as pool:
            return pool.map(self.infer_document, corpus.documents)

    def infer_document(self, document: Document):
        return self.infer(document)

    def transform(self, corpus: Corpus) -> Corpus:
        data = self.infer_corpus(corpus)
        return self._data_join_func(corpus, data)

    def _data_join_func(self, corpus, data):
        return corpus


class ElementLevel(DocumentLevel):
    """
    Base class for things that run inferance on Elements
    """

    def infer_document(self, document: Document):
        with ThreadPool() as pool:
            return pool.map(self.infer_element, document.elements)

    def infer_element(self, element: DocumentElement):
        return self.infer(element)


class ClaimLevel(ElementLevel):
    """
    Base class for things that run inferance on Claims
    """

    def infer_element(self, element: DocumentElement):
        with ThreadPool() as pool:
            return pool.map(self.infer_claim, element.claims)

    def infer_claim(self, claim: Claim):
        return self.infer(claim)
