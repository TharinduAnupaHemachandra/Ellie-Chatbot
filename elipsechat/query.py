import os

import faiss

import pickle

embeddings_path = os.path.join(os.getcwd(), "D:\MetaElipse\Projects\ElipseChat-Pro\embeddings")

def ask_query(query, userselected, threshold, k):
  all_docs = []

  # db.index = None
  # db = None

  for filename in userselected:
    file_name = filename.replace(".pdf", "").replace(".PDF", "")
    with open(os.path.join("embeddings", f"{file_name}.pkl"), "rb") as f:
      db = pickle.load(f)

    # Load the FAISS index from disk.
    index = faiss.read_index(os.path.join("embeddings", f"{file_name}_docs.index"))

    # merge the index and store
    db.index = index

    docs = db.similarity_search_with_score(query, k=k)
    # print("\t\tDocs Retrieved", len(docs))
    for d in docs:
        # print("d :):):):)")
        # print(d)
        # print("d :):):):)")
        page_content = d[0].page_content
        page_content = f"{page_content}"
        d[0].page_content = page_content
        all_docs.append(d)

  all_docs.sort(key=lambda x: x[1], reverse=False)

  all_docs_filtered = [f for f in all_docs if f[1] < threshold]  # Do filtering here based on the sc
  # print("All Docs Length Filtered", len(all_docs_filtered))

  final_docs = [f[0] for f in all_docs_filtered]

  return all_docs, final_docs