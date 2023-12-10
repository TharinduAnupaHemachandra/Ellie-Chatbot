from PyPDF2 import PdfReader
import os

from langchain.text_splitter import CharacterTextSplitter
from langchain.schema import Document

from langchain.embeddings import HuggingFaceEmbeddings

from langchain.vectorstores import FAISS
from langchain.document_loaders import TextLoader

import pickle
import shutil

import glob

text_splitter = CharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=200,
            separator="\n",
        )

model_name = "sentence-transformers/all-mpnet-base-v2"
model_kwargs = {'device': 'cpu'}
encode_kwargs = {'normalize_embeddings': False}
hf = HuggingFaceEmbeddings(
    model_name=model_name,
    model_kwargs=model_kwargs,
    encode_kwargs=encode_kwargs
)

input_directory_path = os.path.join(os.getcwd(), "../input_files")

pdf_files = glob.glob(os.path.join(input_directory_path, "*.pdf"))

embeddings_path = os.path.join(os.getcwd(), "../embeddings")

for pdf_file in pdf_files:
  file_name = os.path.basename(pdf_file)
  file_name_without_extension = file_name.replace(".pdf", "").replace(".PDF", "")

  pdf_reader = PdfReader(pdf_file)

  page_text = []
  i = 0
  for page in pdf_reader.pages:
      i = i + 1
      page_text.append({
          "file_name": file_name_without_extension,
          "page": i,
          "content": page.extract_text()
      })

  chunks_all = []

  for p in page_text:
    chunked_parts = text_splitter.split_text(text=p["content"])
    for c in chunked_parts:
      chunks_all.append(Document(page_content=c, metadata={'source': p["file_name"], 'p_no': p["page"]}))

  db = FAISS.from_documents(chunks_all, hf)
  faiss.write_index(db.index, f"{file_name_without_extension}_docs.index")
  db.index = None

  with open(os.path.join(embeddings_path, f"{file_name_without_extension}.pkl"), "wb") as f:
    pickle.dump(db, f)
    print("Created:", file_name_without_extension)
  shutil.move(f'{file_name_without_extension}_docs.index', embeddings_path)