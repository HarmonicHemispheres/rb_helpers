"""
# ----------------- OVERVIEW ----------------- #
Script to pull clockify time entries for the recent N days

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

"""


# ----------------- IMPORTS ----------------- #
import requests
import pyodbc
import rich
from rich.progress import track
from rich.console import Console
import yaml
from pathlib import Path
from datetime import timedelta, datetime
from functools import lru_cache


# ----------------- GLOBALS ----------------- #
CONFIG_PATH = Path("clockify.yaml")
WORKSPACE_ID = ""
API_KEY = ""
DB_CONN = ""
DAYS_TO_SYNC = 30

# ----------------- METHODS ----------------- #
def parse_duration(duration_str):
    """
       REF: Edge Bing Chat
    PROMPT: ?
      DOCS:
    Parse a duration string in the format "PT#H#M" and return a timedelta object.
    :param duration_str: A string representing a duration in the format "PT#H#M"
    :return: A timedelta object representing the duration
    """
    hours = 0
    minutes = 0

    # Remove the "PT" prefix
    duration_str = duration_str[2:]

    # Split the string into hours and minutes components
    if 'H' in duration_str:
        hours_str, duration_str = duration_str.split('H')
        hours = int(hours_str)
    if 'M' in duration_str:
        minutes_str, _ = duration_str.split('M')
        minutes = int(minutes_str)

    # Create and return a timedelta object
    return timedelta(hours=hours, minutes=minutes).seconds / 60

def read_config(file_path):    
    with open(file_path) as file:
        config = yaml.safe_load(file)
    return config

def request_clockify(url, params={}):
    headers = { "X-Api-Key": API_KEY }
    try:
        resp = requests.get(url, headers=headers, params=params)
        data = resp.json()
        return data
    except Exception as error:
        rich.print(f"[ERROR] -> {error}")
        rich.print(f"[ERROR] -> {resp}")
    
    
def get_users():
    url = f"https://api.clockify.me/api/v1/workspaces/{WORKSPACE_ID}/users"
    resp = request_clockify(url)
    return resp

@lru_cache
def get_project(project_id):
    url = f'https://api.clockify.me/api/v1/workspaces/{WORKSPACE_ID}/projects/{project_id}'
    resp = request_clockify(url)
    return resp

@lru_cache
def get_client(client_id):
    url = f'https://api.clockify.me/api/v1/workspaces/{WORKSPACE_ID}/clients/{client_id}'
    resp = request_clockify(url)
    return resp

@lru_cache
def get_task(project_id, task_id):
    url = f'https://api.clockify.me/api/v1/workspaces/{WORKSPACE_ID}/projects/{project_id}/tasks/{task_id}'
    resp = request_clockify(url)
    return resp

@lru_cache
def get_tags():
    url = f"https://api.clockify.me/api/v1/workspaces/{WORKSPACE_ID}/tags"
    resp = request_clockify(url)
    try:
        return {tag.get("id"):tag.get("name") for tag in resp}
    except Exception as error:
        # no tags found
        print(error)
        return {}

def convert_string_to_float(s: str) -> float:
    s = str(s)
    return float(s[:-2] + '.' + s[-2:])

def convert_time(minutes):
    """
           REF: Edge Bing Chat
        PROMPT: can you write a python script to convert a float 
                that represents an amount of time to the format: "0:30", "1:15", "5:45"
    """
    # calculate the hours and remaining minutes
    minutes = int(minutes)
    hours = minutes // 60
    minutes = minutes % 60
    # format the output as a string with a colon
    return f"{hours}:{minutes:02d}"

    
def build_time_entry(user_data, time_entry):
    entry = {}
    try:
        # -- get project
        user = user_data.get("name")
        email = user_data.get("email")
        description = time_entry.get("description")
        project = get_project(time_entry.get("projectId"))
        project_name = project.get("name")
        is_billable = time_entry.get("billable")
        rate_per_hour_usd =  convert_string_to_float(project['hourlyRate']['amount']) if project['hourlyRate'] else 0

        # -- get client
        client = project.get("clientName")
        if DEBUG:
            rich.print(f'-> {user} - {client} - {project_name} - {description}')

        # -- get task
        task_id = time_entry.get("taskId")
        task_project_id = time_entry.get("projectId")
        task = ""
        if task_id and task_project_id:
            task = get_task(task_project_id, task_id)
            task = task.get("name")

        # -- other
        duration_minutes = parse_duration(time_entry.get("timeInterval").get("duration"))
        duration_hours = parse_duration(time_entry.get("timeInterval").get("duration")) / 60
        
        tags = ""
        tag_ids = time_entry.get("tagIds")
        if tag_ids and len(tag_ids) > 0:
            tags_dict = get_tags()
            tags = ",".join([tags_dict.get(tid) for tid in tag_ids])

        start_dt = datetime.strptime(time_entry.get("timeInterval").get("start"), "%Y-%m-%dT%H:%M:%SZ")
        end_dt = datetime.strptime(time_entry.get("timeInterval").get("end"), "%Y-%m-%dT%H:%M:%SZ")
        start_date = start_dt.date()
        start_time = start_dt.strftime("%I:%M %p")
        end_date = end_dt.date()
        end_time = end_dt.strftime("%I:%M %p")
        amount_usd = rate_per_hour_usd * float(duration_hours)

        # -- Set Entry values (defines oder of dict too)
        return {
            "Project": project_name,
            "Client": client,
            "Description": description,
            "Task": task,
            "User": user,
            "Email": email,
            "Tags": tags,
            "Billable": "Yes" if is_billable else "No",
            "Start Date": start_date,
            "Start Time": start_time,
            "End Date": end_date,
            "End Time": end_time,
            "Duration (h)": duration_hours,
            "Duration (decimal)": convert_time(duration_minutes),
            "Billable Rate (USD)": rate_per_hour_usd,
            "Billable Amount (USD)": amount_usd,
        }

    except Exception as error:
        rich.print(f"[ERROR] -> {error}")

        raise error




