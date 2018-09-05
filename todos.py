#!/home/d3l1r1um/opt/python-3.6.6/bin/python3

import cgi
import requests
import todoslib
import json

# get payload from slack
mylist = vars(cgi.FieldStorage())["list"]

# expected vars
user_id = ""
response_url = ""
command = ""
text = ""

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

# escape special characters

text = cgi.escape(text)
        
# could theoretically check if any of the other expected vars are
# missing from the payload, but that would mean there's a problem
# bigger than the scope of my app and it didn't seem too important to
# handle in this exercise

if (text == ""):

    # no parameters were passed, let's get incomplete tasks
    
    todos = todoslib.get_todos(user_id)

    num_todos = len(todos)
    if(num_todos == 0):
        post_msg = "You have no incomplete tasks!\n\nTo get a list of your completed tasks (if you have some), use:\n`/todos all`\n\nTo add a new task, use:\n`/todos add <your task description> #priority`\nPriority is optional, and default priority is `med`. Valid priority values are `high`, `med`, and `low`."
    else:
        m = []
        m.append("{{\"text\": \"You have {0} incomplete tasks:\", \"attachments\": [".format(num_todos))
        cnt = 0
            
        for todo in todos:
            m.append("{{ \"callback_id\": \"complete\", \"fallback\": \"{1}\", \"color\": \"{0}\", \"actions\": [ {{ \"name\": \"complete\", \"type\": \"button\", \"text\": \"{1}\", \"value\": \"{2}\" }} ] }}".format(todos[todo][0], todos[todo][1], todo))
            cnt += 1
            if (cnt < num_todos):
                m.append(", ")

        m.append("]}")
        msg = ''.join(m)

        post_msg = msg.encode("utf-8")

elif (text == "all"):

    todos = todoslib.get_all_todos(user_id)

    num_todos = len(todos)
    if(num_todos == 0):
        post_msg = "You have no tasks!\n\nTo add a new task, use:\n`/todos add <your task description> #priority`\nPriority is optional, and default priority is `med`. Valid priority values are `high`, `med`, and `low`."
    else:
        m = []
        m.append("{{\"text\": \"You have {0} tasks:\", \"attachments\": [".format(num_todos))
        cnt = 0
            
        for todo in todos:
            complete = todos[todo][2]
            if (complete == 1):
                check = ":white_check_mark:"
                name = "incomplete"
            else:
                check = ":white_square:"
                name = "complete"

            m.append("{{ \"callback_id\": \"complete\", \"fallback\": \"{1}\", \"color\": \"{0}\", \"actions\": [ {{ \"name\": \"{4}\", \"type\": \"button\", \"text\": \"{3} {1}\", \"value\": \"{2}\" }} ] }}".format(todos[todo][0], todos[todo][1], todo, check, name))
            cnt += 1
            if (cnt < num_todos):
                m.append(", ")

        m.append("]}")
        msg = ''.join(m)

        post_msg = msg.encode("utf-8")
else:
    post_msg = "This is where I'd be trying to figure out what parameters are passed if not \"all\"."
        
r = requests.post(response_url, data=post_msg)

print("Content-type: text/plain\n")
# print(r.text)
