#!/usr/bin/env python

import html
import cgi
import requests
import json
import re
import todoslib

# get payload from slack
mylist = vars(cgi.FieldStorage())["list"]

# expected vars
user_id = ""
response_url = ""
command = ""
text = ""
callback_id = ""

for x in mylist:
    name = x.name
    value = x.value

    if (name == "user_id"):
        user_id = value

    if (name == "response_url"):
        response_url = value

    if (name == "command"):
        command = value

    if (name == "text"):
        text = value

    if (name == "callback_id"):
        callback_id = value


# could theoretically check if any of the other expected vars are
# missing from the payload, but that would mean there's a problem
# bigger than the scope of my app and it didn't seem too important to
# handle in this exercise

if (text == ""):

    # no parameters were passed, let's get incomplete tasks
    
    todos = todoslib.get_todos(user_id)

    num_todos = len(todos)
    if (num_todos == 0):
        post_msg = "{\"text\": \"You have no incomplete tasks!\n\nTo get a list of your completed tasks (if you have some), use:\n`/todos all`\n\nTo add a new task, use:\n`/todos add <your task description> #priority`\nPriority is optional, and default priority is `med`. Valid priority values are `high`, `med`, and `low`.\"}"
    else:
        plural = "tasks"
        if (num_todos == 1):
            plural = "task"

        m = []
        m.append("{{\"text\": \"You have {0} incomplete {1}:\", \"attachments\": [".format(num_todos, plural))
        cnt = 0
            
        for todo in todos:
            m.append("{{ \"callback_id\": \"complete\", \"fallback\": \"{1}\", \"color\": \"{0}\", \"actions\": [ {{ \"name\": \"complete\", \"type\": \"button\", \"text\": \"{1}\", \"value\": \"{2}\", \"confirm\": {{ \"title\": \"Mark task complete?\", \"text\": \"Are you sure you want to mark this task as complete?\", \"ok_text\": \"Yes\" }} }} ] }}".format(todos[todo][0], todos[todo][1], todo))
            cnt += 1
            if (cnt < num_todos):
                m.append(", ")

        m.append("]}")
        msg = ''.join(m)
        post_msg = msg

elif (text == "all"):

    todos = todoslib.get_all_todos(user_id)

    num_todos = len(todos)
    if (num_todos == 0):
        post_msg = "{\"text\": \"You have no tasks!\n\nTo add a new task, use:\n`/todos add <your task description> #priority`\nPriority is optional, and default priority is `med`. Valid priority values are `high`, `med`, and `low`.\"}"
    else:
        plural = "tasks"
        if (num_todos == 1):
            plural = "task"

        m = []
        m.append("{{\"text\": \"You have {0} {1}:\", \"attachments\": [".format(num_todos, plural))
        cnt = 0
            
        for todo in todos:
            complete = todos[todo][2]
            if (complete == 1):
                check = ":white_check_mark:"
                name = "incomplete"
            else:
                check = ":white_square:"
                name = "complete"

            m.append("{{ \"callback_id\": \"complete\", \"fallback\": \"{1}\", \"color\": \"{0}\", \"actions\": [ {{ \"name\": \"{4}\", \"type\": \"button\", \"text\": \"{3} {1}\", \"value\": \"{2}\", \"confirm\": {{ \"title\": \"Mark task {4}?\", \"text\": \"Are you sure you want to mark this task as {4}?\", \"ok_text\": \"Yes\" }} }} ] }}".format(todos[todo][0], todos[todo][1], todo, check, name))
            cnt += 1
            if (cnt < num_todos):
                m.append(", ")

        m.append("]}")
        msg = ''.join(m)
        post_msg = msg

else:

    # figure out what parameters were passed

    param_search = re.search(r'add(.*)', text, re.I)
    if (param_search):

        # params start with add
        params = param_search.group(1)

        priority = "med"

        param_search2 = re.search(r'(.*)#(.*)', params, re.I)
        if (param_search2):
            task = param_search2.group(1)
            task = task.strip()
            priority = param_search2.group(2).strip()
            if not task:
                post_msg = "{\"text\": \":bomb: Can't add an empty task.\"}"
            else:
                post_msg = todoslib.add_todo(user_id, task, priority)
        else:
            task = params.strip()
            if not task:
                post_msg = "{\"text\": \":bomb: Can't add an empty task.\"}"
            else:
                post_msg = todoslib.add_todo(user_id, task, priority)

    else:
        post_msg = "{\"text\": \":bomb: Command parameters are invalid.\"}"

r = requests.post(response_url, data=post_msg)

print("Content-type: text/plain\n")
