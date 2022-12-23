A fork of [jamietr1](https://github.com/jamietr1/obsidian-automation)'s project to create a new daily note within your Obsidian vault. I made some changes to his code to list Todoist tasks that are due the same day that the note is created. It will also create a new task on Todoist with a link to the Obsidian note (due date will be set to "today") so you can make sure you complete your note for the day. 

## Setup:
1. `python3 -m venv ./venv`
2. `./venv/bin/python3 -m pip install -r requirements.txt`
3. Make a "Projects", "Reading List", "Goals" project in todoist.
    
    * Go to todoist.com and login
    * Make your projects
    * Copy the id for your project from the URL bar
4. Add a `.env` file to your project directory with the following codeblock example.

```
daily_notes_root="/path/to/notes"
obsidian_sharelink='obsidian://open?vault=Notes&file=Daily%2F'
weather_zip="Cleveland+Ohio"
todoist_api_key="111111"
goals_project_id="111111"
projectsideas_project_id="111111"
readinglist_project_id="111111"
slack_bot_token="xyz-123"
slack_default_channel="channel-name"
```

5. Set a cronjob to run this script in the morning

```
##### Obsidian Notes #####
1 0 * * * /home/path_to_project/venv/bin/python3 /home/path_to_project/daily_obsidian_note.py 2>&1
```

6. Review the script and make changes if you wish


## Template Example:
```
[[2022-12-22.Thu]] | [[2022-12-24.Sat]]
#Daily-Notes
⛅️  🌡️+43°F 🌬️↖19mph
---

## To-Do:
- [ ] <font color="yellow">Medium Priority:</font> Testing 
- [ ] <font color="red">HIGH Priority:</font> Testing  
- [ ] Dishes 

## Today's Notes:




---

## Goals:
- [ ] 10 Cups of water

## Reading:
- [ ] Reading 1
- [ ] Reading 2
- [ ] Reading 3

## Create:


##### Project Ideas:
- [ ] Project 1
- [ ] Project 2
- [ ] Project 3


## Learning:
- [ ] Learning 1
- [ ] Learning 2

```