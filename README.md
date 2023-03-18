# Daily Obsidian Note Generator
I recently learned about the powerful note-taking app, Obsidian. It changed the way I've been taking notes but something was missing... I wanted Todoist tasks inside of my daily Obsidian note so I could collect my thoughts and track my accomplishments of the day. 

If you don't know, Obsidian is a knowledge base application that works on local Markdown files. You can use it to take notes, plan a research paper or use it for mathematics but the thing I use Obsidian for the most is to create daily notes.

Every morning at 12:01AM, I have a new note created for me in my Obsidian for the day filled with my daily tasks from Todoist and a section for my thoughts of the day. This is accomplished via a python project I wrote called Daily Obsidian Note. Generic name right?

My code started as a fork of [jamietr1](https://github.com/jamietr1/obsidian-automation) daily note generator but I ended up rewriting alot of it to match what I desired from a daily note. Such as, using Todoist as the primary "source of truth" of tasks instead of relying on past notes.

The script will query the Todoist api and retrieve tasks that are due the same day that the note is created. It also has the ability to query a Todoist project and return the list of tasks in that project.

Once the note has been created, it will also create a new task on Todoist with a link to the Obsidian note (the due date will be set to "today") so you can make sure you complete your note for the day from all of your devices.

## Setup
1. `python3 -m venv ./venv`
2. `./venv/bin/python3 -m pip install -r requirements.txt`
3. Make a "Projects", "Reading List", "Goals" and "Learning" project in todoist.
    
    * Go to todoist.com and login
    * Make your projects
    * Copy the id for your project from the URL bar
4. Add a `.env` file to your project directory with the following codeblock example.

```
daily_notes_root="/path/to/notes"
obsidian_sharelink='obsidian://open?vault=Notes&file=Daily%2F'
todoist_api_key="111111"
goals_project_id="111111"
projectsideas_project_id="111111"
readinglist_project_id="111111"
learning_project_id="111111"
slack_bot_token="xyz-123"
slack_default_channel="channel-name"
```

5. Set a cronjob to run this script in the morning

```
##### Obsidian Notes #####
1 0 * * * /home/path_to_project/venv/bin/python3 /home/path_to_project/daily_obsidian_note.py 2>&1
```

6. Review the script and make changes if you wish

## Template Example
```
[[2022-12-22.Thu]] | [[2022-12-24.Sat]]
#Daily-Notes

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
