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
from langchain.vectorstores import Chroma
from chromadb.config import Settings


logging.config.fileConfig('logging.conf')
logger = logging.getLogger('db')

load_dotenv()
db_dir = os.environ.get('DB_DIR')

REFERENCE_LOADERS = {
    ".csv"  : (CSVLoader, {}),
    ".html" : (UnstructuredHTMLLoader, {}),
    ".pdf"  : (PDFMinerLoader, {}),
    ".txt"  : (TextLoader, {"encoding": "utf8"}),
}


def refs_clear():
    logger.debug(f'Clear reference store.')
    client = __get_db_client()
    client.delete_collection()


def refs_ingest(source_dirs):
    logger.debug(f'Ingest content from paths: {source_dirs}')
    client = __get_db_client()

    refs_collection = client.get()
    existing_refs= [metadata['source'] for metadata in refs_collection['metadatas']]

    new_refs_chunks = __process_references(source_dirs, existing_refs)
    client.add_documents(new_refs_chunks)
    client.persist()


def refs_get_retreiver():
    logger.debug('Get reference retreiver')
    client = __get_db_client()
    return client.as_retriever()


def __load_reference(ref_path: str) -> Document:
    _, file_ext = os.path.splitext(ref_path)
    if file_ext in REFERENCE_LOADERS:
        loader_class, loader_args = REFERENCE_LOADERS[file_ext]
        loader = loader_class(ref_path, **loader_args)
        return loader.load()[0]

    raise ValueError(f"Unsupported file extension '{file_ext}'")


def __load_references(source_dirs: str, ignore_refs: List[str]) -> List[Document]:
    references = []
    for source_dir in source_dirs:
        for ext in REFERENCE_LOADERS:
            references.extend(
                glob.glob(os.path.join(source_dir, f'**/*{ext}'), recursive=True)
            )

    reference_paths = [file_path for file_path in references if file_path not in ignore_refs]
    with Pool(processes=os.cpu_count()) as pool:
        results = []
        with tqdm(total=len(reference_paths), desc='Loading references to DB.', ncols=80) as progress:
            for _, doc in enumerate(pool.imap_unordered(__load_reference, reference_paths)):
                results.append(doc)
                progress.update()

    return results

def __process_references(source_dirs, existing_refs) -> List[Document]:
    chunk_size=500
    chunk_overlap=50
    logger.info(f'Loading documents from {source_dirs}')
    refs = __load_references(source_dirs, existing_refs)
    if not refs:
        logger.info('No references found.')
        exit(0)
    logger.info(f'Loaded {len(refs)} resources.')
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    chunks = text_splitter.split_documents(refs)
    logger.info(f'Split reference content into {len(chunks)} chunks of text of no more than {chunk_size} tokens.')
    return chunks


def __get_db_client():
    return Chroma(persist_directory=db_dir,
                  embedding_function=HuggingFaceEmbeddings(model_name='all-MiniLM-L6-v2'),
                  client_settings=Settings(chroma_db_impl='duckdb+parquet',
                                           persist_directory=db_dir))
