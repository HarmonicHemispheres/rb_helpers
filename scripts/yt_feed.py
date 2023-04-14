"""
------------------ OVERVIEW ------------------
This script scrapes youtube for details about a list of channels

------------------ INSTALL ------------------
> pip install duckdb rich requests

------------------ USAGE ------------------
first create a config for what channels to scrape:
```
# comments supported (channels.txt)
# <group icon \ text>,  <group name>, <channel name>
📰, new, @60minutes
🤖, tech, @Microsoft
🤖, tech, @TwoMinutePapers
🚀, space, @SpaceX
```

then configure the global user params:
SLEEP_SECONDS: how long the script waits before a new pull
      N_POSTS: how many posts to display in the terminal output
     CHANNELS: a config file for what channels to pull
       NEW_DB: decide whether to create a new database on run

RUN
> python yt_feed.py


------------------ DETAILS ------------------
LICENSE:  MIT

"""

# ------------------ IMPORTS ------------------
from datetime import datetime, timedelta
import re
import time
import duckdb
from rich import print
from rich.console import Console
from rich.progress import track
from rich.table import Table
import hashlib
import requests
from pathlib import Path
import shutil
import uuid
import codecs

# ------------------ GLOBALS ------------------
# --- USER PARAMS
SLEEP_SECONDS = 60*5
N_POSTS = 30
CHANNELS = "channels.txt"
NEW_DB = False

# --- OTHER PARAMS
DB = None


# ------------------ HELPERS ------------------
class Database:
    def __init__(self, create_new=True):
        self.dbfile = 'ytstore.duckdb'
        p = Path(self.dbfile)
        
        if p.exists() and create_new:
            shutil.copy(p, f"ytstore_{datetime.now().strftime('%Y%m%d')}.duckdb")
            p.unlink()
        
        self.conn = duckdb.connect(self.dbfile)

        if not p.exists() or create_new:
            self.conn.execute("""
                CREATE TABLE posts(
                    post_id VARCHAR PRIMARY KEY,
                    channel VARCHAR,
                    views INT,
                    title VARCHAR,
                    published DATETIME,
                    vid_len VARCHAR,
                    created DATETIME,
                    grp VARCHAR,
                    grp_icon VARCHAR,
                    url VARCHAR
                )
            """)
        
    
    def insert_post(self, data):
        title_fixed = data.get("title").replace("'","''")
        sql = f"""
        INSERT OR REPLACE INTO posts VALUES
        (
            '{data.get("post_id")}',
            '{data.get("channel")}',
            '{data.get("views")}',
            '{title_fixed}',
            '{data.get("published")}',
            '{data.get("vid_len")}',
            '{data.get("created")}',
            '{data.get("grp")}',
            '{data.get("grp_icon")}',
            '{data.get("url")}'
        )
        """
        cursor = self.conn.cursor()
        cursor.execute(sql)
        cursor.commit()

    def select_posts(self, n=20):
        sql = f"""
        SELECT * FROM posts
        ORDER BY published DESC
        LIMIT {n}
        """ 
        cursor = self.conn.cursor()
        cursor.execute(sql)
        return [row for row in cursor.fetchall()]


def open_channel_file(path):
    p = Path(path)
    channels = []
    with codecs.open(p, "r", encoding="utf-8") as fp:
        for line in fp.readlines():
            if len(line) == 0 or line.startswith("#") or line in ("\n","\r\n") or line == " "*len(line):
                continue
            else:
                channels.append([
                    l.strip() for l in line.replace("\n","").replace("\r\n","").split(",")
                    ])
    return channels


def get_hash(s:str):
    hash_object = hashlib.sha1(s.encode())
    hex_dig = hash_object.hexdigest()
    return hex_dig

def convert_to_datetime(time_str):
    """ REF = BING CHAT """
    num = int(re.search(r'\d+', time_str).group())
    if 'week' in time_str:
        return datetime.now() - timedelta(weeks=num)
    elif 'day' in time_str:
        return datetime.now() - timedelta(days=num)
    elif 'month' in time_str:
        return datetime.now() - timedelta(days=num*30)
    elif 'hour' in time_str:
        return datetime.now() - timedelta(hours=num)
    elif 'minute' in time_str:
        return datetime.now() - timedelta(minutes=num)
    else:
        return None
    
