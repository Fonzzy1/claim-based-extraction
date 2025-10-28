from tqdm import tqdm
from multiprocessing.dummy import Pool as ThreadPool
import dill
import os
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.http import MediaIoBaseDownload
import os
import io
from io import BytesIO
from multiprocessing.dummy import Pool as ThreadPool
from typing import Literal, Optional, List, Union
from pydantic import BaseModel as PyBaseModel, model_validator
from dataclasses import dataclass, field
from tqdm.contrib.concurrent import thread_map

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
            "small-scale solar",
            "large-scale solar",
            "concentrated solar power",
        },
        "Wind Power": {
            "offshore wind",
            "onshore wind",
        },
        "Hydro Power": {
            "small-scale hydro",
            "large-scale hydro",
        },
    },
    "Fossil Fuels": {
        "Coal": {
            "brown coal",
            "black coal",
            "peat",
        },
        "Gas": {
            "conventional gas",
            "non-conventional gas",
            "LNG",
        },
        "Oil": {
            "oil",
        },
    },
    "Non-Viable Alternatives": {
        "Biomass": {
            "waste fermentation",
            "farmed biomass",
            "biofuel",
        },
        "Nuclear": {
            "large-scale fission",
            "small modular fission",
            "fusion",
        },
        "CCS": {
            "post-combustion carbon capture",
            "pre-combustion carbon capture",
            "direct air carbon capture",
        },
        "Ocean Energy": {
            "wave energy",
            "tidal energy",
            "ocean thermal energy",
        },
        "Geothermal": {
            "geothermal energy",
        },
    },
    "Storage and Transportation": {
        "Long-Term Storage": {
            "gravity storage",
            "pumped hydro storage",
            "compressed air energy storage",
            "large-scale batteries",
            "hydrogen storage",
        },
        "Peaking Supply": {
            "battery energy storage system",
            "home batteries",
            "flywheel storage",
            "thermal storage",
        },
        "Transport": {
            "electrical transmission lines",
            "gas pipelines",
            "hydrogen pipelines",
            "oil pipelines",
        },
    },
}

ISSUE_TAXONOMY = {
    "Economic": {
        "Low Government Revenues",
        "High Government Expenditure",
        "Unemployment",
        "Low Economic Growth",
        "High Energy Costs",
        "Reduced Economic Competitiveness",
    },
    "Security": {
        "Inconsistent Energy Availability",
        "Energy Infrastructure Vulnerability",
        "Resource Depletion",
        "International Resource Dependency",
        "Plan Viability",
    },
    "Environmental Sustainability": {
        "Climate Change",
        "Destruction of Ecology",
        "Destruction of Natural Beauty",
        "Air Pollution",
        "Water Resource Stress",
        "Biodiversity Loss",
    },
    "Justice": {
        "Inequity",
        "Lack of Public Consent",
        "Adverse Health Impacts",
        "Regional Decline",
        "Social Displacement",
        "Energy Access Inequality",
    },
    "National Standing": {
        "A Failure to Meet International Obligations",
        "Reputation with Trade Partners",
        "Weak Leadership in Clean Energy Transition",
        "Declining Global Influence on Energy Policy",
    },
}


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


class EvaluationLabel(PyBaseModel):
    tech_level_1: Optional[TechLevel1]
    tech_level_2: Optional[TechLevel2] = None
    tech_level_3: Optional[TechLevel3] = None

    issue_level_1: IssueLevel1
    issue_level_2: Optional[IssueLevel2] = None

    impact: Impact  # same as old sentiment

    # @model_validator(mode="after")
    # def check_tech_hierarchy(self, values):
    #     lvl1, lvl2, lvl3 = (
    #         values.tech_level_1,
    #         values.tech_level_2,
    #         values.tech_level_3,
    #     )

    #     if lvl2 and (
    #         lvl1 not in TECH_TAXONOMY or lvl2 not in TECH_TAXONOMY[lvl1]
    #     ):
    #         raise ValueError(
    #             f"tech_level_2 '{lvl2}' is not a valid child of tech_level_1 '{lvl1}'"
    #         )

    #     if lvl3:
    #         if not lvl2 or lvl2 not in TECH_TAXONOMY.get(lvl1, {}):
    #             raise ValueError(
    #                 f"Cannot validate tech_level_3 '{lvl3}' without valid lvl2 '{lvl2}' under lvl1 '{lvl1}'"
    #             )
    #         if lvl3 not in TECH_TAXONOMY[lvl1][lvl2]:
    #             raise ValueError(
    #                 f"tech_level_3 '{lvl3}' is not a valid child of tech_level_2 '{lvl2}' under tech_level_1 '{lvl1}'"
    #             )
    #     return values

    # @model_validator(mode="after")
    # def check_issue_hierarchy(self, values):
    #     lvl1, lvl2 = values.issue_level_1, values.issue_level_2

    #     if lvl2 and (
    #         lvl1 not in ISSUE_TAXONOMY or lvl2 not in ISSUE_TAXONOMY[lvl1]
    #     ):
    #         raise ValueError(
    #             f"issue_level_2 '{lvl2}' is not a valid child of issue_level_1 '{lvl1}'"
    #         )
    #     return values

    def __repr__(self):
        """Natural-language sentence form."""
        tech = self.tech_level_3 or self.tech_level_2 or "a technology"
        tech_parent = f"({self.tech_level_1})" if self.tech_level_1 else ""
        issue2 = f" issue of {self.issue_level_2}" if self.issue_level_2 else ""
        return (
            f"Policies that support the use of {tech} {tech_parent} "
            f"will {self.impact} the {self.issue_level_1} issue of {issue2}."
        )


class IssueDeclarationLabel(PyBaseModel):
    issue_level_1: IssueLevel1
    issue_level_2: Optional[IssueLevel2] = None

    # @model_validator(mode="after")
    # def check_issue_hierarchy(self, values):
    #     lvl1, lvl2 = values.issue_level_1, values.issue_level_2
    #     if lvl2 and (
    #         lvl1 not in ISSUE_TAXONOMY or lvl2 not in ISSUE_TAXONOMY[lvl1]
    #     ):
    #         raise ValueError(
    #             f"issue_level_2 '{lvl2}' is not a valid child of issue_level_1 '{lvl1}'"
    #         )
    #     return values

    def __repr__(self):
        """Natural-language sentence form."""
        issue2 = f" issue of {self.issue_level_2}" if self.issue_level_2 else ""
        return (
            f"Policies affecting Australia’s energy generation "
            f"should address the {self.issue_level_1} issue of {issue2}."
        )


# --- Unified Label Union Type ---
class Label(PyBaseModel):
    evaluation: Optional[EvaluationLabel] = None
    issue: Optional[IssueDeclarationLabel] = None


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
            return thread_map(self.infer_document, corpus.documents)

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
