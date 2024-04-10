import click
from kode_search.indexer import main as index_main
from kode_search.searcher import search as search_main


@click.group()
def cli():
    pass


@cli.command()
def index():
    index_main()


@cli.command()
@click.argument("query")
def search(query):
    search_main(query)


if __name__ == "__main__":
    cli()