def get_time_entries(users):
    today = datetime.now() - timedelta(days=1)
    date_n_days_ago = today - timedelta(days=DAYS_TO_SYNC)
    date_n_days_ago_str = date_n_days_ago.strftime('%Y-%m-%d')
    date_today_str = today.strftime('%Y-%m-%d')
    params = {'start': f'{date_n_days_ago_str}T13:00:46Z', 'end': f'{date_today_str}T13:00:46Z'}
    rich.print(f"Collecting Time Entries from {date_n_days_ago_str}T13:00:46Z  to  {date_today_str}T13:00:46Z")
    entries = []
    for step in track(range(len(users)),
                    description=f"Collecting Time Entries from {len(users)} Users"
                    ):
        user = users[step]
        user_id = user.get("id")

        url = f"https://api.clockify.me/api/v1/workspaces/{WORKSPACE_ID}/user/{user_id}/time-entries"
        resp = request_clockify(url, params=params)
        if isinstance(resp, (tuple, list)):
            for r in resp:
                entry = build_time_entry(user, r)
                if entry:
                    entries.append(entry)
        else:
            entry = build_time_entry(user, resp)
            if entry:
                entries.append(entry)
    
    return entries

def to_csv(time_entries, out):
    if len(time_entries) < 1:
        return
    
    entries = sorted(time_entries, key=lambda x: x["User"])
    
    with open(out, "w") as csv:
        text = ",".join([f'"{k}"' for k in entries[0].keys()]) + "\n"
        for entry in entries:
            text += ",".join([f'"{v}"' for v in entry.values()]) + "\n"

        csv.write(text)


if __name__ == '__main__':
    
    # --- load config
    config = read_config(CONFIG_PATH)
    WORKSPACE_ID = config.get("WORKSPACE_ID", "")
    API_KEY = config.get("API_KEY", "")
    DB_CONN = config.get("DB_CONN", "")
    DAYS_TO_SYNC = config.get("DAYS_TO_SYNC", 15)
    INTERACTIVE = config.get("INTERACTIVE", False)
    DEBUG = config.get("DEBUG", True)

    # --- set variables
    out_csv = Path("time_entries.csv")
    entries = []
    user_count = 0
    banner = """
   (  (   .  (     (  (     ((  )   ( (       (   (  (  (    (    
  ()) )\   . )\   ()) )\    ))\(_\ )\))\      )\  )\ )\ )\   )\   
 ((_))(_)   ((_) ((_))(_)__((_)(__)(_)(_)    ((_)((_)(_)(_) ((_)  
(/ __| |   / _ \(/ __| |/ /_ _| __| \ / /    | _ \ | | | |  | |   
| (__| |__| (_) | (__|   < | || _| \   /     |  _/ |_| | |__| |__ 
 \___|____|\___/ \___|_|\_\___|_|   |_|      |_|  \___/|____|____|
                                                            v0.1.5
    
    """

    rich.print(banner)
    try:
        # --- iter over users
        users = get_users()
        entries = get_time_entries(users)
        user_count = len({u["User"] for u in entries})
        if DEBUG:
            rich.print(entries)

        # --- save details to csv
        to_csv(entries, out=out_csv)

        # --- upload to database
        # for user in users:
        #     insert_to_sql(user)
    
    except Exception as error:

        import traceback    
        rich.print(f"[ERROR] --> {error}")
        if DEBUG:
            traceback.print_exc()


    # -- wait for user to exit
    if len(entries) > 0:
        rich.print(f"[INFO] -> collected {len(entries)} time entries for {user_count} users!")
        rich.print(f"[INFO] -> csv saved to {out_csv.absolute()}")
    if INTERACTIVE:
        input("\nPress Enter to Exit")


