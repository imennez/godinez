import os
import glob
from typing import List
import logging.config
from dotenv import load_dotenv
from multiprocessing import Pool
from tqdm import tqdm
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.docstore.document import Document
from langchain.document_loaders import (
    TextLoader,
    CSVLoader,
    PDFMinerLoader,
    UnstructuredHTMLLoader,
)


logging.config.fileConfig('logging.conf')
logger = logging.getLogger()

load_dotenv()
db_dir = os.environ.get('DB_DIR')

REFERENCE_LOADERS = {
    ".csv"  : (CSVLoader, {}),
    ".html" : (UnstructuredHTMLLoader, {}),
    ".pdf"  : (PDFMinerLoader, {}),
    ".txt"  : (TextLoader, {"encoding": "utf8"}),
}


def db_ingest(source_dirs):
    logger.info(f'Ingest content from paths: {source_dirs}')
    load_references(source_dirs);


def load_reference(ref_path: str) -> Document:
    _, file_ext = os.path.splitext(ref_path)
    if file_ext in REFERENCE_LOADERS:
        loader_class, loader_args = REFERENCE_LOADERS[file_ext]
        loader = loader_class(ref_path, **loader_args)
        return loader.load()[0]

    raise ValueError(f"Unsupported file extension '{file_ext}'")


def load_references(source_dirs: str) -> List[Document]:
    references = []
    for source_dir in source_dirs:
        for ext in REFERENCE_LOADERS:
            references.extend(
                glob.glob(os.path.join(source_dir, f'**/*{ext}'), recursive=True)
            )

    reference_paths = [file_path for file_path in references]
    with Pool(processes=os.cpu_count()) as pool:
        results = []
        with tqdm(total=len(reference_paths), desc='Loading references to DB.', ncols=80) as pbar:
            for i, doc in enumerate(pool.imap_unordered(load_reference, reference_paths)):
                results.append(doc)
                pbar.update()

    return results