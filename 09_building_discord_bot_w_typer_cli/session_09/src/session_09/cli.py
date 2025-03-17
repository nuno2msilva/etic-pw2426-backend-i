import typer
from .bot import run_bot

app = typer.Typer()

@app.command()
def start(token: str):
    """
    Start the Discord bot using the provided token.
    """
    run_bot(token)

if __name__ == "__main__":
    app()