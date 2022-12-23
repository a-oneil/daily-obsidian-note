#!/venv/bin/python3
import arrow, requests, os, time, traceback
from todoist_api_python.api import TodoistAPI
from dotenv import dotenv_values
from datetime import datetime
from slack_sdk import WebClient

''' Notes Config '''
# Very hacky way of getting the running directory's env file for wherever you decide to put this script.
config=dotenv_values(__file__.replace("daily_obsidian_note.py",".env"))
today = datetime.now().strftime("%Y-%m-%d")
daily_notes = config['daily_notes_root']
weather_location = config['weather_zip']
tag = config['tag']

''' Todoist Config '''
todoist = TodoistAPI(config['todoist_api_key'])
goals_project_id = config['goals_project_id']
projectsideas_project_id = config['projectsideas_project_id']
readinglist_project_id = config['readinglist_project_id']
learning_project_id = config['learning_project_id']
obsidian_sharelink = config['obsidian_sharelink']

slack_bot_token = config["slack_bot_token"]    
slack_client = WebClient(slack_bot_token)
slack_default_channel = config["slack_default_channel"] 

def get_link_for_file(file, link_text=""):
    if link_text != "":
        return "[[" + file.replace(".md", "") + "|" + link_text + "]]"
    else:
        return "[[" + file.replace(".md", "") + "]]"

def get_weather(location):
    headers = requests.utils.default_headers()
    payload = {'format': '2'}
    r = requests.get("http://wttr.in/" + location, params=payload, headers=headers)
    return r.text.strip()

def get_daily_notes_filename(offset=0):
    file_date = arrow.now()
    if offset != 0:
        file_date = file_date.shift(days=offset)
    return(file_date.format('YYYY-MM-DD.ddd') + ".md")

def get_tasks(project_id,note):
    try:
        tasks = todoist.get_tasks(project_id=project_id)
        for x in tasks:
            note.write(f"- [ ] {x.content}\n")
    except Exception as error:
        print(error)

def get_todays_tasks(note):
    try:
        tasks = todoist.get_tasks()
        for x in tasks:
            due = x.due
            if due:
                due_date = str(due.date)
                past = datetime.strptime(due_date, "%Y-%m-%d")
                overdue = past <= datetime.now() 
                
                if (due_date == today or overdue) and not "Daily Note:" in x.content:
                    if 1 == x.priority:
                        task_title = f'- [ ]'
                    elif 2 == x.priority:
                        task_title = f'- [ ] <font color="#6495ED">Low Priority:</font>'
                    elif 3 == x.priority:
                        task_title = f'- [ ] <font color="yellow">Medium Priority:</font>'
                    elif 4 == x.priority:
                        task_title = f'- [ ] <font color="red">HIGH Priority:</font>'
                    note.write(f'{task_title} {x.content} \n')
    except Exception as error:
        print(error)

def create_task(taskname,due_date,urgency):
    try:
        todoist.add_task(
            content=taskname,
            due_string=due_date,
            due_lang="en",
            priority=urgency,
        )
    except Exception as error:
        print(error)

def main():
    daily_notes_file = os.path.join(daily_notes, get_daily_notes_filename())
    # if not os.path.exists(daily_notes_file):
    #     print("File already exists. Not overwriting...")
    # else:
    print(f"Generating daily notes file {os.path.basename(daily_notes_file)}...")
    with open(daily_notes_file, 'w+') as note:
        nav_bar = get_link_for_file(get_daily_notes_filename(offset=-1))
        nav_bar += " | " + get_link_for_file(get_daily_notes_filename(offset=1))
        nav_bar += "\n" + tag
        nav_bar += "\n" + get_weather(weather_location)
        nav_bar += "\n---"
        note.write(nav_bar)
        note.write("\n\n## To-Do:\n")
        get_todays_tasks(note)
        note.write("\n## Today's Notes:\n\n\n\n")
        note.write("\n---\n")
        note.write("\n## Goals:\n")
        get_tasks(goals_project_id,note)
        note.write("\n## Reading:\n")
        get_tasks(readinglist_project_id,note)
        note.write("\n## Create:\n\n")
        note.write("\n##### Project Ideas:\n")
        get_tasks(projectsideas_project_id,note)
        note.write("\n## Learning:\n")
        get_tasks(learning_project_id,note)

    note.close()

    todoist_message = f"[Daily Note: {get_daily_notes_filename()}]({obsidian_sharelink}{get_daily_notes_filename()})"
    slack_message = f"Daily Note Created: <{obsidian_sharelink}{get_daily_notes_filename()}|{get_daily_notes_filename()}>"

    create_task(todoist_message,"Today",4)
    slack_client.chat_postMessage(channel=slack_default_channel, text=slack_message)

if __name__ == "__main__":
    retry_count = 5
    count = 0
    try:
        main()
    except Exception as e:
        # Print error out to console and try again if count is less than retry count.
        print(traceback.format_exc())
        count += 1
        if count < retry_count:
            time.sleep(20)
            main()
        else:
            exit(1)