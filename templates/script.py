"""
------------------ OVERVIEW ------------------
Describe your script here. what does it do or accomplish?

------------------ INSTALL ------------------
> pip install rich typer

------------------ USAGE ------------------
GLOBALS PARAMS::
SLEEP_SECONDS: how long the script waits before doing something
    FILE_PATH: a path to save stuff to!

RUN
> python yt_feed.py

------------------ DETAILS ------------------
    LICENSE:  <LICENSE>
     AUTHOR:  <AUTHOR NAME>
LAST UPDATE:  <DATE>
    VERSION:  <SEMANTIC VERSION>
"""

# ------------------ IMPORTS ------------------
from rich import print
from rich.console import Console
from rich.progress import track
from rich.progress import Progress
from rich.table import Table
from pathlib import Path
import typer


# ------------------ GLOBALS ------------------
# --- USER PARAMS
SLEEP_SECONDS: int        = 12
FILE_PATH: Path           = Path("random_file.txt")

# --- OTHER PARAMS
# PI = 3.141592653589
# DB = None


# ------------------ HELPERS ------------------
# --- UTIL METHODS
...

# --- MODEL CLASSES
... 

# --- MAIN CLASSES
...


# ------------------ MAIN PROCESS ------------------
def main():
    # --- VARIABLES
    ...


    # --- RUN APP
    # 1. Progress Bar Setup
    # for step in track(range(100)):
    #     do_a_thing()

    # 2. Spinner Wheel Setup
    # with Progress() as progress:

    #     task1 = progress.add_task("[red]Downloading...", total=1000)
    #     task2 = progress.add_task("[green]Processing...", total=1000)
    pass

if __name__ == '__main__':
    typer.run(main)


