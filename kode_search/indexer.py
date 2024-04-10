import os
from whoosh.index import create_in, open_dir
from whoosh.fields import Schema, TEXT, ID
from whoosh import index


# Function to index documents
def index_docs(directory, writer):
    indexed_files = 0
    for root, _, files in os.walk(directory):
        if "indexdir" in root:
            continue
        for file in files:
            if file.endswith(
                (
                    ".py",
                    ".js",
                    ".ts",
                    ".jsx",
                    ".tsx",
                    ".java",
                    ".cpp",
                    ".c",
                    ".html",
                    ".css",
                )
            ):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        file_content = f.read()
                        writer.add_document(title=file_path, content=file_content)
                        indexed_files += 1
                        print(f"Indexed: {file_path}")
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")

    return indexed_files


def main():
    # Define the schema for indexing
    schema = Schema(title=ID(stored=True, unique=True), content=TEXT)

    # Specify the directory where the index will be stored
    indexdir = "indexdir"
    if not os.path.exists(indexdir):
        os.mkdir(indexdir)

    # Get the parent directory of the current script
    repo_path = os.getcwd()

    # Create or open the index
    if index.exists_in(indexdir):
        ix = open_dir(indexdir)
    else:
        ix = create_in(indexdir, schema)

    # Indexing the documents
    writer = ix.writer()
    num_indexed_files = index_docs(repo_path, writer)
    writer.commit()
    print(f"Indexing complete for {num_indexed_files} files.")


if __name__ == "__main__":
    main()
