from whoosh.index import open_dir
from whoosh.qparser import QueryParser
from colorama import Fore, Style, init
import os

init(autoreset=True)


def search(query):

    if not os.path.exists("indexdir"):
        print(f"{Fore.RED}Index directory not found. Please run 'askode index' first.")
        return

    ix = open_dir("indexdir")

    with ix.searcher() as searcher:
        query_obj = QueryParser("content", ix.schema).parse(query)
        results = searcher.search(query_obj, limit=None)
        results = [(result["title"], result.score) for result in results]

        if not results:
            print(f"{Fore.RED}No results found.")
            return

        for idx, (title, _) in enumerate(results, start=1):
            print(f"{Fore.BLUE}{idx}. {title}")

        try:
            choice = int(
                input(
                    f"\n{Fore.MAGENTA}Enter number to view code snippet, or 0 to exit: "
                )
            )
            if choice:
                selected_path = results[choice - 1][0]
                show_file_snippet(selected_path, query)
        except (ValueError, IndexError):
            print(f"{Fore.RED}Invalid selection.")


def show_file_snippet(file_path, search_term, context_lines=2):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            lines = file.readlines()
            for i, line in enumerate(lines):
                if search_term.lower() in line.lower():
                    start = max(i - context_lines, 0)
                    end = min(i + context_lines + 1, len(lines))
                    snippet = "".join(lines[start:end])
                    print(f"\n{Fore.YELLOW}...{snippet}...\n")
                    break
    except Exception as e:
        print(f"{Fore.RED}Error reading file: {e}")
