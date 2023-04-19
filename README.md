
<p align="center">
    <img src="banner.jpg" />
    <br />
    <br />
    <i>
    a list of various scripts, examples, packages and docs that help me do stuff
    </i>
    <br />
    <br />
    <img
        src="https://img.shields.io/badge/Powered By Python-black?color=black&style=for-the-badge&logo=python"
        alt="Credit to OpenAi"/>
    <img
        src="https://img.shields.io/badge/Powered By DUCKDB-black?color=black&style=for-the-badge&logo=DuckDB"
        alt="Credit to DuckDB"/>
</p>


<br>
<br>

<!-- ----------------------------- SCRIPTS ----------------------------- -->

# Scripts
<details>
<summary>
    <b style="font-size:15px;"><code>time_display.py</code>
    - cli program to display datetimes for multiple regions and formats</b>
</summary>

```
--------- DETAILS ---------
VERSION:  0.1.0

--------- INSTALL ---------
> pip install rich pytz

--------- USAGE ---------
> python time_display.py

USA.PACIFIC:  2023-04-18  08:56 PM  PDT-0700
USA.CENTRAL:  2023-04-18  10:56 PM  CDT-0500
USA.EASTERN:  2023-04-18  11:56 PM  EDT-0400
      INDIA:  2023-04-19  09:26 AM  IST+0530
```

</details>

<details>
<summary>
    <b style="font-size:15px;"><code>yt_feed.py</code>
    - This script scrapes youtube for details about a list of channels</b>
</summary>

```
------------------ DETAILS ------------------
VERSION:  0.1.0

------------------ INSTALL ------------------
> pip install duckdb rich requests

------------------ USAGE ------------------
first create a config for what channels to scrape:
'''
# comments supported (channels.txt)
# <group icon \ text>,  <group name>, <channel name>
📰, new, @60minutes
🤖, tech, @Microsoft
🤖, tech, @TwoMinutePapers
🚀, space, @SpaceX
'''

then configure the global user params:
       SLEEP_SECONDS: how long the script waits before a new pull
             N_POSTS: how many posts to display in the terminal output
            CHANNELS: a config file for what channels to pull
              NEW_DB: decide whether to create a new database on run
BACKUP_AFTER_N_SYNCS: (None)  will not take a backup ever
                      (<int>) will take a backup every <int> number of syncs 
         BACKUP_PATH: (None)  will create a new backup with the current datetime stamp
                      (<str>) will only backup to a specific path

RUN
> python yt_feed.py
```

</details>

<details>
<summary>
    <b style="font-size:15px;"><code>clockify_pull.py</code>
    - Script to pull clockify time entries for the recent N days</b>
</summary>
    

```
# ----------------- DETAILS ----------------- #
VERSION = 0.1.5

# ----------------- CREATE CONFIG ----------------- #
config must be called "clockify.yaml"

'''
WORKSPACE_ID: "<YOUR WORKSPACE ID>"
API_KEY: "<CLOCKIFY API KEY>"
DAYS_TO_SYNC: <INT>     # how many days back from yesterday to pull
DB_CONN: "<ODBC CONNECTION STRING>"
DEBUG: <BOOL>     # if true will print extra detail
INTERACTIVE: <BOOL>      # if true will wait for user input before quiting program
'''

# ----------------- INSTALLS ----------------- #
> pip install rich pyyaml pyodbc requests pyinstaller

# ----------------- BUILD A INSTALLER ----------------- #
> pyinstaller --onefile --icon .\static\clockify_pull_1.ico --name "clockify_pull_0.1.5.exe" .\scripts\clockify_pull.py 

```

</details>

<details>
<summary>
    <b style="font-size:15px;"><code>img_to_ico.py</code>
    - converts a image file to .ico</b>
</summary>

`.ico` files are common for app\file\folder icons. this script will convert a png or jpg to ico

```
# ----------------- DETAILS ----------------- #
VERSION = 0.1.0

# ----------------- INSTALLS ----------------- #
> pip install rich Pillow typer

# ----------------- USAGE ----------------- #
# BASIC
> python img_to_ico.py <PATH>

# CUSTOM DIMENSIONS
> python img_to_ico.py <PATH> --px-dim 48
> python img_to_ico.py <PATH> --px-dim 256

# CUSTOM OUTFILE PATH
> python img_to_ico.py <PATH> --out <PATH>
```

</details>

<br>
<br>

<!-- ----------------------------- CHEATSHEETS ----------------------------- -->
# Cheatsheets
- `duckdb_queries.sql` - a list of commands for duckdb (WIP) 

<br>
<br>

<!-- ----------------------------- TEMPLATES ----------------------------- -->
# Templates
- `script.py` - a generic python cli script
- `typer_cli.py` - simple typer cli template
- `readme.md` - template for repo readme

<br>
<br>

<!-- ----------------------------- SNIPPETS ----------------------------- -->
# Snippets
- `proc.py` - a class to handle subprocess across platforms