def print_friendly_time_diff(input_date):
    """ REF = BING CHAT 
    PROMPT: 
        write a python method to print out how many minutes, hours,
        days, weeks or months a date is away from datetime.now() 
        and print it in a friendly way
    """
    now = datetime.now()
    diff = now - input_date
    diff_seconds = diff.total_seconds()
    if diff_seconds < 60:
        return f"{diff_seconds:.0f} seconds ago"
    elif diff_seconds < 3600:
        return f"{diff_seconds/60:.0f} minutes ago"
    elif diff_seconds < 86400:
        return f"{diff_seconds/3600:.0f} hours ago"
    elif diff_seconds < 604800:
        return f"{diff_seconds/86400:.0f} days ago"
    elif diff_seconds < 2629800:
        return f"{diff_seconds/604800:.0f} weeks ago"
    else:
        return f"{diff_seconds/2629800:.0f} months ago"

def get_yt_channel_page(tag:str, group, icon):
    global DB

    url = f"https://www.youtube.com/{tag}/videos"
    r = requests.get(url)

    # with open("YT.html", "w", encoding="utf-8") as fp:
    #     fp.write(r.text)
    # exit()

    s_title = '"title":{"runs":[{"text":"' # then find title=""
    s_published = '"publishedTimeText":{"simpleText":"' # "}
    s_len = '"lengthText":{"accessibility":{"accessibilityData":{"label":"'
    s_views = '"viewCountText":{"simpleText":"' # "},
    s_url = '"watchEndpoint":{"videoId":"'
    
    for t in r.text.split(s_title)[1:]:
        try:
            # -- PARSE
            title = t.split('"}]', maxsplit=1)[0]
            published = t.split(s_published, 3)[1].split('"}',3)[0]
            views = t.split(s_views, 1)[1].split('"}',1)[0]
            views = int(views.replace(" views","").replace(",",""))
            length = t.split(s_len, 1)[1].split('"}},"simpleText":"',1)[1].split('"}',1)[0]
            url_code = t.split(s_url,1)[1].split('"')[0]
            url = f"https://www.youtube.com/watch?v={url_code}"
            _hash = get_hash(title)

            # -- INSERT NEW POSTS
            DB.insert_post({
                "post_id": _hash,
                "channel": tag,
                "views": views,
                "title": title,
                "published": str(convert_to_datetime(published)),
                "vid_len": length,
                "created": str(datetime.now()),
                "grp": str(group),
                "grp_icon": str(icon),
                "url": url
            })

        except Exception as error:
            # import traceback
            # traceback.print_exc()
            # print(f"ERROR:  {error}")
            pass

def current_time():
    now_utc = datetime.now()
    return now_utc.strftime('%Y-%m-%d  %I:%M %p  %Z')


# ------------------ MAIN PROCESS ------------------
if __name__ == '__main__':

    # --- VARIABLES
    DB = Database(create_new=NEW_DB)
    console = Console()
    channels_loaded = open_channel_file(CHANNELS)
    last_sync = None

    while True:
        # --- CLEAR SCREEN
        console.clear()

        # --- GET DATA
        records = reversed(DB.select_posts(n=N_POSTS))

        # --- DISPLAY NEW POSTS
        table = Table(title="Youtube Posts")
        # table.add_column("post_id", style="green4")
        table.add_column("channel", style="white", justify="left")
        # table.add_column("group", style="green4")
        table.add_column("views", style="green4", justify="left")
        table.add_column("vid_len", style="green4", justify="left")
        table.add_column("title", style="white", justify="left",overflow="fold")
        table.add_column("published_date", style="green4", justify="left")
        table.add_column("published_rel", style="green4", justify="left")
        table.add_column("url", justify="left")
        # table.add_column("created", style="green4")
        # table.add_column("group_icon", style="green4")

        for row in records:
            table.add_row(
                f"{row[8]} {row[1]}",
                f"{row[2]:,}",
                str(row[5]),
                str(row[3]),
                row[4].strftime('%Y-%m-%d %H:%M'),
                print_friendly_time_diff(row[4]),
                f"{row[9]}"
                )

        print(table)
        if last_sync:
            console.print(f"Last Sync: {last_sync}")
        
        # --- SLEEP BEFORE UPDATE
        for step in track(range(SLEEP_SECONDS), description="Next Sync In:"):
            time.sleep(1)

        # --- UPDATE POST DATABASE
        for step in track(range(len(channels_loaded)),
                          description="Syncing With Youtube"
                          ):
            icon, group, ch = channels_loaded[step]
            get_yt_channel_page(ch, group, icon)
        last_sync = current_time()
        
        



